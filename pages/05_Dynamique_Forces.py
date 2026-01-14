"""
Dynamique : Forces et Mouvement
===============================

Exploration interactive des forces, des lois de Newton et de la dynamique.
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(
    page_title="Dynamique - cours de physique",
    page_icon="🍎",
    layout="wide"
)

st.title("🍎 Dynamique : Forces et Lois de Newton")
st.warning("🚧 Cette page est en cours de construction. Le contenu peut être incomplet ou sujet à changements.")
st.markdown("### Comprendre pourquoi les choses bougent")

# Introduction Théorique
with st.expander("📖 Théorie : Les causes du mouvement", expanded=True):
    st.markdown(r"""
    ### 1. Deuxième Loi de Newton
    La relation fondamentale de la dynamique relie la force à l'accélération :
    
    $$ \sum \vec{F} = m \vec{a} $$
    
    Si la somme des forces est nulle, l'objet garde sa vitesse constante (ou reste immobile).
    
    ### 2. Forces Usuelles
    *   **Poids** : attraction terrestre, $\vec{P} = m\vec{g}$ (vers le bas).
    *   **Réaction Normale** : force de contact perpendiculaire à la surface, $\vec{N}$.
    *   **Frottement** : force parallèle à la surface qui s'oppose au mouvement (ou à sa tendance).
        *   *Statique* ($v=0$) : $f_s \le \mu_s N$.
        *   *Cinétique* ($v \neq 0$) : $f_k = \mu_k N$.
    *   **Rappel Elastique (Ressort)** : $\vec{F} = -k \Delta x \vec{u}$ (Loi de Hooke).
    *   **Trainée (Fluide)** : Résistance de l'air, souvent modèle quadratique $F_{drag} = \frac{1}{2} \rho S C_x v^2$ ou simplifié $F = -K v^2$.
    """)

st.markdown("---")
st.markdown("## 🎮 Exploration interactive")

tab1, tab2, tab3 = st.tabs(["⛰️ Plan Incliné (Frottements)", "🌀 Ressort (Hooke)", "🪂 Chute avec Trainée"])

# --- TAB 1: Plan Incliné ---
with tab1:
    st.markdown("### Bloc sur un Plan Incliné avec Frottements")
    st.markdown("""
    Un bloc est posé sur une pente. Va-t-il glisser ?
    *   **Forces en jeu** : Poids, Normale, Frottement.
    *   **Condition de glissement** : La composante du poids le long de la pente doit dépasser le frottement statique maximal.
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        angle_deg = st.slider("Angle de la pente (°)", 0.0, 90.0, 30.0, 1.0)
        mass = st.slider("Masse (kg)", 0.1, 10.0, 1.0, 0.1)
        mu_s = st.slider("Coeff. Frottement Statique (μs)", 0.0, 1.0, 0.5, 0.05)
        mu_k = st.slider("Coeff. Frottement Cinétique (μk)", 0.0, 1.0, 0.3, 0.05)
        
        g = 9.81
        angle_rad = np.radians(angle_deg)
        
        # Calcul des forces
        # Poids
        P = mass * g
        Px = P * np.sin(angle_rad) # Pousse vers le bas de la pente
        Py = P * np.cos(angle_rad) # Presse contre la pente
        
        # Normale (compense Py si pas d'autre force verticale relative au plan)
        N = Py
        
        # Frottement Max Statique
        f_s_max = mu_s * N
        
        st.markdown("---")
        st.markdown("**Bilan des Forces :**")
        st.latex(f"P_x = {Px:.2f} \\text{{ N}}")
        st.latex(f"f_{{s,max}} = {f_s_max:.2f} \\text{{ N}}")
        
        # État du mouvement
        is_sliding = Px > f_s_max
        if is_sliding:
            f_fric = mu_k * N
            net_force = Px - f_fric
            acc = net_force / mass
            st.error(f"🚀 **GLISSEMENT !** Accélération = {acc:.2f} m/s²")
        else:
            f_fric = Px # Frottement statique égal à la force motrice pour équilibre
            acc = 0.0
            st.success("🛑 **IMMOBILE** (Frottement suffisant)")

    with col2:
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Dessin du plan
        x_slope = np.linspace(0, 10, 100)
        y_slope = np.tan(angle_rad) * x_slope
        
        # Rotation pour affichage "à plat" ou garder repère labo ?
        # Gardons repère labo simple : Plan comme une ligne.
        # Bloc au milieu environ
        L = 5.0 # Position sur x
        H = L * np.tan(angle_rad)
        
        # Plan
        ax.plot([0, 10], [0, 10 * np.tan(angle_rad)], 'k-', linewidth=2)
        ax.fill_between([0, 10], [0, 0], [0, 10 * np.tan(angle_rad)], color='lightgray', alpha=0.5)
        
        # Bloc (carré simple centré en L, H, tourné)
        # Mais pour simplifier la visualisation des vecteurs, on dessine souvent le bloc "droit" mais les axes tournés ?
        # Non, restons géométriques.
        
        # Centre de masse du bloc
        # On le décale un peu "au dessus" de la pente (normale)
        offset = 0.5 
        cx = L - offset * np.sin(angle_rad)
        cy = H + offset * np.cos(angle_rad)
        
        # Vecteurs (Partent du centre de masse)
        scale = 0.5 # Echelle graphique pour les flèches
        
        # Poids (Toujours vertical bas)
        ax.arrow(cx, cy, 0, -P*scale, head_width=0.2, head_length=0.3, fc='blue', ec='blue', label='Poids')
        
        # Normale (Perpendiculaire pente)
        nx = -np.sin(angle_rad)
        ny = np.cos(angle_rad)
        ax.arrow(cx, cy, N*nx*scale, N*ny*scale, head_width=0.2, head_length=0.3, fc='green', ec='green', label='Normale')
        
        # Frottement (Parallèle pente, vers le haut)
        fx = -np.cos(angle_rad)
        fy = -np.sin(angle_rad)
        ax.arrow(cx - 0.2*nx, cy - 0.2*ny, f_fric*fx*scale, f_fric*fy*scale, head_width=0.2, head_length=0.3, fc='red', ec='red', label='Frottement')
        # Décalage léger du point d'application du frottement (au contact) pour lisibilité
        
        ax.set_aspect('equal')
        ax.set_xlim(-1, 11)
        ax.set_ylim(-1, 11)
        ax.legend()
        ax.set_title("Diagramme des Forces")
        st.pyplot(fig)
        plt.close()

