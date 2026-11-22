"""
Études de kiné : support d'apprentissage interactif
===================================================

Tous les cours des blocs 1 et 2 du bachelier en kinésithérapie et réadaptation
de l'UCLouvain (KINE1BA), avec explications, zones interactives, quiz
randomisés et fiches mémo. Les anciennes pages de physique sont dans la section
« Archives ».

Lancer avec :
    streamlit run Accueil.py
"""

from pathlib import Path

import streamlit as st

from app.course import render_course
from courses import load

ROOT = Path(__file__).parent

st.set_page_config(page_title="Études de kiné", page_icon=":material/school:", layout="wide",
                   initial_sidebar_state="auto")


def course_page(mod):
    def run():
        render_course(mod)

    run.__name__ = f"page_{mod.COURSE.code.lower()}"
    return st.Page(run, title=mod.COURSE.short, icon=mod.COURSE.icon, url_path=mod.COURSE.code.lower())


sections: dict[str, list] = {
    "": [
        st.Page(ROOT / "views" / "home.py", title="Accueil", icon=":material/home:", default=True),
        st.Page(ROOT / "views" / "revision.py", title="Révision mélangée", icon=":material/quiz:",
                url_path="revision"),
        st.Page(ROOT / "views" / "lexique.py", title="Lexique", icon=":material/dictionary:", url_path="lexique"),
    ]
}
course_pages = {}
for mod in load():
    c = mod.COURSE
    course_pages[c.code] = course_page(mod)
    sections.setdefault(f"Bloc {c.bloc} · quadrimestre {c.quad}", []).append(course_pages[c.code])
st.session_state["_course_pages"] = course_pages  # pour les liens de l'accueil

archive = ROOT / "archive"
sections["Archives : physique"] = [
    st.Page(archive / "Accueil_physique.py", title="Ancien accueil", icon=":material/inventory_2:",
            url_path="archive-accueil"),
] + [
    st.Page(p, title=p.stem[3:].replace("_", " "), icon=":material/inventory_2:",
            url_path=f"archive-{p.stem[:2]}")
    for p in sorted((archive / "physique").glob("*.py"))
]

st.navigation(sections, expanded=True).run()
