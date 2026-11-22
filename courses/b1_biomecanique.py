"""LFSM1109 Biomécanique et analyse du système locomoteur."""

import math

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from app import ui
from app.course import Course
from app.quiz import gen_qcm, multi, num, qcm, vf

COURSE = Course(
    code="LFSM1109", title="Biomécanique et analyse du système locomoteur", short="Biomécanique",
    bloc=1, quad=2, credits=5, hours="45 h + 15 h", icon=":material/accessibility_new:",
    intro="La biomécanique, c'est la physique appliquée au corps humain : où est le centre de gravité, "
          "quelle force doit produire un muscle, pourquoi on boite. Le kiné s'en sert tous les jours pour "
          "comprendre une posture, doser un exercice ou analyser la marche.",
    acquis=[
        "Appliquer les concepts de mécanique au corps humain.",
        "Analyser un mouvement en mécanismes articulaires et musculaires.",
        "Utiliser cinématique et cinétique pour mesurer des paramètres du mouvement.",
        "Calculer énergie, travail et puissance musculaire.",
        "Analyser la marche normale et pathologique, et les adaptations après blessure ou entraînement.",
    ],
)

G = 9.81

TERMS = {
    "centre de gravité": ("Centre de gravité", "Point où l'on peut considérer que tout le poids d'un corps est "
                          "appliqué. Chez l'adulte debout, il est un peu en avant de la 2e vertèbre sacrée "
                          "(environ 55 % de la taille).", "Centre de gravité"),
    "polygone de sustentation": ("Polygone de sustentation", "Surface au sol délimitée par les appuis (les "
                                 "pieds, une canne…). Le corps est en équilibre statique tant que la "
                                 "projection de son centre de gravité tombe dedans.", "Polygone de sustentation"),
    "moment de force": ("Moment de force", "Effet de rotation d'une force autour d'un axe : force × bras de "
                        "levier (distance perpendiculaire entre l'axe et la ligne d'action). Unité : N·m.",
                        "Moment d'une force"),
    "bras de levier": ("Bras de levier", "Distance perpendiculaire entre l'axe de rotation et la ligne d'action "
                       "de la force.", "Bras de levier"),
    "moment d'inertie": ("Moment d'inertie", "Résistance d'un corps à la mise en rotation. Dépend de la masse et "
                         "surtout de sa répartition : I = Σ m·r². Unité : kg·m².", "Moment d'inertie"),
    "rayon de giration": ("Rayon de giration", "Distance à l'axe où il faudrait concentrer toute la masse d'un "
                          "segment pour avoir le même moment d'inertie : I = m·k².", "Rayon de giration"),
    "anthropométrie": ("Anthropométrie", "Mesure des dimensions du corps (longueurs, masses, centres de masse "
                       "des segments). Les tables de Dempster ou de Winter donnent ces valeurs en proportion "
                       "de la taille et de la masse.", "Anthropométrie"),
    "force de réaction du sol": ("Force de réaction du sol", "Force exercée par le sol sur le corps (3e loi de "
                                 "Newton), mesurée avec une plateforme de force.", None),
    "cycle de marche": ("Cycle de marche", "Intervalle entre deux contacts successifs du même pied au sol. "
                        "Environ 60 % d'appui et 40 % d'oscillation à vitesse normale.", "Marche (humain)"),
    "trendelenburg": ("Signe de Trendelenburg", "Chute du bassin du côté opposé à la jambe d'appui, signe d'une "
                      "faiblesse du moyen fessier du côté de l'appui.", "Signe de Trendelenburg"),
    "steppage": ("Steppage", "Marche où l'on lève le genou très haut pour ne pas accrocher la pointe du pied, qui "
                 "tombe à cause d'une faiblesse des releveurs (souvent une atteinte du nerf fibulaire commun).",
                 "Steppage"),
    "puissance": ("Puissance", "Travail fourni par unité de temps (W = J/s). Pour une rotation : P = M·ω.",
                  "Puissance (physique)"),
    "statique": ("Statique", "Étude des corps en équilibre : somme des forces nulle et somme des moments nulle.",
                 "Statique"),
}

# --- Tables anthropométriques (Winter, 2009), simplifiées ----------------------
# fraction de la masse totale, position du centre de masse depuis l'extrémité proximale
SEGMENTS = {
    "tête + cou": (0.081, 0.50),
    "tronc": (0.497, 0.50),
    "bras": (0.028, 0.436),
    "avant-bras": (0.016, 0.430),
    "main": (0.006, 0.506),
    "cuisse": (0.100, 0.433),
    "jambe": (0.0465, 0.433),
    "pied": (0.0145, 0.50),
}
# longueurs en fraction de la taille (Drillis et Contini, repris par Winter)
LENGTHS = {"tête + cou": 0.182, "tronc": 0.288, "bras": 0.186, "avant-bras": 0.146, "main": 0.108,
           "cuisse": 0.245, "jambe": 0.246, "pied_h": 0.039, "pied_l": 0.152}


def _unit(deg):
    r = math.radians(deg)
    return np.array([math.sin(r), math.cos(r)])