# --- TAB 2: Ressort ---
with tab2:
    st.markdown("### Oscillateur Harmonique (Masse-Ressort)")
    col_spring1, col_spring2 = st.columns([1, 2])
    
    with col_spring1:
        k_spring = st.slider("Raideur k (N/m)", 1.0, 50.0, 10.0, 1.0)
        m_spring = st.slider("Masse m (kg)", 0.1, 5.0, 1.0, 0.1)
        amp_spring = st.slider("Amplitude Initiale (m)", 0.1, 2.0, 1.0, 0.1)
        
        omega_0 = np.sqrt(k_spring / m_spring)
        T_0 = 2 * np.pi / omega_0
        
        st.latex(f"\\omega_0 = \\sqrt{{k/m}} = {omega_0:.2f} \\text{{ rad/s}}")
        st.latex(f"T = {T_0:.2f} \\text{{ s}}")
        
    with col_spring2:
        t_spring = np.linspace(0, 3*T_0, 300)
        # x(t) = A cos(omega t)
        x_spring = amp_spring * np.cos(omega_0 * t_spring)
        # F(t) = -k x(t)
        F_spring = -k_spring * x_spring
        
        fig, (ax_x, ax_f) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
        ax_x.plot(t_spring, x_spring, 'b-', label='Position x(t)')
        ax_x.set_ylabel("Position (m)")
        ax_x.grid(True, alpha=0.3)
        ax_x.legend()
        
        ax_f.plot(t_spring, F_spring, 'r-', label='Force Rappel F(t)')
        ax_f.set_ylabel("Force (N)")
        ax_f.set_xlabel("Temps (s)")
        ax_f.grid(True, alpha=0.3)
        ax_f.legend()
        
        st.pyplot(fig)
        plt.close()

