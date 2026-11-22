"""Questionnaires randomisés à plusieurs niveaux.

Une question est décrite une fois, puis « construite » à chaque tirage avec un
générateur aléatoire : l'ordre des réponses change, et les questions numériques
tirent de nouvelles valeurs. Le tirage dépend d'une graine gardée en session,
donc il reste stable tant qu'on ne demande pas un nouveau questionnaire.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Callable

import streamlit as st

from app import progress

LEVELS = {1: "Facile", 2: "Moyen", 3: "Difficile"}


@dataclass
class Instance:
    """Une question prête à afficher."""

    kind: str  # "single", "multi", "tf", "num"
    prompt: str
    options: list[str] = field(default_factory=list)
    correct: set[int] = field(default_factory=set)
    answer: float | None = None
    tol: float = 0.02  # tolérance relative pour les questions numériques
    unit: str = ""
    why: str = ""


@dataclass
class Question:
    level: int
    build: Callable[[random.Random], Instance]
    course: str = ""  # rempli par le registre des cours
    repeatable: bool = False  # générée depuis une table : peut être tirée plusieurs fois


# --- Fabriques -------------------------------------------------------------


def _shuffle(good: list[str], bad: list[str], rng: random.Random, max_bad: int | None = None):
    bad = list(bad)
    if max_bad is not None and len(bad) > max_bad:
        bad = rng.sample(bad, max_bad)
    options = list(good) + bad
    rng.shuffle(options)
    correct = {options.index(g) for g in good}
    return options, correct


def qcm(level: int, prompt: str, good: str, bad: list[str], why: str = "") -> Question:
    """Une seule bonne réponse."""

    def build(rng):
        options, correct = _shuffle([good], bad, rng, max_bad=4)
        return Instance("single", prompt, options, correct, why=why)

    return Question(level, build)


def multi(level: int, prompt: str, good: list[str], bad: list[str], why: str = "") -> Question:
    """Plusieurs bonnes réponses possibles (cocher toutes les bonnes)."""

    def build(rng):
        options, correct = _shuffle(good, bad, rng)
        return Instance("multi", prompt, options, correct, why=why)

    return Question(level, build)


def vf(level: int, statement: str, true: bool, why: str = "") -> Question:
    """Vrai ou faux."""

    def build(rng):
        return Instance("tf", statement, ["Vrai", "Faux"], {0 if true else 1}, why=why)

    return Question(level, build)


def num(level: int, gen: Callable[[random.Random], dict]) -> Question:
    """Question numérique. ``gen(rng)`` renvoie un dict avec prompt, answer,
    et optionnellement unit, tol (relative) et why."""

    def build(rng):
        d = gen(rng)
        return Instance(
            "num", d["prompt"], answer=d["answer"], tol=d.get("tol", 0.02),
            unit=d.get("unit", ""), why=d.get("why", ""),
        )

    return Question(level, build, repeatable=True)


def gen_qcm(level: int, gen: Callable[[random.Random], tuple]) -> Question:
    """QCM tiré d'une table. ``gen(rng)`` renvoie (prompt, bonne, [mauvaises], why)."""

    def build(rng):
        prompt, good, bad, why = gen(rng)
        bad = [b for b in dict.fromkeys(bad) if b != good]
        options, correct = _shuffle([good], bad, rng, max_bad=3)
        return Instance("single", prompt, options, correct, why=why)

    return Question(level, build, repeatable=True)


def table_qcm(level: int, table: dict[str, str], template: str, reverse_template: str | None = None,
              why: str = "") -> Question:
    """Questions générées depuis un dictionnaire clé → valeur.

    ``template`` contient ``{k}`` (on demande la valeur) ; ``reverse_template``
    contient ``{v}`` (on demande la clé). Les valeurs en double sont gérées.
    """

    keys = list(table)

    def gen(rng):
        k = rng.choice(keys)
        v = table[k]
        if reverse_template and rng.random() < 0.5:
            # on cherche une clé qui a cette valeur ; les mauvaises réponses ont une autre valeur
            bad = [x for x in keys if table[x] != v]
            return reverse_template.format(v=v), k, rng.sample(bad, min(6, len(bad))), why
        bad = list({table[x] for x in keys if table[x] != v})
        return template.format(k=k), v, rng.sample(bad, min(6, len(bad))), why

    return gen_qcm(level, gen)


# --- Correction ------------------------------------------------------------


def _is_right(inst: Instance, given) -> bool:
    if given is None:
        return False
    if inst.kind == "num":
        if inst.answer == 0:
            return abs(given) < 1e-9 + inst.tol
        return math.isclose(given, inst.answer, rel_tol=inst.tol)
    if inst.kind == "multi":
        return set(given) == inst.correct
    return given in inst.correct


def _fmt(x: float) -> str:
    if x == 0:
        return "0"
    if abs(x) >= 1e5 or abs(x) < 1e-3:
        return f"{x:.3g}"
    return f"{x:.4g}".replace(".", ",")