def body_points(taille, dorsi, genou, tronc, epaule, coude):
    """Points d'un bonhomme 2D vu de profil (x vers l'avant), pieds à plat."""
    L = {k: v * taille for k, v in LENGTHS.items()}
    cheville = np.array([0.0, L["pied_h"]])
    a_jambe = dorsi  # angle de la jambe par rapport à la verticale (vers l'avant)
    gen = cheville + L["jambe"] * _unit(a_jambe)
    a_cuisse = a_jambe - genou
    hanche = gen + L["cuisse"] * _unit(a_cuisse)
    epa = hanche + L["tronc"] * _unit(tronc)
    tete_haut = epa + L["tête + cou"] * _unit(tronc)
    # bras : angle depuis la verticale descendante, vers l'avant
    psi = epaule - tronc
    d_bras = np.array([math.sin(math.radians(psi)), -math.cos(math.radians(psi))])
    cou = epa + L["bras"] * d_bras
    psi_f = psi + coude
    d_ab = np.array([math.sin(math.radians(psi_f)), -math.cos(math.radians(psi_f))])
    poi = cou + L["avant-bras"] * d_ab
    main = poi + L["main"] * d_ab
    talon = np.array([-0.25 * L["pied_l"], 0.0])
    orteil = np.array([0.75 * L["pied_l"], 0.0])
    return dict(cheville=cheville, genou=gen, hanche=hanche, epaule=epa, tete=tete_haut, coude=cou,
                poignet=poi, main=main, talon=talon, orteil=orteil)


def body_com(p, charge=0.0, masse=60.0):
    def mid(a, b, f):
        return a + f * (b - a)

    parts = [
        (SEGMENTS["pied"][0] * 2, mid(p["talon"], p["orteil"], 0.5) + np.array([0, 0.02])),
        (SEGMENTS["jambe"][0] * 2, mid(p["genou"], p["cheville"], SEGMENTS["jambe"][1])),
        (SEGMENTS["cuisse"][0] * 2, mid(p["hanche"], p["genou"], SEGMENTS["cuisse"][1])),
        (SEGMENTS["tronc"][0], mid(p["hanche"], p["epaule"], 0.5)),
        (SEGMENTS["tête + cou"][0], mid(p["epaule"], p["tete"], 0.6)),
        (SEGMENTS["bras"][0] * 2, mid(p["epaule"], p["coude"], SEGMENTS["bras"][1])),
        (SEGMENTS["avant-bras"][0] * 2, mid(p["coude"], p["poignet"], SEGMENTS["avant-bras"][1])),
        (SEGMENTS["main"][0] * 2, mid(p["poignet"], p["main"], SEGMENTS["main"][1])),
    ]
    total = sum(m for m, _ in parts) * masse + charge
    com = sum(m * masse * pos for m, pos in parts)
    if charge:
        com = com + charge * p["main"]
    return com / total


# --- Chapitres -----------------------------------------------------------------


