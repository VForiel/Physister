"""LFSM1201 Physiologie cellulaire et biochimie."""

import math

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from app import ui
from app.course import Course
from app.quiz import gen_qcm, multi, num, qcm, vf

COURSE = Course(
    code="LFSM1201", title="Physiologie cellulaire et biochimie", short="Physiologie cellulaire",
    bloc=2, quad=1, credits=4, hours="37,5 h", icon=":material/bubble_chart:",
    intro="Comment une cellule échange avec son milieu, d'où vient le potentiel électrique des membranes, comment "
          "un muscle se contracte et où il trouve son énergie. C'est la base de la neurophysiologie et de la "
          "physiologie de l'effort.",
    acquis=[
        "Décrire les caractéristiques de fonctionnement communes aux cellules eucaryotes.",
        "Décrire la structure de la cellule musculaire striée et la mécanique de sa contraction.",
        "Décrire les voies métaboliques et leur régulation.",
        "Mobiliser ces concepts pour résoudre des cas concrets.",
    ],
)

R, F = 8.314, 96485

TERMS = {
    "diffusion": ("Diffusion", "Déplacement spontané d'une substance de là où elle est concentrée vers là où elle "
                  "l'est moins, sans énergie.", "Diffusion de la matière"),
    "osmose": ("Osmose", "Passage de l'eau à travers une membrane semi-perméable, du milieu le moins concentré en "
               "solutés vers le plus concentré.", "Osmose"),
    "transport actif": ("Transport actif", "Transport contre le gradient de concentration, qui consomme de l'ATP "
                        "(directement : pompes ; ou indirectement : cotransports).", "Transport actif"),
    "pompe na/k": ("Pompe Na⁺/K⁺-ATPase", "Pompe membranaire qui sort 3 Na⁺ et fait entrer 2 K⁺ en consommant un ATP. "
                   "Elle maintient les gradients ioniques.", "Pompe sodium-potassium"),
    "potentiel de repos": ("Potentiel de repos", "Différence de potentiel entre l'intérieur et l'extérieur d'une "
                           "cellule au repos : environ −70 mV pour un neurone, −90 mV pour une fibre musculaire.",
                           "Potentiel de repos"),
    "équation de nernst": ("Équation de Nernst", "Donne le potentiel d'équilibre d'un ion : E = (RT/zF)·ln(Cext/Cint).",
                           "Équation de Nernst"),
    "second messager": ("Second messager", "Molécule intracellulaire (AMPc, Ca²⁺, IP₃) qui relaie le signal d'une "
                        "hormone ou d'un neurotransmetteur fixé sur un récepteur de membrane.", "Second messager"),
    "couplage excitation-contraction": ("Couplage excitation-contraction", "Suite d'événements qui relie le "
                                        "potentiel d'action de la fibre musculaire à la contraction, via la libération "
                                        "de Ca²⁺ par le réticulum sarcoplasmique.", "Couplage excitation-contraction"),
    "pont actine-myosine": ("Pont actine-myosine", "Liaison temporaire de la tête de myosine sur l'actine ; son "
                            "basculement fait glisser les filaments.", "Myosine"),
    "glycolyse": ("Glycolyse", "Dégradation du glucose en 2 pyruvates dans le cytoplasme, avec un gain net de 2 ATP, "
                  "sans oxygène.", "Glycolyse"),
    "cycle de krebs": ("Cycle de Krebs", "Cycle de réactions dans la mitochondrie qui oxyde l'acétyl-CoA en CO₂ et "
                       "charge des transporteurs d'électrons (NADH, FADH₂).", "Cycle de Krebs"),
    "phosphorylation oxydative": ("Phosphorylation oxydative", "Production d'ATP par la chaîne respiratoire "
                                  "mitochondriale, qui utilise l'O₂ comme accepteur final d'électrons.",
                                  "Phosphorylation oxydative"),
    "phosphocréatine": ("Phosphocréatine", "Réserve d'énergie du muscle qui régénère l'ATP instantanément, pour "
                        "environ 10 secondes d'effort maximal.", "Phosphocréatine"),
    "bêta-oxydation": ("Bêta-oxydation", "Découpage des acides gras en acétyl-CoA dans la mitochondrie.",
                       "Bêta-oxydation"),
    "lactate": ("Lactate", "Produit de la glycolyse quand le pyruvate n'entre pas assez vite dans la mitochondrie. "
                "Il n'est pas un « déchet » : il est réutilisé comme carburant.", "Acide lactique"),
}

