"""LKNR1211 Formation en motricité 1."""

import plotly.graph_objects as go
import streamlit as st

from app import ui
from app.course import Course
from app.quiz import gen_qcm, multi, num, qcm, table_qcm, vf

COURSE = Course(
    code="LKNR1211", title="Formation en motricité 1", short="Motricité 1",
    bloc=2, quad=1, credits=4, hours="15 h + 52,5 h", icon=":material/sprint:",
    intro="Un cours surtout pratique (course, musculation, souplesse), mais avec une vraie théorie de l'entraînement "
          "derrière : comment structurer une séance, doser l'endurance, la force, la vitesse et la souplesse. Tu "
          "t'en serviras pour toi, puis pour tes patients.",
    acquis=[
        "Démontrer ses capacités motrices de base (endurance, coordination).",
        "Analyser anatomiquement et biomécaniquement ses propres mouvements.",
        "Prendre conscience de son corps, de ses besoins et de ses limites.",
        "Développer son niveau psychomoteur par l'expérience vécue.",
    ],
)

TERMS = {
    "surcharge progressive": ("Surcharge progressive", "Principe selon lequel il faut augmenter progressivement la "
                              "charge d'entraînement pour continuer à progresser.", None),
    "surcompensation": ("Surcompensation", "Après un effort et une récupération suffisante, l'organisme dépasse son "
                        "niveau initial. Trop peu de récupération : fatigue ; trop : retour à la base.", "Surcompensation"),
    "vo2max": ("VO₂max", "Consommation maximale d'oxygène : la limite de la filière aérobie (mL/kg/min).", "VO2 max"),
    "vma": ("VMA", "Vitesse maximale aérobie : la vitesse de course atteinte à VO₂max, tenable environ 4 à 8 min.",
            "Vitesse maximale aérobie"),
    "fc de réserve": ("FC de réserve", "Différence entre la FC maximale et la FC de repos ; base de la méthode de "
                      "Karvonen.", None),
    "seuil lactique": ("Seuil lactique", "Intensité au-delà de laquelle le lactate s'accumule rapidement dans le sang.",
                       "Seuil lactique"),
    "borg": ("Échelle de Borg", "Échelle de perception de l'effort (6 à 20, ou 0 à 10 pour la version modifiée).",
             "Échelle de Borg"),
    "fractionné": ("Entraînement fractionné", "Alternance de périodes d'effort intense et de récupération (ex. 30 s "
                   "vite / 30 s lent).", "Entraînement fractionné de haute intensité"),
}

PRINCIPES = {
    "Surcharge progressive": "augmenter la charge pour continuer à progresser",
    "Spécificité": "on progresse surtout dans ce qu'on entraîne",
    "Réversibilité": "les gains se perdent si on arrête",
    "Individualisation": "adapter à chaque personne",
    "Alternance travail-récupération": "progresser pendant la récupération (surcompensation)",
    "Progressivité": "augmenter d'abord le volume, ensuite l'intensité",
}


def ch_principes():
    ui.md(r"""
**Les principes de l'entraînement**
""")
    ui.table([[k, v] for k, v in PRINCIPES.items()], headers=["Principe", "En clair"])
    ui.md(r"""
**La [[surcompensation]]** : un entraînement fatigue d'abord, puis l'organisme récupère et dépasse son niveau de
départ. La séance suivante doit tomber au **sommet** de cette surcompensation. Trop rapprochées : on accumule la
fatigue (surmenage). Trop espacées : on perd le bénéfice.

**Structure d'une séance**
1. **Échauffement** (10 à 20 min) : progressif, général puis spécifique. Il augmente la température musculaire,
   la fréquence cardiaque, la vitesse de conduction nerveuse, et prépare mentalement.
2. **Corps de séance** : l'objectif du jour.
3. **Retour au calme** (5 à 10 min) : diminuer progressivement l'intensité.

**Les paramètres** : intensité, volume (durée, nombre de répétitions), fréquence, récupération, type d'exercice.
""")
    ui.memo("**FITT** : **F**réquence, **I**ntensité, **T**emps, **T**ype. Quatre réglages pour doser n'importe quel "
            "exercice, chez un sportif comme chez un patient.")


