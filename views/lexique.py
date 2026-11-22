import streamlit as st

from app import ui
from courses import all_terms

ui.start_page()
st.title("Lexique")
st.markdown("Tous les termes définis dans les cours, avec un lien vers Wikipédia quand il est utile.")

terms = all_terms()
query = st.text_input("Rechercher un terme", placeholder="ex. sarcomère, prévalence, Babinski…",
                      icon=":material/search:")
items = sorted(terms.values(), key=lambda t: t[0].lower())
if query:
    q = query.lower()
    items = [t for t in items if q in t[0].lower() or q in t[1].lower()]
st.caption(f"{len(items)} termes")

letter = None
for name, definition, wiki in items:
    first = name[0].upper()
    if first != letter and not query:
        letter = first
        st.subheader(letter, divider="gray")
    link = f" [Wikipédia]({ui.wiki_url(wiki)})" if wiki else ""
    st.markdown(f"**{name}** : {definition}{link}")
