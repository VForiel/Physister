"""LFSM1105 Physique."""

import math

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from app import ui
from app.course import Course
from app.quiz import multi, num, qcm, vf

COURSE = Course(
    code="LFSM1105", title="Physique", short="Physique",
    bloc=1, quad=1, credits=5, hours="37,5 h + 15 h", icon=":material/rocket_launch:",
    intro="La physique donne les outils de la biomécanique (Q2) et de la physiologie (bloc 2) : forces, "
          "énergie, électricité des nerfs, pression du sang. Les anciennes pages de physique plus détaillées "
          "sont toujours dans la section **Archives** du menu.",
    acquis=[
        "Maîtriser les outils mathématiques de base et interpréter un graphique.",
        "Décrire la dynamique d'un solide avec les lois de Newton et prédire son mouvement.",
        "Connaître les principes d'électricité et de magnétisme et résoudre des exercices.",
        "Appliquer la mécanique des fluides à la circulation sanguine et à la pression artérielle.",
    ],
)

G = 9.81

TERMS = {
    "vecteur": ("Vecteur", "Grandeur avec une norme (une valeur), une direction et un sens : force, vitesse, "
                "accélération. Les grandeurs sans direction (masse, énergie, température) sont des scalaires.",
                "Vecteur"),
    "analyse dimensionnelle": ("Analyse dimensionnelle", "Vérifier qu'une formule est cohérente en comparant les "
                               "unités des deux côtés.", "Analyse dimensionnelle"),
    "quantité de mouvement": ("Quantité de mouvement", "p = m·v (kg·m/s). Elle se conserve dans un système isolé, "
                              "par exemple pendant une collision.", "Quantité de mouvement"),
    "impulsion": ("Impulsion", "Force × durée d'application (N·s). Elle égale la variation de quantité de "
                  "mouvement : F·Δt = Δp.", "Impulsion (mécanique)"),
    "frottement": ("Frottement", "Force qui s'oppose au glissement entre deux surfaces : F ≤ μ·N.", "Frottement"),
    "loi de hooke": ("Loi de Hooke", "Un ressort exerce une force proportionnelle à son allongement : F = −k·x.",
                     "Loi de Hooke"),
    "énergie mécanique": ("Énergie mécanique", "Somme de l'énergie cinétique et de l'énergie potentielle. Elle se "
                          "conserve s'il n'y a pas de frottement.", "Énergie mécanique"),
    "loi d'ohm": ("Loi d'Ohm", "U = R·I : la tension aux bornes d'une résistance est proportionnelle au courant "
                  "qui la traverse.", "Loi d'Ohm"),
    "pression": ("Pression", "Force par unité de surface : P = F/S. Unité SI : pascal (Pa). En médecine, on "
                 "utilise souvent le mmHg (1 mmHg ≈ 133 Pa).", "Pression"),
    "poussée d'archimède": ("Poussée d'Archimède", "Force verticale vers le haut subie par un corps immergé, égale "
                            "au poids du fluide déplacé.", "Poussée d'Archimède"),
    "loi de poiseuille": ("Loi de Poiseuille", "Débit d'un fluide visqueux dans un tube : Q = π r⁴ ΔP / (8 η L). "
                          "Le débit dépend du rayon à la puissance 4.", "Loi de Poiseuille"),
    "bernoulli": ("Principe de Bernoulli", "Dans un fluide parfait, là où la vitesse augmente, la pression "
                  "diminue.", "Théorème de Bernoulli"),
    "champ électrique": ("Champ électrique", "Zone où une charge subit une force électrique. Mesuré en V/m.",
                         "Champ électrique"),
    "condensateur": ("Condensateur", "Deux conducteurs séparés par un isolant, qui stockent des charges. La "
                     "membrane cellulaire se comporte comme un condensateur.", "Condensateur (électricité)"),
}


