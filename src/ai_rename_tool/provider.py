from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Sequence
from pathlib import Path
from .naming import sanitize_filename, is_good_name

@dataclass(frozen=True)
class Suggestion:
    src: Path
    dst_name: str

ProviderFn = Callable[[Sequence[Path]], Sequence[str]]

def local_heuristic_provider(paths: Sequence[Path]) -> Sequence[str]:
    out: list[str] = []
    for p in paths:
        base = p.stem.replace("_", " ").replace("-", " ")
        candidate = sanitize_filename(base.title() + p.suffix.lower())
        if not is_good_name(candidate):
            candidate = sanitize_filename(p.name)
        out.append(candidate)
    return out