def ch_corps():
    ui.md(r"""
En biomécanique, on modélise le corps comme une **chaîne de segments rigides** (pied, jambe, cuisse,
tronc…) reliés par des articulations. Chaque segment a une masse, une longueur et un centre de masse
connus grâce aux tables d'[[anthropométrie]] (Dempster, Winter). On les exprime **en proportion** de la
masse et de la taille de la personne : la cuisse pèse environ 10 % du corps, quelle que soit la personne.

Le [[centre de gravité]] (CG) du corps entier est la **moyenne pondérée** des centres de masse des segments :

$$x_{CG} = \frac{\sum_i m_i \, x_i}{\sum_i m_i}$$

Il bouge dès que les segments bougent : lever les bras le fait monter, se pencher le fait avancer.
Et tant que sa projection verticale tombe dans le [[polygone de sustentation]], on tient debout sans tomber.
""")
    st.markdown("#### À toi : fais un squat sans tomber")
    st.caption("Plie les genoux sans pencher le tronc : le centre de gravité recule derrière les talons et "
               "tu tombes en arrière. Penche ensuite le tronc ou tends les bras pour rattraper l'équilibre.")
    c1, c2 = st.columns([1, 2])
    with c1:
        taille = st.slider("Taille (m)", 1.40, 2.00, 1.68, 0.01, key="bm_taille")
        masse = st.slider("Masse (kg)", 40, 120, 60, key="bm_masse")
        genou = st.slider("Flexion du genou (°)", 0, 130, 0, key="bm_genou")
        dorsi = st.slider("Inclinaison de la jambe vers l'avant (°)", -10, 40, 0, key="bm_dorsi",
                          help="C'est la flexion dorsale de cheville.")
        tronc = st.slider("Inclinaison du tronc vers l'avant (°)", -10, 80, 0, key="bm_tronc")
        epaule = st.slider("Flexion d'épaule (°)", 0, 180, 0, key="bm_epaule")
        coude = st.slider("Flexion du coude (°)", 0, 140, 0, key="bm_coude")
        charge = st.slider("Charge tenue dans les mains (kg)", 0, 30, 0, key="bm_charge")
    p = body_points(taille, dorsi, genou, tronc, epaule, coude)
    com = body_com(p, charge, masse)
    ok = p["talon"][0] <= com[0] <= p["orteil"][0]
    with c2:
        fig = go.Figure()
        chain = ["orteil", "talon", "cheville", "genou", "hanche", "epaule", "tete"]
        fig.add_trace(go.Scatter(x=[p[k][0] for k in chain], y=[p[k][1] for k in chain], mode="lines+markers",
                                 line=dict(width=6, color="#8a93a8"), marker=dict(size=8), name="Corps",
                                 hoverinfo="skip"))
        arm = ["epaule", "coude", "poignet", "main"]
        fig.add_trace(go.Scatter(x=[p[k][0] for k in arm], y=[p[k][1] for k in arm], mode="lines+markers",
                                 line=dict(width=5, color="#a9b0c2"), name="Bras", hoverinfo="skip"))
        if charge:
            fig.add_trace(go.Scatter(x=[p["main"][0]], y=[p["main"][1]], mode="markers", name="Charge",
                                     marker=dict(size=10 + charge / 2, symbol="square", color="#6b7280")))
        color = "#2e8b57" if ok else "#c0392b"
        fig.add_trace(go.Scatter(x=[com[0], com[0]], y=[com[1], 0], mode="lines", line=dict(dash="dot", color=color),
                                 name="Projection du CG"))
        fig.add_trace(go.Scatter(x=[com[0]], y=[com[1]], mode="markers", marker=dict(size=16, color=color,
                                 symbol="circle-x"), name="Centre de gravité"))
        fig.add_shape(type="rect", x0=p["talon"][0], x1=p["orteil"][0], y0=-0.03, y1=0,
                      fillcolor="rgba(46,139,87,0.35)", line_width=0)
        fig.update_layout(height=520, margin=dict(l=10, r=10, t=10, b=10), showlegend=True,
                          legend=dict(orientation="h", y=-0.05),
                          xaxis=dict(range=[-1.0, 1.2], title="m", zeroline=False),
                          yaxis=dict(range=[-0.05, taille * 1.1], scaleanchor="x", title="m"))
        st.plotly_chart(fig, width="stretch")
        h_pct = com[1] / taille
        if ok:
            st.success(f"Équilibre : la projection du CG tombe dans la base d'appui. Hauteur du CG : "
                       f"{com[1]:.2f} m ({h_pct:.0%} de la taille).")
        else:
            side = "arrière" if com[0] < p["talon"][0] else "avant"
            st.error(f"Déséquilibre vers l'{side} : la projection du CG sort de la base d'appui.")
    ui.tip("Position debout, bras le long du corps : le CG est à environ 55 % de la taille. "
           "Bras levés, il monte de quelques centimètres. C'est pour ça qu'on écarte les bras sur une poutre : "
           "on ne baisse pas le CG, on augmente surtout le moment d'inertie, ce qui ralentit les déséquilibres.")
    ui.clinic("Une personne âgée qui se lève d'une chaise doit d'abord **avancer le tronc** pour amener son CG "
              "au-dessus des pieds. Si elle n'y arrive pas (raideur de hanche, peur), elle retombe dans la chaise. "
              "On lui apprend à reculer les pieds sous la chaise et à se pencher « nez au-dessus des orteils ».")
    ui.table([{"Segment": k, "Masse (% du corps)": f"{v[0] * 100:.1f}",
               "CG depuis le bout proximal (% longueur)": f"{v[1] * 100:.1f}"} for k, v in SEGMENTS.items()])
    st.caption("Valeurs de Winter (2009), pour un seul membre. Une jambe entière (cuisse + jambe + pied) fait "
               "environ 16 % du poids du corps.")


