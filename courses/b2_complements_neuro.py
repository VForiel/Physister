"""LKNR1200 Compléments de neurophysiologie."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from app import ui
from app.course import Course
from app.quiz import gen_qcm, multi, qcm, vf

COURSE = Course(
    code="LKNR1200", title="Compléments de neurophysiologie", short="Compléments de neuro",
    bloc=2, quad=2, credits=2, hours="22,5 h", icon=":material/psychology:",
    intro="Trois sujets essentiels pour le kiné : comment on apprend un geste (et comment l'enseigner), comment "
          "fonctionne la douleur (et pourquoi elle n'est pas un simple signal de lésion), et le rôle du cortex "
          "associatif, de la motivation et du sommeil.",
    acquis=[
        "Expliquer la nociception et la douleur.",
        "Expliquer l'apprentissage moteur et la plasticité cérébrale.",
        "Décrire les fonctions associatives du cortex fronto-pariétal.",
        "Comprendre la motivation et son impact sur le comportement moteur.",
        "Connaître la neurobiologie et les fonctions du sommeil.",
    ],
)

TERMS = {
    "plasticité cérébrale": ("Plasticité cérébrale", "Capacité du système nerveux à se modifier (connexions, cartes "
                             "corticales) avec l'expérience, l'apprentissage ou après une lésion.", "Neuroplasticité"),
    "potentialisation à long terme": ("Potentialisation à long terme (LTP)", "Renforcement durable d'une synapse après "
                                      "une stimulation répétée : base cellulaire de la mémoire.", "Potentialisation à long terme"),
    "interférence contextuelle": ("Interférence contextuelle", "Pratiquer plusieurs tâches mélangées (pratique "
                                  "aléatoire) perturbe la performance pendant l'entraînement mais améliore la "
                                  "rétention et le transfert.", None),
    "connaissance du résultat": ("Connaissance du résultat (KR)", "Feedback sur l'issue du mouvement (« tu as mis "
                                 "12 secondes », « le ballon est passé à côté »).", None),
    "connaissance de la performance": ("Connaissance de la performance (KP)", "Feedback sur la façon de faire le "
                                       "mouvement (« ton genou part en dedans »).", None),
    "nociception": ("Nociception", "Détection et transmission des stimulus potentiellement dangereux par les "
                    "nocicepteurs. Ce n'est pas encore la douleur.", "Nociception"),
    "douleur": ("Douleur", "Selon l'IASP (2020) : expérience sensorielle et émotionnelle désagréable associée, ou "
                "ressemblant à celle associée, à une lésion tissulaire réelle ou potentielle.", "Douleur"),
    "gate control": ("Théorie du portillon (gate control)", "Melzack et Wall (1965) : dans la moelle, l'activité des "
                     "grosses fibres du toucher peut « fermer la porte » aux messages nociceptifs.",
                     "Théorie du portillon"),
    "sensibilisation centrale": ("Sensibilisation centrale", "Amplification des messages de douleur par le système "
                                 "nerveux central : la douleur devient plus forte, plus étendue, déclenchée par "
                                 "moins.", "Sensibilisation centrale"),
    "douleur nociplastique": ("Douleur nociplastique", "Douleur liée à une modulation altérée de la nociception, "
                              "sans lésion tissulaire ni nerveuse claire qui l'explique (fibromyalgie, certaines "
                              "lombalgies chroniques).", None),
    "allodynie": ("Allodynie", "Douleur provoquée par un stimulus normalement non douloureux (le simple toucher).",
                  "Allodynie"),
    "héminégligence": ("Héminégligence", "Après une lésion pariétale (souvent droite), le patient ignore la moitié "
                       "de l'espace et de son corps (souvent la gauche).", "Héminégligence"),
    "fonctions exécutives": ("Fonctions exécutives", "Fonctions du cortex préfrontal : planifier, inhiber, garder en "
                             "mémoire de travail, changer de stratégie.", "Fonctions exécutives"),
    "sommeil paradoxal": ("Sommeil paradoxal (REM)", "Stade de sommeil avec rêves, mouvements rapides des yeux et "
                          "atonie musculaire.", "Sommeil paradoxal"),
}


def ch_apprentissage():
    ui.md(r"""
**Les stades de l'apprentissage moteur** (Fitts et Posner) :
1. **Cognitif** : on réfléchit à chaque étape, gestes lents et irréguliers, beaucoup d'erreurs.
2. **Associatif** : le geste se stabilise, on corrige mieux ses erreurs.
3. **Autonome** : le geste est automatique, on peut faire autre chose en même temps.

**Organiser la pratique**
- **Bloquée** (AAA BBB CCC) ou **aléatoire** (ABC BCA CAB) : la pratique aléatoire est moins bonne pendant
  l'entraînement, mais **meilleure pour la rétention** (c'est l'[[interférence contextuelle]]).
