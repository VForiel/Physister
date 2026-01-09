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
st.markdown("### Apprentissage interactif pour étudiants en physique")

st.markdown("""
Bienvenue ! Cette application interactive t'aide à comprendre les concepts fondamentaux 
de physique à travers des explications claires et des visualisations pratiques.

---

### 📚 Sujets disponibles

Sélectionne un sujet dans la barre latérale pour commencer :

- **Cinématique** : vitesse, accélération et mouvement
- *(D'autres sujets arrivent bientôt !)*

---

### 🎯 Comment utiliser

1. Choisis un sujet dans la barre latérale
2. Lis attentivement les explications
3. Joue avec les visualisations interactives
4. Ajuste les paramètres pour voir comment ils affectent la physique
5. Observe les graphiques et animations en temps réel

---

### 💡 Conseils d'apprentissage

- Commence par les bases et progresse graduellement
- Expérimente avec des valeurs extrêmes pour comprendre les limites
- Essaie de prédire ce qui va se passer avant de changer les paramètres
- Fais des liens entre les mathématiques et les représentations visuelles
- **Pose des questions à ton grand frère !**

---

*Fait avec ❤️ pour t'aider à comprendre la physique*
""")