def ch_outils():
    ui.md(r"""
**Unités et puissances de 10.** Toujours travailler en unités SI (mètre, kilogramme, seconde, ampère…) et
convertir **avant** de calculer. Préfixes à connaître : kilo (10³), centi (10⁻²), milli (10⁻³), micro (10⁻⁶),
nano (10⁻⁹).

L'[[analyse dimensionnelle]] est ton meilleur filet de sécurité : si ta formule donne des m/s pour une force,
elle est fausse. Une force est en newtons, et $1\,\text{N} = 1\,\text{kg·m/s}^2$.

**Trigonométrie du triangle rectangle** (indispensable pour décomposer les forces) :

$$\sin\alpha = \frac{\text{opposé}}{\text{hypoténuse}} \qquad \cos\alpha = \frac{\text{adjacent}}{\text{hypoténuse}} \qquad \tan\alpha = \frac{\text{opposé}}{\text{adjacent}}$$
""")
    ui.memo("**SOH-CAH-TOA** : **S**inus = **O**pposé/**H**ypoténuse, **C**osinus = **A**djacent/**H**ypoténuse, "
            "**T**angente = **O**pposé/**A**djacent.")
    st.markdown("#### À toi : décompose une force")
    c1, c2 = st.columns([1, 2])
    with c1:
        F = st.slider("Norme de la force (N)", 10, 500, 200, key="ph_F")
        a = st.slider("Angle avec l'horizontale (°)", 0, 90, 30, key="ph_a")
    fx, fy = F * math.cos(math.radians(a)), F * math.sin(math.radians(a))
    with c2:
        fig = go.Figure()
        fig.add_annotation(x=fx, y=fy, ax=0, ay=0, xref="x", yref="y", axref="x", ayref="y", arrowhead=3,
                           arrowwidth=3, arrowcolor="#4d5f92")
        fig.add_annotation(x=fx, y=0, ax=0, ay=0, xref="x", yref="y", axref="x", ayref="y", arrowhead=2,
                           arrowcolor="#c0392b")
        fig.add_annotation(x=fx, y=fy, ax=fx, ay=0, xref="x", yref="y", axref="x", ayref="y", arrowhead=2,
                           arrowcolor="#2e8b57")
        fig.update_layout(height=280, margin=dict(l=10, r=10, t=10, b=10), xaxis_range=[0, 520], yaxis_range=[0, 520],
                          yaxis_scaleanchor="x")
        ui.chart(fig, "physique_0")
        st.markdown(f"Composante horizontale (rouge) : $F\\cos\\alpha$ = **{fx:.0f} N** · "
                    f"verticale (vert) : $F\\sin\\alpha$ = **{fy:.0f} N**")
    ui.md(r"""
**[[vecteur|Vecteurs]]** : on additionne les vecteurs **composante par composante**, jamais leurs normes
directement. Deux forces de 100 N peuvent donner une résultante de 0 N (opposées) à 200 N (même sens).
""")
    ui.tip("Pour les dérivées et intégrales (vitesse = dérivée de la position, etc.), relis la page archivée "
           "« Dérivées et intégrales » : elle a des exemples pas à pas.")