def ch_inertie():
    ui.md(r"""
La masse dit à quel point un corps résiste à une **accélération linéaire**. Pour une **rotation**, ce qui
compte est le [[moment d'inertie]] : pas seulement la masse, mais **où elle se trouve** par rapport à l'axe.

$$I = \sum_i m_i \, r_i^2 \qquad \text{et} \qquad M = I \, \alpha$$

(*M* : moment de force en N·m, *α* : accélération angulaire en rad/s²). Le *r²* change tout : une masse
deux fois plus loin de l'axe compte **quatre fois** plus.

On résume souvent un segment par son [[rayon de giration]] *k* : $I = m k^2$. Et pour passer de l'axe du
centre de masse à un autre axe parallèle, on utilise le **théorème de Huygens** (ou des axes parallèles) :

$$I_{\text{axe}} = I_{CG} + m \, d^2$$
""")
    st.markdown("#### À toi : la jambe du coureur")
    st.caption("Moment d'inertie du membre inférieur autour de la hanche selon la flexion du genou "
               "(masses et longueurs de Winter, sujet de 70 kg et 1,75 m).")
    flex = st.slider("Flexion du genou pendant l'oscillation (°)", 0, 130, 0, key="bm_inertie")
    m, h = 70, 1.75
    lt, ls = 0.245 * h, 0.246 * h
    mt, ms, mf = 0.100 * m, 0.0465 * m, 0.0145 * m
    # rayons de giration autour du CG (Winter) : cuisse 0.323, jambe 0.302, pied 0.475 de la longueur
    it = mt * (0.323 * lt) ** 2 + mt * (0.433 * lt) ** 2
    knee = np.array([0, -lt])
    d = np.array([math.sin(math.radians(flex)), -math.cos(math.radians(flex))])
    s_com = knee + 0.433 * ls * d
    ankle = knee + ls * d
    i_s = ms * (0.302 * ls) ** 2 + ms * float(s_com @ s_com)
    i_f = mf * (0.475 * 0.152 * h) ** 2 + mf * float(ankle @ ankle)
    total = it + i_s + i_f
    straight = it + ms * (0.302 * ls) ** 2 + ms * (lt + 0.433 * ls) ** 2 + mf * (0.475 * 0.152 * h) ** 2 + mf * (lt + ls) ** 2
    c1, c2 = st.columns(2)
    c1.metric("Moment d'inertie autour de la hanche", f"{total:.2f} kg·m²",
              delta=f"{(total / straight - 1):+.0%} par rapport à jambe tendue", delta_color="inverse")
    c2.metric("Effort pour la même accélération angulaire", f"{total / straight:.0%}")
    ui.tip("C'est pour ça que les sprinteurs ramènent le talon sous les fesses : avec le genou très fléchi, "
           "la jambe tourne plus facilement autour de la hanche, et la ramener vers l'avant coûte moins d'effort.")
    ui.memo("**Masse loin de l'axe = rotation difficile.** La patineuse qui ramène ses bras tourne plus vite "
            "(conservation du moment cinétique $L = I\\omega$ : si *I* baisse, *ω* augmente).")


def ch_statique():
    ui.md(r"""
Un corps est en équilibre ([[statique]]) quand **rien ne l'accélère**, ni en translation ni en rotation :

$$\sum \vec F = \vec 0 \qquad \text{et} \qquad \sum M = 0$$

Le [[moment de force]] mesure l'effet de rotation : $M = F \times d_\perp$, où $d_\perp$ est le
[[bras de levier]], la distance **perpendiculaire** entre l'axe et la ligne d'action de la force. Une force
qui passe par l'axe ne fait rien tourner, même si elle est énorme.

**Méthode pour tout exercice de statique**
1. Isoler le système (par exemple l'avant-bras + la main).
2. Dessiner **toutes** les forces : poids des segments, charge, muscle, réaction articulaire.
3. Choisir l'axe à l'articulation : la réaction articulaire, inconnue, disparaît de l'équation des moments.
4. $\sum M = 0$ donne la force musculaire, puis $\sum \vec F = \vec 0$ donne la réaction articulaire.
""")
    st.markdown("#### Les trois genres de leviers")
    ui.table([
        ["1er genre (inter-appui)", "Axe entre la force et la résistance", "Tête en équilibre sur l'atlas ; triceps qui étend le coude",
         "Équilibre"],
        ["2e genre (inter-résistant)", "Résistance entre l'axe et la force", "Se mettre sur la pointe des pieds (triceps sural)",
         "Force : bras de levier de la force plus grand"],
        ["3e genre (inter-moteur)", "Force entre l'axe et la résistance", "Biceps qui fléchit le coude ; la plupart des muscles",
         "Vitesse et amplitude, au prix d'une grande force"],
    ], headers=["Genre", "Disposition", "Exemple", "Avantage"])
    ui.memo("**A-R-M** : ce qui est **au milieu** donne le genre. **A**xe au milieu = 1er, **R**ésistance au "
            "milieu = 2e, **M**oteur (muscle) au milieu = 3e.")

    st.markdown("#### À toi : le biceps qui porte une charge")
    st.caption("Bras vertical, le biceps s'insère à 4 cm du coude. On néglige le brachial et le "
               "brachio-radial : tout le travail est pour le biceps (c'est une simplification classique).")
    c1, c2 = st.columns([1, 2])
    with c1:
        angle = st.slider("Flexion du coude (°)", 10, 150, 90, key="bm_coude_stat",
                          help="90° : avant-bras horizontal.")
        charge = st.slider("Charge dans la main (kg)", 0.0, 20.0, 5.0, 0.5, key="bm_charge_stat")
        masse = st.slider("Masse de la personne (kg)", 40, 110, 65, key="bm_masse_stat")
        d_ins = st.slider("Distance d'insertion du biceps (cm)", 2.0, 6.0, 4.0, 0.5, key="bm_ins") / 100

    def biceps(theta_deg):
        th = math.radians(theta_deg)
        fa = np.array([math.sin(th), -math.cos(th)])  # direction de l'avant-bras
        ins = d_ins * fa
        orig = np.array([0.0, 0.30])
        u = (orig - ins) / np.linalg.norm(orig - ins)
        r_m = abs(ins[0] * u[1] - ins[1] * u[0])
        m_seg = 0.022 * masse
        m_grav = m_seg * G * 0.682 * 0.25 * math.sin(th) + charge * G * 0.35 * math.sin(th)
        f = m_grav / r_m
        reaction = np.linalg.norm(f * u + np.array([0, -(m_seg + charge) * G]))
        return f, r_m, m_grav, reaction

    f, r_m, m_grav, reac = biceps(angle)
    with c2:
        k1, k2, k3 = st.columns(3)
        k1.metric("Moment à vaincre", f"{m_grav:.1f} N·m")
        k2.metric("Force du biceps", f"{f:.0f} N", help=f"≈ {f / G:.0f} kg-force")
        k3.metric("Réaction au coude", f"{reac:.0f} N")
        thetas = np.arange(10, 151, 2)
        fs = [biceps(t)[0] for t in thetas]
        fig = go.Figure(go.Scatter(x=thetas, y=fs, mode="lines", name="Force du biceps"))
        fig.add_trace(go.Scatter(x=[angle], y=[f], mode="markers", marker=dict(size=12), name="Position choisie"))
        fig.update_layout(height=300, margin=dict(l=10, r=10, t=30, b=10), title="Force du biceps selon l'angle",
                          xaxis_title="Flexion du coude (°)", yaxis_title="Force (N)", showlegend=False)
        st.plotly_chart(fig, width="stretch")
    ui.md(rf"""
Avec un bras de levier du biceps d'environ **{r_m * 100:.1f} cm** contre **35 cm** pour la charge, le biceps
doit tirer à peu près **{0.35 / r_m:.0f} fois** plus fort que le poids qu'il retient. Le levier de 3e genre
coûte cher en force, mais un petit raccourcissement du muscle déplace la main de beaucoup, et vite.
""")
    ui.warn("Le bras de levier, c'est la distance **perpendiculaire** à la ligne d'action, pas la distance "
            "le long du segment. À 90° de flexion l'avant-bras est horizontal : le poids de la charge a son bras "
            "de levier maximal, et le moment est le plus grand.")
    ui.clinic("Pour soulager une articulation (coxarthrose, par exemple), on cherche à **réduire les moments** : "
              "une canne tenue du côté opposé à la hanche douloureuse réduit fortement le moment que doivent "
              "compenser les abducteurs, donc la force de compression dans la hanche.")


