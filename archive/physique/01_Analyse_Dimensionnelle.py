import streamlit as st
import pandas as pd

def show_dimensional_analysis_page():
    st.title("📏 Analyse Dimensionnelle")

    st.markdown("""
    L'analyse dimensionnelle est un outil puissant en physique pour vérifier l'homogénéité des formules et déduire des relations entre grandeurs physiques.
    
    ### 1. Principe d'Homogénéité
    Une équation physique doit être homogène : on ne peut additionner ou soustraire que des grandeurs de même dimension.
    
    Exemple : 
    $v = d/t$
    
    Dimension de $v$ : $[L] \cdot [T]^{-1}$
    """)

    st.header("Les 7 Grandeurs de Base")

    st.markdown("En pratique, on utilise surtout les 3 premières grandeurs. Les autres peuvent être bricolées a partir de ces 3 premières mais de façon assez complexe, donc par soucis de simplicité, on les ajoute comme des grandeurs de base.")
    
    data = {
        "Grandeur": ["Longueur", "Masse", "Temps", "Courant électrique", "Température thermodynamique", "Quantité de matière", "Intensité lumineuse"],
        "Dimension": ["L", "M", "T", "I", "Θ (Theta)", "N", "J"],
        "Unité SI": ["mètre (m)", "kilogramme (kg)", "seconde (s)", "ampère (A)", "kelvin (K)", "mole (mol)", "candela (cd)"]
    }
    df = pd.DataFrame(data)
    st.table(df)

    st.header("🔍 Vérificateur de Dimension (Quiz)")

    tab1, tab2, tab3 = st.tabs(["Force", "Énergie/Travail", "Puissance"])

    with tab1:
        st.write("Quelle est la dimension de la **Force** ($F = m \cdot a$) ?")
        col1, col2, col3 = st.columns(3)
        if col1.button("M L T⁻²", key="q1_1"):
            st.success("Correct ! $F = m \cdot a \Rightarrow [M] \cdot ([L] \cdot [T]^{-2})$")
        if col2.button("M L² T⁻²", key="q1_2"):
            st.error("Faux. Ça c'est l'Énergie.")
        if col3.button("M L⁻¹ T⁻²", key="q1_3"):
            st.error("Faux. Ça c'est la Pression.")

    with tab2:
        st.write("Quelle est la dimension du **Travail** ($W = F \cdot d$) ou de l'**Énergie** ?")
        col1, col2, col3 = st.columns(3)
        if col1.button("M L T⁻²", key="q2_1"):
            st.error("Faux. Ça c'est la Force.")
        if col2.button("M L² T⁻²", key="q2_2"):
            st.success("Correct ! $W = F \cdot d \Rightarrow ([M][L]T^{-2}) \cdot [L] = [M][L]^2 T^{-2}$")
        if col3.button("M L² T⁻³", key="q2_3"):
            st.error("Faux. Ça c'est la Puissance.")

    with tab3:
        st.write("Quelle est la dimension de la **Puissance** ($P = E / t$) ?")
        col1, col2, col3 = st.columns(3)
        if col1.button("M L² T⁻²", key="q3_1"):
            st.error("Faux. Ça c'est l'Énergie.")
        if col2.button("M L² T⁻³", key="q3_2"):
            st.success("Correct ! $P = E/t \Rightarrow ([M][L]^2 T^{-2}) / [T] = [M][L]^2 T^{-3}$")
        if col3.button("M L⁻¹ T⁻¹", key="q3_3"):
            st.error("Faux. Ça c'est la Viscosité dynamique (pas loin!).")

    st.header("Quelques Dimensions Dérivées")
    st.latex(r'''
    \begin{aligned}
    \text{Vitesse } (v) &: [L][T]^{-1} \\
    \text{Accélération } (a) &: [L][T]^{-2} \\
    \text{Force } (F) &: [M][L][T]^{-2} \\
    \text{Énergie } (E) &: [M][L]^2[T]^{-2} \\
    \text{Puissance } (P) &: [M][L]^2[T]^{-3} \\
    \text{Pression } (p) &: [M][L]^{-1}[T]^{-2}
    \end{aligned}
    ''')

    st.markdown("---")
    st.header("🦵 Cas Pratique : La Marche et le Pendule")
    
    st.markdown(r"""
    Imaginons que vous étudiez la marche. La jambe peut être modélisée en première approximation comme un **pendule simple** : une masse suspendue à un fil (la jambe) qui oscille sous l'effet de la gravité.
    
    On cherche à déterminer la période $T$ d'un pas (le temps d'un balancement).
    
    **Les paramètres du problème sont :**
    - La longueur de la jambe $L$ (Dimension : $[L]$)
    - La masse de la jambe $m$ (Dimension : $[M]$)
    - L'accélération de la pesanteur $g$ (Dimension : $[L][T]^{-2}$)
    
    On cherche $T$ (Dimension : $[T]$) sous la forme $T = C \cdot L^\alpha \cdot m^\beta \cdot g^\gamma$ (où $C$ est une constante sans dimension).
    
    **Analyse Dimensionnelle :**
    $$
    [T] = [L]^\alpha \cdot [M]^\beta \cdot ([L][T]^{-2})^\gamma
    $$
    
    En regroupant les termes :
    $$
    [T]^1 = [L]^{\alpha + \gamma} \cdot [M]^\beta \cdot [T]^{-2\gamma}
    $$
    
    **Identification des exposants :**
    1. Pour $[M]$ : $\beta = 0$ $\rightarrow$ **La masse n'influe pas sur la période !** (C'est contre-intuitif mais vrai pour un pendule simple).
    2. Pour $[T]$ : $-2\gamma = 1 \Rightarrow \gamma = -1/2$.
    3. Pour $[L]$ : $\alpha + \gamma = 0 \Rightarrow \alpha = - \gamma = 1/2$.
    
    **Résultat :**
    $$
    T = C \cdot L^{1/2} \cdot g^{-1/2} = C \sqrt{\frac{L}{g}}
    $$
    
    Cela explique pourquoi les personnes de grande taille (grand $L$) ont naturellement une cadence de marche plus lente (grand $T$) que les personnes de petite taille !
    """)

    st.markdown("---")
    st.header("⚠️ Gare aux pièges ! (Limites)")
    
    st.warning(r"""
    **Attention : Homogénéité ≠ Validité Physique**
    
    L'analyse dimensionnelle est nécessaire mais pas suffisante (un équation physique **est** forcément homogène, mais une équation homogène **n'est pas** forcément physique).
    
    Reprenons notre pendule. Nous avons trouvé $T = C \sqrt{L/g}$.
    L'analyse dimensionnelle ne peut PAS nous donner la valeur de la constante $C$.
    
    - La physique (Lois de Newton) nous dit que pour de petites oscillations : $T = 2\pi \sqrt{L/g}$. Donc $C \approx 6.28$.
    - Une autre théorie fausse aurait pu proposer $T = \frac{1}{2} \sqrt{L/g}$. C'est homogène, mais c'est faux !
    
    **Le problème de la complexité :**
    Plus il y a de paramètres, plus il y a de combinaisons possibles qui respectent l'homogénéité.
    Si on ajoute une deuxième longueur (ex: $r$, le rayon de la masse), on pourrait avoir :
    $$
    T = \sqrt{\frac{L}{g}} \cdot f\left(\frac{r}{L}\right)
    $$
    Où $f$ est une fonction inconnue arbitraire. Dimensionnellement, $r/L$ est sans dimension, donc on peut le mettre n'importe où sans briser l'homogénéité !
    
    **Conclusion :** Utilisez l'analyse dimensionnelle pour **éliminer les formules impossibles** (ex: $T = \sqrt{g/L}$ est impossible car en $s^{-1}$), mais pas pour prouver qu'une formule est vraie.
    """)

if __name__ == "__main__":
    show_dimensional_analysis_page()