def ch_cinematique():
    ui.md(r"""
La **cinématique** décrit le mouvement sans s'occuper de ses causes.

- Vitesse : $v = \dfrac{dx}{dt}$ ; accélération : $a = \dfrac{dv}{dt}$.
- **Mouvement rectiligne uniformément accéléré** (MRUA, *a* constante) :
  $$v = v_0 + a t \qquad x = x_0 + v_0 t + \tfrac12 a t^2 \qquad v^2 = v_0^2 + 2a\,\Delta x$$

**Projectile** : on sépare les deux axes. Horizontalement, rien n'accélère (*vitesse constante*, si on néglige
l'air). Verticalement, c'est une chute libre ($a = -g$).

$$x(t) = v_0\cos\theta \cdot t \qquad y(t) = h_0 + v_0\sin\theta \cdot t - \tfrac12 g t^2$$
""")
    st.markdown("#### À toi : lance une balle")
    c1, c2 = st.columns([1, 2])
    with c1:
        v0 = st.slider("Vitesse initiale (m/s)", 1.0, 30.0, 12.0, 0.5, key="ph_v0")
        th = st.slider("Angle (°)", 0, 90, 45, key="ph_th")
        h0 = st.slider("Hauteur de lancer (m)", 0.0, 3.0, 2.0, 0.1, key="ph_h0")
    vx, vy = v0 * math.cos(math.radians(th)), v0 * math.sin(math.radians(th))
    t_vol = (vy + math.sqrt(vy ** 2 + 2 * G * h0)) / G
    t = np.linspace(0, t_vol, 200)
    x, y = vx * t, h0 + vy * t - 0.5 * G * t ** 2
    with c2:
        fig = go.Figure(go.Scatter(x=x, y=y, mode="lines"))
        fig.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="x (m)", yaxis_title="y (m)",
                          xaxis_range=[0, 100], yaxis_range=[0, 50])
        ui.chart(fig, "physique_1")
        k1, k2, k3 = st.columns(3)
        k1.metric("Portée", f"{x[-1]:.1f} m")
        k2.metric("Hauteur max", f"{h0 + vy ** 2 / (2 * G):.1f} m")
        k3.metric("Temps de vol", f"{t_vol:.2f} s")
    ui.tip("Depuis le sol, la portée est maximale à 45°. Depuis une hauteur (lancer du poids), l'angle optimal est "
           "un peu plus faible, vers 40°. Vérifie-le avec les curseurs !")
    ui.md(r"""
**Mouvement circulaire uniforme** : la vitesse garde la même valeur mais change de direction, donc il y a une
accélération, dirigée **vers le centre** (centripète) :

$$a_c = \frac{v^2}{r} = \omega^2 r \qquad v = \omega r \qquad \omega = \frac{2\pi}{T}$$
""")


def ch_dynamique():
    ui.md(r"""
**Les trois lois de Newton**
1. **Inertie** : sans force résultante, un corps reste immobile ou garde une vitesse constante.
2. **Loi fondamentale** : $\sum \vec F = m \vec a$ (plus généralement $\sum \vec F = \dfrac{d\vec p}{dt}$).
3. **Action-réaction** : si A pousse B, B pousse A avec une force égale et opposée.

La [[quantité de mouvement]] $\vec p = m\vec v$ se **conserve** quand aucune force extérieure n'agit. Et une
force qui agit pendant un temps Δt change la quantité de mouvement : c'est l'[[impulsion]].

$$\vec F \cdot \Delta t = \Delta \vec p$$
""")
    ui.clinic("Pour une même variation de vitesse (Δp fixé), **allonger le temps** d'impact réduit la force. "
              "C'est pour ça qu'on apprend à fléchir les genoux à la réception d'un saut : le choc dure plus longtemps, "
              "et les forces sur les articulations et le ligament croisé diminuent.")
    st.markdown("#### À toi : réception d'un saut")
    c1, c2 = st.columns([1, 2])
    with c1:
        m = st.slider("Masse (kg)", 40, 100, 60, key="ph_m_rec")
        h = st.slider("Hauteur de chute (m)", 0.1, 1.5, 0.5, 0.05, key="ph_h_rec")
        dt = st.slider("Durée de l'amorti (ms)", 20, 500, 100, 10, key="ph_dt") / 1000
    v = math.sqrt(2 * G * h)
    f = m * v / dt + m * G
    with c2:
        st.metric("Vitesse à l'impact", f"{v:.2f} m/s")
        st.metric("Force moyenne du sol", f"{f:.0f} N", help="Force pour freiner, plus le poids.")
        st.metric("En multiples du poids du corps", f"{f / (m * G):.1f} × PC")
    ui.md(r"""
**Collisions** : la quantité de mouvement totale se conserve toujours. L'énergie cinétique, elle, ne se conserve
que dans un choc **élastique** ; dans un choc **mou** (les objets restent collés), une partie part en déformation
et en chaleur.
""")