def ch_energie():
    ui.md(r"""
- **Travail** d'une force constante : $W = F \cdot d \cdot \cos\theta$ (en joules). Pour une rotation : $W = M \cdot \Delta\theta$.
- **Énergie cinétique** : $E_c = \tfrac12 m v^2$ (translation) et $\tfrac12 I \omega^2$ (rotation).
- **Énergie potentielle de pesanteur** : $E_p = m g h$.
- **Théorème de l'énergie cinétique** : le travail de toutes les forces = la variation d'énergie cinétique.
- **[[puissance|Puissance]]** : $P = \dfrac{W}{\Delta t} = F \cdot v = M \cdot \omega$ (en watts).

Attention, le travail **mécanique** n'est pas l'effort **physiologique**. Tenir une charge immobile ne fait
aucun travail mécanique ($d = 0$), mais les muscles consomment de l'énergie et on se fatigue.

**Concentrique, excentrique, isométrique**
- Concentrique : le muscle se raccourcit, $M$ et $\omega$ dans le même sens, puissance positive (il **produit** de l'énergie).
- Excentrique : le muscle s'allonge en freinant, puissance négative (il **absorbe** de l'énergie, comme un frein).
- Isométrique : pas de mouvement, puissance nulle.
""")
    st.markdown("#### À toi : la hauteur d'un saut vertical")
    st.caption("Les applis de saut mesurent le temps de vol et en déduisent la hauteur. Le centre de gravité "
               "monte pendant la moitié du vol et redescend pendant l'autre.")
    c1, c2 = st.columns([1, 2])
    with c1:
        tv = st.slider("Temps de vol (ms)", 300, 800, 500, 10, key="bm_tv") / 1000
        m = st.slider("Masse (kg)", 40, 110, 60, key="bm_m_saut")
    h = G * tv ** 2 / 8
    v0 = G * tv / 2
    p_sayers = 60.7 * h * 100 + 45.3 * m - 2055
    with c2:
        k1, k2, k3 = st.columns(3)
        k1.metric("Hauteur du saut", f"{h * 100:.1f} cm")
        k2.metric("Vitesse au décollage", f"{v0:.2f} m/s")
        k3.metric("Puissance de pointe (Sayers)", f"{p_sayers:.0f} W")
    ui.md(r"""
Pourquoi $h = \dfrac{g\, t_v^2}{8}$ ? Le temps de montée vaut $t_v/2$. Pendant la montée, la vitesse passe de
$v_0$ à 0 : $v_0 = g \cdot t_v/2$. Et l'énergie cinétique devient potentielle : $\tfrac12 m v_0^2 = m g h$,
donc $h = \dfrac{v_0^2}{2g} = \dfrac{g\, t_v^2}{8}$. La masse disparaît : elle ne change pas la hauteur pour
une vitesse de décollage donnée. La formule de Sayers (1999), elle, est empirique.
""")