- **Constante** ou **variable** (varier distances, vitesses, contextes) : la variabilité améliore le transfert.
- **Massée** (sans pause) ou **distribuée** (avec pauses, sur plusieurs jours) : la pratique distribuée gagne.

**Le feedback** : [[connaissance du résultat]] (KR) et [[connaissance de la performance]] (KP). Trop de feedback
rend dépendant : on le **diminue progressivement**, et on laisse le patient s'auto-évaluer. Une **attention
externe** (« pousse le sol », « vise la cible ») marche mieux qu'une attention interne (« contracte ton quadriceps »).
""")
    st.markdown("#### À toi : pratique bloquée ou aléatoire ?")
    st.caption("Courbes schématiques inspirées de Shea et Morgan (1979) : performance pendant l'entraînement, puis "
               "rétention après 10 jours sans pratique.")
    t = np.arange(1, 19)
    bloc = 100 - 60 * np.exp(-t / 3)
    alea = 100 - 70 * np.exp(-t / 6)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=bloc, name="Bloquée", mode="lines+markers"))
    fig.add_trace(go.Scatter(x=t, y=alea, name="Aléatoire", mode="lines+markers"))
    fig.add_trace(go.Scatter(x=[22], y=[bloc[-1] - 30], name="Rétention bloquée", mode="markers", marker=dict(size=14)))
    fig.add_trace(go.Scatter(x=[22], y=[alea[-1] - 8], name="Rétention aléatoire", mode="markers", marker=dict(size=14)))
    fig.add_vline(x=20, line_dash="dot", annotation_text="10 jours de pause")
    fig.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="Essais d'entraînement",
                      yaxis_title="Performance (%)", legend=dict(orientation="h", y=-0.25))
    st.plotly_chart(fig, width="stretch")
    ui.tip("Pour réviser, c'est pareil ! Mélanger les matières (la page « Révision mélangée ») est moins confortable "
           "que de réviser un cours d'un bloc, mais on retient mieux.")
    ui.md(r"""
**La [[plasticité cérébrale]]** : l'apprentissage modifie les synapses ([[potentialisation à long terme]],
« les neurones qui s'activent ensemble se connectent ensemble » : règle de Hebb) et les cartes corticales (la
représentation des doigts d'un violoniste s'agrandit). Après un AVC, la récupération s'appuie sur cette plasticité :
elle dépend de la **quantité**, de l'**intensité**, de la **spécificité** et de la **motivation** de la pratique.
""")
    ui.clinic("La **thérapie par contrainte induite** (CIMT) après un AVC : on immobilise le bras sain pour forcer "
              "l'utilisation intensive du bras parétique. Elle exploite la plasticité et combat le « non-usage appris ».")


def ch_douleur():
    ui.md(r"""
**[[nociception|Nociception]] ≠ douleur.** La nociception est le signal des nocicepteurs ; la [[douleur]] est une
**expérience** construite par le cerveau, qui tient compte du contexte, des émotions, des croyances et de
l'expérience passée. On peut avoir une lésion sans douleur (soldat blessé au combat) et une douleur sans lésion
(membre fantôme).

**Les fibres de la nociception**
- **Aδ** (myélinisées, rapides) : douleur **rapide**, aiguë, bien localisée (la piqûre).
- **C** (non myélinisées, lentes) : douleur **lente**, sourde, diffuse (la brûlure qui suit).

**La modulation**
- Dans la moelle : la [[gate control|théorie du portillon]] (frotter une zone cognée soulage).
- Par les **voies descendantes** du tronc cérébral (substance grise périaqueducale) : le cerveau peut freiner ou
  amplifier le signal (endorphines, attention, peur, stress).

**Les types de douleur** (IASP)
- **Nociceptive** : liée à une lésion ou une menace des tissus (entorse).
- **Neuropathique** : liée à une lésion du système nerveux (sciatique, zona) : brûlures, décharges électriques.
- **[[douleur nociplastique|Nociplastique]]** : modulation altérée, sans lésion qui l'explique, souvent avec
  [[sensibilisation centrale]] : la douleur s'étend, devient plus forte ([[allodynie]], hyperalgésie).
""")
    ui.clinic("Expliquer la douleur au patient (**éducation aux neurosciences de la douleur**) réduit la peur et le "
              "catastrophisme, et l'aide à reprendre le mouvement. « Avoir mal ne veut pas toujours dire se faire "
              "mal » : c'est particulièrement vrai dans les douleurs chroniques.")
    ui.memo("**Aδ** = **A**iguë et rapide (myélinisée) ; **C** = **C**almement lente, sourde (non myélinisée).")


def ch_cortex():
    ui.md(r"""
**Les aires associatives** intègrent les informations de plusieurs sens et préparent l'action.