def ch_forces():
    ui.md(r"""
| Force | Formule | Remarques |
|---|---|---|
| Poids | $P = m g$ | vers le bas, *g* ≈ 9,81 m/s² |
| Réaction normale | $N$ | perpendiculaire à la surface |
| [[frottement\|Frottement]] sec | $F_f \le \mu_s N$ (statique), $F_f = \mu_c N$ (glissement) | s'oppose au glissement |
| Ressort ([[loi de hooke\|Hooke]]) | $F = -k\,x$ | proportionnelle à l'allongement |
| Amortissement visqueux | $F = -c\,v$ | proportionnelle à la vitesse |

Un ressort avec une masse oscille à la pulsation $\omega_0 = \sqrt{k/m}$. Avec un amortissement, les oscillations
diminuent.
""")
    st.markdown("#### À toi : oscillateur amorti")
    c1, c2 = st.columns([1, 2])
    with c1:
        k = st.slider("Raideur k (N/m)", 10, 500, 100, key="ph_k")
        mm = st.slider("Masse m (kg)", 0.5, 10.0, 2.0, 0.5, key="ph_mm")
        c = st.slider("Amortissement c (N·s/m)", 0.0, 60.0, 3.0, 0.5, key="ph_c")
    t = np.linspace(0, 6, 1500)
    x, vv = 0.1, 0.0
    xs = []
    dt_ = t[1] - t[0]
    for _ in t:
        a = (-k * x - c * vv) / mm
        vv += a * dt_
        x += vv * dt_
        xs.append(x)
    crit = 2 * math.sqrt(k * mm)
    with c2:
        fig = go.Figure(go.Scatter(x=t, y=xs, mode="lines"))
        fig.update_layout(height=280, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="t (s)",
                          yaxis_title="position (m)", xaxis_range=[0, 6], yaxis_range=[-0.12, 0.12])
        ui.chart(fig, "physique_2")
        regime = "sous-amorti (oscille)" if c < crit else ("critique" if abs(c - crit) < 1 else "sur-amorti (pas d'oscillation)")
        st.caption(f"Amortissement critique : c = 2√(km) ≈ {crit:.1f} N·s/m. Régime actuel : {regime}.")
    ui.clinic("Les tendons et ligaments sont **viscoélastiques** : un peu ressort (élastiques), un peu amortisseur "
              "(visqueux). Leur réponse dépend de la vitesse d'étirement, et ils se relâchent quand on maintient "
              "un étirement (fluage, relaxation). On le reverra en techniques de base (bloc 2).")


def ch_energie():
    ui.md(r"""
- Travail d'une force : $W = \vec F \cdot \vec d = F d \cos\theta$ (J).
- Énergie cinétique $E_c = \tfrac12 m v^2$ ; énergie potentielle de pesanteur $E_p = m g h$ ; élastique $\tfrac12 k x^2$.
- [[énergie mécanique|Énergie mécanique]] $E_m = E_c + E_p$ : **constante** sans frottement.
- Puissance $P = W/\Delta t = F \cdot v$ (W).

**Méthode** : quand on demande une vitesse à partir d'une hauteur (ou l'inverse), pense d'abord énergie, c'est
souvent bien plus rapide que Newton. Une balle lâchée de *h* arrive au sol à $v = \sqrt{2 g h}$, quelle que soit
sa masse.
""")
    ui.memo("Énergie = **capacité** à faire un travail. Puissance = **vitesse** à laquelle on le fait. Monter un "
            "escalier en marchant ou en courant demande la **même énergie**, mais pas la même puissance.")


