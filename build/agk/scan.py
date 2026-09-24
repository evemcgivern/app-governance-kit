import argparse
import os
import re
import sys
import zipfile
from pathlib import Path

MAX_QUOTE_WORDS = 15
SCAN_DIRS = ("methods", "agents", "case-studies", "site", "dist", "demo-estate", "README.md")  # Task 14b adds "field-guide"
QUOTE_DIRS = ("methods", "agents", "case-studies", "site")
TEXT_SUFFIXES = {".md", ".csv", ".html", ".json", ".txt"}
QUOTE_RE = re.compile(r"[\"“]([^\"”\n]+)[\"”]")
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
    for n, line in enumerate(text.splitlines(), start=1):
        if line.lstrip().startswith(">") and len(line.lstrip("> ").split()) >= MAX_QUOTE_WORDS:
            hits.append(f"{label}:{n}: blockquote of {MAX_QUOTE_WORDS}+ words")
        for q in QUOTE_RE.findall(line):
            if len(q.split()) >= MAX_QUOTE_WORDS:
                hits.append(f"{label}:{n}: quoted run of {MAX_QUOTE_WORDS}+ words")
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
        if f.suffix in (".docx", ".xlsx", ".pptx"):
            hits += private_hits(docx_text(f), words, label)
        elif f.suffix in TEXT_SUFFIXES:
            hits += private_hits(f.read_text(encoding="utf-8", errors="replace"), words, label)
    for f in _files(root, QUOTE_DIRS):
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
