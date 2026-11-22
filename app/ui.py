"""Briques d'affichage communes à tous les cours.

Dans le texte des cours, ``[[clé]]`` ou ``[[clé|texte affiché]]`` renvoie vers
un terme du lexique : le mot reçoit une infobulle (survol à la souris) et sa
définition est reprise dans le lexique en bas de page, avec un lien Wikipédia.
"""

from __future__ import annotations

import random
import re
from urllib.parse import quote_plus

import streamlit as st

TERM_RE = re.compile(r"\[\[([^\]|\\]+)(?:\\?\|([^\]]+))?\]\]")  # « \| » permis dans les tableaux

CSS = """
<style>
abbr.term { text-decoration: underline dotted; text-underline-offset: 3px; cursor: help; }
div.why { font-size: 0.92rem; opacity: 0.9; border-left: 2px solid var(--primary-color, #4d5f92);
          padding: 0.1rem 0 0.1rem 0.8rem; margin-top: 0.3rem; }
.code-badge { font-family: ui-monospace, monospace; font-size: 0.85rem; padding: 0.1rem 0.45rem;
              border: 1px solid rgba(128,128,128,0.35); border-radius: 8px; margin-right: 0.4rem; }
</style>
"""


def glossary() -> dict:
    from courses import all_terms  # import tardif : évite une boucle d'imports

    return all_terms()


def wiki_url(title: str) -> str:
    # « go » ouvre directement l'article s'il existe, sinon la page de recherche
    return f"https://fr.wikipedia.org/w/index.php?search={quote_plus(title)}&go=Go"


def youtube_url(query: str) -> str:
    return f"https://www.youtube.com/results?search_query={quote_plus(query)}"


def _page_terms() -> list:
    return st.session_state.setdefault("_page_terms", [])


def start_page():
    st.session_state["_page_terms"] = []
    st.markdown(CSS, unsafe_allow_html=True)


def _attr(text: str) -> str:
    text = re.sub(r"\$([^$]+)\$", r"\1", text)  # pas de LaTeX dans une infobulle
    return text.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def terms(text: str, html: bool = True) -> str:
    """Remplace les [[termes]] et les note pour le lexique de la page."""
    gl = glossary()
    seen = _page_terms()

    def repl(m):
        key = m.group(1).strip().lower()
        shown = m.group(2) or m.group(1)
        entry = gl.get(key)
        if entry is None:
            return shown
        if key not in seen:
            seen.append(key)
        if not html:
            return f"**{shown}**"
        return f'<abbr class="term" title="{_attr(entry[1])}">{shown}</abbr>'

    return TERM_RE.sub(repl, text)


def md(text: str):
    """Markdown avec LaTeX et termes du lexique."""
    st.markdown(terms(text), unsafe_allow_html=True)


# --- Encadrés ----------------------------------------------------------------


def tip(text: str):
    """Astuce pour comprendre ou retenir."""
    st.info(terms(text, html=False), icon=":material/lightbulb:")


def memo(text: str):
    """Moyen mnémotechnique."""
    st.success(terms(text, html=False), icon=":material/psychology:")


def warn(text: str):
    """Piège classique, erreur fréquente à l'examen."""
    st.warning(terms(text, html=False), icon=":material/report:")


def clinic(text: str):
    """Lien avec la pratique du kiné."""
    st.info("**En clinique.** " + terms(text, html=False), icon=":material/stethoscope:")


def key_points(points: list[str]):
    """À retenir."""
    body = "\n".join(f"- {terms(p, html=False)}" for p in points)
    st.success("**À retenir**\n\n" + body, icon=":material/bookmark:")


def chart(fig, key: str):
    """Graphique Plotly à axes fixes : quand on bouge un curseur, seules les courbes changent.

    Un interrupteur rend l'échelle automatique ; le zoom et le déplacement faits à la souris (barre d'outils du
    graphique) sont gardés quand les données changent (uirevision).
    """
    auto = st.toggle("Échelle auto", key=f"{key}_auto", help="Ajuster les axes aux courbes. Sinon les axes restent "
                     "fixes pour mieux voir l'effet des réglages. Zoom et déplacement : barre d'outils du graphique.")
    fig.update_layout(uirevision=key)
    if auto:
        fig.update_xaxes(autorange=True)
        fig.update_yaxes(autorange=True)
        fig.update_layout(uirevision=f"{key}_auto")
    st.plotly_chart(fig, width="stretch", key=key, config={"displaylogo": False})


def section(title: str, text: str = ""):
    st.subheader(title, divider="gray")
    if text:
        md(text)


def table(rows: list[dict] | list[list], headers: list[str] | None = None):
    """Petit tableau sans index."""
    import pandas as pd

    df = pd.DataFrame(rows, columns=headers) if headers else pd.DataFrame(rows)
    st.dataframe(df, hide_index=True, width="stretch")