def ch_electricite():
    ui.md(r"""
**Charges et champ.** Deux charges de même signe se repoussent, de signes opposés s'attirent (loi de Coulomb :
$F = k\dfrac{q_1 q_2}{r^2}$). Une charge crée autour d'elle un [[champ électrique]] ; une différence de potentiel
(**tension**, en volts) pousse les charges à se déplacer.

**Circuits** : le **courant** *I* (ampères) est un débit de charges. La [[loi d'ohm|loi d'Ohm]] relie tension,
résistance et courant :

$$U = R \cdot I \qquad P = U \cdot I$$

Résistances en **série** : $R = R_1 + R_2$. En **parallèle** : $\dfrac1R = \dfrac1{R_1} + \dfrac1{R_2}$.

**Le lien avec le corps** : la membrane d'un neurone sépare des charges (environ −70 mV à l'intérieur au repos).
Elle se comporte comme un [[condensateur]] (la bicouche lipidique isole) en parallèle avec des résistances (les
canaux ioniques). C'est le modèle électrique du neurone que tu verras en neurophysiologie.

**Magnétisme** : un courant crée un champ magnétique, et un champ magnétique variable crée un courant (induction).
Applications : l'**IRM**, la **stimulation magnétique transcrânienne** (TMS) en recherche sur la motricité.
""")
    ui.clinic("L'**électrothérapie** (TENS contre la douleur, électrostimulation des muscles) applique ces lois : "
              "l'intensité qui traverse les tissus dépend de la tension et de la résistance de la peau, d'où "
              "l'importance du gel et de la taille des électrodes.")


def ch_fluides():
    ui.md(r"""
**[[pression|Pression]]** : $P = F/S$. Dans un fluide au repos, elle augmente avec la profondeur :

$$P = P_0 + \rho g h$$

Debout, la pression dans les veines des pieds est bien plus haute qu'au cœur (la colonne de sang pèse). C'est
pour ça qu'on mesure la tension au bras, **à hauteur du cœur**.

La [[poussée d'archimède|poussée d'Archimède]] vaut le poids du fluide déplacé : $F_A = \rho_{\text{fluide}}\, V\, g$.

**Débit et continuité** : le débit $Q = S \cdot v$ est le même partout dans un tuyau sans fuite. Là où le tuyau
se rétrécit, le sang accélère. Et selon [[bernoulli|Bernoulli]], là où il accélère, la pression baisse.

**Fluide visqueux : la [[loi de poiseuille|loi de Poiseuille]]**

$$Q = \frac{\pi r^4 \,\Delta P}{8 \eta L} \qquad \Rightarrow \qquad R = \frac{8 \eta L}{\pi r^4}$$

Le rayon est à la **puissance 4** : c'est en changeant le diamètre des artérioles (vasoconstriction,
vasodilatation) que le corps règle les débits.
""")
    st.markdown("#### À toi : le pouvoir du rayon")
    pct = st.slider("Rayon du vaisseau (% du rayon normal)", 50, 150, 100, key="ph_r")
    ratio = (pct / 100) ** 4
    c1, c2 = st.columns(2)
    c1.metric("Débit (même pression)", f"{ratio:.0%}")
    c2.metric("Résistance", f"{1 / ratio:.0%}")
    st.caption("Un rétrécissement de 20 % du rayon (plaque d'athérome, vasoconstriction) divise presque le débit "
               "par 2,5. Une dilatation de 20 % le double presque.")
    ui.md(r"""
**Pression artérielle** : notée systolique/diastolique en mmHg (par ex. 120/80). Elle résulte du débit cardiaque
et de la résistance des vaisseaux : $\text{PA} = Q \times R$, l'équivalent de $U = R \cdot I$ pour le sang.
""")


CHAPTERS = [
    ("Outils mathématiques", ch_outils),
    ("Cinématique", ch_cinematique),
    ("Dynamique et quantité de mouvement", ch_dynamique),
    ("Forces usuelles", ch_forces),
    ("Travail et énergie", ch_energie),
    ("Électricité et magnétisme", ch_electricite),
    ("Fluides et circulation", ch_fluides),
]


def _q_chute(rng):
    h = rng.choice([0.2, 0.45, 0.8, 1.25, 2.0])
    v = math.sqrt(2 * G * h)
    return dict(prompt=f"Une personne tombe d'une hauteur de {h} m. Quelle est sa vitesse à l'impact (m/s) ? (g = 9,81, sans frottement)",
                answer=v, unit="m/s", why=f"Conservation de l'énergie : v = √(2gh) = √(2 × 9,81 × {h}) ≈ {v:.2f} m/s.")