# --- TAB 3: Trainée ---
with tab3:
    st.markdown("### Chute Libre avec Frottement de l'Air (Trainée)")
    st.markdown("On compare la chute libre classique (vide) avec la chute réelle.")
    
    col_drag1, col_drag2 = st.columns([1, 2])
    
    with col_drag1:
        h_drop = st.slider("Hauteur de chute (m)", 10.0, 200.0, 50.0, 10.0)
        m_obj = st.slider("Masse Objet (kg)", 0.01, 10.0, 1.0, 0.01) # Petit objet léger sensible au vent
        coeff_K = st.slider("Coeff Trainée K (kg/m)", 0.0, 1.0, 0.1, 0.01)
        st.caption("Modèle : $F_{drag} = -K v^2$")
        
        # Calcul Vitesse Limite
        if coeff_K > 0:
            v_lim = np.sqrt(m_obj * 9.81 / coeff_K)
            st.latex(f"v_{{lim}} = \\sqrt{{mg/K}} = {v_lim:.2f} \\text{{ m/s}}")
        else:
            st.markdown("Pas de frottement -> Vitesse infinie ? (Non, chute libre)")
    
    with col_drag2:
        # Simulation Numérique (Euler ou analytique si possible)
        # Analytique v(t) = v_lim * tanh(g*t/v_lim) pour v0=0
        
        t_max = np.sqrt(2*h_drop/9.81) * 3 # Un peu plus que le temps de chute libre
        if coeff_K > 0 and v_lim < 1000: # Si trainée significative, chute plus longue
             t_max *= 1.5
             
        t_drag = np.linspace(0, t_max, 200)
        
        # Chute Libre (Vacuum)
        v_vac = 9.81 * t_drag
        z_vac = h_drop - 0.5 * 9.81 * t_drag**2
        z_vac = np.maximum(z_vac, 0) # Sol
        
        # Avec Drag
        if coeff_K > 0:
            # v(t) = v_lim * tanh(g*t/v_lim)
            v_real = v_lim * np.tanh(9.81 * t_drag / v_lim)
            # z(t) = h - (v_lim^2 / g) * ln(cosh(g*t/v_lim))
            z_real = h_drop - (v_lim**2 / 9.81) * np.log(np.cosh(9.81 * t_drag / v_lim))
            z_real = np.maximum(z_real, 0)
        else:
            v_real = v_vac
            z_real = z_vac
            
        fig, (ax_z, ax_v) = plt.subplots(2, 1, figsize=(8, 8), sharex=True)
        
        ax_z.plot(t_drag, z_vac, 'b--', alpha=0.5, label='Vide (Sans frottement)')
        ax_z.plot(t_drag, z_real, 'b-', label='Réel (Avec Trainée)')
        ax_z.set_ylabel("Altitude z (m)")
        ax_z.set_ylim(bottom=0)
        ax_z.grid(True)
        ax_z.legend()
        
        ax_v.plot(t_drag, v_vac, 'r--', alpha=0.5, label='Vide (Lineaire)')
        ax_v.plot(t_drag, v_real, 'r-', label='Réel (Sature vers Vlim)')
        if coeff_K > 0:
            ax_v.axhline(v_lim, color='green', linestyle=':', label='Vitesse Limite')
        ax_v.set_ylabel("Vitesse v (m/s)")
        ax_v.set_xlabel("Temps (s)")
        ax_v.grid(True)
        ax_v.legend()
        
        st.pyplot(fig)
        plt.close()
