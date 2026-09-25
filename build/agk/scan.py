import argparse
import os
import re
import sys
import zipfile
from pathlib import Path

MAX_QUOTE_WORDS = 15
SCAN_DIRS = ("methods", "agents", "case-studies", "site", "dist", "demo-estate", "README.md")
QUOTE_DIRS = ("methods", "agents", "case-studies", "site")
TEXT_SUFFIXES = {".md", ".csv", ".html", ".json", ".txt", ".svg", ".py", ".yml", ".yaml", ".toml", ".css"}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico"}
QUOTE_RE = re.compile(r"[\"“]([^\"”]*)[\"”]")
TAG_STRIP_RE = re.compile(r"<[^>]+>")
JSON_DATA_BLOCK_RE = re.compile(r'<script type="application/json"[^>]*>.*?</script>', re.S)


def _blank_json_data_blocks(text: str) -> str:
    # Injected data blobs (site/*.html's <script type="application/json">
    # payloads) hold real field values -- our own prose, not a copied
    # quotation -- that just happen to use JSON's double-quote string
    # syntax and often run past 15 words per field. Blank them out
    # (preserving line numbers for anything after) so they're never
    # mistaken for a copyright-risk quoted run.
    return JSON_DATA_BLOCK_RE.sub(lambda m: "\n" * m.group(0).count("\n"), text)


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
    text = _blank_json_data_blocks(text)
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
        non_blockquote_indices = []
        non_blockquote_texts = []
        for i, line in enumerate(para_lines):
            if not line.lstrip().startswith(">"):
                non_blockquote_indices.append(i)
                non_blockquote_texts.append(line)

        if non_blockquote_texts:
            # Build position map: (start_char_pos, para_line_index, actual_line_number)
            position_map = []
            current_pos = 0
            for para_idx, line_text in zip(non_blockquote_indices, non_blockquote_texts):
                position_map.append((current_pos, para_idx, start_line + para_idx))
                current_pos += len(line_text) + 1  # +1 for space between lines

            joined_para = " ".join(non_blockquote_texts)

            # Find quotes and map back to their starting line
            for match in QUOTE_RE.finditer(joined_para):
                q = match.group(1)
                if len(q.split()) >= MAX_QUOTE_WORDS:
                    char_pos = match.start()
                    quote_line = start_line  # default
                    # Find which line this match starts on
                    for i in range(len(position_map)):
                        if i < len(position_map) - 1:
                            # Check if char_pos is between this and next position
                            if position_map[i][0] <= char_pos < position_map[i+1][0]:
                                quote_line = position_map[i][2]
                                break
                        else:
                            # Last entry
                            if char_pos >= position_map[i][0]:
                                quote_line = position_map[i][2]
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
            yield from (f for f in sorted(p.rglob("*")) if f.is_file() and "__pycache__" not in f.parts)


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
