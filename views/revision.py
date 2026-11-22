import streamlit as st

from app import ui
from app.quiz import quiz
from courses import load

ui.start_page()
mods = load()

st.title("Révision mélangée")
st.markdown(
    "Un quiz qui pioche dans plusieurs cours à la fois, comme un examen. Mélanger les matières "
    "est plus difficile sur le moment, mais on retient beaucoup mieux (c'est l'« apprentissage "
    "entrelacé »)."
)

names = {m.COURSE.code: m.COURSE.short for m in mods}
c1, c2 = st.columns(2)
blocs = c1.pills("Blocs", [1, 2], default=[1, 2], selection_mode="multi",
                 format_func=lambda b: f"Bloc {b}", key="rev_blocs")
quads = c2.pills("Quadrimestres", [1, 2], default=[1, 2], selection_mode="multi",
                 format_func=lambda q: f"Q{q}", key="rev_quads")
eligible = [m for m in mods if m.COURSE.bloc in (blocs or []) and m.COURSE.quad in (quads or [])]
chosen = st.multiselect("Cours", [m.COURSE.code for m in eligible],
                        default=[m.COURSE.code for m in eligible],
                        format_func=lambda c: f"{c} · {names[c]}", key="rev_courses")

questions = [q for m in mods if m.COURSE.code in chosen for q in m.QUESTIONS]
if not questions:
    st.info("Choisis au moins un cours.")
else:
    quiz(questions, key=f"quiz_revision_{abs(hash(tuple(sorted(chosen)))) % 10**6}", progress_code="REVISION", show_course=True, course_names=names)