def _correct_text(inst: Instance) -> str:
    if inst.kind == "num":
        return f"{_fmt(inst.answer)} {inst.unit}".strip()
    return " ; ".join(inst.options[i] for i in sorted(inst.correct))


# --- Affichage -------------------------------------------------------------


def build_instances(questions: list[Question], seed: int, level: int | None, n: int):
    pool = [q for q in questions if level is None or q.level == level]
    rng = random.Random(seed)
    chosen = rng.sample(pool, min(n, len(pool)))
    # questions générées : on peut les retirer pour compléter le questionnaire
    extra = [q for q in pool if q.repeatable]
    while len(chosen) < n and extra:
        chosen.append(rng.choice(extra))
    return [(q, q.build(random.Random(seed * 1000 + i))) for i, q in enumerate(chosen)]


def quiz(questions: list[Question], key: str, progress_code: str, show_course: bool = False,
         course_names: dict | None = None):
    """Questionnaire complet : choix du niveau, tirage, correction expliquée."""

    if not questions:
        st.info("Pas encore de questions pour ce cours.")
        return

    counts = {lvl: sum(q.level == lvl for q in questions) for lvl in LEVELS}
    c1, c2, c3 = st.columns([3, 2, 2], vertical_alignment="bottom")
    with c1:
        labels = ["Tout"] + [f"{name}" for lvl, name in LEVELS.items() if counts[lvl]]
        choice = st.segmented_control(
            "Niveau", labels, default="Tout", key=f"{key}_lvl",
            help="Facile : définitions et reconnaissance. Moyen : comprendre et relier. "
                 "Difficile : appliquer, calculer, raisonner sur un cas.",
        )
    level = None
    for lvl, name in LEVELS.items():
        if choice == name:
            level = lvl
    with c2:
        n = st.number_input("Nombre de questions", 3, 40, 8, key=f"{key}_n")
    seed_key = f"{key}_seed"
    if seed_key not in st.session_state:
        st.session_state[seed_key] = random.randrange(1_000_000)
    with c3:
        if st.button("Nouveau tirage", icon=":material/shuffle:", key=f"{key}_new", width="stretch"):
            st.session_state[seed_key] = random.randrange(1_000_000)
            st.session_state.pop(f"{key}_graded", None)

    available = sum(1 for q in questions if level is None or q.level == level)
    st.caption(
        f"{available} questions dans la banque pour ce niveau "
        f"({counts[1]} faciles, {counts[2]} moyennes, {counts[3]} difficiles). "
        "Les réponses sont mélangées et les valeurs numériques changent à chaque tirage."
    )

    seed = st.session_state[seed_key]
    tag = f"{key}_{seed}_{level}_{n}"
    items = build_instances(questions, seed, level, int(n))
    graded_key = f"{key}_graded"
    graded = st.session_state.get(graded_key) == tag

    with st.form(f"{tag}_form", border=False):
        answers = []
        for i, (q, inst) in enumerate(items):
            with st.container(border=True):
                head = f"**Question {i + 1}** · {LEVELS[q.level]}"
                if show_course and course_names:
                    head += f" · {course_names.get(q.course, q.course)}"
                st.caption(head)
                st.markdown(inst.prompt)
                k = f"{tag}_q{i}"
                if inst.kind in ("single", "tf"):
                    val = st.radio("Ta réponse", range(len(inst.options)), index=None, key=k,
                                   format_func=lambda j, o=inst.options: o[j], label_visibility="collapsed",
                                   horizontal=inst.kind == "tf")
                elif inst.kind == "multi":
                    st.caption("Plusieurs réponses possibles : coche toutes les bonnes.")
                    val = [j for j, opt in enumerate(inst.options)
                           if st.checkbox(opt, key=f"{k}_{j}")]
                else:
                    val = st.number_input(f"Ta réponse ({inst.unit})" if inst.unit else "Ta réponse",
                                          value=None, format="%.4g", key=k)
                answers.append(val)

                if graded:
                    ok = _is_right(inst, val)
                    if ok:
                        st.success("Juste !", icon=":material/check_circle:")
                    else:
                        st.error(f"Réponse attendue : **{_correct_text(inst)}**", icon=":material/cancel:")
                    if inst.why:
                        st.caption(f":material/info: {inst.why}")
        submitted = st.form_submit_button("Corriger", type="primary", icon=":material/fact_check:")

    if submitted:
        score = sum(_is_right(inst, a) for (q, inst), a in zip(items, answers))
        progress.record_quiz(progress_code, score, len(items), choice or "Tout")
        st.session_state[graded_key] = tag
        st.session_state[f"{key}_score"] = (score, len(items))
        st.rerun()

    if graded and f"{key}_score" in st.session_state:
        score, total = st.session_state[f"{key}_score"]
        ratio = score / total if total else 0
        msg = ("Excellent, tu maîtrises !" if ratio >= 0.85 else
               "Bien, encore quelques points à revoir." if ratio >= 0.6 else
               "Relis la partie cours puis refais un tirage : c'est comme ça qu'on apprend.")
        st.metric("Score", f"{score} / {total}", help=msg)
        st.write(msg)
