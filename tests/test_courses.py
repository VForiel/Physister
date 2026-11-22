"""Vérifications de tous les cours : lancer avec ``python -m pytest tests`` depuis la racine."""

import os
import random
import re
import sys
import tempfile
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ["PROGRESS_FILE"] = os.path.join(tempfile.mkdtemp(), "progress.json")

from courses import MODULES, all_terms, load  # noqa: E402

MODS = load()


def test_all_modules_present():
    assert len(MODS) == len(MODULES)


@pytest.mark.parametrize("mod", MODS, ids=lambda m: m.COURSE.code)
def test_questions_build(mod):
    assert len(mod.QUESTIONS) >= 12, "banque de questions trop petite"
    levels = {q.level for q in mod.QUESTIONS}
    assert levels == {1, 2, 3}, f"niveaux présents : {levels}"
    for q in mod.QUESTIONS:
        for seed in range(15):
            inst = q.build(random.Random(seed))
            assert inst.prompt
            if inst.kind == "num":
                assert inst.answer is not None
            else:
                assert inst.correct, inst.prompt
                assert len(inst.options) >= 2, inst.prompt
                assert len(set(inst.options)) == len(inst.options), f"options en double : {inst.prompt}"
                assert all(0 <= i < len(inst.options) for i in inst.correct)


TERM_RE = re.compile(r"\[\[([^\]|\\]+)(?:\\?\|[^\]]+)?\]\]")


def test_terms_exist():
    terms = all_terms()
    missing = []
    for path in (ROOT / "courses").glob("*.py"):
        for key in TERM_RE.findall(path.read_text(encoding="utf-8")):
            if key.strip().lower() not in terms:
                missing.append(f"{path.name}: {key}")
    assert not missing, missing


def _script(code: str, chapter: str | None, tab_seed: int = 0) -> str:
    return f"""
import sys
sys.path.insert(0, {str(ROOT)!r})
import streamlit as st
from courses import load
from app.course import render_course
mod = [m for m in load() if m.COURSE.code == {code!r}][0]
render_course(mod)
"""


@pytest.mark.parametrize("mod", MODS, ids=lambda m: m.COURSE.code)
def test_chapters_render(mod):
    code = mod.COURSE.code
    for name, _ in mod.CHAPTERS:
        at = AppTest.from_string(_script(code, name), default_timeout=60)
        at.session_state[f"{code}_chapter"] = name
        at.run()
        assert not at.exception, f"{code} / {name} : {at.exception}"
