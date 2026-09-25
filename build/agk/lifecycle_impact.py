import csv
from collections.abc import Collection
from pathlib import Path

from agk.lifecycle import STAGES

COLUMNS = ("xw_id", "primary_stages", "secondary_stages")
STAGE_SLUGS = {slug for slug, _ in STAGES}


class LifecycleImpactError(Exception):
    pass


def _parse_stages(value: str) -> list[str]:
    return [s.strip() for s in value.split(";") if s.strip()]


def load_lifecycle_impact(path: Path, known_xw: Collection[str]) -> dict[str, dict[str, list[str]]]:
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if tuple(reader.fieldnames or ()) != COLUMNS:
            raise LifecycleImpactError(f"columns must be {','.join(COLUMNS)}; got {reader.fieldnames}")
        out: dict[str, dict[str, list[str]]] = {}
        for n, row in enumerate(reader, start=2):
            row = {k: (v or "").strip() for k, v in row.items()}
            rid = row["xw_id"]
            if rid not in known_xw:
                raise LifecycleImpactError(f"line {n}: unknown crosswalk row {rid}")
            if rid in out:
                raise LifecycleImpactError(f"line {n}: duplicate row {rid}")
            primary = _parse_stages(row["primary_stages"])
            secondary = _parse_stages(row["secondary_stages"])
            for slug in primary + secondary:
                if slug not in STAGE_SLUGS:
                    raise LifecycleImpactError(f"line {n}: unknown stage {slug!r}")
            overlap = set(primary) & set(secondary)
            if overlap:
                raise LifecycleImpactError(
                    f"line {n}: {rid} lists {', '.join(sorted(overlap))} in both primary and secondary")
            if not primary and not secondary:
                raise LifecycleImpactError(f"line {n}: {rid} has no primary or secondary stages")
            out[rid] = {"primary": primary, "secondary": secondary}
    missing = sorted(set(known_xw) - out.keys())
    if missing:
        raise LifecycleImpactError(f"no lifecycle impact for {', '.join(missing)}")
    return out
