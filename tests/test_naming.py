from __future__ import annotations
from ai_rename_tool.naming import is_good_name, sanitize_filename, default_category
from pathlib import Path

def test_is_good_name():
    assert is_good_name("Hello.txt")
    assert not is_good_name("")
    assert not is_good_name(" bad.txt")
    assert not is_good_name("bad/.txt")

def test_sanitize_filename():
    assert sanitize_filename("Bad*Name?.txt") == "Bad_Name_.txt"
    assert sanitize_filename("  trim  ") == "trim"

def test_default_category():
    assert default_category(Path("a.jpg")) == "images"
    assert default_category(Path("a.mp3")) == "audio"