def ch_marche():
    ui.md(r"""
Un [[cycle de marche]] va d'un contact du talon droit au contact suivant du **même** talon. À vitesse
normale (environ 1,3 m/s), il se répartit en :

- **Phase d'appui (≈ 60 %)** : attaque du talon, mise en charge, milieu d'appui, fin d'appui, pré-oscillation.
- **Phase d'oscillation (≈ 40 %)** : oscillation initiale, moyenne et terminale.
- Deux périodes de **double appui** d'environ 10 % chacune. Quand on court, elles disparaissent et sont
  remplacées par une phase de vol.

**Pas ou foulée ?** Le **pas** va d'un pied à l'autre (droit → gauche). La **foulée** (ou enjambée) va d'un pied
au même pied, elle vaut deux pas. La **cadence** se compte en pas par minute (environ 100 à 120).

La composante verticale de la [[force de réaction du sol]] a une forme en « M » : un premier pic à la mise en
charge (le corps est freiné dans sa descente), un creux au milieu d'appui (le CG passe au sommet de sa
trajectoire), puis un second pic à la poussée.
""")
    st.markdown("#### À toi : la force de réaction du sol")
    v = st.slider("Vitesse de marche (m/s)", 0.6, 2.0, 1.3, 0.1, key="bm_vitesse")
    t = np.linspace(0, 100, 400)
    amp = 0.12 + 0.22 * (v - 0.6) / 1.4  # les pics se creusent quand la vitesse augmente (allure typique)
    base = np.where(t <= 100, np.sin(np.pi * t / 100), 0)
    grf = base * (1 - amp * np.exp(-((t - 50) / 14) ** 2)) * (1 + amp)
    grf = grf / grf.max() * (1.05 + 0.25 * (v - 0.6) / 1.4)
    fig = go.Figure(go.Scatter(x=t, y=grf, mode="lines", name="Force verticale"))
    fig.add_hline(y=1, line_dash="dot", annotation_text="poids du corps")
    fig.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="% de la phase d'appui",
                      yaxis_title="Force / poids du corps", yaxis_range=[0, 1.5])
    st.plotly_chart(fig, width="stretch")
    st.caption("Allure schématique : les valeurs exactes dépendent de la personne. Plus on marche vite, plus les "
               "pics montent et plus le creux se creuse.")
    st.markdown("#### Quelques boiteries à reconnaître")
    ui.table([
        ["Boiterie d'esquive (antalgique)", "Douleur à l'appui (entorse, arthrose…)", "Appui raccourci du côté douloureux, on « fuit » la jambe"],
        ["[[trendelenburg|Trendelenburg]]", "Faiblesse du moyen fessier du côté de l'appui", "Le bassin chute du côté opposé à l'appui"],
        ["Duchenne", "Faiblesse du moyen fessier, compensée", "Le tronc se penche du côté de l'appui pour réduire le moment"],
        ["[[steppage|Steppage]]", "Pied tombant (releveurs, nerf fibulaire commun)", "Genou levé très haut, le pied claque au sol"],
        ["Fauchage", "Hémiplégie (spasticité du triceps sural, genou raide)", "La jambe fait un arc de cercle vers l'extérieur"],
        ["Marche à petits pas", "Maladie de Parkinson", "Pas courts, traînants, peu de ballant des bras, festination"],
    ], headers=["Boiterie", "Cause", "Ce qu'on voit"])
    ui.memo("Duchenne et Trendelenburg ont la même cause (moyen fessier faible). **Trendelenburg** : c'est le "
            "**bassin** qui tombe. **Duchenne** : c'est le **tronc** qui se penche pour éviter que le bassin tombe.")


CHAPTERS = [
    ("Corps rigides et centre de gravité", ch_corps),
    ("Moment d'inertie", ch_inertie),
    ("Statique : forces, moments, leviers", ch_statique),
    ("Énergie, travail, puissance", ch_energie),
    ("La marche", ch_marche),
]

# --- Quiz ----------------------------------------------------------------------


def _q_moment(rng):
    f = rng.choice([50, 80, 100, 120, 150, 200])
    d = rng.choice([0.05, 0.1, 0.2, 0.25, 0.3, 0.4])
    return dict(prompt=f"Une force de {f} N agit perpendiculairement au segment, à {d * 100:.0f} cm de l'axe "
                       f"articulaire. Quel est son moment (en N·m) ?",
                answer=f * d, unit="N·m", why=f"M = F × d = {f} × {d} = {f * d:g} N·m.")


def _q_angle(rng):
    f = rng.choice([100, 200, 300])
    d = rng.choice([0.2, 0.3, 0.4])
    a = rng.choice([30, 45, 60])
    ans = f * d * math.sin(math.radians(a))
    return dict(prompt=f"Une force de {f} N s'applique à {d * 100:.0f} cm de l'axe et fait un angle de {a}° avec "
                       f"le segment. Quel est son moment (N·m) ?",
                answer=ans, unit="N·m",
                why=f"Seule la composante perpendiculaire compte : M = F·d·sin(α) = {f} × {d} × sin {a}° ≈ {ans:.1f} N·m.")