def _q_newton(rng):
    m = rng.choice([2, 5, 10, 20])
    a = rng.choice([0.5, 1.5, 2, 3])
    return dict(prompt=f"Quelle force résultante faut-il pour donner une accélération de {a} m/s² à une masse de {m} kg ?",
                answer=m * a, unit="N", why=f"F = m·a = {m} × {a} = {m * a:g} N.")


def _q_ohm(rng):
    u = rng.choice([6, 9, 12, 24])
    r = rng.choice([100, 200, 470, 1000])
    return dict(prompt=f"Une tension de {u} V est appliquée sur une résistance de {r} Ω. Quel courant la traverse (mA) ?",
                answer=u / r * 1000, unit="mA", why=f"I = U/R = {u}/{r} = {u / r * 1000:.3g} mA.")


def _q_poiseuille(rng):
    f = rng.choice([0.5, 0.8, 0.9, 1.2, 2])
    return dict(prompt=f"Le rayon d'une artériole est multiplié par {f} (pression constante). Par combien le débit "
                       f"est-il multiplié ?",
                answer=f ** 4, tol=0.02, why=f"Q ∝ r⁴ : facteur {f}⁴ ≈ {f ** 4:.3g}.")


def _q_hydro(rng):
    h = rng.choice([0.5, 1.0, 1.2, 1.3])
    p = 1060 * G * h / 133.3
    return dict(prompt=f"Debout, les pieds sont {h} m sous le cœur. De combien (mmHg) la pression sanguine y est-elle plus "
                       f"élevée qu'au niveau du cœur ? (ρ sang = 1060 kg/m³, 1 mmHg = 133,3 Pa)",
                answer=p, unit="mmHg", tol=0.03, why=f"ΔP = ρgh = 1060 × 9,81 × {h} ≈ {1060 * G * h:.0f} Pa ≈ {p:.0f} mmHg.")


def _q_projectile(rng):
    v0 = rng.choice([8, 10, 12, 15])
    th = rng.choice([30, 45, 60])
    portee = v0 ** 2 * math.sin(math.radians(2 * th)) / G
    return dict(prompt=f"Une balle est lancée depuis le sol à {v0} m/s avec un angle de {th}°. Quelle est sa portée (m) ? "
                       f"(g = 9,81, sans frottement)",
                answer=portee, unit="m", tol=0.03,
                why=f"Portée = v₀²·sin(2θ)/g = {v0}² × sin({2 * th}°)/9,81 ≈ {portee:.2f} m.")


def _q_impulsion(rng):
    m = rng.choice([50, 60, 70])
    v = rng.choice([2, 3, 4])
    dt = rng.choice([0.05, 0.1, 0.2])
    f = m * v / dt
    return dict(prompt=f"Une personne de {m} kg arrive au sol à {v} m/s et s'arrête en {dt * 1000:.0f} ms. Quelle est la "
                       f"force moyenne de freinage (N), sans compter le poids ?",
                answer=f, unit="N", tol=0.02, why=f"F·Δt = Δp → F = m·v/Δt = {m}×{v}/{dt} = {f:.0f} N.")