- **Cortex pariétal postérieur** : construit la représentation de l'espace et du corps, et guide le geste vers un
  objet. Une lésion pariétale (surtout droite) donne une [[héminégligence]] : le patient ignore la moitié gauche
  de l'espace (il ne mange que la moitié droite de son assiette). Il peut aussi exister une **apraxie** (difficulté
  à réaliser un geste sur commande, sans paralysie).
- **Cortex préfrontal** : [[fonctions exécutives]] (planifier, inhiber, flexibilité), prise de décision,
  comportement social. Une lésion préfrontale donne des difficultés à organiser, de l'impulsivité ou de l'apathie.

**La motivation** : le **système dopaminergique** (de l'aire tegmentale ventrale au striatum) signale la valeur
attendue d'une action et l'écart entre récompense attendue et obtenue. Il pousse à agir et à apprendre. La
motivation augmente la vigueur et la vitesse des mouvements, et améliore l'apprentissage. Fixer des objectifs
atteignables, valoriser les progrès, donner du choix au patient : c'est jouer sur ces mécanismes.
""")
    ui.clinic("Un patient héminégligent après un AVC droit : placer les objets importants, la télé et les visites "
              "progressivement du côté négligé, et l'entraîner à explorer ce côté (balayage visuel).")


def ch_sommeil():
    ui.md(r"""
**L'architecture du sommeil** : des **cycles** d'environ **90 minutes**, 4 à 6 par nuit. Chaque cycle passe par le
sommeil lent léger (N1, N2), le sommeil lent **profond** (N3, surtout en début de nuit) et le [[sommeil paradoxal]]
 (REM, surtout en fin de nuit : rêves, atonie musculaire).

**Ses fonctions** : récupération physique (hormone de croissance libérée en sommeil profond), **consolidation de
la mémoire** (y compris les apprentissages moteurs : on progresse « en dormant »), régulation des émotions,
élimination des déchets du cerveau, immunité.

**La régulation** : le **processus homéostatique** (la pression de sommeil monte pendant l'éveil, avec
l'adénosine, que la caféine bloque) et le **processus circadien** (horloge biologique, réglée par la lumière via la
mélatonine).
""")
    h = [0, 1, 2, 3, 3, 2, 4, 1, 2, 3, 2, 4, 4, 1, 2, 2, 4, 4, 1, 2, 4, 4, 4, 0]
    labels = {0: "Éveil", 1: "N1", 2: "N2", 3: "N3", 4: "REM"}
    order = {0: 0, 4: 1, 1: 2, 2: 3, 3: 4}
    x = np.linspace(0, 8, len(h))
    fig = go.Figure(go.Scatter(x=x, y=[order[v] for v in h], mode="lines", line_shape="hv"))
    fig.update_layout(height=240, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="Heures de sommeil",
                      yaxis=dict(tickvals=list(order.values()), ticktext=[labels[k] for k in order], autorange="reversed"))
    st.plotly_chart(fig, width="stretch")
    st.caption("Hypnogramme schématique : sommeil profond (N3) en début de nuit, sommeil paradoxal (REM) plus long en fin de nuit.")
    ui.clinic("Le manque de sommeil augmente la sensibilité à la douleur et le risque de blessure, et ralentit la "
              "récupération. Demander « Comment dormez-vous ? » fait partie de l'anamnèse, surtout dans les douleurs "
              "chroniques.")


CHAPTERS = [
    ("Apprentissage moteur et plasticité", ch_apprentissage),
    ("Nociception et douleur", ch_douleur),
    ("Cortex associatif et motivation", ch_cortex),
    ("Le sommeil", ch_sommeil),
]

FEEDBACKS = [
    ("« Ta balle est passée 20 cm à droite de la cible. »", "Connaissance du résultat (KR)"),
    ("« Ton coude s'écarte trop pendant le lancer. »", "Connaissance de la performance (KP)"),
    ("« Tu as tenu 18 secondes en équilibre. »", "Connaissance du résultat (KR)"),
    ("« Ton genou part vers l'intérieur à la réception. »", "Connaissance de la performance (KP)"),
]
DOULEURS = [
    ("Douleur de cheville après une entorse, qui augmente à l'appui.", "Nociceptive"),
    ("Brûlures et décharges électriques le long de la jambe après une hernie qui comprime une racine.", "Neuropathique"),
    ("Douleurs diffuses depuis des années, sans lésion retrouvée, avec allodynie et fatigue.", "Nociplastique"),
]


def _q_fb(rng):
    t, good = rng.choice(FEEDBACKS)
    return (f"Quel type de feedback ? {t}", good, ["Connaissance du résultat (KR)", "Connaissance de la performance (KP)"], "")


def _q_dl(rng):
    t, good = rng.choice(DOULEURS)
    return (f"Quel type de douleur ? {t}", good, ["Nociceptive", "Neuropathique", "Nociplastique"], "")


QUESTIONS = [
    qcm(1, "Quels sont les trois stades de l'apprentissage moteur (Fitts et Posner) ?", "Cognitif, associatif, autonome",
        ["Initial, moyen, final", "Moteur, sensitif, mixte", "Lent, rapide, automatique"]),
    gen_qcm(1, _q_fb),
    qcm(1, "Combien dure environ un cycle de sommeil ?", "90 minutes", ["20 minutes", "4 heures", "8 heures"]),
    vf(1, "La nociception et la douleur sont la même chose.", False, "La douleur est une expérience construite par le cerveau."),
    qcm(1, "Quelles fibres transmettent la douleur rapide et bien localisée ?", "Les fibres Aδ", ["Les fibres C",
        "Les fibres Aα", "Les fibres Aβ"]),
    gen_qcm(2, _q_dl),
    qcm(2, "Pourquoi la pratique aléatoire est-elle intéressante ?", "Elle améliore la rétention, malgré une moins bonne performance pendant l'entraînement",
        ["Elle donne de meilleurs résultats pendant l'entraînement", "Elle est plus confortable", "Elle supprime le besoin de feedback"]),
    qcm(2, "Que dit la théorie du portillon ?", "L'activité des fibres du toucher peut freiner la transmission nociceptive dans la moelle",
        ["La douleur vient uniquement du cerveau", "Les fibres C ferment la moelle", "La douleur est proportionnelle à la lésion"]),
    multi(2, "Quels sont des rôles du sommeil ?", ["Consolidation de la mémoire", "Récupération physique",
          "Régulation des émotions"], ["Augmenter la sensibilité à la douleur", "Bloquer l'apprentissage moteur"]),
    qcm(2, "Une lésion pariétale droite donne souvent…", "une héminégligence gauche", ["une aphasie",
        "une paralysie droite", "une perte de l'odorat"]),
    qcm(3, "Un patient apprend à se relever du sol. Comment organiser la pratique pour la rétention ?",
        "Varier les situations, espacer les séances et diminuer progressivement le feedback",
        ["Répéter 100 fois le même geste en une séance, avec feedback à chaque essai", "Ne jamais lui dire ce qui ne va pas",
         "Faire uniquement de la théorie"]),
    qcm(3, "Quelle consigne favorise le mieux l'apprentissage d'un saut ?", "« Pousse le sol le plus fort possible »",
        ["« Contracte tes quadriceps »", "« Pense à tes ischio-jambiers »", "« Fléchis la hanche à 60° »"],
        "Une attention externe (sur l'effet du mouvement) est plus efficace."),
    qcm(3, "Une patiente lombalgique chronique a mal au moindre toucher de la peau du dos. Ce phénomène s'appelle…",
        "allodynie (signe de sensibilisation centrale)", ["hyperréflexie", "anesthésie", "héminégligence"]),
    qcm(3, "Pourquoi le manque de sommeil est-il important à repérer chez un patient douloureux ?",
        "Il augmente la sensibilité à la douleur et freine la récupération", ["Il n'a pas d'effet",
        "Il diminue toujours la douleur", "Il améliore l'apprentissage moteur"]),
]

CARDS = [
    ("Stades de Fitts et Posner", "Cognitif, associatif, autonome"),
    ("Interférence contextuelle", "Pratique aléatoire : moins bien sur le moment, mieux retenu"),
    ("KR / KP", "Feedback sur le résultat / sur la façon de faire"),
    ("Attention externe", "Se concentrer sur l'effet du mouvement : meilleur apprentissage"),
    ("Règle de Hebb", "Les neurones qui s'activent ensemble se connectent ensemble"),
    ("Définition IASP de la douleur", "Expérience sensorielle et émotionnelle désagréable…"),
    ("Fibres Aδ / C", "Douleur rapide localisée / lente diffuse"),
    ("Gate control", "Les fibres du toucher ferment la porte à la nociception (Melzack et Wall, 1965)"),
    ("Douleur nociplastique", "Modulation altérée sans lésion explicative"),
    ("Allodynie", "Douleur au stimulus normalement indolore"),
    ("Héminégligence", "Lésion pariétale droite → ignore la gauche"),
    ("Cycle de sommeil", "≈ 90 min ; N3 en début de nuit, REM en fin de nuit"),
]

VIDEOS = [
    ("Apprentissage moteur : pratique variable et aléatoire", "apprentissage moteur pratique aléatoire interférence contextuelle"),
    ("Comprendre la douleur (neurosciences de la douleur)", "comprendre la douleur neurosciences éducation patient"),
    ("Tame the beast : la douleur persistante", "Tame the Beast douleur persistante"),
    ("Les cycles du sommeil", "cycles du sommeil stades explication"),
]

LINKS = [("Retrain Pain : cours gratuit sur la douleur (FR)", "https://www.retrainpain.org/francais")]
