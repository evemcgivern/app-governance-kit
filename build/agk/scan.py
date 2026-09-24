import argparse
import os
import re
import sys
import zipfile
from pathlib import Path

MAX_QUOTE_WORDS = 15
SCAN_DIRS = ("methods", "agents", "case-studies", "site", "dist", "demo-estate", "README.md")
QUOTE_DIRS = ("methods", "agents", "case-studies", "site")
TEXT_SUFFIXES = {".md", ".csv", ".html", ".json", ".txt", ".svg"}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico"}
QUOTE_RE = re.compile(r"[\"“]([^\"”]+)[\"”]")
TAG_STRIP_RE = re.compile(r"<[^>]+>")


def load_words(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    return [l.strip() for l in lines if l.strip() and not l.lstrip().startswith("#")]


def private_hits(text: str, words: list[str], label: str) -> list[str]:
    hits = []
    for n, line in enumerate(text.splitlines(), start=1):
        for w in words:
            if re.search(rf"(?<!\w){re.escape(w)}(?!\w)", line, re.IGNORECASE):
                hits.append(f"{label}:{n}: private term {w!r}")
    return hits


def long_quotes(text: str, label: str) -> list[str]:
    hits = []
    lines = text.splitlines()

    # Split into paragraphs (separated by blank lines)
    paragraphs = []
    current_para = []
    start_line = 1
    for i, line in enumerate(lines):
        if line.strip():
            if not current_para:
                start_line = i + 1
            current_para.append(line)
        else:
            if current_para:
                paragraphs.append((start_line, current_para))
                current_para = []
    if current_para:
        paragraphs.append((start_line, current_para))

    # Process each paragraph
    for start_line, para_lines in paragraphs:
        # Check blockquotes: consecutive lines starting with ">"
        i = 0
        while i < len(para_lines):
            if para_lines[i].lstrip().startswith(">"):
                blockquote_lines = []
                block_start = start_line + i
                while i < len(para_lines) and para_lines[i].lstrip().startswith(">"):
                    blockquote_lines.append(para_lines[i].lstrip("> ").strip())
                    i += 1
                joined_blockquote = " ".join(blockquote_lines)
                if len(joined_blockquote.split()) >= MAX_QUOTE_WORDS:
                    hits.append(f"{label}:{block_start}: blockquote of {MAX_QUOTE_WORDS}+ words")
            else:
                i += 1

        # Check for quoted runs: join all non-blockquote lines and find quotes
        non_blockquote_lines = [line for line in para_lines if not line.lstrip().startswith(">")]
        if non_blockquote_lines:
            joined_para = " ".join(non_blockquote_lines)
            # Find positions of quotes in the joined text
            for match in QUOTE_RE.finditer(joined_para):
                q = match.group(1)
                if len(q.split()) >= MAX_QUOTE_WORDS:
                    # Find which line the quote starts on by tracking character position
                    char_pos = match.start()
                    current_pos = 0
                    quote_line = start_line
                    for i, line in enumerate(non_blockquote_lines):
                        line_with_space = line + " "
                        line_len = len(line_with_space)
                        if current_pos + line_len > char_pos:
                            quote_line = start_line + para_lines.index(line)
                            break
                        current_pos += line_len
                    hits.append(f"{label}:{quote_line}: quoted run of {MAX_QUOTE_WORDS}+ words")

    return hits


def docx_text(path: Path) -> str:
    parts = []
    with zipfile.ZipFile(path) as z:
        for name in z.namelist():
            if name.endswith(".xml"):
                parts.append(TAG_STRIP_RE.sub(" ", z.read(name).decode("utf-8", "replace")))
    return "\n".join(parts)


def _files(root: Path, entries: tuple[str, ...]):
    for entry in entries:
        p = root / entry
        if p.is_file():
            yield p
        elif p.is_dir():
            yield from (f for f in sorted(p.rglob("*")) if f.is_file())


def scan(root: Path, words: list[str]) -> list[str]:
    hits = []
    for f in _files(root, SCAN_DIRS):
        label = str(f.relative_to(root))
        # Skip .gitkeep files
        if f.name == ".gitkeep":
            continue
        if f.suffix in (".docx", ".xlsx", ".pptx"):
            hits += private_hits(docx_text(f), words, label)
        elif f.suffix in TEXT_SUFFIXES:
            hits += private_hits(f.read_text(encoding="utf-8", errors="replace"), words, label)
        elif f.suffix not in IMAGE_SUFFIXES:
            # Flag files that cannot be scanned
            suffix = f.suffix or "files without an extension"
            hits.append(f"{label}: cannot scan {suffix} files; remove it or teach the scan to read it")
    for f in _files(root, QUOTE_DIRS):
        # Skip .gitkeep files
        if f.name == ".gitkeep":
            continue
        if f.suffix in (".md", ".html"):
            hits += long_quotes(f.read_text(encoding="utf-8", errors="replace"), str(f.relative_to(root)))
    return hits


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Pre-publish scan.")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    words_path = os.environ.get("AGK_PRIVATE_WORDS")
    if not words_path or not Path(words_path).is_file():
        print("error: set AGK_PRIVATE_WORDS to your private word list (kept outside the repo)", file=sys.stderr)
        return 2
    hits = scan(args.root, load_words(Path(words_path)))
    for h in hits:
        print(h, file=sys.stderr)
    print("scan clean" if not hits else f"{len(hits)} hit(s)")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
