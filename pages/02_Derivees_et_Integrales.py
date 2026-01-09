import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Dérivées et Intégrales",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Dérivées et Intégrales")
st.markdown("""
### Les deux super-pouvoirs de la physique

En physique, on passe notre temps à se poser deux questions :
1.  **Comment ça change ?** (Vitesse, accélération, pente, taux de variation) -> **La Dérivée**
2.  **Combien ça fait au total ?** (Distance parcourue, énergie accumulée, aire totale) -> **L'Intégrale**
""")

st.write("Visualise comment on passe d'une grandeur à l'autre.")
    
st.graphviz_chart("""
digraph G {
    rankdir=LR;
    node [fontname="Helvetica", shape=box, style=filled, color="#BBDEFB"];
    
    Pos [label="Position / Angle\n(m ou °)", fillcolor="#E3F2FD"];
    Vit [label="Vitesse\n(m/s ou °/s)", fillcolor="#FFF3E0"];
    Acc [label="Accélération\n(m/s² ou °/s²)", fillcolor="#FFEBEE"];
    
    Pos -> Vit [label="DÉRIVÉE\n(Pente)", color="#1565C0", fontcolor="#1565C0"];
    Vit -> Acc [label="DÉRIVÉE\n(Pente)", color="#E65100", fontcolor="#E65100"];
    
    Acc -> Vit [label="INTÉGRALE\n(Aire)", color="#C62828", fontcolor="#C62828", style=dashed];
    Vit -> Pos [label="INTÉGRALE\n(Aire)", color="#2E7D32", fontcolor="#2E7D32", style=dashed];
}
""")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["⚡ La Dérivée", "∫ L'Intégrale", "📚 Formules Usuelles", "💡 Astuces de Grand Frère", "📝 Exemples Détaillés"])

# --- SECTION DÉRIVÉE ---
with tab1:
    st.header("⚡ La Dérivée : Le Zoom sur l'Instant")
    st.info("La dérivée, c'est simple : c'est la **pente** de la courbe à un moment précis. C'est la vitesse instantanée.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### L'analogie du Compteur de Vitesse")
        st.markdown("""
        Imagine que tu es en voiture.
        *   Ta position change tout le temps.
        *   Si tu regardes ton **compteur de vitesse** à un instant précis, tu lis ta **dérivée** (la vitesse).
        
        Mathématiquement, on note souvent la fonction $f(x)$ et sa dérivée $f'(x)$.
        
        Si $f(t)$ est ta position au temps $t$, alors $f'(t)$ est ta vitesse.
        """)
        
    with col2:
        st.markdown("#### Expérience Interactive")
        st.write("Regarde la courbe $f(x) = x^2$ (par exemple, une balle qui accélère).")
        x0 = st.slider("Choisis un point x", -5.0, 5.0, 1.0, 0.1)
        
        # Plotting
        x = np.linspace(-6, 6, 200)
        y = x**2
        
        # Tangent line: y = f'(x0) * (x - x0) + f(x0)
        # f'(x) = 2x
        slope = 2 * x0
        y0 = x0**2
        y_tangent = slope * (x - x0) + y0
        
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(x, y, label="f(x) = x²", linewidth=2)
        ax.plot(x, y_tangent, '--', color='red', label=f"Tangente (pente = {slope:.2f})")
        ax.scatter([x0], [y0], color='red', s=100, zorder=5)
        ax.set_ylim(-5, 40)
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_title(f"Au point x={x0}, la pente est {slope:.2f}")
        st.pyplot(fig)
        
        st.success(f"""
        **Analyse :**
        *   Au point **x = {x0}**, la fonction vaut **{y0:.2f}**.
        *   La pente de la ligne rouge est **{slope:.2f}**.
        *   C'est ça la dérivée ! $f'({x0}) = {slope:.2f}$.
        """)

