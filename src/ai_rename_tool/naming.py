from __future__ import annotations

import re
from pathlib import Path

__all__ = ["is_good_name", "sanitize_filename", "default_category"]

_SAFE_CHARS = re.compile(r"[^A-Za-z0-9._-]+")

def is_good_name(name: str) -> bool:
    if not name or len(name) > 255:
        return False
    if name.strip() != name:
        return False
    if any(ch in name for ch in ("/", '"')):
        return False
    if re.fullmatch(r"[._-]+", name):
        return False
    if re.search(r"\s{2,}", name):
        return False
    return True

def sanitize_filename(name: str) -> str:
    if not name:
        return ""
    base = name.strip()
    base = _SAFE_CHARS.sub("_", base)
    base = re.sub(r"_+", "_", base)
    return base

def default_category(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}:
        return "images"
    if suffix in {".mp4", ".mov", ".mkv", ".avi", ".webm"}:
        return "video"
    if suffix in {".mp3", ".wav", ".flac", ".aac", ".ogg"}:
        return "audio"
    if suffix in {".zip", ".7z", ".rar", ".tar", ".gz", ".bz2"}:
        return "archives"
    if suffix in {".pdf", ".txt", ".md", ".rtf", ".doc", ".docx", ".xls", ".xlsx"}:
        return "documents"
    return "other"
