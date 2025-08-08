from __future__ import annotations
from pathlib import Path
from ai_rename_tool.core import scan_paths, build_plan, write_plan_json, read_plan_json
from ai_rename_tool.provider import local_heuristic_provider

def test_scan_paths(tmp_path: Path):
    (tmp_path / "a.txt").write_text("x")
    (tmp_path / ".hidden").write_text("x")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "b.txt").write_text("y")
    files = scan_paths(tmp_path)
    names = {p.name for p in files}
    assert "a.txt" in names
    assert "b.txt" in names
    assert ".hidden" not in names

def test_build_and_roundtrip(tmp_path: Path):
    (tmp_path / "a.txt").write_text("x")
    (tmp_path / "b.txt").write_text("y")
    files = scan_paths(tmp_path)
    plan = build_plan(tmp_path, files, provider=local_heuristic_provider, categorise=False)
    assert len(plan) == 2
    json_path = tmp_path / "plan.json"
    write_plan_json(plan, json_path)
    plan2 = read_plan_json(json_path)
    assert [(i.src.name, i.dst.name) for i in plan] == [(i.src.name, i.dst.name) for i in plan2]
