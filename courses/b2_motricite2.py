"""LKNR1212 Formation en motricité 2."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from app import ui
from app.course import Course
from app.quiz import gen_qcm, multi, num, qcm, table_qcm, vf

COURSE = Course(
    code="LKNR1212", title="Formation en motricité 2", short="Motricité 2",
    bloc=2, quad=2, credits=2, hours="30 h de pratique", icon=":material/pool:",
    intro="Un cours 100 % pratique en quatre volets : aisance aquatique, activités physiques adaptées (APSA, "
          "fauteuil, handicap sensoriel), renforcement avec petit matériel, et coordination avec ballons. Ce "
          "chapitre donne les bases théoriques pour comprendre et justifier ce que tu fais en séance.",
    acquis=[
        "Démontrer ses capacités motrices (coordination, souplesse).",
        "Analyser un mouvement, les muscles sollicités, et adapter le geste.",
        "Expliquer et justifier des gestes à un pair pour des pathologies ciblées (cas simulés).",
        "Affiner l'observation d'une tâche motrice et des comportements moteurs.",
    ],
)

TERMS = {
    "pression hydrostatique": ("Pression hydrostatique", "Pression exercée par l'eau, qui augmente avec la profondeur : "
                               "elle favorise le retour veineux et limite l'œdème.", "Pression hydrostatique"),
    "viscosité": ("Viscosité de l'eau", "Résistance de l'eau au mouvement, qui augmente avec la vitesse : plus on va "
                  "vite, plus c'est dur.", "Viscosité"),
    "apsa": ("APSA", "Activités physiques et sportives adaptées : activités modifiées pour être accessibles aux "
             "personnes en situation de handicap ou atteintes de maladies chroniques.", None),
    "step": ("Modèle STEP", "Outil pour adapter une activité en modifiant l'Espace (Space), la Tâche (Task), "
             "l'Équipement (Equipment) ou les Personnes (People).", None),
    "proprioception": ("Proprioception", "Sens de la position et du mouvement de son corps.", "Proprioception"),
    "chaîne cinétique": ("Chaîne cinétique", "Succession de segments qui bougent ensemble ; ouverte (extrémité libre) "
                         "ou fermée (extrémité fixée).", None),
}

# appui sur les membres inférieurs debout statique selon le niveau d'immersion (ordres de grandeur,
# d'après Harrison et al., 1992)
IMMERSION = [(0, 100), (0.29, 85), (0.53, 50), (0.72, 33), (0.82, 10), (1.0, 0)]
NIVEAUX = {"Genoux": 0.29, "Épines iliaques (bassin)": 0.53, "Appendice xiphoïde (bas du sternum)": 0.72,
           "C7 (épaules)": 0.82}


def ch_eau():
    ui.md(r"""
**Les propriétés de l'eau utiles en rééducation**
- La **poussée d'Archimède** allège le corps : on peut marcher, sauter, se renforcer avec moins de charge sur les
  articulations (arthrose, post-opératoire, obésité).
- La [[pression hydrostatique]] favorise le retour veineux, réduit l'œdème, et rend l'inspiration un peu plus
  difficile (attention aux insuffisants cardiaques et respiratoires).
- La [[viscosité]] crée une résistance qui augmente avec la **vitesse** et la **surface** : on dose l'effort en
  allant plus ou moins vite, ou avec des palmes, des haltères en mousse.
- La **chaleur** (bassin de rééducation vers 32 à 34 °C) détend et diminue la douleur.
""")
    st.markdown("#### À toi : quelle charge sur les jambes dans l'eau ?")
    niveau = st.select_slider("Niveau de l'eau", list(NIVEAUX), key="m2_niveau")
    h = NIVEAUX[niveau]
    xs = np.array([p for p, _ in IMMERSION])
    ys = np.array([c for _, c in IMMERSION])
    charge = float(np.interp(h, xs, ys))
    c1, c2 = st.columns([1, 2])
    c1.metric("Charge sur les membres inférieurs", f"≈ {charge:.0f} %", help="Debout, immobile.")
    with c2:
        x = np.linspace(0, 1, 100)
        fig = go.Figure(go.Scatter(x=x * 100, y=np.interp(x, xs, ys), mode="lines"))
        fig.add_trace(go.Scatter(x=[h * 100], y=[charge], mode="markers", marker=dict(size=12)))
        fig.update_layout(height=230, margin=dict(l=10, r=10, t=10, b=10), showlegend=False,
                          xaxis_title="Hauteur d'immersion (% de la taille)", yaxis_title="Charge (% poids du corps)")
        st.plotly_chart(fig, width="stretch")
    st.caption("Ordres de grandeur pour une personne debout immobile (d'après Harrison et al., 1992). En marchant, la "
               "charge augmente, d'autant plus qu'on marche vite.")
    ui.warn("Contre-indications ou précautions de la balnéothérapie : plaies ouvertes, infections, incontinence non "
            "contrôlée, épilepsie non stabilisée, insuffisance cardiaque ou respiratoire sévère, peur de l'eau (à "
            "travailler d'abord). Et toujours la sécurité : surveillance, accès au bassin.")
    ui.md(r"""