def _q_biceps(rng):
    charge = rng.choice([2, 4, 5, 8, 10])
    d_ch = rng.choice([0.30, 0.35])
    d_b = rng.choice([0.03, 0.04, 0.05])
    f = charge * G * d_ch / d_b
    return dict(prompt=f"Avant-bras horizontal, tu tiens {charge} kg à {d_ch * 100:.0f} cm du coude. Le biceps "
                       f"s'insère à {d_b * 100:.0f} cm du coude et tire verticalement. On néglige le poids de "
                       f"l'avant-bras et les autres fléchisseurs. Quelle force (N) doit développer le biceps ? (g = 9,81)",
                answer=f, unit="N", tol=0.03,
                why=f"Équilibre des moments au coude : F × {d_b} = {charge} × 9,81 × {d_ch}, donc F ≈ {f:.0f} N.")


def _q_saut(rng):
    tv = rng.choice([0.40, 0.45, 0.50, 0.55, 0.60])
    h = G * tv ** 2 / 8
    return dict(prompt=f"Le temps de vol d'un saut vertical est de {tv * 1000:.0f} ms. Quelle est la hauteur "
                       f"du saut (en cm) ? (g = 9,81)",
                answer=h * 100, unit="cm", tol=0.03, why=f"h = g·t²/8 = 9,81 × {tv}² / 8 ≈ {h * 100:.1f} cm.")


def _q_puissance(rng):
    m = rng.choice([50, 60, 70, 80])
    h = rng.choice([0.15, 0.2, 0.3])
    t = rng.choice([0.5, 1.0, 2.0])
    p = m * G * h / t
    return dict(prompt=f"Une personne de {m} kg monte une marche de {h * 100:.0f} cm en {t} s. Quelle puissance "
                       f"mécanique moyenne (W) faut-il pour élever son centre de gravité ? (g = 9,81)",
                answer=p, unit="W", tol=0.03, why=f"P = m·g·h / t = {m} × 9,81 × {h} / {t} ≈ {p:.0f} W.")


def _q_com(rng):
    m1, x1 = rng.choice([(2, 0.1), (3, 0.2), (5, 0.1)])
    m2, x2 = rng.choice([(1, 0.4), (2, 0.5), (1, 0.6)])
    x = (m1 * x1 + m2 * x2) / (m1 + m2)
    return dict(prompt=f"Deux segments : {m1} kg avec son centre de masse à {x1 * 100:.0f} cm de l'épaule, "
                       f"{m2} kg à {x2 * 100:.0f} cm. Où est le centre de masse de l'ensemble (cm depuis l'épaule) ?",
                answer=x * 100, unit="cm", tol=0.02,
                why=f"x = (m₁x₁ + m₂x₂)/(m₁ + m₂) = ({m1}×{x1 * 100:.0f} + {m2}×{x2 * 100:.0f})/{m1 + m2} ≈ {x * 100:.1f} cm.")


LEVIERS = {
    "Biceps qui fléchit le coude": "3e genre (inter-moteur)",
    "Se mettre sur la pointe des pieds": "2e genre (inter-résistant)",
    "Tête en équilibre sur l'atlas": "1er genre (inter-appui)",
    "Triceps brachial qui étend le coude": "1er genre (inter-appui)",
    "Deltoïde qui lève le bras tendu": "3e genre (inter-moteur)",
    "Quadriceps qui étend le genou (assis)": "3e genre (inter-moteur)",
}


def _q_levier(rng):
    k = rng.choice(list(LEVIERS))
    return (f"De quel genre de levier s'agit-il : **{k}** ?", LEVIERS[k],
            ["1er genre (inter-appui)", "2e genre (inter-résistant)", "3e genre (inter-moteur)"],
            "Regarde ce qui est au milieu : l'axe (1er), la résistance (2e) ou le muscle (3e).")