IONS = {  # concentrations typiques d'une cellule de mammifère (mmol/L) : intérieur, extérieur, valence
    "K⁺": (140, 4, 1), "Na⁺": (12, 145, 1), "Cl⁻": (7, 110, -1), "Ca²⁺": (0.0001, 2.5, 2),
}


def nernst(cin, cout, z, t=37):
    return 1000 * R * (t + 273.15) / (z * F) * math.log(cout / cin)


def ch_echanges():
    ui.md(r"""
La cellule est un **système ouvert** : elle échange en permanence matière et énergie avec son milieu, à travers
une membrane qui laisse passer certaines choses et pas d'autres.

| Transport | Énergie ? | Exemples |
|---|---|---|
| [[diffusion\|Diffusion]] simple | non (suit le gradient) | O₂, CO₂, petites molécules liposolubles |
| Diffusion facilitée (canal, transporteur) | non | canaux ioniques, transporteur du glucose GLUT4 |
| [[osmose\|Osmose]] | non | eau, par les aquaporines |
| [[transport actif\|Transport actif]] primaire | oui, ATP | [[pompe na/k\|pompe Na⁺/K⁺]], pompe à Ca²⁺ |
| Transport actif secondaire | oui, indirect (utilise le gradient de Na⁺) | cotransport Na⁺-glucose de l'intestin |
| Endocytose / exocytose | oui | libération des neurotransmetteurs |

**La loi de Fick** : le flux de diffusion est proportionnel à la surface, au gradient de concentration et à la
perméabilité, et inversement proportionnel à l'épaisseur. C'est pour ça que les alvéoles pulmonaires sont
immenses et très fines.
""")
    ui.memo("La pompe Na⁺/K⁺ : « **3 dehors, 2 dedans** » (3 Na⁺ sortent, 2 K⁺ entrent) pour 1 ATP. Elle consomme "
            "jusqu'à un tiers de l'énergie de l'organisme au repos !")
    ui.clinic("Le muscle à l'effort fait entrer le glucose grâce au transporteur **GLUT4**, qui monte à la membrane "
              "avec la contraction, même sans insuline. C'est pour ça que l'exercice fait baisser la glycémie chez "
              "le diabétique, et qu'on surveille l'hypoglycémie pendant les séances.")