**L'aisance aquatique** : flotter, se déplacer, s'immerger, se remettre debout. Avec un patient (ou un pair qui
simule un handicap), on adapte : flotteurs, aide au retournement, entrée progressive. L'**aquagym** combine cardio
et renforcement avec une faible charge articulaire.
""")


def ch_apsa():
    ui.md(r"""
**Les [[apsa|APSA]]** visent à rendre l'activité physique accessible à tous. Le modèle [[step|STEP]] propose quatre
leviers d'adaptation :

| Levier | Exemples |
|---|---|
| **S**pace (espace) | réduire le terrain, délimiter des zones |
| **T**ask (tâche) | simplifier les règles, autoriser un rebond, plus de temps |
| **E**quipment (équipement) | ballon plus gros ou sonore, cible plus grande, fauteuil de sport |
| **P**eople (personnes) | équipes équilibrées, rôles adaptés, travail en binôme |
""")
    ui.md(r"""
**Le fauteuil roulant** : propulsion (pousser loin en arrière, longs mouvements fluides plutôt que de petits
à-coups, pour protéger les épaules), franchir un petit obstacle (lever les roues avant, « wheeling »), transferts
(fauteuil freiné, repose-pieds relevés).

**Simuler un handicap sensoriel** (bandeau, bouchons d'oreilles) : guider une personne malvoyante (elle te tient le
bras au-dessus du coude, tu annonces les obstacles), utiliser des repères sonores et tactiles. L'expérience aide à
comprendre ce que vit le patient… sans prétendre le vivre vraiment.
""")
    ui.clinic("Les épaules des utilisateurs de fauteuil manuel sont très sollicitées (douleurs fréquentes) : technique "
              "de propulsion, renforcement des muscles de la coiffe et des fixateurs de la scapula, et réglage du "
              "fauteuil sont des rôles du kiné.")


def ch_renfo():
    ui.md(r"""
**Le petit matériel** permet de se renforcer partout, y compris au domicile du patient.

| Matériel | Intérêt | Point d'attention |
|---|---|---|
| Bandes élastiques | résistance qui augmente avec l'étirement, portable, peu chère | la résistance est faible en début de mouvement |
| TRX (sangles de suspension) | poids du corps, gainage, intensité réglée par l'inclinaison | demande un bon contrôle du tronc |
| Kettlebell | mouvements dynamiques (swing), chaîne postérieure | technique stricte (charnière de hanche) |
| Medicine ball | lancers, puissance, coordination | contrôler les réceptions |
| Swissball | instabilité, gainage, proprioception | progressivité, sécurité |
| Poids du corps | aucun matériel, fonctionnel | progression par levier, tempo, amplitude |

**Faire progresser un exercice au poids du corps** : augmenter le **bras de levier** (pompes sur les genoux → sur
les pieds), réduire la base d'appui, ajouter de l'instabilité, ralentir le **tempo**, augmenter l'**amplitude**,
passer en unilatéral.

**Expliquer et justifier un geste à un pair** : dire quel muscle travaille, dans quel mode, pourquoi cet exercice
pour cette pathologie, comment l'adapter s'il est trop facile ou trop dur, et ce qui doit faire arrêter.
""")
    ui.memo("Pour rendre un exercice plus dur sans ajouter de charge, pense **LIBTA** : **L**evier plus long, "
            "**I**nstabilité, **B**ase d'appui plus petite, **T**empo plus lent, **A**mplitude plus grande.")


def ch_coordination():
    ui.md(r"""
**La coordination** : organiser les mouvements de plusieurs segments dans le temps et l'espace pour atteindre un
but. Elle s'appuie sur la vision, la [[proprioception]] et l'anticipation.

**Les jeux de ballon et parcours techniques** développent : la coordination œil-main et œil-pied, la prise
d'information (regarder les partenaires, anticiper la trajectoire), le timing, la latéralité, et l'adaptation à un
environnement qui change (habiletés « ouvertes »).

