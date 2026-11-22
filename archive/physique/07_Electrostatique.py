"""
Électrostatique
===============

Charges électriques, loi de Coulomb et champ électrique.
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(
    page_title="Électrostatique - cours de physique",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Électrostatique : Charges et Champs")
st.warning("🚧 Cette page est en cours de construction. Le contenu peut être incomplet ou sujet à changements.")
st.markdown("### Les forces invisibles entre les charges")

# Introduction Théorique
with st.expander("📖 Théorie : Coulomb et Gauss", expanded=True):
    st.markdown(r"""
    ### 1. Loi de Coulomb
    La force électrostatique entre deux charges ponctuelles $q_1$ et $q_2$ séparées par une distance $r$ est :
    
    $$ \vec{F}_{1 \to 2} = k \frac{q_1 q_2}{r^2} \vec{u}_{12} $$
    
    *   $k \approx 9 \times 10^9$ N·m²/C².
    *   Les charges de même signe se repoussent, les signes opposés s'attirent.
    
    ### 2. Champ Électrique
    Le champ électrique $\vec{E}$ créé par une charge $q$ est la force subie par une charge test unitaire :
    
    $$ \vec{E} = \frac{\vec{F}}{q_{test}} = k \frac{q}{r^2} \vec{u} $$
    
    ### 3. Théorème de Gauss
    Le flux du champ électrique à travers une surface fermée est proportionnel à la charge intérieure :
    
    $$ \oint \vec{E} \cdot d\vec{S} = \frac{Q_{int}}{\epsilon_0} $$
    
    *   Application (Sphère chargée) : À l'extérieur, le champ est le même que si toute la charge était concentrée au centre. À l'intérieur d'une coquille vide, le champ est nul.
    """)

st.markdown("---")
st.markdown("## 🎮 Exploration interactive")

tab1, tab2 = st.tabs(["🧲 Loi de Coulomb", "🌐 Champ Électrique (2D)"])

# --- TAB 1: Coulomb ---
with tab1:
    st.markdown("### Force entre deux charges")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        q1 = st.slider("Charge q1 (µC)", -10.0, 10.0, 5.0, 1.0)
        q2 = st.slider("Charge q2 (µC)", -10.0, 10.0, -5.0, 1.0)
        dist = st.slider("Distance r (cm)", 1.0, 50.0, 10.0, 1.0)
        
        # Calcul
        k = 9e9
        r_m = dist / 100.0
        q1_C = q1 * 1e-6
        q2_C = q2 * 1e-6
        
        F_mag = k * abs(q1_C * q2_C) / (r_m**2)
        
        st.markdown("---")
        st.latex(f"|F| = k \\frac{{|q_1 q_2|}}{{r^2}} = {F_mag:.2f} \\text{{ N}}")
        
        if q1 * q2 > 0:
            st.error("Répulsion ! ⬅️ ➡️")
        elif q1 * q2 < 0:
            st.success("Attraction ! ➡️ ⬅️")
        else:
            st.info("Force nulle (une charge est neutre).")

    with col2:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.set_xlim(-0.3, 0.3)
        ax.set_ylim(-0.2, 0.2)
        ax.axis('off')
        
        # Position des charges
        # Centré sur 0. q1 à gauche, q2 à droite
        # Ecartement visuel fixe ou proportionnel ? Fixe pour lisibilité
        pos1 = -0.1
        pos2 = 0.1
        
        # Dessin q1
        color1 = 'red' if q1 > 0 else 'blue' if q1 < 0 else 'gray'
        circle1 = plt.Circle((pos1, 0), 0.03, color=color1, alpha=0.7)
        ax.add_patch(circle1)
        ax.text(pos1, -0.06, f"q1\n{q1}µC", ha='center')
        
        # Dessin q2
        color2 = 'red' if q2 > 0 else 'blue' if q2 < 0 else 'gray'
        circle2 = plt.Circle((pos2, 0), 0.03, color=color2, alpha=0.7)
        ax.add_patch(circle2)
        ax.text(pos2, -0.06, f"q2\n{q2}µC", ha='center')
        
        # Flèches de force
        if F_mag > 1e-9: # Eviter calcul 0
            # Echelle visuelle (logique ? ou saturée ?)
            # On veut voir la direction surtout
            vis_len = 0.05
            
            # F12 (Force sur 1 exercée par 2)
            # Répulsion : vers la gauche (-1). Attraction : vers la droite (+1)
            direction = -1 if (q1*q2 > 0) else 1
            ax.arrow(pos1, 0, direction*vis_len, 0, head_width=0.02, head_length=0.02, color='black')
            ax.text(pos1 + direction*vis_len*1.2, 0.02, "F(2->1)", ha='center')
            
            # F21 (Force sur 2 exercée par 1)
            # Répulsion : vers la droite (1). Attraction : vers la gauche (-1)
            direction2 = 1 if (q1*q2 > 0) else -1
            ax.arrow(pos2, 0, direction2*vis_len, 0, head_width=0.02, head_length=0.02, color='black')
            ax.text(pos2 + direction2*vis_len*1.2, 0.02, "F(1->2)", ha='center')
            
        st.pyplot(fig)

# --- TAB 2: Champ Electrique ---
with tab2:
    st.markdown("### Visualisation du Champ Électrique")
    st.markdown("Dipôle Électrique : Deux charges opposées.")
    
    col_field1, col_field2 = st.columns([1, 3])
    
    with col_field1:
        st.write("Configuration")
        sep_dist = st.slider("Séparation", 0.1, 2.0, 1.0, 0.1)
        q_val = st.slider("Valeur Charge (+/-)", 1.0, 10.0, 1.0, 1.0)
    
    with col_field2:
        # Grille
        nx, ny = 20, 20
        x = np.linspace(-2, 2, nx)
        y = np.linspace(-2, 2, ny)
        X, Y = np.meshgrid(x, y)
        
        # Charges
        charges = [
            {'q': q_val, 'x': -sep_dist/2, 'y': 0},
            {'q': -q_val, 'x': sep_dist/2, 'y': 0}
        ]
        
        Ex, Ey = np.zeros((ny, nx)), np.zeros((ny, nx))
        
        for charge in charges:
            # r = sqrt((x-x0)^2 + (y-y0)^2)
            dx = X - charge['x']
            dy = Y - charge['y']
            r2 = dx**2 + dy**2
            r = np.sqrt(r2)
            
            # E = k q / r^2 * u . Avec u = r_vec / r
            # Ex = k q / r^2 * (dx/r) = k q dx / r^3
            # Eviter division par zero au coeur de la charge
            with np.errstate(divide='ignore', invalid='ignore'):
                 Ex_c = charge['q'] * dx / (r**3)
                 Ey_c = charge['q'] * dy / (r**3)
            
            # Masquer le centre
            Ex_c[r < 0.2] = 0
            Ey_c[r < 0.2] = 0
            
            Ex += Ex_c
            Ey += Ey_c
            
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Streamplot pour les lignes de champ
        # Normaliser pour la couleur
        Emag = np.sqrt(Ex**2 + Ey**2)
        # Log scale pour couleur pour voir les faibles champs
        strm = ax.streamplot(x, y, Ex, Ey, color=np.log(Emag+1), linewidth=1.5, cmap='autumn')
        
        # Dessiner les charges
        for charge in charges:
            c = 'red' if charge['q'] > 0 else 'blue'
            ax.add_patch(plt.Circle((charge['x'], charge['y']), 0.1, color=c))
            sign = '+' if charge['q'] > 0 else '-'
            ax.text(charge['x'], charge['y'], sign, color='white', ha='center', va='center', fontweight='bold')

        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_aspect('equal')
        ax.set_title("Lignes de Champ Électrique")
        st.pyplot(fig)
        plt.close()