def ch_potentiel():
    ui.md(r"""
L'intérieur de la cellule est riche en **K⁺**, l'extérieur en **Na⁺** et **Cl⁻**. Ces gradients sont maintenus par
la pompe Na⁺/K⁺.

Pour chaque ion, il existe un potentiel où la force électrique compense exactement la force de diffusion : le
**potentiel d'équilibre**, donné par l'[[équation de nernst|équation de Nernst]] :

$$E_{ion} = \frac{RT}{zF} \ln\frac{[\text{ion}]_{ext}}{[\text{ion}]_{int}} \approx \frac{61{,}5\ \text{mV}}{z}
\log_{10}\frac{[\text{ion}]_{ext}}{[\text{ion}]_{int}} \quad (37\,°C)$$

Au repos, la membrane est surtout perméable au **K⁺** : le [[potentiel de repos]] (≈ −70 mV) est donc proche de
$E_K$ (≈ −90 mV), un peu tiré vers $E_{Na}$ (≈ +60 mV) par une petite perméabilité au Na⁺. L'équation de
**Goldman-Hodgkin-Katz** fait cette moyenne pondérée par les perméabilités.
""")
    st.markdown("#### À toi : le potentiel d'équilibre")
    c1, c2 = st.columns([1, 2])
    with c1:
        ion = st.selectbox("Ion", list(IONS), key="pc_ion")
        cin0, cout0, z = IONS[ion]
        cin = st.number_input("Concentration intérieure (mmol/L)", 0.0001, 500.0, float(cin0), format="%.4g", key=f"pc_in_{ion}")
        cout = st.number_input("Concentration extérieure (mmol/L)", 0.0001, 500.0, float(cout0), format="%.4g", key=f"pc_out_{ion}")
    with c2:
        st.metric(f"E({ion})", f"{nernst(cin, cout, z):+.0f} mV")
        st.markdown("**Potentiel de membrane (Goldman-Hodgkin-Katz)**")
        pna = st.slider("Perméabilité relative au Na⁺ (P_K = 1)", 0.0, 20.0, 0.04, 0.01, key="pc_pna",
                        help="Au repos ≈ 0,04. Au pic du potentiel d'action, elle grimpe à ≈ 20.")
        k, na, cl = IONS["K⁺"], IONS["Na⁺"], IONS["Cl⁻"]
        num_ = 1 * k[1] + pna * na[1] + 0.45 * cl[0]
        den = 1 * k[0] + pna * na[0] + 0.45 * cl[1]
        vm = 1000 * R * 310.15 / F * math.log(num_ / den)
        st.metric("Potentiel de membrane", f"{vm:+.0f} mV")
    ui.clinic("Une **hyperkaliémie** (K⁺ sanguin trop élevé, insuffisance rénale) réduit le gradient de K⁺ : le "
              "potentiel de repos devient moins négatif, les cellules cardiaques deviennent instables. "
              "C'est une urgence (risque d'arrêt cardiaque).")
    ui.tip("Essaie : augmente la concentration extérieure de K⁺ de 4 à 10 mmol/L, et regarde E(K⁺) devenir moins "
           "négatif. C'est exactement l'hyperkaliémie.")


def ch_signal():
    ui.md(r"""
Les cellules communiquent par des **messagers chimiques** :
- **autocrine** (sur elle-même), **paracrine** (cellules voisines), **endocrine** (hormones par le sang),
  **synaptique** (neurotransmetteurs).

**Les récepteurs**
- Les messagers **liposolubles** (hormones stéroïdes, thyroïdiennes) traversent la membrane et agissent sur des
  récepteurs **intracellulaires** qui modifient l'expression des gènes (effet lent et durable).
- Les messagers **hydrosolubles** (adrénaline, insuline, la plupart des neurotransmetteurs) se fixent sur des
  récepteurs **membranaires** : canaux ioniques, récepteurs couplés aux protéines G (qui produisent un
  [[second messager]] comme l'AMPc), récepteurs-enzymes (récepteur de l'insuline).

**Amplification** : une seule molécule d'adrénaline peut, par cascade, activer des milliers d'enzymes.

**Les moteurs cellulaires** : la **myosine** marche sur l'actine (contraction musculaire), la **kinésine** et la
**dynéine** marchent sur les microtubules (transport dans les axones, battement des cils).
""")


