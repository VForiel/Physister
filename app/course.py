"""Description d'un cours et rendu de sa page."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import ModuleType

import streamlit as st

from app import progress, ui
from app.quiz import quiz


@dataclass
class Course:
    code: str
    title: str
    short: str  # titre court pour la barre latérale
    bloc: int
    quad: int
    credits: int
    hours: str
    icon: str
    intro: str  # pourquoi ce cours compte pour un kiné, en deux ou trois phrases
    acquis: list[str] = field(default_factory=list)  # d'après la fiche officielle


def _chapter_key(code: str) -> str:
    return f"{code}_chapter"


def render_course(mod: ModuleType):
    ui.start_page()
    c: Course = mod.COURSE
    st.title(c.title)
    st.markdown(
        f"<span class='code-badge'>{c.code}</span> Bloc {c.bloc} · Q{c.quad} · {c.credits} crédits · {c.hours}",
        unsafe_allow_html=True,
    )
    ui.md(c.intro)
    _progress_box(mod)

    tab_cours, tab_quiz, tab_cards, tab_res = st.tabs(
        [":material/menu_book: Cours", ":material/quiz: Quiz", ":material/style: Fiches mémo",
         ":material/link: Ressources"]
    )

    with tab_cours:
        if c.acquis:
            with st.expander("Ce que l'UCLouvain attend de toi à la fin du cours (acquis d'apprentissage)"):
                for a in c.acquis:
                    st.markdown(f"- {a}")
        chapters = mod.CHAPTERS
        names = [name for name, _ in chapters]
        key = _chapter_key(c.code)
        if st.session_state.get(key) not in names:
            st.session_state[key] = names[0]
        done = set(progress.course(c.code).get("chapters", []))
        choice = st.segmented_control("Chapitre", names, key=key, label_visibility="collapsed",
                                      format_func=lambda n: f"✓ {n}" if n in done else n)
        if choice is None:  # clic sur le chapitre déjà actif : on le garde
            choice = names[0]
        i = names.index(choice)
        st.header(f"{i + 1}. {choice}")
        chapters[i][1]()

        st.divider()
        done_key = f"{c.code}_done_{i}"
        st.session_state[done_key] = choice in done  # toujours repartir du fichier enregistré
        st.checkbox("J'ai lu et compris ce chapitre", key=done_key,
                    on_change=lambda: progress.set_chapter(c.code, choice, st.session_state[done_key]))
        b1, _, b2 = st.columns([2, 3, 2])
        if i > 0:
            b1.button(f"← {names[i - 1]}", key=f"{c.code}_prev", width="stretch",
                      on_click=lambda: st.session_state.update({key: names[i - 1]}))
        if i < len(names) - 1:
            b2.button(f"{names[i + 1]} →", key=f"{c.code}_next", width="stretch", type="primary",
                      on_click=lambda: st.session_state.update({key: names[i + 1]}))
        ui.page_glossary()

    with tab_quiz:
        st.markdown("Teste-toi : choisis un niveau, réponds, puis clique sur **Corriger** "
                    "pour voir les explications. **Nouveau tirage** donne d'autres questions.")
        quiz(mod.QUESTIONS, key=f"quiz_{c.code}", progress_code=c.code)

    with tab_cards:
        st.markdown("Lis le recto, essaie de répondre de tête, puis retourne la fiche. "
                    "Sois honnête avec toi-même : les fiches « à revoir » reviennent à la fin.")
        ui.flashcards(getattr(mod, "CARDS", []), key=f"cards_{c.code}", code=c.code)

    with tab_res:
        ui.resources(getattr(mod, "VIDEOS", []), getattr(mod, "LINKS", []), c.code)


def _progress_box(mod: ModuleType):
    c: Course = mod.COURSE
    p = progress.course(c.code)
    n_done = len(set(p.get("chapters", [])) & {n for n, _ in mod.CHAPTERS})
    q = p.get("quiz")
    label = f"Ma progression : {n_done}/{len(mod.CHAPTERS)} chapitres"
    if q:
        label += f" · meilleur quiz {q['best']:.0%}"
    with st.popover(label, icon=":material/insights:"):
        st.progress(n_done / len(mod.CHAPTERS), text=f"{n_done} chapitres lus sur {len(mod.CHAPTERS)}")
        if q:
            st.markdown(f"**Quiz** : {q['tries']} essais, dernier {q['last']:.0%}, meilleur {q['best']:.0%}")
            hist = q.get("history", [])[-8:]
            if hist:
                st.caption(" · ".join(f"{h['date'][5:10]} {h['score']}/{h['total']}" for h in hist))
        else:
            st.caption("Pas encore de quiz fait pour ce cours.")
        n_again = len(p.get("cards_again", []))
        st.markdown(f"**Fiches à revoir** : {n_again}")
        if st.button("Réinitialiser ce cours", icon=":material/restart_alt:", key=f"{c.code}_reset"):
            progress.reset(c.code)
            st.session_state.pop(f"cards_{c.code}_cards", None)
            st.rerun()