# --- Fiches mémo -------------------------------------------------------------


def flashcards(cards: list[tuple[str, str]], key: str, code: str):
    """Fiches recto/verso tirées au hasard. Les fiches « à revoir » sont enregistrées
    et peuvent être reprises seules plus tard."""
    from app import progress

    if not cards:
        st.info("Pas de fiches pour ce cours.")
        return
    saved_again = [f for f in progress.course(code).get("cards_again", []) if f in dict(cards)]

    c1, c2 = st.columns([3, 2], vertical_alignment="center")
    with c1:
        only_again = st.toggle(f"Seulement mes fiches à revoir ({len(saved_again)})", key=f"{key}_only",
                               disabled=not saved_again)
        reverse = st.toggle("Sens inverse (verso → recto)", key=f"{key}_rev")
    deck = [i for i, (f, _) in enumerate(cards) if not only_again or f in saved_again]

    state = st.session_state.get(f"{key}_cards")
    if state is None or state["deck"] != deck:
        order = list(deck)
        random.shuffle(order)
        state = {"deck": deck, "order": order, "pos": 0, "flip": False, "known": 0, "again": []}
        st.session_state[f"{key}_cards"] = state
    with c2:
        st.caption(f"Su : {state['known']} · À revoir : {len(state['again'])} · Restantes : "
                   f"{len(state['order']) - state['pos']}")

    def answer(knew: bool):
        idx = state["order"][state["pos"]]
        front = cards[idx][0]
        again = [f for f in progress.course(code).get("cards_again", []) if f != front]
        if knew:
            state["known"] += 1
        else:
            state["again"].append(idx)
            again.append(front)
        progress.set_cards_again(code, again)
        state.update(pos=state["pos"] + 1, flip=False)

    if state["pos"] >= len(state["order"]):
        st.success("Paquet terminé !")
        if state["again"]:
            if st.button(f"Revoir tout de suite les {len(state['again'])} fiches ratées", key=f"{key}_redo",
                         type="primary"):
                state.update(order=state["again"], again=[], pos=0, flip=False)
                st.rerun()
        if st.button("Recommencer le paquet", key=f"{key}_all"):
            del st.session_state[f"{key}_cards"]
            st.rerun()
        return

    idx = state["order"][state["pos"]]
    front, back = cards[idx]
    if reverse:
        front, back = back, front
    # pas de HTML autour du texte : le LaTeX ($…$) ne serait plus interprété
    with st.container(border=True):
        st.markdown(f"#### {terms(front)}", unsafe_allow_html=True)
        if state["flip"]:
            st.divider()
            st.markdown(terms(back), unsafe_allow_html=True)

    b1, b2, b3 = st.columns(3)
    if not state["flip"]:
        b1.button("Retourner", key=f"{key}_flip", type="primary", width="stretch", icon=":material/flip:",
                  on_click=lambda: state.update(flip=True))
    else:
        b1.button("Je savais", key=f"{key}_ok", width="stretch", icon=":material/check:",
                  on_click=answer, args=(True,))
        b2.button("À revoir", key=f"{key}_ko", width="stretch", icon=":material/replay:",
                  on_click=answer, args=(False,))
    if b3.button("Mélanger", key=f"{key}_shuf", width="stretch", icon=":material/shuffle:"):
        del st.session_state[f"{key}_cards"]
        st.rerun()

    with st.expander("Voir toutes les fiches sous forme de liste"):
        for f, b in cards:
            st.markdown(f"- **{terms(f, html=False)}** : {terms(b, html=False)}")


# --- Ressources et lexique ---------------------------------------------------


def resources(videos: list[tuple[str, str]], links: list[tuple[str, str]], code: str, year: int = 2026):
    st.markdown(f"[Fiche officielle du cours {code} sur le site de l'UCLouvain]"
                f"(https://uclouvain.be/cours-{year}-{code.lower()})")
    if videos:
        st.markdown("#### Vidéos")
        st.caption("Chaque lien ouvre une recherche YouTube ciblée : choisis une vidéo récente, "
                   "de préférence d'une chaîne universitaire ou d'un enseignant.")
        for title, query in videos:
            st.markdown(f"- [{title}]({youtube_url(query)})")
    if links:
        st.markdown("#### Pour aller plus loin")
        for title, url in links:
            st.markdown(f"- [{title}]({url})")


def page_glossary():
    keys = _page_terms()
    if not keys:
        return
    gl = glossary()
    st.subheader("Lexique de la page", divider="gray")
    st.caption("Les mots soulignés en pointillés dans le texte ont une infobulle : passe la souris dessus.")
    for k in sorted(keys, key=lambda x: gl[x][0].lower()):
        name, definition, wiki = gl[k]
        link = f" [Wikipédia]({wiki_url(wiki)})" if wiki else ""
        st.markdown(f"**{name}** : {definition}{link}")