def ch_endurance():
    ui.md(r"""
L'**endurance** est la capacité à maintenir un effort longtemps. Elle dépend de la [[vo2max|VO₂max]], du
[[seuil lactique]] (le pourcentage de VO₂max qu'on tient longtemps) et de l'économie de course.

**Les formes d'entraînement**
- **Continu** : à intensité modérée, longtemps (footing). Développe la base aérobie.
- **[[fractionné|Fractionné]] / intervalles** : alternances d'efforts intenses (souvent 90 à 110 % de la
  [[vma|VMA]]) et de récupérations. Très efficace pour la VO₂max.

**Doser l'intensité**
- La **FC maximale** : 220 − âge (simple, peu précise) ou 208 − 0,7 × âge (Tanaka, un peu meilleure).
- La méthode de **Karvonen** utilise la [[fc de réserve]] : $\text{FC cible} = \text{FC}_{repos} + x\,\% \times
  (\text{FC}_{max} - \text{FC}_{repos})$.
- La perception de l'effort ([[borg|échelle de Borg]]) et le **test de la parole** (on peut parler mais pas
  chanter : intensité modérée).
""")
    st.markdown("#### À toi : tes zones d'entraînement")
    c1, c2 = st.columns([1, 2])
    with c1:
        age = st.slider("Âge", 16, 80, 21, key="m1_age")
        fcr = st.slider("FC de repos (bpm)", 40, 100, 65, key="m1_fcr")
        formule = st.radio("FC max", ["220 − âge", "Tanaka : 208 − 0,7 × âge"], key="m1_formule")
        vma = st.slider("VMA (km/h)", 8.0, 22.0, 13.0, 0.5, key="m1_vma")
    fcm = 220 - age if formule.startswith("220") else round(208 - 0.7 * age)
    zones = [("Récupération", 0.50, 0.60), ("Endurance fondamentale", 0.60, 0.70), ("Aérobie soutenue", 0.70, 0.80),
             ("Seuil", 0.80, 0.90), ("Intensité maximale", 0.90, 1.00)]
    with c2:
        st.metric("FC maximale estimée", f"{fcm} bpm")
        rows = [[n, f"{round(fcr + a * (fcm - fcr))} à {round(fcr + b * (fcm - fcr))} bpm"] for n, a, b in zones]
        ui.table(rows, headers=["Zone (Karvonen, % FC de réserve)", "FC cible"])
        st.markdown(f"Fractionné 30 s / 30 s à 100 % VMA : cours à **{vma:.1f} km/h**, soit **{vma / 3.6 * 30:.0f} m** "
                    f"en 30 s.")
    ui.tip("La formule 220 − âge peut se tromper de 10 à 15 bpm pour une personne donnée. Chez les patients sous "
           "bêtabloquants, la FC ne monte pas normalement : on dose alors avec l'échelle de Borg.")


def ch_force():
    ui.md(r"""
**Musculation** : machines guidées (sûres, isolent un muscle, bonnes pour débuter), **poids libres** (plus de
coordination et de stabilisation), **poids du corps** (accessible partout).

**Les bons réflexes techniques** : amplitude complète contrôlée, respiration (souffler à l'effort, éviter de
bloquer longtemps sur des charges lourdes), dos neutre, progression de la charge seulement quand la technique est
parfaite.

Les paramètres selon l'objectif (force, hypertrophie, endurance musculaire, puissance) sont dans le cours de
techniques de base (LKNR1202).

**Vitesse et coordination** : la vitesse dépend surtout du système nerveux (recrutement, synchronisation des unités
motrices) et de la technique. On la travaille **frais**, en début de séance, avec des efforts courts (moins de
10 s) et des récupérations complètes.

**Apprentissage moteur** : un geste nouveau passe par des stades (cognitif, associatif, autonome) : voir le cours
de compléments de neurophysiologie. Au début, peu de consignes, un seul point à la fois.
""")


def ch_souplesse():
    ui.md(r"""
**La souplesse** (ou flexibilité) est l'amplitude de mouvement d'une articulation ou d'un groupe d'articulations.

| Méthode | Comment | Quand |
|---|---|---|
| Statique passive | tenir 15 à 60 s, sans douleur | après l'effort, séances dédiées |
| Dynamique | mouvements amples, contrôlés, répétés | échauffement |
| PNF (contracter-relâcher) | contraction 5 s du muscle étiré, relâchement, gain d'amplitude | séances dédiées, gains rapides |
| Balistique | rebonds | à éviter en général (risque) |

**Mobilisations articulaires** : faire bouger les articulations dans toutes leurs amplitudes, surtout à
l'échauffement.
""")
    ui.warn("À l'échauffement d'un sport explosif, préfère les étirements **dynamiques** : de longs étirements "
            "statiques juste avant peuvent diminuer un peu la force et la vitesse.")
    ui.memo("**Échauffement** : dynamique. **Retour au calme et séances souplesse** : statique ou PNF.")


CHAPTERS = [
    ("Principes et séance", ch_principes),
    ("Endurance", ch_endurance),
    ("Force, vitesse, coordination", ch_force),
    ("Souplesse", ch_souplesse),
]


def _q_karvonen(rng):
    age = rng.choice([20, 25, 30, 40, 50])
    fcr = rng.choice([55, 60, 70])
    pct = rng.choice([60, 70, 80])
    fcm = 220 - age
    cible = fcr + pct / 100 * (fcm - fcr)
    return dict(prompt=f"Une personne de {age} ans a une FC de repos de {fcr} bpm. Avec FCmax = 220 − âge et la méthode "
                       f"de Karvonen, quelle est la FC cible à {pct} % de la FC de réserve ?",
                answer=cible, unit="bpm", tol=0.01,
                why=f"FCmax = {fcm} ; FC de réserve = {fcm - fcr} ; cible = {fcr} + {pct / 100} × {fcm - fcr} ≈ {cible:.0f} bpm.")


