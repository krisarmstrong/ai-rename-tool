"""Automation sessions for ai-rename-tool."""

from __future__ import annotations

import nox

nox.options.sessions = ["tests"]


@nox.session(python=["3.10", "3.11", "3.12"])
def tests(session: nox.Session) -> None:
    session.install(".")
    session.install("pytest", "pytest-cov")
    session.run("pytest", "--cov=ai_rename_tool", "--cov-report=term-missing", "--cov-report=html")