QUESTIONS = [
    qcm(1, "Le moment d'une force vaut…", "la force multipliée par le bras de levier",
        ["la force divisée par la distance", "la masse multipliée par l'accélération", "la force multipliée par la vitesse"],
        "M = F × d⊥, en N·m."),
    qcm(1, "Quelle proportion du cycle de marche occupe la phase d'appui, à vitesse normale ?", "Environ 60 %",
        ["Environ 40 %", "Environ 50 %", "Environ 80 %"], "60 % d'appui, 40 % d'oscillation."),
    qcm(1, "Le centre de gravité d'un adulte debout se situe environ…", "en avant de la 2e vertèbre sacrée",
        ["au niveau du nombril, sur la peau", "au niveau de la 12e vertèbre thoracique", "entre les deux genoux"],
        "Vers 55 % de la taille, en avant de S2."),
    vf(1, "Une force dont la ligne d'action passe par l'axe articulaire ne crée aucun moment.", True,
       "Son bras de levier est nul, donc M = 0."),
    vf(1, "La foulée correspond à la distance entre un pied et l'autre pied.", False,
       "Ça, c'est le pas. La foulée va d'un pied au même pied : deux pas."),
    gen_qcm(1, _q_levier),
    num(1, _q_moment),
    qcm(2, "Pourquoi le sprinteur plie-t-il fortement le genou pendant l'oscillation ?",
        "Pour diminuer le moment d'inertie de la jambe autour de la hanche",
        ["Pour augmenter la masse de la jambe", "Pour allonger le bras de levier du quadriceps",
         "Pour baisser son centre de gravité"],
        "Masse rapprochée de l'axe → I plus petit → plus facile à faire tourner vite."),
    multi(2, "Quelles conditions caractérisent l'équilibre statique ?",
          ["La somme des forces est nulle", "La somme des moments est nulle"],
          ["La vitesse est maximale", "Toutes les forces sont égales", "Le centre de gravité est au sol"],
          "Pas d'accélération linéaire ni angulaire."),
    qcm(2, "Pendant la phase de descente d'un squat, le quadriceps travaille en…", "excentrique",
        ["concentrique", "isométrique", "il ne travaille pas"],
        "Il s'allonge en freinant la descente : puissance négative."),
    qcm(2, "Un patient a une boiterie de Trendelenburg à l'appui sur la jambe droite. Quel muscle est faible ?",
        "Le moyen fessier droit", ["Le moyen fessier gauche", "Le grand fessier droit", "Le psoas gauche"],
        "Le moyen fessier du côté de l'appui stabilise le bassin ; s'il est faible, le bassin tombe du côté opposé."),
    qcm(2, "Le pied qui « tombe » et la marche en steppage évoquent surtout une atteinte…",
        "du nerf fibulaire commun (releveurs du pied)",
        ["du nerf fémoral", "du nerf tibial", "du nerf obturateur"],
        "Le fibulaire commun innerve le tibial antérieur et les autres releveurs."),
    vf(2, "Tenir un haltère immobile, bras tendu, ne produit aucun travail mécanique.", True,
       "Pas de déplacement, donc W = 0, même si le muscle consomme de l'énergie."),
    num(2, _q_angle),
    num(2, _q_com),
    num(2, _q_saut),
    num(3, _q_biceps),
    num(3, _q_puissance),
    qcm(3, "Pourquoi une canne se tient-elle du côté opposé à la hanche douloureuse ?",
        "Elle crée un moment qui remplace en partie celui des abducteurs de la hanche douloureuse, et réduit la compression",
        ["Elle soulage le genou du même côté", "Elle allonge le pas du côté douloureux",
         "Elle augmente la base d'appui du côté douloureux"],
        "La canne est loin de l'axe (grand bras de levier) : une petite force suffit à réduire beaucoup le moment."),
    qcm(3, "Le moment d'inertie d'un segment autour de l'articulation proximale vaut…",
        "I_CG + m·d², avec d la distance entre le centre de masse et l'articulation",
        ["I_CG − m·d²", "m·d", "I_CG × d²"], "C'est le théorème de Huygens (axes parallèles)."),
    qcm(3, "Pendant la course, par rapport à la marche…", "les phases de double appui disparaissent et une phase de vol apparaît",
        ["le double appui dure plus longtemps", "la phase d'appui dépasse 60 %", "les pics de force verticale diminuent"],
        "La course se définit justement par une phase de vol."),
]

CARDS = [
    ("Formule du moment de force", "$M = F \\times d_\\perp$ (N·m)"),
    ("Conditions de l'équilibre statique", "$\\sum F = 0$ et $\\sum M = 0$"),
    ("Moment d'inertie", "$I = \\sum m r^2$, résistance à la rotation (kg·m²)"),
    ("Théorème de Huygens", "$I = I_{CG} + m d^2$"),
    ("Hauteur d'un saut à partir du temps de vol", "$h = g\\,t_v^2 / 8$"),
    ("Puissance en rotation", "$P = M \\cdot \\omega$"),
    ("Levier de 3e genre", "Muscle entre l'axe et la résistance (ex. biceps)"),
    ("Levier de 2e genre", "Résistance entre l'axe et le muscle (ex. pointe des pieds)"),
    ("Levier de 1er genre", "Axe entre la force et la résistance (ex. tête sur l'atlas)"),
    ("Répartition du cycle de marche", "60 % appui, 40 % oscillation, 2 × 10 % double appui"),
    ("Boiterie de Trendelenburg", "Bassin qui chute côté opposé à l'appui : moyen fessier faible côté appui"),
    ("Steppage", "Releveurs faibles (nerf fibulaire commun) : genou levé haut"),
    ("Masse d'une cuisse", "Environ 10 % de la masse du corps"),
    ("Hauteur du CG debout", "Environ 55 % de la taille, en avant de S2"),
]

VIDEOS = [
    ("Les trois types de leviers dans le corps", "leviers corps humain biomécanique 1er 2e 3e genre"),
    ("Centre de gravité et équilibre", "centre de gravité polygone de sustentation biomécanique"),
    ("Le cycle de marche et ses phases", "cycle de marche phases appui oscillation kinésithérapie"),
    ("Exercices de statique : moment au coude", "biomécanique exercice moment de force coude biceps"),
]

LINKS = [
    ("Physiopedia : Gait (marche)", "https://www.physio-pedia.com/Gait"),
    ("Physiopedia : Levers", "https://www.physio-pedia.com/index.php?search=levers+biomechanics"),
]