def _q_vma(rng):
    vma = rng.choice([12, 14, 15, 16, 18])
    pct = rng.choice([90, 100, 110])
    d = vma * pct / 100 / 3.6 * 30
    return dict(prompt=f"Ta VMA est de {vma} km/h. Quelle distance (m) parcours-tu en 30 s à {pct} % de ta VMA ?",
                answer=d, unit="m", tol=0.02, why=f"{vma} × {pct / 100} / 3,6 = {vma * pct / 100 / 3.6:.2f} m/s × 30 s ≈ {d:.0f} m.")


QUESTIONS = [
    table_qcm(1, PRINCIPES, "Que dit le principe de **{k}** ?", "Quel principe : « {v} » ?"),
    qcm(1, "Que signifie FITT ?", "Fréquence, Intensité, Temps, Type", ["Force, Intensité, Tempo, Technique",
        "Fréquence, Intervalle, Tension, Tonus", "Flexibilité, Intensité, Temps, Tolérance"]),
    qcm(1, "Quelle est la formule la plus simple de la FC maximale ?", "220 − âge", ["200 + âge", "180 − âge / 2", "FC repos × 2"]),
    vf(1, "Les étirements balistiques (avec rebonds) sont recommandés à l'échauffement.", False),
    qcm(1, "Quels étirements privilégier à l'échauffement ?", "Dynamiques", ["Statiques longs", "Balistiques", "Aucun mouvement"]),
    num(2, _q_karvonen),
    qcm(2, "À quel moment de la séance travailler la vitesse ?", "En début de séance, quand on est frais",
        ["En fin de séance, fatigué", "Pendant le retour au calme", "Peu importe"]),
    multi(2, "Quels sont les effets de l'échauffement ?", ["Hausse de la température musculaire",
          "Hausse de la fréquence cardiaque", "Conduction nerveuse plus rapide"], ["Baisse de la VO₂max", "Fatigue durable"]),
    qcm(2, "Que se passe-t-il si les séances sont trop rapprochées par rapport à la récupération ?",
        "On accumule la fatigue (risque de surmenage)", ["On progresse plus vite", "Rien", "On gagne en souplesse"]),
    num(2, _q_vma),
    qcm(3, "Un patient sous bêtabloquants fait de la réadaptation à l'effort. Comment doser l'intensité ?",
        "Avec l'échelle de Borg (perception de l'effort), car la FC est freinée", ["Avec 220 − âge",
        "Avec la FC de repos seule", "Au hasard"]),
    qcm(3, "Pourquoi la VMA est-elle utile pour construire un fractionné ?",
        "Elle permet de fixer des allures précises (en % de VMA) pour chaque répétition",
        ["Elle donne la FC maximale", "Elle mesure la souplesse", "Elle remplace l'échauffement"]),
    qcm(3, "Selon le principe de spécificité, un coureur de fond qui ne fait que de la musculation lourde…",
        "progressera peu en endurance", ["progressera autant en endurance", "améliorera sa VO₂max au maximum",
        "deviendra plus souple"]),
    qcm(3, "Quelle progression respecte la progressivité ?", "Augmenter d'abord la durée, ensuite l'intensité",
        ["Augmenter intensité et volume en même temps fortement", "Commencer au maximum puis diminuer", "Ne jamais rien changer"]),
]

CARDS = [
    ("FITT", "Fréquence, Intensité, Temps, Type"),
    ("Surcompensation", "Après effort + récupération, on dépasse le niveau initial"),
    ("FC max (Tanaka)", "208 − 0,7 × âge"),
    ("Karvonen", "FC cible = FC repos + x % × (FC max − FC repos)"),
    ("VMA", "Vitesse à VO₂max, tenable 4 à 8 min"),
    ("Test de la parole", "Modéré = on peut parler, pas chanter"),
    ("Étirements à l'échauffement", "Dynamiques"),
    ("PNF contracter-relâcher", "Contraction 5 s du muscle étiré, puis gain d'amplitude"),
    ("Travail de vitesse", "Frais, < 10 s, récupération complète"),
]

VIDEOS = [
    ("Bien s'échauffer avant de courir", "échauffement course à pied gammes"),
    ("Calculer ses zones cardiaques (Karvonen)", "méthode Karvonen zones fréquence cardiaque"),
    ("Le fractionné et la VMA", "fractionné VMA 30 30 explication"),
    ("Les bases de la musculation", "technique squat soulevé de terre débutant"),
]

LINKS = [("Physiopedia : Principles of exercise", "https://www.physio-pedia.com/index.php?search=exercise+principles")]
