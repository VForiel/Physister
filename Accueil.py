"""
Cours de physique - application d'apprentissage interactive
===========================================================

Une application Streamlit interactive pour aider à comprendre les concepts
fondamentaux de physique à travers des explications claires et des visualisations interactives.

Lancer avec :
    streamlit run Accueil.py
"""

import streamlit as st

# Configurer la page
st.set_page_config(
    page_title="Cours de physique",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Page principale
st.title("🔬 Cours de physique")

st.markdown("""
Coucou petite soeur ! Cette application interactive t'aide à comprendre les concepts fondamentaux 
de physique à travers des explications claires et des visualisations pratiques 😉

---

### 🎯 Comment utiliser

1. Choisis un sujet dans la barre latérale
2. Lis attentivement les explications
3. Joue avec les visualisations interactives
4. Ajuste les paramètres pour voir comment ils affectent la physique
5. Observe les graphiques et animations en temps réel

---

### 💡 Conseils d'apprentissage

- Commence par les bases (toutes les notions sont introduites dans l'ordre) et progresse graduellement
- Expérimente avec des valeurs extrêmes pour comprendre les limites
- Essaie de prédire ce qui va se passer avant de changer les paramètres
- Fais des liens entre les mathématiques et les représentations visuelles (en physique, on utilise les maths car c'est necessaire pour formaliser, mais on préfère largement tout ce qui visuel pour bien comprendre !)
- **Pose des questions à ton grand frère !**

---

*Fait avec ❤️ pour t'aider à comprendre la meilleur matière des sciences !*
""")