QUESTIONS = [
    qcm(1, "Quelle est l'unité SI de la force ?", "Le newton (kg·m/s²)", ["Le joule", "Le watt", "Le pascal"]),
    qcm(1, "Que vaut sin α dans un triangle rectangle ?", "opposé / hypoténuse",
        ["adjacent / hypoténuse", "opposé / adjacent", "hypoténuse / opposé"]),
    vf(1, "Sans frottement, deux objets de masses différentes lâchés de la même hauteur arrivent au sol en même temps.", True),
    qcm(1, "La 3e loi de Newton dit que…", "à toute action correspond une réaction égale et opposée",
        ["F = m·a", "un corps sans force reste au repos ou en mouvement uniforme", "l'énergie se conserve"]),
    vf(1, "La masse est une grandeur vectorielle.", False, "C'est un scalaire : pas de direction."),
    num(1, _q_newton),
    num(1, _q_ohm),
    qcm(2, "Dans le mouvement d'un projectile (sans air), la composante horizontale de la vitesse…", "reste constante",
        ["diminue", "augmente", "s'annule au sommet"], "Aucune force horizontale ne s'exerce."),
    qcm(2, "Pourquoi fléchir les genoux à la réception d'un saut réduit-il les forces ?",
        "Le temps d'amorti s'allonge, donc la force moyenne diminue pour la même variation de quantité de mouvement",
        ["La masse du corps diminue", "La vitesse d'impact diminue", "La gravité diminue"]),
    qcm(2, "Le débit dans un vaisseau dépend du rayon à la puissance…", "4", ["1", "2", "3"]),
    multi(2, "Quelles grandeurs se conservent dans une collision parfaitement élastique ?",
          ["La quantité de mouvement totale", "L'énergie cinétique totale"], ["La vitesse de chaque objet", "La force"]),
    num(2, _q_chute),
    num(2, _q_projectile),
    qcm(2, "Selon Bernoulli, là où un fluide accélère dans un rétrécissement, sa pression…", "diminue",
        ["augmente", "ne change pas", "devient nulle"]),
    num(3, _q_poiseuille),
    num(3, _q_hydro),
    num(3, _q_impulsion),
    qcm(3, "Pourquoi mesure-t-on la pression artérielle au bras, à hauteur du cœur ?",
        "Pour éviter l'effet de la colonne de sang (ρgh), qui fausserait la mesure",
        ["Parce que l'artère du bras est la plus grosse", "Parce que le bras n'a pas de veines",
         "Parce que la pression est nulle ailleurs"]),
    qcm(3, "Une membrane cellulaire sépare des charges grâce à sa bicouche lipidique isolante. Elle se comporte comme…",
        "un condensateur", ["une bobine", "un générateur de courant alternatif", "un fil conducteur"]),
]

CARDS = [
    ("2e loi de Newton", "$\\sum F = m a$"),
    ("Quantité de mouvement", "$p = m v$ (kg·m/s)"),
    ("Impulsion", "$F \\cdot \\Delta t = \\Delta p$"),
    ("MRUA : position", "$x = x_0 + v_0 t + \\tfrac12 a t^2$"),
    ("MRUA : sans le temps", "$v^2 = v_0^2 + 2 a \\Delta x$"),
    ("Accélération centripète", "$a_c = v^2 / r$"),
    ("Loi de Hooke", "$F = -k x$"),
    ("Énergie cinétique", "$E_c = \\tfrac12 m v^2$"),
    ("Vitesse après une chute de h", "$v = \\sqrt{2 g h}$"),
    ("Loi d'Ohm", "$U = R I$"),
    ("Pression hydrostatique", "$P = P_0 + \\rho g h$"),
    ("Loi de Poiseuille", "$Q = \\pi r^4 \\Delta P / (8 \\eta L)$ : débit ∝ r⁴"),
    ("Continuité du débit", "$Q = S \\cdot v$ constant"),
    ("SOH-CAH-TOA", "sin = O/H, cos = A/H, tan = O/A"),
    ("1 mmHg", "≈ 133 Pa"),
]

VIDEOS = [
    ("Les lois de Newton expliquées", "lois de Newton explication cours physique"),
    ("Mouvement d'un projectile", "mouvement projectile parabolique cours physique"),
    ("Loi de Poiseuille et circulation sanguine", "loi de Poiseuille circulation sanguine"),
    ("Conservation de l'énergie mécanique", "conservation énergie mécanique exercice"),
]

LINKS = [
    ("Simulations PhET (Université du Colorado), en français", "https://phet.colorado.edu/fr/simulations/browse"),
    ("Khan Academy (FR) : physique", "https://fr.khanacademy.org/science/physics"),
]
