import argparse
import json
import re
import sys
from pathlib import Path

MAX_EXTRA = 1
BLOCK_RE = re.compile(r"```findings[ \t]*\n(.*?)\n```", re.S)


class GradeError(Exception):
    pass


def _norm(fid: str) -> str:
    parts = [p.strip() for p in fid.split("+")]
    return "+".join(sorted(parts)) if len(parts) > 1 else parts[0]


def parse_findings(text: str) -> set[tuple[str, str]]:
    blocks = BLOCK_RE.findall(text)
    if not blocks:
        raise GradeError("no findings block in tool output")
    try:
        data = json.loads(blocks[-1])
    except json.JSONDecodeError as e:
        raise GradeError(f"findings block is not valid JSON: {e}") from e
    if not isinstance(data, list):
        raise GradeError("findings block must be a JSON list")
    out = set()
    for item in data:
        if not isinstance(item, dict) or not isinstance(item.get("type"), str) or not isinstance(item.get("id"), str):
            raise GradeError(f"each finding needs string 'type' and 'id': {item!r}")
        out.add((item["type"], _norm(item["id"])))
    return out


def grade(findings: set[tuple[str, str]], key: list[dict], tool: str) -> dict:
    expected = {(k["type"], _norm(k["id"])) for k in key if k["tool"] == tool}
    if not expected:
        raise GradeError(f"no answer-key entries for tool {tool!r}")
    types = {t for t, _ in expected}
    missed = sorted(expected - findings)
    extra = sorted(f for f in findings - expected if f[0] in types)
    return {"passed": not missed and len(extra) <= MAX_EXTRA,
            "missed": [list(m) for m in missed], "extra": [list(e) for e in extra]}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Grade a tool's output against the answer key.")
    parser.add_argument("--tool", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--key", type=Path, default=Path("demo-estate/answer-key.json"))
    args = parser.parse_args(argv)
    try:
        result = grade(parse_findings(args.output.read_text(encoding="utf-8")),
                       json.loads(args.key.read_text(encoding="utf-8")), args.tool)
    except GradeError as e:
        print(f"FAIL: {e}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
