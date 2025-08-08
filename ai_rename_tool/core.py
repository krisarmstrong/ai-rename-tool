from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence
from .naming import sanitize_filename, is_good_name, default_category
from .provider import ProviderFn, local_heuristic_provider

@dataclass(frozen=True)
class PlanItem:
    src: Path
    dst: Path

def scan_paths(root: Path, include_hidden: bool = False) -> list[Path]:
    files: list[Path] = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if not include_hidden and any(part.startswith(".") for part in p.relative_to(root).parts):
            continue
        files.append(p)
    return files

def build_plan(
    root: Path,
    files: Sequence[Path],
    provider: ProviderFn = local_heuristic_provider,
    categorise: bool = False,
) -> list[PlanItem]:
    suggestions = provider(files)
    if len(suggestions) != len(files):
        raise ValueError("provider returned mismatched suggestion count")
    plan: list[PlanItem] = []
    used: set[Path] = set()
    for src, proposed in zip(files, suggestions):
        candidate = sanitize_filename(proposed)
        if not is_good_name(candidate):
            candidate = sanitize_filename(src.name)
        dst_dir = root / (default_category(src) if categorise else src.parent.relative_to(root))
        dst_dir.mkdir(parents=True, exist_ok=True)
        dst = _resolve_conflict(dst_dir / candidate, used)
        if dst != src:
            plan.append(PlanItem(src=src, dst=dst))
            used.add(dst)
    return plan

def _resolve_conflict(target: Path, used: set[Path]) -> Path:
    if target not in used and not target.exists():
        return target
    stem, suffix = target.stem, target.suffix
    for i in range(1, 10000):
        cand = target.with_name(f"{stem}_{i}{suffix}")
        if cand not in used and not cand.exists():
            return cand
    raise RuntimeError("could not resolve unique filename after 10k attempts")

def write_plan_json(plan: Sequence[PlanItem], path: Path) -> None:
    data = [{"src": str(i.src), "dst": str(i.dst)} for i in plan]
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")

def write_plan_csv(plan: Sequence[PlanItem], path: Path) -> None:
    import csv
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["src", "dst"])
        for i in plan:
            w.writerow([str(i.src), str(i.dst)])

def read_plan_json(path: Path) -> list[PlanItem]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [PlanItem(src=Path(d["src"]), dst=Path(d["dst"])) for d in data]

def apply_plan(plan: Sequence[PlanItem]) -> None:
    for item in plan:
        item.dst.parent.mkdir(parents=True, exist_ok=True)
        item.src.replace(item.dst)

def undo_plan(path: Path) -> None:
    plan = read_plan_json(path)
    for item in reversed(plan):
        if item.dst.exists():
            item.dst.replace(item.src)