**Observer une tâche motrice** : regarde d'abord le **résultat** (réussi ? précis ?), puis la **qualité** du
mouvement segment par segment (appuis, alignements, synchronisation), compare au côté opposé et à un modèle, et
repère les **compensations**. Filmer au ralenti aide beaucoup.
""")
    ui.tip("En sports collectifs avec des patients, un ballon plus gros et plus lent (ballon de baudruche, ballon "
           "mousse) donne plus de temps pour prendre l'information : c'est le levier « Equipment » du modèle STEP.")


CHAPTERS = [
    ("Milieu aquatique", ch_eau),
    ("Activités physiques adaptées", ch_apsa),
    ("Renforcement avec petit matériel", ch_renfo),
    ("Coordination et observation", ch_coordination),
]


def _q_immersion(rng):
    k = rng.choice(list(NIVEAUX))
    xs = [p for p, _ in IMMERSION]
    ys = [c for _, c in IMMERSION]
    good = f"≈ {np.interp(NIVEAUX[k], xs, ys):.0f} %"
    bad = [f"≈ {v} %" for v in (100, 85, 50, 33, 10) if f"≈ {v} %" != good]
    return (f"Debout immobile, immergée jusqu'au niveau **{k.lower()}**, quelle charge environ porte une personne sur ses "
            f"jambes ?", good, bad, "Ordres de grandeur d'après Harrison et al. (1992).")


STEP = {"S": "Space (espace)", "T": "Task (tâche)", "E": "Equipment (équipement)", "P": "People (personnes)"}

QUESTIONS = [
    table_qcm(1, STEP, "Dans le modèle STEP, que signifie **{k}** ?"),
    vf(1, "Dans l'eau, plus on bouge vite, plus la résistance est grande.", True, "C'est l'effet de la viscosité."),
    qcm(1, "Comment une personne malvoyante se fait-elle guider ?", "Elle tient le bras du guide au-dessus du coude",
        ["Le guide la pousse dans le dos", "Le guide la tient par la main en marchant derrière", "Elle suit la voix sans contact"]),
    qcm(1, "Quelle est la température habituelle d'un bassin de rééducation ?", "Environ 32 à 34 °C", ["Environ 20 °C",
        "Environ 40 °C", "Environ 26 °C"]),
    gen_qcm(2, _q_immersion),
    multi(2, "Quels effets a la pression hydrostatique ?", ["Elle favorise le retour veineux", "Elle limite l'œdème",
          "Elle rend l'inspiration un peu plus difficile"], ["Elle augmente la charge sur les articulations"]),
    qcm(2, "Comment rendre une pompe plus difficile sans charge ajoutée ?", "Allonger le bras de levier (passer des genoux aux pieds)",
        ["Raccourcir l'amplitude", "Accélérer en rebondissant", "Élargir les appuis"]),
    qcm(2, "Quelle technique de propulsion protège le mieux les épaules en fauteuil manuel ?",
        "Des poussées longues et fluides", ["De petites poussées rapides", "Pousser uniquement avec un bras", "Tirer sur les roues vers l'avant"]),
    qcm(3, "Une patiente opérée d'une prothèse de genou ne peut pas encore porter tout son poids. Pourquoi la balnéothérapie est-elle intéressante ?",
        "La poussée d'Archimède réduit la charge, ce qui permet de marcher et de se renforcer plus tôt",
        ["L'eau froide réduit l'inflammation", "La viscosité supprime toute résistance", "Elle remplace la rééducation à sec"]),
    qcm(3, "Dans un jeu de ballon, un patient n'arrive pas à attraper la balle à temps. Quelle adaptation STEP choisir ?",
        "Un ballon plus gros et plus lent (Equipment)", ["Agrandir le terrain", "Ajouter des joueurs adverses", "Raccourcir le temps de jeu"]),
    qcm(3, "Pourquoi la balnéothérapie demande-t-elle de la prudence chez l'insuffisant cardiaque sévère ?",
        "La pression hydrostatique augmente le retour veineux et la charge de travail du cœur",
        ["L'eau ralentit le cœur jusqu'à l'arrêt", "Le chlore est toxique pour le cœur", "Ce n'est pas un problème"]),
    qcm(3, "Pour justifier un exercice à un pair, que dois-tu expliquer en priorité ?",
        "Le muscle visé, le mode de contraction, le lien avec la pathologie et les adaptations possibles",
        ["Uniquement le nombre de répétitions", "La marque du matériel", "Rien, il suffit de montrer"]),
]

CARDS = [
    ("Poussée d'Archimède", "Allège le corps : moins de charge articulaire"),
    ("Pression hydrostatique", "Retour veineux, moins d'œdème, inspiration plus difficile"),
    ("Viscosité", "Résistance qui augmente avec la vitesse"),
    ("Charge immergé jusqu'au bassin", "≈ 50 % du poids du corps (debout)"),
    ("Charge immergé jusqu'aux épaules", "≈ 10 % du poids du corps (debout)"),
    ("Modèle STEP", "Space, Task, Equipment, People"),
    ("Guider une personne malvoyante", "Elle tient le bras du guide au-dessus du coude"),
    ("Propulsion du fauteuil", "Poussées longues et fluides"),
    ("Rendre un exercice plus dur (LIBTA)", "Levier, Instabilité, Base réduite, Tempo lent, Amplitude"),
]

VIDEOS = [
    ("Balnéothérapie et rééducation", "balnéothérapie rééducation exercices piscine"),
    ("Activités physiques adaptées et modèle STEP", "STEP model adapted physical activity"),
    ("Exercices avec bandes élastiques", "exercices bandes élastiques renforcement"),
    ("Propulsion en fauteuil roulant", "technique propulsion fauteuil roulant manuel"),
]

LINKS = [("Physiopedia : Hydrotherapy", "https://www.physio-pedia.com/Hydrotherapy")]