# --- SECTION INTÉGRALE ---
with tab2:
    st.header("∫ L'Intégrale : L'Accumulation")
    st.info("L'intégrale, c'est l'inverse : c'est la **somme** de tous les petits changements. C'est l'aire sous la courbe.")

    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### L'analogie du Réservoir")
        st.markdown("""
        Imagine que tu remplis une baignoire.
        *   Le débit d'eau (litres par seconde) change peut-être (tu ouvres plus ou moins le robinet).
        *   L'**intégrale** de ce débit sur le temps, c'est le **volume total** d'eau dans la baignoire.
        
        En graphique, c'est littéralement la surface coloriée sous le trait.
        """)

    with col2:
        st.markdown("#### Expérience Interactive")
        st.write("Fonction de vitesse : $f(x) = \\cos(x) + 2$")
        
        range_val = st.slider("Choisis l'intervalle [a, b]", 0.0, 10.0, (1.0, 5.0))
        a, b = range_val
        
        x = np.linspace(0, 10, 200)
        y = np.cos(x) + 2
        
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(x, y, label="f(x) = cos(x) + 2", color='green')
        
        # Fill area
        x_fill = np.linspace(a, b, 100)
        y_fill = np.cos(x_fill) + 2
        ax.fill_between(x_fill, y_fill, alpha=0.3, color='green', label="Aire (Intégrale)")
        
        # Calculate area roughly implies exact math: sin(x) + 2x
        area = (np.sin(b) + 2*b) - (np.sin(a) + 2*a)
        
        ax.set_ylim(0, 4)
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_title(f"Aire entre {a} et {b} ≈ {area:.2f}")
        st.pyplot(fig)
        
        st.success(f"L'intégrale (la surface verte) vaut **{area:.2f}**.")

# --- SECTION TABLEAU ---
with tab3:
    st.header("📚 Tableau des Classiques")
    st.write("Voici les fonctions que tu croiseras 99% du temps en physique.")
    
    st.markdown("""
    | Fonction $f(x)$ | Dérivée $f'(x)$ (La pente) | Primitive $\int f(x) dx$ (L'aire) |
    | :--- | :--- | :--- |
    | **Constante** ($C$) | $0$ | $Cx$ |
    | **Puissance** ($x^n$) | $nx^{n-1}$ | $\\frac{x^{n+1}}{n+1}$ |
    | **Exponentielle** ($e^{ax}$) | $ae^{ax}$ | $\\frac{1}{a}e^{ax}$ |
    | **Logarithme** ($\ln x$) | $1/x$ | $x\ln x - x$ |
    | **Sinus** ($\sin x$) | $\cos x$ | $-\cos x$ |
    | **Cosinus** ($\cos x$) | $-\sin x$ | $\sin x$ |
    """)
    
    st.warning("⚠️ **Attention au signe moins** quand tu dérives/intègres cosinus et sinus ! Regarde l'onglet Astuces.")

# --- SECTION ASTUCES ---
with tab4:
    st.header("💡 Astuces de Grand Frère")
    
    st.subheader("1. Le Cycle Trigonométrique")
    st.markdown("""
    Pour ne jamais te tromper de signe entre sinus et cosinus, imagine un cercle ou une horloge.
    
    *   **Pour DÉRIVER** : Tu tournes dans le sens des Aiguilles d'une Montre (Sens **D**érivée -> **D**roite/Descente/Direct).
    *   **Pour INTÉGRER** : Tu tournes en sens inverse.
    
    $$ \sin \Rightarrow \cos \Rightarrow -\sin \Rightarrow -\cos \Rightarrow \sin $$
    """)
    st.code("Dériver : sin -> cos -> -sin -> -cos\nIntégrer : cos -> sin -> -cos -> -sin", language="text")

    st.subheader("2. L'homogénéité (Les unités)")
    st.markdown("""
    Gros doute en examen ? Vérifie les unités !
    
    *   Une **Dérivée** ($dx/dt$), c'est une division par le temps.
        *   Si $x$ est en mètres, $x'$ est en m/s.
    *   Une **Intégrale** ($\int v dt$), c'est une multiplication par le temps.
        *   Si $v$ est en m/s, l'intégrale est en mètres.
        
    *Si tu intègres une accélération (m/s²), tu obtiens une vitesse (m/s). Si tu dérives, tu obtiens des m/s³, ce qui est bizarre (le jerk).*
    """)
    
    st.subheader("3. L'argument de l'exponentielle")
    st.markdown("""
    En physique, on a souvent des $e^{-t/\\tau}$ ou des $\\cos(\\omega t)$.
    Quand tu dérives par rapport au temps $t$, n'oublie jamais de **sortir ce qui est devant le t**.
    
    *   Dérivée de $e^{\\alpha t}$ $\\rightarrow$ $\\alpha e^{\\alpha t}$
    *   Intégrale de $e^{\\alpha t}$ $\\rightarrow$ $\\frac{1}{\\alpha} e^{\\alpha t}$
    
    (C'est la règle de la chaîne, ou "chain rule" en anglais).
    """)