def ch_contraction():
    ui.md(r"""
**Structure** : muscle → faisceaux → **fibres** (cellules multinucléées) → **myofibrilles** → [[sarcomère|sarcomères]].
Le sarcomère, entre deux **stries Z**, contient des filaments fins d'**actine** (avec la tropomyosine et la
troponine) et épais de **myosine**.

**Le [[couplage excitation-contraction]]**
1. Le motoneurone libère l'**acétylcholine** à la jonction neuromusculaire.
2. Un potentiel d'action parcourt la membrane et plonge dans les **tubules T**.
3. Le **réticulum sarcoplasmique** libère du **Ca²⁺**.
4. Le Ca²⁺ se fixe sur la **troponine**, qui déplace la **tropomyosine** et libère les sites de l'actine.
5. Les têtes de myosine forment des [[pont actine-myosine|ponts]], basculent (**coup de rame**) et font glisser
   l'actine vers le centre du sarcomère.
6. Un nouvel **ATP** détache la tête ; son hydrolyse la réarme.
7. Le Ca²⁺ est repompé dans le réticulum (avec de l'ATP) : relâchement.
""")
    ui.warn("L'ATP sert à **détacher** la myosine, pas seulement à la faire tirer. Sans ATP, les ponts restent "
            "bloqués : c'est la **rigidité cadavérique**.")
    st.markdown("#### À toi : la relation tension-longueur")
    st.caption("La force dépend du chevauchement entre actine et myosine, donc de la longueur du sarcomère.")
    L = st.slider("Longueur du sarcomère (µm)", 1.3, 3.8, 2.2, 0.05, key="pc_L")
    xs = np.array([1.27, 1.67, 2.0, 2.25, 3.65])
    ys = np.array([0, 0.84, 1.0, 1.0, 0])
    x = np.linspace(1.27, 3.65, 200)
    y = np.interp(x, xs, ys)
    f = float(np.interp(L, xs, ys))
    fig = go.Figure(go.Scatter(x=x, y=y, mode="lines"))
    fig.add_trace(go.Scatter(x=[L], y=[f], mode="markers", marker=dict(size=13)))
    fig.update_layout(height=260, margin=dict(l=10, r=10, t=10, b=10), showlegend=False,
                      xaxis_title="Longueur du sarcomère (µm)", yaxis_title="Force active (relative)")
    st.plotly_chart(fig, width="stretch")
    msg = ("trop court : les filaments se chevauchent et se gênent" if L < 2.0 else
           "zone optimale : chevauchement maximal" if L <= 2.25 else
           "étiré : moins de ponts possibles" if L < 3.65 else "plus aucun chevauchement : force nulle")
    st.caption(f"Force {f:.0%} du maximum : {msg}. Courbe d'après Gordon, Huxley et Julian (1966), fibre de grenouille.")
    ui.clinic("Un muscle immobilisé en position raccourcie (plâtre) perd des sarcomères en série et sa courbe se "
              "déplace : il devient plus court et faible en position allongée. Les étirements et le travail "
              "**excentrique** font l'inverse, ils ajoutent des sarcomères en série.")


def ch_metabolisme():
    ui.md(r"""
**Anabolisme** (construire, consomme de l'énergie) et **catabolisme** (dégrader, libère de l'énergie) sont
couplés par l'**ATP**. Le muscle n'en stocke que pour 2 à 3 secondes : il doit le régénérer en permanence par
trois filières.

| Filière | Substrat | O₂ ? | Débit | Durée à effort maximal |
|---|---|---|---|---|
| ATP-[[phosphocréatine]] | PCr | non | très élevé | ≈ 10 s |
| [[glycolyse\|Glycolyse]] anaérobie | glucose, glycogène | non | élevé | ≈ 30 s à 2 min, produit du [[lactate]] |
| Oxydative | glucides, lipides ([[bêta-oxydation]]), un peu de protéines | oui | modéré | des heures |

**La voie oxydative** : glucose → (glycolyse, cytoplasme) → pyruvate → acétyl-CoA → ([[cycle de krebs|cycle de
Krebs]], mitochondrie) → NADH, FADH₂ → ([[phosphorylation oxydative|chaîne respiratoire]], O₂) → environ
**30 à 32 ATP** par glucose, contre **2** pour la glycolyse seule.
""")
    st.markdown("#### À toi : qui fournit l'énergie ?")
    t = np.linspace(1, 180, 300)
    pcr = np.exp(-t / 8)
    gly = (1 - np.exp(-t / 5)) * np.exp(-t / 40)
    ox = 1 - np.exp(-t / 45)
    s = pcr + gly + ox
    fig = go.Figure()
    for y, name in ((pcr / s, "ATP-PCr"), (gly / s, "Glycolyse anaérobie"), (ox / s, "Oxydative")):
        fig.add_trace(go.Scatter(x=t, y=y, stackgroup="one", name=name))
    fig.update_layout(height=280, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="Durée d'un effort maximal (s)",
                      yaxis_title="Part de l'énergie", yaxis_tickformat=".0%", legend=dict(orientation="h"))
    st.plotly_chart(fig, width="stretch")
    st.caption("Schéma qualitatif : les filières ne s'allument pas l'une après l'autre, elles se recouvrent. Vers "
               "1 à 2 minutes d'effort maximal, la filière oxydative fournit déjà environ la moitié de l'énergie.")
    ui.md(r"""
**Régulation** : l'**insuline** (après un repas) favorise le stockage (glycogène, triglycérides, protéines) ;
le **glucagon** et l'**adrénaline** (jeûne, effort) favorisent la libération du glucose et des acides gras.
""")
    ui.warn("Le lactate n'est **pas** la cause des courbatures (elles viennent de micro-lésions, surtout après de "
            "l'excentrique) et il est éliminé en moins d'une heure. C'est même un carburant pour le cœur et les "
            "fibres lentes.")


