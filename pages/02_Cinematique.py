"""
Cinématique : vitesse et accélération
=====================================

Exploration interactive des concepts de vitesse instantanée et d'accélération.
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

# Configurer la page
st.set_page_config(
    page_title="Cinématique - cours de physique",
    page_icon="📐",
    layout="wide"
)

st.title("📐 Cinématique : vitesse et accélération")
st.markdown("### Comprendre le mouvement à travers les dérivées")

# Introduction
st.markdown("""
---
## 🎯 Ce que tu vas apprendre

Dans cette leçon, tu vas découvrir :
- Comment passer de la vitesse **moyenne** (distance/temps) à la vitesse **instantanée**
- Ce que les dérivées signifient physiquement
- La relation entre position, vitesse et accélération
- Comment visualiser et interpréter les graphiques de mouvement

---
""")

# Section Théorie
with st.expander("📖 Théorie : de la moyenne à l'instantané", expanded=True):
    st.markdown("""
    ### Vitesse Moyenne vs. Vitesse Instantanée
    
    **Tu connais déjà :** Vitesse moyenne = Distance parcourue / Temps écoulé
    
    $$v_{\\text{moyenne}} = \\frac{\\Delta x}{\\Delta t} = \\frac{x_2 - x_1}{t_2 - t_1}$$
    
    **Le Problème :** Cela nous dit la vitesse *globale*, mais pas ce qui se passe à chaque instant !
    
    **La Solution :** Pour trouver la vitesse à un moment *précis*, on rend $\\Delta t$ de plus en plus petit :
    
    $$v(t) = \\lim_{\\Delta t \\to 0} \\frac{\\Delta x}{\\Delta t} = \\frac{dx}{dt}$$
    
    C'est la **dérivée** de la position par rapport au temps ! Elle nous dit à quelle vitesse la position change *maintenant*.
    
    ### Et l'Accélération ?
    
    L'accélération, c'est la vitesse à laquelle la *vitesse* change :
    
    $$a(t) = \\frac{dv}{dt} = \\frac{d^2x}{dt^2}$$
    
    C'est la dérivée de la vitesse (ou la dérivée seconde de la position) !
    
    ### Interprétation Physique
    
    - **Position** $x(t)$ : Où tu es au temps $t$
    - **Vitesse** $v(t) = \\frac{dx}{dt}$ : À quelle vitesse ta position change (rapidité & direction)
    - **Accélération** $a(t) = \\frac{dv}{dt}$ : À quelle vitesse ta vitesse change (accélère/ralentit)
    
    **Idée Clé :** La dérivée est la *pente* de la tangente à la courbe en chaque point !
    """)

# Terminologie vitesse (scalaire) vs vecteur vitesse
with st.expander("🧭 Terminologie : vitesse (scalaire) vs vecteur vitesse", expanded=False):
        st.markdown(r"""
        ### Deux notions différentes
    
        - **Vecteur vitesse** \(\vec v(t) = \dfrac{d\vec x}{dt}\) : grandeur orientée (direction et sens). Elle peut être positive ou négative selon l'axe choisi (ou pointer dans n'importe quelle direction en 2D/3D).
        - **Vitesse (scalaire)** \(v(t) = \lVert \vec v(t) \rVert \ge 0\) : c'est la **rapidité**, toujours positive, sans information de direction.
    
        ### Moyennes sur un intervalle
        - **Vitesse moyenne (scalaire)** sur \([t_1,t_2]\) :
            $$\overline{v}_\text{scalaire} = \frac{1}{\Delta t} \int_{t_1}^{t_2} \lVert \vec v(t) \rVert \, dt \quad \text{avec} \ \Delta t=t_2-t_1$$
        - **Vecteur vitesse moyen** sur \([t_1,t_2]\) :
            $$\overline{\vec v} = \frac{\Delta \vec x}{\Delta t} = \frac{\vec x(t_2)-\vec x(t_1)}{t_2-t_1}$$
    
        ### Circuit fermé : pourquoi différence ?
        - Sur un **circuit fermé** (on revient au point de départ), on a \(\vec x(t_2) = \vec x(t_1)\) donc :
            $$\overline{\vec v} = \frac{\vec x(t_2)-\vec x(t_1)}{\Delta t} = \vec 0$$
        - Pourtant, on a bien **bougé** : la rapidité était positive la plupart du temps, donc :
            $$\overline{v}_\text{scalaire} = \frac{1}{\Delta t} \int_{t_1}^{t_2} \lVert \vec v(t) \rVert dt \, > \, 0$$
    
        > En clair : la **vitesse moyenne (scalaire)** mesure « combien vite on s'est déplacé en moyenne », tandis que le **vecteur vitesse moyen** dépend du **déplacement net**. Si le déplacement net est nul (boucle fermée), le vecteur vitesse moyen est nul, même si la vitesse scalaire moyenne est positive.
    
        ### Exemple simple : mouvement circulaire uniforme
        Pour un rayon \(R\) et une pulsation \(\omega\), on a une rapidité constante \(v=R\,\omega\). Sur une période \(T=\tfrac{2\pi}{\omega}\) :
    
        - $$\overline{v}_\text{scalaire} = \frac{1}{T} \int_0^T v \, dt = v = R\,\omega$$
        - $$\overline{\vec v} = \frac{\vec x(T)-\vec x(0)}{T} = \vec 0$$
    
        Cela illustre parfaitement « vitesse positive » vs « vecteur vitesse moyen nul » sur un tour complet.
        """)

# Visualisation interactive
st.markdown("---")
st.markdown("## 🎮 Exploration interactive")

# Créer des onglets pour différents exemples
tab1, tab2, tab3 = st.tabs(["📍 Position → vitesse", "🚀 Vitesse → accélération", "🎢 Mouvement complet"])

with tab1:
    st.markdown("### Comprendre la vitesse comme dérivée de la position")
    st.markdown("""
    **Objectif :** Voir comment la *pente* de la courbe de position nous donne la vitesse !
    
    - La **courbe bleue** montre la position en fonction du temps
    - La **courbe orange** montre la vitesse (la dérivée)
    - La **ligne verte** est la tangente au temps sélectionné
    - La pente de la ligne tangente = vitesse instantanée
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Choisis un mouvement")
        
        motion_type_1 = st.selectbox(
            "Type de mouvement",
            ["Vitesse Constante", "Accélération Constante", "Mouvement Harmonique", "Polynôme Personnalisé"],
            key="motion_1"
        )
        
        if motion_type_1 == "Vitesse Constante":
            v0 = st.slider("Vitesse (m/s)", -5.0, 5.0, 2.0, 0.1, key="v0_1")
            x0 = st.slider("Position Initiale (m)", -10.0, 10.0, 0.0, 0.5, key="x0_1")
            st.latex(f"x(t) = {x0:.1f} + {v0:.1f}t")
        
        elif motion_type_1 == "Accélération Constante":
            a = st.slider("Accélération (m/s²)", -3.0, 3.0, 1.0, 0.1, key="a_1")
            v0 = st.slider("Vitesse Initiale (m/s)", -5.0, 5.0, 0.0, 0.5, key="v0_2")
            x0 = st.slider("Position Initiale (m)", -10.0, 10.0, 0.0, 0.5, key="x0_2")
            st.latex(f"x(t) = {x0:.1f} + {v0:.1f}t + \\frac{{{a:.1f}}}{{2}}t^2")
        
        elif motion_type_1 == "Mouvement Harmonique":
            A = st.slider("Amplitude (m)", 0.5, 5.0, 3.0, 0.5, key="A_1")
            omega = st.slider("Fréquence Angulaire (rad/s)", 0.5, 3.0, 1.0, 0.1, key="omega_1")
            phi = st.slider("Phase (rad)", 0.0, 2*np.pi, 0.0, 0.1, key="phi_1")
            st.latex(f"x(t) = {A:.1f}\\cos({omega:.1f}t + {phi:.2f})")
        
        else:  # Polynôme Personnalisé
            a2 = st.slider("Coefficient t²", -1.0, 1.0, 0.2, 0.1, key="a2_1")
            a1 = st.slider("Coefficient t", -3.0, 3.0, 1.0, 0.5, key="a1_1")
            a0 = st.slider("Constante", -10.0, 10.0, 0.0, 1.0, key="a0_1")
            st.latex(f"x(t) = {a0:.1f} + {a1:.1f}t + {a2:.1f}t^2")
        
        st.markdown("---")
        selected_time_1 = st.slider("Sélectionne le temps (s)", 0.0, 10.0, 5.0, 0.1, key="time_1")
    
    with col2:
        # Générer le tableau de temps
        t = np.linspace(0, 10, 1000)
        
        # Calculer la position selon le type de mouvement
        if motion_type_1 == "Vitesse Constante":
            x = x0 + v0 * t
            v = np.ones_like(t) * v0
        elif motion_type_1 == "Accélération Constante":
            x = x0 + v0 * t + 0.5 * a * t**2
            v = v0 + a * t
        elif motion_type_1 == "Mouvement Harmonique":
            x = A * np.cos(omega * t + phi)
            v = -A * omega * np.sin(omega * t + phi)
        else:  # Polynôme Personnalisé
            x = a0 + a1 * t + a2 * t**2
            v = a1 + 2 * a2 * t
        
        # Calculer la position et la vitesse au temps sélectionné
        idx = np.argmin(np.abs(t - selected_time_1))
        x_at_t = x[idx]
        v_at_t = v[idx]
        
        # Créer une figure avec deux sous-graphiques
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
        
        # Tracer la position
        ax1.plot(t, x, 'b-', linewidth=2, label='Position x(t)')
        ax1.plot(selected_time_1, x_at_t, 'ro', markersize=10, label=f'À t={selected_time_1:.1f}s')
        
        # Tracer la ligne tangente
        dt = 1.0  # Longueur de la ligne tangente
        tangent_t = np.array([selected_time_1 - dt, selected_time_1 + dt])
        tangent_x = x_at_t + v_at_t * (tangent_t - selected_time_1)
        ax1.plot(tangent_t, tangent_x, 'g--', linewidth=2, label=f'Tangente (pente = {v_at_t:.2f} m/s)')
        
        ax1.set_ylabel('Position (m)', fontsize=12, fontweight='bold')
        ax1.legend(loc='best', fontsize=10)
        ax1.grid(True, alpha=0.3)
        ax1.set_title('Position en fonction du temps', fontsize=14, fontweight='bold')
        
        # Tracer la vitesse
        ax2.plot(t, v, 'orange', linewidth=2, label='Vitesse v(t) = dx/dt')
        ax2.plot(selected_time_1, v_at_t, 'ro', markersize=10, label=f'À t={selected_time_1:.1f}s: v={v_at_t:.2f} m/s')
        ax2.axhline(0, color='k', linestyle='-', linewidth=0.5)
        ax2.set_xlabel('Temps (s)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Vitesse (m/s)', fontsize=12, fontweight='bold')
        ax2.legend(loc='best', fontsize=10)
        ax2.grid(True, alpha=0.3)
        ax2.set_title('Vitesse en fonction du temps (dérivée de la position)', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        
        # Afficher les valeurs numériques
        st.markdown(f"""
        **Au temps t = {selected_time_1:.2f} s :**
        - Position : **x = {x_at_t:.2f} m**
        - Vitesse : **v = {v_at_t:.2f} m/s** (pente de la courbe de position)
        
        💡 **Remarque :** La vitesse à chaque instant égale la pente de la courbe de position à cet instant !
        """)

with tab2:
    st.markdown("### Comprendre l'accélération comme dérivée de la vitesse")
    st.markdown("""
    **Objectif :** Voir comment la *pente* de la courbe de vitesse nous donne l'accélération !
    
    - La **courbe orange** montre la vitesse en fonction du temps
    - La **courbe rouge** montre l'accélération (la dérivée de la vitesse)
    - La **ligne verte** est la tangente à la courbe de vitesse
    - La pente de la ligne tangente = accélération instantanée
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Choisis un mouvement")
        
        motion_type_2 = st.selectbox(
            "Type de mouvement",
            ["Accélération Constante", "Accélération Variable", "Mouvement Harmonique"],
            key="motion_2"
        )
        
        if motion_type_2 == "Accélération Constante":
            a_const = st.slider("Accélération (m/s²)", -5.0, 5.0, 2.0, 0.1, key="a_const")
            v0_const = st.slider("Vitesse Initiale (m/s)", -5.0, 5.0, 0.0, 0.5, key="v0_const")
            st.latex(f"v(t) = {v0_const:.1f} + {a_const:.1f}t")
            st.latex(f"a(t) = {a_const:.1f}")
        
        elif motion_type_2 == "Accélération Variable":
            alpha = st.slider("Taux de Variation (m/s³)", -0.5, 0.5, 0.2, 0.05, key="alpha")
            a0 = st.slider("Accélération Initiale (m/s²)", -3.0, 3.0, 0.0, 0.5, key="a0_var")
            v0_var = st.slider("Vitesse Initiale (m/s)", -5.0, 5.0, 0.0, 0.5, key="v0_var")
            st.latex(f"a(t) = {a0:.1f} + {alpha:.2f}t")
            st.latex(f"v(t) = {v0_var:.1f} + {a0:.1f}t + \\frac{{{alpha:.2f}}}{{2}}t^2")
        
        else:  # Mouvement Harmonique
            A_harm = st.slider("Amplitude (m/s)", 1.0, 5.0, 3.0, 0.5, key="A_harm")
            omega_harm = st.slider("Fréquence Angulaire (rad/s)", 0.5, 3.0, 1.0, 0.1, key="omega_harm")
            st.latex(f"v(t) = {A_harm:.1f}\\sin({omega_harm:.1f}t)")
            st.latex(f"a(t) = {A_harm:.1f} \\cdot {omega_harm:.1f}\\cos({omega_harm:.1f}t)")
        st.markdown("---")
        selected_time_2 = st.slider("Sélectionne le temps (s)", 0.0, 10.0, 5.0, 0.1, key="time_2")
    
    with col2:
        # Générer le tableau de temps
        t = np.linspace(0, 10, 1000)
        
        # Calculer la vitesse et l'accélération selon le type de mouvement
        if motion_type_2 == "Accélération Constante":
            v = v0_const + a_const * t
            a = np.ones_like(t) * a_const
        elif motion_type_2 == "Accélération Variable":
            a = a0 + alpha * t
            v = v0_var + a0 * t + 0.5 * alpha * t**2
        else:  # Mouvement Harmonique
            v = A_harm * np.sin(omega_harm * t)
            a = A_harm * omega_harm * np.cos(omega_harm * t)
        
        # Calculer les valeurs au temps sélectionné
        idx = np.argmin(np.abs(t - selected_time_2))
        v_at_t = v[idx]
        a_at_t = a[idx]
        
        # Créer une figure avec deux sous-graphiques
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
        
        # Tracer la vitesse
        ax1.plot(t, v, 'orange', linewidth=2, label='Vitesse v(t)')
        ax1.plot(selected_time_2, v_at_t, 'ro', markersize=10, label=f'À t={selected_time_2:.1f}s')
        
        # Tracer la ligne tangente
        dt = 1.0
        tangent_t = np.array([selected_time_2 - dt, selected_time_2 + dt])
        tangent_v = v_at_t + a_at_t * (tangent_t - selected_time_2)
        ax1.plot(tangent_t, tangent_v, 'g--', linewidth=2, label=f'Tangente (pente = {a_at_t:.2f} m/s²)')
        
        ax1.axhline(0, color='k', linestyle='-', linewidth=0.5)
        ax1.set_ylabel('Vitesse (m/s)', fontsize=12, fontweight='bold')
        ax1.legend(loc='best', fontsize=10)
        ax1.grid(True, alpha=0.3)
        ax1.set_title('Vitesse en fonction du temps', fontsize=14, fontweight='bold')
        
        # Tracer l'accélération
        ax2.plot(t, a, 'red', linewidth=2, label='Accélération a(t) = dv/dt')
        ax2.plot(selected_time_2, a_at_t, 'ro', markersize=10, label=f'À t={selected_time_2:.1f}s: a={a_at_t:.2f} m/s²')
        ax2.axhline(0, color='k', linestyle='-', linewidth=0.5)
        ax2.set_xlabel('Temps (s)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Accélération (m/s²)', fontsize=12, fontweight='bold')
        ax2.legend(loc='best', fontsize=10)
        ax2.grid(True, alpha=0.3)
        ax2.set_title('Accélération en fonction du temps (dérivée de la vitesse)', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        
        # Afficher les valeurs numériques et l'interprétation
        st.markdown(f"""
        **Au temps t = {selected_time_2:.2f} s :**
        - Vitesse : **v = {v_at_t:.2f} m/s**
        - Accélération : **a = {a_at_t:.2f} m/s²** (pente de la courbe de vitesse)
        
        **Interprétation Physique :**
        """)
        
        if a_at_t > 0.1:
            st.success(f"✅ **Accélère !** La vitesse augmente à {a_at_t:.2f} m/s²")
        elif a_at_t < -0.1:
            st.warning(f"⚠️ **Ralentit !** La vitesse diminue à {abs(a_at_t):.2f} m/s²")
        else:
            st.info("🔄 **Vitesse constante** (approximativement). L'accélération est proche de zéro.")

with tab3:
    st.markdown("### Le tableau complet : position, vitesse et accélération")
    st.markdown("""
    **Objectif :** Voir comment position, vitesse et accélération sont toutes reliées !
    
    - **Bleu :** Position x(t)
    - **Orange :** Vitesse v(t) = dx/dt (1ère dérivée)
    - **Rouge :** Accélération a(t) = dv/dt = d²x/dt² (2ème dérivée)
    
    Regarde comment elles sont connectées quand tu changes les paramètres !
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Conçois ton mouvement")
        
        motion_type_3 = st.selectbox(
            "Type de Mouvement",
            ["Mouvement de Projectile", "Oscillateur Harmonique", "Mouvement Amorti", "Personnalisé"],
            key="motion_3"
        )
        
        if motion_type_3 == "Mouvement de Projectile":
            st.markdown("*Lancer une balle vers le haut avec la gravité*")
            v0_proj = st.slider("Vitesse Initiale (m/s)", 0.0, 20.0, 10.0, 0.5, key="v0_proj")
            h0 = st.slider("Hauteur Initiale (m)", 0.0, 10.0, 0.0, 0.5, key="h0")
            g = 9.81
            st.latex(f"x(t) = {h0:.1f} + {v0_proj:.1f}t - \\frac{{9.81}}{{2}}t^2")
            st.latex(f"v(t) = {v0_proj:.1f} - 9.81t")
            st.latex(f"a(t) = -9.81 \\text{{ m/s}}^2")
        
        elif motion_type_3 == "Oscillateur Harmonique":
            st.markdown("*Comme une masse sur un ressort*")
            A_osc = st.slider("Amplitude (m)", 0.5, 5.0, 2.0, 0.5, key="A_osc")
            omega_osc = st.slider("Fréquence Angulaire (rad/s)", 0.5, 3.0, 1.5, 0.1, key="omega_osc")
            phi_osc = st.slider("Phase (rad)", 0.0, 2*np.pi, 0.0, 0.1, key="phi_osc")
            st.latex(f"x(t) = {A_osc:.1f}\\cos({omega_osc:.1f}t + {phi_osc:.2f})")
        
        elif motion_type_3 == "Mouvement Amorti":
            st.markdown("*Mouvement avec friction*")
            A_damp = st.slider("Amplitude Initiale (m)", 1.0, 5.0, 3.0, 0.5, key="A_damp")
            omega_damp = st.slider("Fréq. d'Oscillation (rad/s)", 0.5, 3.0, 2.0, 0.1, key="omega_damp")
            gamma = st.slider("Coefficient d'Amortissement", 0.0, 1.0, 0.2, 0.05, key="gamma")
            st.latex(f"x(t) = {A_damp:.1f}e^{{-{gamma:.2f}t}}\\cos({omega_damp:.1f}t)")
        
        else:  # Personnalisé
            st.markdown("*Crée le tien !*")
            a3 = st.slider("Coefficient t³", -0.1, 0.1, 0.02, 0.01, key="a3")
            a2_cust = st.slider("Coefficient t²", -1.0, 1.0, 0.3, 0.1, key="a2_cust")
            a1_cust = st.slider("Coefficient t", -3.0, 3.0, 1.0, 0.5, key="a1_cust")
            a0_cust = st.slider("Constante", -5.0, 5.0, 0.0, 0.5, key="a0_cust")
            st.latex(f"x(t) = {a0_cust:.1f} + {a1_cust:.1f}t + {a2_cust:.1f}t^2 + {a3:.2f}t^3")
        
        st.markdown("---")
        show_animation = st.checkbox("Afficher l'Objet en Mouvement", value=True, key="show_anim")
    
    with col2:
        # Générer le tableau de temps
        t = np.linspace(0, 10, 1000)
        
        # Calculer x, v, a selon le type de mouvement
        if motion_type_3 == "Mouvement de Projectile":
            x = h0 + v0_proj * t - 0.5 * g * t**2
            v = v0_proj - g * t
            a = np.ones_like(t) * (-g)
            # S'arrêter quand on touche le sol
            if np.any(x < 0):
                idx_ground = np.where(x < 0)[0][0]
                x[idx_ground:] = 0
                v[idx_ground:] = 0
                a[idx_ground:] = 0
        
        elif motion_type_3 == "Oscillateur Harmonique":
            x = A_osc * np.cos(omega_osc * t + phi_osc)
            v = -A_osc * omega_osc * np.sin(omega_osc * t + phi_osc)
            a = -A_osc * omega_osc**2 * np.cos(omega_osc * t + phi_osc)
        
        elif motion_type_3 == "Mouvement Amorti":
            x = A_damp * np.exp(-gamma * t) * np.cos(omega_damp * t)
            v = A_damp * np.exp(-gamma * t) * (-gamma * np.cos(omega_damp * t) - omega_damp * np.sin(omega_damp * t))
            a_term1 = gamma**2 * np.cos(omega_damp * t)
            a_term2 = 2 * gamma * omega_damp * np.sin(omega_damp * t)
            a_term3 = -omega_damp**2 * np.cos(omega_damp * t)
            a = A_damp * np.exp(-gamma * t) * (a_term1 + a_term2 + a_term3)
        
        else:  # Personnalisé
            x = a0_cust + a1_cust * t + a2_cust * t**2 + a3 * t**3
            v = a1_cust + 2 * a2_cust * t + 3 * a3 * t**2
            a = 2 * a2_cust + 6 * a3 * t
        
        # Créer une figure avec trois sous-graphiques
        fig = plt.figure(figsize=(12, 10))
        
        if show_animation:
            # Créer 4 sous-graphiques : animation + 3 graphiques
            gs = fig.add_gridspec(4, 1, height_ratios=[1, 1, 1, 1])
            ax_anim = fig.add_subplot(gs[0])
            ax1 = fig.add_subplot(gs[1])
            ax2 = fig.add_subplot(gs[2])
            ax3 = fig.add_subplot(gs[3])
            
            # Sous-graphique d'animation
            current_t = 5.0  # Milieu de la plage de temps
            idx_current = np.argmin(np.abs(t - current_t))
            x_current = x[idx_current]
            v_current = v[idx_current]
            a_current = a[idx_current]
            
            # Dessiner l'objet
            ax_anim.plot([0, 10], [0, 0], 'k-', linewidth=1)  # Ligne du sol
            ax_anim.plot(current_t, x_current, 'bo', markersize=20, label='Objet')
            
            # Dessiner le vecteur vitesse
            if abs(v_current) > 0.1:
                arrow_scale = 0.3
                ax_anim.arrow(current_t, x_current, arrow_scale * v_current/abs(v_current), 0,
                            head_width=0.3, head_length=0.2, fc='orange', ec='orange', linewidth=2,
                            label=f'v={v_current:.1f} m/s')
            
            # Dessiner le vecteur accélération
            if abs(a_current) > 0.1:
                arrow_scale = 0.2
                ax_anim.arrow(current_t, x_current, 0, arrow_scale * a_current/abs(a_current),
                            head_width=0.2, head_length=0.2, fc='red', ec='red', linewidth=2,
                            label=f'a={a_current:.1f} m/s²')
            
            ax_anim.set_xlim(-0.5, 10.5)
            ax_anim.set_ylim(min(x)-2, max(x)+2)
            ax_anim.set_ylabel('Position (m)', fontsize=10)
            ax_anim.set_title(f"Mouvement de l'objet à t={current_t:.1f}s", fontsize=12, fontweight='bold')
            ax_anim.legend(loc='upper right', fontsize=8)
            ax_anim.grid(True, alpha=0.3)
            ax_anim.set_xticks([])
            
        else:
            gs = fig.add_gridspec(3, 1)
            ax1 = fig.add_subplot(gs[0])
            ax2 = fig.add_subplot(gs[1])
            ax3 = fig.add_subplot(gs[2])
        
        # Tracer la position
        ax1.plot(t, x, 'b-', linewidth=2, label='Position x(t)')
        ax1.axhline(0, color='k', linestyle='-', linewidth=0.5)
        ax1.set_ylabel('Position (m)', fontsize=11, fontweight='bold')
        ax1.legend(loc='best', fontsize=9)
        ax1.grid(True, alpha=0.3)
        ax1.set_title('Position', fontsize=12, fontweight='bold')
        
        # Tracer la vitesse
        ax2.plot(t, v, 'orange', linewidth=2, label='Vitesse v(t) = dx/dt')
        ax2.axhline(0, color='k', linestyle='-', linewidth=0.5)
        ax2.set_ylabel('Vitesse (m/s)', fontsize=11, fontweight='bold')
        ax2.legend(loc='best', fontsize=9)
        ax2.grid(True, alpha=0.3)
        ax2.set_title('Vitesse (1ère dérivée)', fontsize=12, fontweight='bold')
        
        # Tracer l'accélération
        ax3.plot(t, a, 'red', linewidth=2, label='Accélération a(t) = dv/dt = d²x/dt²')
        ax3.axhline(0, color='k', linestyle='-', linewidth=0.5)
        ax3.set_xlabel('Temps (s)', fontsize=11, fontweight='bold')
        ax3.set_ylabel('Accélération (m/s²)', fontsize=11, fontweight='bold')
        ax3.legend(loc='best', fontsize=9)
        ax3.grid(True, alpha=0.3)
        ax3.set_title('Accélération (2ème dérivée)', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

# Résumé et points clés
st.markdown("---")
st.markdown("## 🎓 Points clés à retenir")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 📍 Position
    
    - Où tu es
    - Fonction du temps : x(t)
    - Mesurée en mètres
    """)

with col2:
    st.markdown("""
    ### 🏃 Vitesse
    
    - À quelle vitesse la position change
    - Première dérivée : v = dx/dt
    - Pente de la courbe de position
    - Mesurée en m/s
    """)

with col3:
    st.markdown("""
    ### 🚀 Accélération
    
    - À quelle vitesse la vitesse change
    - Première dérivée de la vitesse
    - Deuxième dérivée de la position
    - a = dv/dt = d²x/dt²
    - Mesurée en m/s²
    """)

st.markdown("---")
st.markdown("""
## 💡 Conseils de pratique

1. **Regarde les pentes :** La dérivée est toujours la pente de la ligne tangente !
2. **Connecte les graphiques :** Observe comment les pics de vitesse se produisent où la position a la pente la plus forte
3. **Intuition physique :** 
   - Vitesse positive → avance
   - Vitesse négative → recule
   - Accélération positive → accélère (si v > 0) ou ralentit moins (si v < 0)
   - Accélération négative → ralentit (si v > 0) ou accélère vers l'arrière (si v < 0)
4. **Les passages par zéro comptent :**
   - Quand vitesse = 0, l'objet s'arrête momentanément (change de direction)
   - Quand accélération = 0, la vitesse est constante

---

**Prête pour plus ?** Essaie de créer tes propres scénarios de mouvement et de prédire à quoi ressembleront les graphiques !
""")