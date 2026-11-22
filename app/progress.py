"""Progression enregistrée côté serveur, dans un fichier JSON.

Le site n'a qu'une utilisatrice : pas de compte, la progression est commune à
tous les appareils. Le fichier se trouve dans ``data/`` (ou là où pointe la
variable d'environnement PROGRESS_FILE, monté sur un volume en production).

Structure : {code du cours: {"quiz": {...}, "chapters": [...], "cards_again": [...]}}
"""

from __future__ import annotations

import json
import os
import threading
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = Path(os.environ.get("PROGRESS_FILE", ROOT / "data" / "progress.json"))
_lock = threading.Lock()


def _read() -> dict:
    try:
        return json.loads(PATH.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _write(data: dict):
    PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(PATH)  # écriture atomique


def all_progress() -> dict:
    with _lock:
        return _read()


def course(code: str) -> dict:
    return all_progress().get(code, {})


def _update(code: str, fn):
    with _lock:
        data = _read()
        entry = data.setdefault(code, {})
        fn(entry)
        _write(data)


def record_quiz(code: str, score: int, total: int, level: str):
    def fn(entry):
        q = entry.setdefault("quiz", {"tries": 0, "best": 0.0, "last": 0.0, "history": []})
        ratio = score / total if total else 0.0
        q["tries"] += 1
        q["last"] = ratio
        q["best"] = max(q["best"], ratio)
        q["history"] = (q["history"] + [{"date": datetime.now().isoformat(timespec="minutes"),
                                         "score": score, "total": total, "level": level}])[-50:]

    _update(code, fn)


def set_chapter(code: str, chapter: str, done: bool):
    def fn(entry):
        chapters = set(entry.get("chapters", []))
        (chapters.add if done else chapters.discard)(chapter)
        entry["chapters"] = sorted(chapters)

    _update(code, fn)


def set_cards_again(code: str, fronts: list[str]):
    def fn(entry):
        entry["cards_again"] = fronts

    _update(code, fn)


def reset(code: str | None = None):
    with _lock:
        data = _read()
        if code is None:
            data = {}
        else:
            data.pop(code, None)
        _write(data)