CHAPTERS = [
    ("Échanges membranaires", ch_echanges),
    ("Potentiel de membrane", ch_potentiel),
    ("Signalisation", ch_signal),
    ("Contraction musculaire", ch_contraction),
    ("Métabolisme énergétique", ch_metabolisme),
]


def _q_nernst(rng):
    ion = rng.choice(["K⁺", "Na⁺"])
    cin, cout, z = IONS[ion]
    cout = rng.choice([cout, cout * 2, cout / 2]) if ion == "K⁺" else rng.choice([cout, 120, 160])
    e = 61.5 / z * math.log10(cout / cin)
    return dict(prompt=f"Avec [{ion}] intérieur = {cin:g} mmol/L et extérieur = {cout:g} mmol/L, calcule le potentiel "
                       f"d'équilibre à 37 °C (mV), avec E = 61,5 · log(ext/int).",
                answer=e, unit="mV", tol=0.03, why=f"E = 61,5 × log({cout:g}/{cin:g}) ≈ {e:+.0f} mV.")


def _q_atp(rng):
    n = rng.choice([1, 2, 3, 5])
    kind = rng.choice(["aérobie", "anaérobie"])
    per = 31 if kind == "aérobie" else 2
    return dict(prompt=f"Combien d'ATP environ produit l'oxydation de {n} glucose(s) par voie **{kind}** ? "
                       f"(prends 31 ATP par glucose en aérobie, 2 en anaérobie)",
                answer=n * per, tol=0.0, unit="ATP", why=f"{n} × {per} = {n * per}.")


ETAPES = ["Libération d'acétylcholine", "Potentiel d'action dans les tubules T", "Libération de Ca²⁺ par le réticulum",
          "Fixation du Ca²⁺ sur la troponine", "Formation des ponts actine-myosine"]


def _q_etape(rng):
    i = rng.randrange(len(ETAPES) - 1)
    return (f"Dans le couplage excitation-contraction, quelle étape suit directement : **{ETAPES[i]}** ?",
            ETAPES[i + 1], [e for j, e in enumerate(ETAPES) if j != i + 1 and j != i], "")


