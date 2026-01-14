"""
Travail et Energie
==================

Conservation de l'énergie, travail des forces et collisions.
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(
    page_title="Énergie - cours de physique",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Travail, Énergie et Collisions")
st.warning("🚧 Cette page est en cours de construction. Le contenu peut être incomplet ou sujet à changements.")
st.markdown("### Rien ne se perd, rien ne se crée, tout se transforme !")

# Introduction Théorique
with st.expander("📖 Théorie : Énergie Mécanique", expanded=True):
    st.markdown(r"""
    ### 1. Formes d'Énergie
    *   **Énergie Cinétique** : Liée au mouvement. $E_k = \frac{1}{2} m v^2$.
    *   **Énergie Potentielle de Pesanteur** : Liée à la hauteur. $E_p = m g z$.
    *   **Énergie Potentielle Élastique** : Liée à la déformation d'un ressort. $E_{pe} = \frac{1}{2} k x^2$.
    
    ### 2. Conservation de l'Énergie Mécanique
    Dans un système conservatif (sans frottement), l'énergie mécanique totale est constante :
    $$ E_m = E_k + E_p = \text{constante} $$
    
    ### 3. Travail d'une Force
    Le travail est l'énergie transférée par une force sur un déplacement :
    $$ W_{A \to B} = \int_A^B \vec{F} \cdot d\vec{l} $$
    Théorème de l'Énergie Cinétique : $\Delta E_k = \sum W$.
    
    ### 4. Collisions (Chocs)
    *   **Quantité de Mouvement** : $\vec{p} = m \vec{v}$. Toujours conservée si système isolé.
    *   **Choc Élastique** : Conservation de $\vec{p}$ ET de l'énergie cinétique $E_k$.
    *   **Choc Inélastique** : Conservation de $\vec{p}$ uniquement. Perte d'énergie (chaleur, déformation).
    """)

st.markdown("---")
st.markdown("## 🎮 Exploration interactive")

tab1, tab2 = st.tabs(["🎢 Montagnes Russes (Conservation)", "💥 Collisions 1D"])

# --- TAB 1: Conservation Energie ---
with tab1:
    st.markdown("### Échange Énergie Potentielle / Cinétique")
    st.markdown("Visualisons comment l'énergie se transforme lors d'une chute libre sans frottement.")
    
    col_en1, col_en2 = st.columns([1, 2])
    
    with col_en1:
        h_start = st.slider("Hauteur de départ (m)", 0.0, 50.0, 20.0, 1.0)
        mass_en = st.slider("Masse (kg)", 1.0, 100.0, 10.0, 1.0, key="m_en")
        g = 9.81
        
        # Energie Totale (initiale, v=0)
        E_tot = mass_en * g * h_start
        st.metric("Énergie Mécanique Totale", f"{E_tot:.0f} J")
        
        st.markdown("---")
        h_current = st.slider("Hauteur actuelle (m)", 0.0, h_start, h_start/2, 0.1)
        
        # Calculs
        Ep_curr = mass_en * g * h_current
        Ek_curr = E_tot - Ep_curr
        v_curr = np.sqrt(2 * Ek_curr / mass_en)
        
        st.latex(f"E_p = mgh = {Ep_curr:.0f} \\text{{ J}}")
        st.latex(f"E_k = E_{{tot}} - E_p = {Ek_curr:.0f} \\text{{ J}}")
        st.latex(f"v = \\sqrt{{2E_k/m}} = {v_curr:.2f} \\text{{ m/s}}")

    with col_en2:
        # Graphique barres
        fig, ax = plt.subplots(figsize=(6, 4))
        categories = ['Énergie Potentielle', 'Énergie Cinétique', 'Total']
        values = [Ep_curr, Ek_curr, E_tot]
        colors = ['blue', 'orange', 'green']
        
        ax.bar(categories, values, color=colors)
        ax.set_ylabel("Énergie (Joules)")
        ax.set_ylim(0, E_tot * 1.2) # Marge
        ax.grid(axis='y', alpha=0.3)
        
        # Ajouter les valeurs sur les barres
        for i, v in enumerate(values):
            ax.text(i, v + E_tot*0.02, f"{v:.0f} J", ha='center')
            
        st.pyplot(fig)
        plt.close()
        
        # Petite animation visuelle de la hauteur ?
        st.progress(h_current / 50.0) # Juste pour visualiser la hauteur relative max 50m

# --- TAB 2: Collisions ---
with tab2:
    st.markdown("### Collisions Elastiques et Inélastiques (1D)")
    st.markdown("""
    Deux boules se rentrent dedans. Que se passe-t-il après le choc ?
    """)
    
    col_col1, col_col2 = st.columns([1, 1])
    
    with col_col1:
        st.subheader("Avant le choc")
        m1 = st.number_input("Masse M1 (kg)", 0.1, 10.0, 1.0, 0.1)
        v1 = st.number_input("Vitesse V1 (m/s)", -20.0, 20.0, 5.0, 0.5)
        
        m2 = st.number_input("Masse M2 (kg)", 0.1, 10.0, 1.0, 0.1)
        v2 = st.number_input("Vitesse V2 (m/s)", -20.0, 20.0, -5.0, 0.5)
        
        type_choc = st.radio("Type de Collision", ["Élastique (Rebond parfait)", "Parfaitement Inélastique (Collage)"])

    with col_col2:
        st.subheader("Calculs")
        
        # Quantité de Mouvement Initiale
        p_init = m1 * v1 + m2 * v2
        Ek_init = 0.5 * m1 * v1**2 + 0.5 * m2 * v2**2
        
        st.write(f"**Momentum Initial :** {p_init:.2f} kg·m/s")
        st.write(f"**Énergie Cinétique Initiale :** {Ek_init:.2f} J")
        
        if type_choc == "Élastique (Rebond parfait)":
            # Formules choc élastique 1D
            v1_final = ((m1 - m2)*v1 + 2*m2*v2) / (m1 + m2)
            v2_final = ((m2 - m1)*v2 + 2*m1*v1) / (m1 + m2)
        else:
            # Choc mou : vitesse commune finale
            v_final = p_init / (m1 + m2)
            v1_final = v_final
            v2_final = v_final
            
        # Après le choc
        p_final = m1 * v1_final + m2 * v2_final
        Ek_final = 0.5 * m1 * v1_final**2 + 0.5 * m2 * v2_final**2
        
        st.markdown("---")
        st.subheader("Après le choc")
        st.success(f"**Vitesse V1 finale :** {v1_final:.2f} m/s")
        st.success(f"**Vitesse V2 finale :** {v2_final:.2f} m/s")
        
        st.write(f"**Momentum Final :** {p_final:.2f} kg·m/s (Conservé ? Oui)")
        
        delta_Ek = Ek_final - Ek_init
        if abs(delta_Ek) < 0.001:
            st.info(f"**Énergie Cinétique Finale :** {Ek_final:.2f} J (Conservée)")
        else:
            st.warning(f"**Énergie Cinétique Finale :** {Ek_final:.2f} J (Perte de {abs(delta_Ek):.2f} J)")

    # Visualisation schématique (Flèches)
    fig, ax = plt.subplots(figsize=(10, 2))
    ax.set_xlim(-15, 15)
    ax.set_ylim(-1, 1)
    ax.axis('off')
    
    # Dessin Avant
    ax.text(-14, 0.5, "AVANT", fontweight='bold')
    # Balle 1
    circle1 = plt.Circle((-5, 0), 0.5 * np.sqrt(m1), color='blue', alpha=0.6)
    ax.add_patch(circle1)
    ax.text(-5, -0.8, "M1", ha='center')
    ax.arrow(-5, 0, v1/5, 0, head_width=0.2, head_length=0.3, color='blue')
    
    # Balle 2
    circle2 = plt.Circle((5, 0), 0.5 * np.sqrt(m2), color='red', alpha=0.6)
    ax.add_patch(circle2)
    ax.text(5, -0.8, "M2", ha='center')
    ax.arrow(5, 0, v2/5, 0, head_width=0.2, head_length=0.3, color='red')
    
    st.pyplot(fig)
    
    fig2, ax2 = plt.subplots(figsize=(10, 2))
    ax2.set_xlim(-15, 15)
    ax2.set_ylim(-1, 1)
    ax2.axis('off')
    
    # Dessin Après
    ax2.text(-14, 0.5, "APRÈS", fontweight='bold')
    
    # Positions arbitraires après choc pour visualiser direction
    # Balle 1
    circle1_f = plt.Circle((-2, 0), 0.5 * np.sqrt(m1), color='blue', alpha=0.6)
    ax2.add_patch(circle1_f)
    ax2.arrow(-2, 0, v1_final/5, 0, head_width=0.2, head_length=0.3, color='blue')
    if abs(v1_final) < 0.1: ax2.text(-2, 0.2, "0", ha='center')
    
    # Balle 2
    circle2_f = plt.Circle((2, 0), 0.5 * np.sqrt(m2), color='red', alpha=0.6)
    ax2.add_patch(circle2_f)
    ax2.arrow(2, 0, v2_final/5, 0, head_width=0.2, head_length=0.3, color='red')
    if abs(v2_final) < 0.1: ax2.text(2, 0.2, "0", ha='center')

    st.pyplot(fig2)
