from __future__ import annotations
import argparse
from pathlib import Path
from . import __version__
from .core import scan_paths, build_plan, write_plan_json, write_plan_csv, apply_plan, undo_plan
from .provider import local_heuristic_provider

DEFAULT_JSON = Path("rename_plan.json")
DEFAULT_CSV = Path("rename_plan.csv")

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="ai-rename-tool", description="Suggest and apply safe file renames.")
    p.add_argument("root", type=Path, nargs="?", default=Path("."), help="Root directory to scan")
    p.add_argument("--categorise", action="store_true", help="Move files into category folders (images, video, etc.)")
    p.add_argument("--include-hidden", action="store_true", help="Include hidden files/folders")
    p.add_argument("--apply", action="store_true", help="Apply the generated plan immediately")
    p.add_argument("--undo", type=Path, help="Undo a previous plan by pointing to its JSON file")
    p.add_argument("--json", type=Path, default=DEFAULT_JSON, help="Path to write plan JSON")
    p.add_argument("--csv", type=Path, default=DEFAULT_CSV, help="Path to write plan CSV")
    p.add_argument("--version", action="store_true", help="Print version and exit")
    return p

def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.version:
        print(__version__)
        return 0
    if args.undo:
        undo_plan(args.undo)
        print(f"Undo complete using {args.undo}")
        return 0
    files = scan_paths(args.root, include_hidden=args.include_hidden)
    plan = build_plan(args.root, files, provider=local_heuristic_provider, categorise=args.categorise)
    write_plan_json(plan, args.json)
    write_plan_csv(plan, args.csv)
    if args.apply:
        apply_plan(plan)
        print("Applied rename plan.")
    else:
        print(f"Plan written to {args.json} and {args.csv}. Use --apply to perform changes.")
    return 0

if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