QUESTIONS = [
    qcm(1, "La pompe Na⁺/K⁺ fait sortir… et entrer…", "3 Na⁺ et 2 K⁺", ["2 Na⁺ et 3 K⁺", "1 Na⁺ et 1 K⁺", "3 K⁺ et 2 Na⁺"]),
    qcm(1, "Quel ion est le plus concentré à l'intérieur de la cellule ?", "K⁺", ["Na⁺", "Cl⁻", "Ca²⁺"]),
    qcm(1, "Quelle filière fournit l'énergie d'un sprint de 6 secondes ?", "ATP-phosphocréatine",
        ["Oxydative", "Bêta-oxydation", "Cycle de Krebs seul"]),
    vf(1, "La diffusion simple consomme de l'ATP.", False, "Elle suit le gradient, sans énergie."),
    qcm(1, "Où se déroule le cycle de Krebs ?", "Dans la mitochondrie", ["Dans le cytoplasme", "Dans le noyau", "Dans le sang"]),
    gen_qcm(2, _q_etape),
    qcm(2, "Sur quelle protéine se fixe le Ca²⁺ pour déclencher la contraction ?", "La troponine",
        ["La myosine", "La titine", "L'acétylcholine"]),
    qcm(2, "Pourquoi le potentiel de repos est-il proche du potentiel d'équilibre du K⁺ ?",
        "Parce qu'au repos la membrane est surtout perméable au K⁺", ["Parce qu'il n'y a pas de Na⁺",
        "Parce que la pompe Na⁺/K⁺ est arrêtée", "Parce que le K⁺ est chargé négativement"]),
    multi(2, "Quels messagers agissent sur des récepteurs intracellulaires ?", ["Cortisol", "Hormones thyroïdiennes"],
          ["Adrénaline", "Insuline", "Acétylcholine"], "Ils sont liposolubles et traversent la membrane."),
    num(2, _q_atp),
    vf(2, "Le lactate est la cause des courbatures du lendemain.", False, "Les courbatures viennent de micro-lésions musculaires."),
    num(3, _q_nernst),
    qcm(3, "Pourquoi la rigidité cadavérique apparaît-elle ?", "Sans ATP, les têtes de myosine ne peuvent plus se détacher de l'actine",
        ["Le Ca²⁺ disparaît", "Les muscles se déshydratent", "L'acétylcholine s'accumule"]),
    qcm(3, "Un muscle est étiré bien au-delà de sa longueur optimale. Sa force active…", "diminue, car moins de ponts sont possibles",
        ["augmente toujours", "reste identique", "devient maximale"]),
    qcm(3, "Pourquoi l'exercice peut-il provoquer une hypoglycémie chez un patient diabétique sous insuline ?",
        "La contraction fait monter GLUT4 à la membrane, ce qui fait entrer le glucose en plus de l'insuline",
        ["L'exercice bloque l'insuline", "Le muscle produit du glucagon", "Le lactate détruit le glucose"]),
    qcm(3, "En hyperkaliémie, le potentiel de repos devient…", "moins négatif (dépolarisé)", ["plus négatif",
        "positif à +60 mV", "inchangé"]),
]

CARDS = [
    ("Pompe Na⁺/K⁺", "3 Na⁺ sortent, 2 K⁺ entrent, 1 ATP"),
    ("Potentiel de repos d'un neurone", "≈ −70 mV"),
    ("Nernst (37 °C)", "E ≈ (61,5/z) · log(ext/int) mV"),
    ("E(K⁺) / E(Na⁺)", "≈ −90 mV / ≈ +60 mV"),
    ("Loi de Fick", "Flux ∝ surface × gradient / épaisseur"),
    ("Ca²⁺ et contraction", "Se fixe sur la troponine, qui déplace la tropomyosine"),
    ("Rôle de l'ATP dans la contraction", "Détacher la myosine de l'actine et la réarmer"),
    ("Filière ATP-PCr", "≈ 10 s, très puissante, sans O₂"),
    ("Glycolyse", "Glucose → 2 pyruvates, 2 ATP net"),
    ("Rendement aérobie du glucose", "≈ 30-32 ATP"),
    ("Second messager", "AMPc, Ca²⁺, IP₃"),
    ("Longueur optimale du sarcomère", "≈ 2,0 à 2,25 µm"),
]

VIDEOS = [
    ("La contraction musculaire animée", "contraction musculaire actine myosine animation"),
    ("Potentiel de repos et équation de Nernst", "potentiel de repos membrane Nernst explication"),
    ("Les filières énergétiques", "filières énergétiques ATP phosphocréatine glycolyse aérobie"),
    ("La pompe sodium-potassium", "pompe sodium potassium animation"),
]

LINKS = [("Simulation PhET : canaux et transport membranaire", "https://phet.colorado.edu/fr/simulations/membrane-channels")]