# --- SECTION EXEMPLES ---
with tab5:
    st.header("📝 Exemples Kiné : La théorie dans la vraie vie")
    st.write("Voyons comment cela s'applique concrètement en rééducation et biomécanique.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Dérivée : Vitesse Angulaire du Coude")
        st.markdown("**Contexte :** Tu analyses la flexion du coude d'un patient. L'angle de flexion $\\theta(t)$ (en degrés) est donné par :")
        st.latex(r"\theta(t) = 3t^2 + 2t + 5")
        st.markdown("**Question :** Quelle est la vitesse angulaire instantanée $\\omega(t)$ (en degrés/seconde) ?")
        
        st.info("""
        **Rappel :** La vitesse angulaire est la **dérivée** de l'angle par rapport au temps.
        $$ \\omega(t) = \\theta'(t) $$
        """)
        
        st.markdown("""
        **Calcul pas à pas :**
        1.  **Identifier les termes :**
            *   $3t^2$ (terme quadratique)
            *   $2t$ (terme linéaire)
            *   $5$ (angle initial constant)
            
        2.  **Dériver chaque terme :**
            *   $(3t^2)' = 3 \\times 2t = 6t$
            *   $(2t)' = 2 \\times 1 = 2$
            *   $(5)' = 0$ (la position initiale ne change pas la vitesse)
            
        3.  **Résultat :**
            $$ \\omega(t) = 6t + 2 \\text{ °/s} $$
        """)
        
        st.success("✅ La vitesse de flexion augmente avec le temps (le mouvement accélère).")
        
    with col2:
        st.subheader("2. Intégrale : Distance de Marche")
        st.markdown("**Contexte :** Un patient en rééducation avance avec une vitesse qui augmente au fil du temps :")
        st.latex(r"v(t) = 3t^2 + 2")
        st.markdown("**Question :** Quelle distance totale $D$ a-t-il parcourue entre $t=0$ et $t=2$ secondes ?")
        
        st.info("""
        **Stratégie :** On intègre chaque terme de la somme séparément.
        $$ D = \\int_{0}^{2} (3t^2 + 2) dt $$
        """)
        
        st.markdown("""
        **Calcul pas à pas :**
        
        **1. Trouver la Primitive de chaque morceau :**
        *   **Terme $3t^2$ :**
            *   On garde le $3$.
            *   $t^2$ devient $\\frac{t^3}{3}$.
            *   $$ 3 \\times \\frac{t^3}{3} = t^3 $$
        *   **Terme $2$ :**
            *   Une constante $C$ devient $Ct$.
            *   $$ 2 \\rightarrow 2t $$
            
        $\\Rightarrow$ **Primitive Totale :** $P(t) = t^3 + 2t$
        
        **2. Évaluer entre 0 et 2 :**
        $$ D = P(2) - P(0) $$
        
        *   **À $t=2$ :**
            $$ P(2) = (2)^3 + 2(2) = 8 + 4 = 12 $$
        *   **À $t=0$ :**
            $$ P(0) = (0)^3 + 2(0) = 0 $$
            
        **3. Résultat Final :**
        $$ D = 12 - 0 = 12 \\text{ mètres} $$
        """)
        
        st.success("✅ Le patient a parcouru **12 mètres**.")
    
