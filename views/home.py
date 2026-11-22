import streamlit as st

from app import progress, ui
from courses import load

ui.start_page()
mods = load()

st.title("Études de kiné")
st.markdown(
    "Coucou petite sœur ! Ce site reprend **tous les cours des blocs 1 et 2** du bachelier en "
    "kinésithérapie et réadaptation de l'UCLouvain, à Louvain-la-Neuve. Il ne remplace pas tes "
    "syllabus ni tes profs : il est là pour t'aider à **comprendre**, à **t'entraîner** et à "
    "**retenir**."
)

c1, c2, c3 = st.columns(3)
with c1.container(border=True):
    st.markdown("**:material/menu_book: Cours**")
    st.caption("Explications pas à pas, schémas et simulations à manipuler. Les mots soulignés en "
               "pointillés ont une définition au survol et dans le lexique en bas de page.")
with c2.container(border=True):
    st.markdown("**:material/quiz: Quiz**")
    st.caption("Questions tirées au hasard, en trois niveaux : facile (définitions), moyen (comprendre), "
               "difficile (calculer, raisonner sur un cas). Chaque correction est expliquée.")
with c3.container(border=True):
    st.markdown("**:material/style: Fiches mémo**")
    st.caption("Recto, verso, et tu dis honnêtement si tu savais. Les fiches ratées reviennent "
               "à la fin du paquet.")

st.subheader("Comment bien l'utiliser", divider="gray")
st.markdown(
    """
1. **Avant le cours** : survole le chapitre, juste pour savoir de quoi on va parler.
2. **Après le cours** : relis le chapitre et joue avec les zones interactives. Essaie de **prédire**
   ce qui va se passer avant de bouger un curseur : c'est là qu'on apprend le plus.
3. **Le lendemain** : fais un quiz *facile* puis *moyen*, sans regarder le cours. Se tester est
   bien plus efficace que relire (c'est prouvé, c'est l'« effet de test »).
4. **Avant l'examen** : quiz *difficiles* et page **Révision mélangée**, qui mélange plusieurs cours
   comme le ferait un examen.
5. **Espace tes révisions** : un peu chaque jour vaut mieux que tout la veille.
"""
)
ui.tip("Ta progression (chapitres lus, scores des quiz, fiches à revoir) est enregistrée sur le site : "
       "tu la retrouves sur ton téléphone comme sur ton ordi.")

st.subheader("Le programme", divider="gray")
prog = progress.all_progress()
pages = st.session_state["_course_pages"]
for bloc in (1, 2):
    st.markdown(f"#### Bloc {bloc}")
    for quad in (1, 2):
        items = [m for m in mods if m.COURSE.bloc == bloc and m.COURSE.quad == quad]
        st.caption(f"Quadrimestre {quad} · {sum(m.COURSE.credits for m in items)} crédits")
        cols = st.columns(3)
        for i, m in enumerate(items):
            c = m.COURSE
            with cols[i % 3].container(border=True):
                st.page_link(pages[c.code], label=c.title, icon=c.icon)
                p = prog.get(c.code, {})
                n_done = len(set(p.get("chapters", [])) & {n for n, _ in m.CHAPTERS})
                score = f" · quiz {p['quiz']['best']:.0%}" if p.get("quiz") else ""
                st.progress(n_done / len(m.CHAPTERS))
                st.caption(f"{c.code} · {c.credits} cr. · {n_done}/{len(m.CHAPTERS)} chapitres{score}")

with st.expander("Remettre toute la progression à zéro"):
    sure = st.checkbox("Oui, je veux tout effacer (chapitres, quiz, fiches) pour tous les cours")
    if st.button("Tout réinitialiser", icon=":material/restart_alt:", disabled=not sure):
        progress.reset()
        st.rerun()

st.divider()
st.caption("Fait avec amour par ton grand frère. Programme d'après le catalogue UCLouvain 2026-2027 "
           "(KINE1BA). Si quelque chose n'est pas clair ou te semble faux : dis-le-moi !")
