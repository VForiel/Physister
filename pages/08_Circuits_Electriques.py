"""
Circuits Électriques
====================

Loi d'Ohm, Kirchhoff et circuits RC.
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(
    page_title="Circuits - cours de physique",
    page_icon="🔋",
    layout="wide"
)

st.title("🔋 Circuits Électriques")
st.warning("🚧 Cette page est en cours de construction. Le contenu peut être incomplet ou sujet à changements.")
st.markdown("### Courant, Tension et Résistance")

# Introduction Théorique
with st.expander("📖 Théorie : Les bases de l'électricité", expanded=True):
    st.markdown(r"""
    ### 1. Loi d'Ohm
    Pour une résistance linéaire : $ U = R \cdot I $
    
    ### 2. Lois de Kirchhoff
    *   **Loi des Nœuds** : La somme des courants qui entrent = la somme des courants qui sortent ($\sum I_{in} = \sum I_{out}$).
    *   **Loi des Mailles** : La somme algébrique des tensions le long d'une maille fermée est nulle ($\sum U = 0$).
    
    ### 3. Circuit RC (Résistance-Condensateur)
    Un condensateur stocke de l'énergie sous forme électrique ($E = \frac{1}{2} C U^2$).
    Lors de la charge à travers une résistance $R$, la tension évolue exponentiellement :
    
    $$ V_C(t) = E (1 - e^{-t/\tau}) $$
    
    avec $\tau = R \cdot C$ la **constante de temps**. À $t = \tau$, le condensateur est chargé à 63%.
    """)

st.markdown("---")
st.markdown("## 🎮 Exploration interactive")

tab1, tab2 = st.tabs(["🔌 Résistances (Série/Parallèle)", "⏱️ Circuit RC (Transitoire)"])

# --- TAB 1: Resistances ---
with tab1:
    st.markdown("### Association de Résistances")
    
    col_res1, col_res2 = st.columns([1, 1])
    
    with col_res1:
        st.subheader("Paramètres")
        r1 = st.slider("Résistance R1 (Ω)", 1.0, 1000.0, 100.0, 10.0)
        r2 = st.slider("Résistance R2 (Ω)", 1.0, 1000.0, 220.0, 10.0)
        v_source = st.slider("Tension Source U (V)", 1.0, 24.0, 12.0, 1.0)
        
        # Calcul Série
        r_eq_serie = r1 + r2
        i_serie = v_source / r_eq_serie
        
        # Calcul Parallèle
        r_eq_para = (r1 * r2) / (r1 + r2)
        i_para = v_source / r_eq_para
        i1_para = v_source / r1
        i2_para = v_source / r2
        
    with col_res2:
        st.subheader("Résultats")
        
        st.markdown("**Circuit SÉRIE**")
        st.latex(f"R_{{eq}} = R_1 + R_2 = {r_eq_serie:.1f} \\Omega")
        st.latex(f"I = U / R_{{eq}} = {i_serie*1000:.1f} \\text{{ mA}}")
        
        st.markdown("---")
        st.markdown("**Circuit PARALLÈLE**")
        st.latex(f"R_{{eq}} = \\frac{{R_1 R_2}}{{R_1 + R_2}} = {r_eq_para:.1f} \\Omega")
        st.latex(f"I_{{tot}} = {i_para*1000:.1f} \\text{{ mA}}")
        st.caption(f"(I1 = {i1_para*1000:.1f} mA, I2 = {i2_para*1000:.1f} mA)")

# --- TAB 2: RC Circuit ---
with tab2:
    st.markdown("### Charge et Décharge d'un Condensateur")
    st.markdown("Voyons comment la tension monte progressivement.")
    
    col_rc1, col_rc2 = st.columns([1, 2])
    
    with col_rc1:
        R_ohm = st.slider("Résistance R (kΩ)", 1.0, 100.0, 10.0, 1.0) * 1000
        C_muF = st.slider("Capacité C (µF)", 1.0, 1000.0, 100.0, 10.0)
        E_volt = st.slider("Tension Générateur E (V)", 1.0, 24.0, 5.0, 1.0)
        
        tau = R_ohm * (C_muF * 1e-6)
        st.metric("Constante de temps τ", f"{tau:.3f} s")
        
        st.info("Le condensateur atteint 99% de la charge après 5τ.")
    
    with col_rc2:
        # Simulation
        t_max = 5 * tau
        t = np.linspace(0, t_max, 200)
        
        # Charge
        v_c = E_volt * (1 - np.exp(-t / tau))
        
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(t, v_c, 'b-', linewidth=2, label=r'$V_C(t)$')
        ax.axhline(E_volt, color='r', linestyle='--', label='E (Max)')
        
        # Point à tau
        idx_tau = np.argmin(np.abs(t - tau))
        v_tau = v_c[idx_tau]
        ax.plot(tau, v_tau, 'go', markersize=8)
        ax.axvline(tau, color='g', linestyle=':', label=r'$\tau = RC$ (63%)')
        ax.text(tau, v_tau + E_volt*0.05, f"{v_tau:.2f} V", color='g', fontweight='bold')
        
        ax.set_xlabel("Temps (s)")
        ax.set_ylabel("Tension (V)")
        ax.set_title("Charge du Condensateur")
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        st.pyplot(fig)
        plt.close()
