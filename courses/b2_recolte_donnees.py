"""LKNR1201 Méthode de récolte des données en sciences de la santé."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from app import ui
from app.course import Course
from app.quiz import gen_qcm, multi, qcm, vf

COURSE = Course(
    code="LKNR1201", title="Méthode de récolte des données en sciences de la santé", short="Récolte de données",
    bloc=2, quad=1, credits=2, hours="22,5 h + 7,5 h", icon=":material/assignment:",
    intro="Avant d'analyser des données, il faut les récolter correctement : choisir la bonne méthode, les bonnes "
          "variables, éviter les biais et respecter la vie privée des participants. Utile pour lire les articles, "
          "et pour ton futur mémoire.",
    acquis=[
        "Connaître les principes et les étapes de la récolte de données.",
        "Distinguer les types de données et de méthodes de récolte.",
        "Identifier les biais dans une récolte de données et dans un article.",
        "Faire une synthèse critique de quelques articles sur une problématique de santé.",
    ],
)

TERMS = {
    "donnée primaire": ("Donnée primaire", "Donnée récoltée directement par le chercheur pour sa question "
                        "(mesures, questionnaires).", None),
    "donnée secondaire": ("Donnée secondaire", "Donnée déjà existante, récoltée pour un autre but (dossiers "
                          "médicaux, registres, bases de l'INAMI).", None),
    "variable nominale": ("Variable nominale", "Catégories sans ordre (sexe, groupe sanguin, sport pratiqué).", None),
    "variable ordinale": ("Variable ordinale", "Catégories ordonnées, sans écarts égaux (douleur légère/modérée/"
                          "sévère, échelle de Likert, score MRC 0-5).", None),
    "variable continue": ("Variable quantitative continue", "Mesure numérique sur une échelle (âge, force en N, "
                          "amplitude en degrés).", None),
    "fiabilité": ("Fiabilité (fidélité)", "Capacité d'une mesure à donner le même résultat quand on la répète dans "
                  "les mêmes conditions (reproductibilité).", "Fiabilité"),
    "validité": ("Validité", "Capacité d'une mesure à mesurer réellement ce qu'elle prétend mesurer.", "Validité (statistique)"),
    "biais de sélection": ("Biais de sélection", "L'échantillon n'est pas représentatif de la population visée.",
                           "Biais de sélection"),
    "biais de mesure": ("Biais de mesure", "Erreur systématique dans la façon de mesurer (appareil mal calibré, "
                        "évaluateur qui connaît le groupe).", None),
    "biais de désirabilité sociale": ("Biais de désirabilité sociale", "Les participants répondent ce qui est bien vu "
                                      "plutôt que la vérité (« je fais mes exercices tous les jours »).",
                                      "Biais de désirabilité sociale"),
    "effet hawthorne": ("Effet Hawthorne", "Les participants changent de comportement parce qu'ils se savent "
                        "observés.", "Effet Hawthorne"),
    "échantillonnage aléatoire": ("Échantillonnage aléatoire", "Chaque membre de la population a la même chance d'être "
                                  "tiré au sort. Meilleure garantie de représentativité.", "Échantillonnage (statistiques)"),
    "rgpd": ("RGPD", "Règlement général sur la protection des données (UE, 2016) : encadre le traitement des données "
             "personnelles, avec des règles renforcées pour les données de santé.",
             "Règlement général sur la protection des données"),
    "pseudonymisation": ("Pseudonymisation", "Remplacer l'identité par un code ; la clé de correspondance existe "
                         "encore, séparément. Les données restent personnelles au sens du RGPD.", "Pseudonymisation"),
    "anonymisation": ("Anonymisation", "Rendre impossible, de façon irréversible, toute réidentification. Les données "
                      "ne sont alors plus des données personnelles.", "Anonymisation"),
    "focus group": ("Focus group", "Entretien de groupe (6 à 10 personnes) animé autour d'un thème, pour recueillir "
                    "des opinions et des expériences.", "Groupe de discussion"),
}

VARIABLES = [
    ("Groupe sanguin", "Nominale"), ("Sport pratiqué", "Nominale"), ("Côté opéré (droit/gauche)", "Nominale"),
    ("Score de force MRC (0 à 5)", "Ordinale"), ("Satisfaction (pas du tout … tout à fait)", "Ordinale"),
    ("Stade d'arthrose (I à IV)", "Ordinale"), ("Amplitude de flexion du genou (°)", "Quantitative continue"),
    ("Temps au Timed Up and Go (s)", "Quantitative continue"), ("Nombre de chutes dans l'année", "Quantitative discrète"),
]


def ch_types():
    ui.md(r"""
**Sources** : [[donnée primaire|primaires]] (tu les récoltes) ou [[donnée secondaire|secondaires]] (elles existent
déjà : dossiers, registres). Les secondaires coûtent moins, mais n'ont pas été pensées pour ta question.

**Types de variables**

| Type | Exemple | Ce qu'on peut calculer |
|---|---|---|
| Qualitative [[variable nominale\|nominale]] | groupe sanguin | fréquences, mode |
| Qualitative [[variable ordinale\|ordinale]] | douleur faible / modérée / forte | médiane, rangs |
| Quantitative discrète | nombre de chutes | moyenne, écart type |
| Quantitative [[variable continue\|continue]] | force (N), amplitude (°) | moyenne, écart type |

**Choisir ses variables** : la variable **dépendante** (le résultat qu'on étudie), les variables
**indépendantes** (les facteurs étudiés), et les **variables de confusion** à mesurer pour pouvoir en tenir compte.
""")
    st.markdown("#### À toi : quel type de variable ?")
    i = st.session_state.setdefault("rd_i", 0) % len(VARIABLES)
    var, good = VARIABLES[i]
    st.markdown(f"> **{var}**")
    rep = st.radio("Type", ["Nominale", "Ordinale", "Quantitative discrète", "Quantitative continue"], index=None,
                   horizontal=True, key=f"rd_v_{i}")
    if rep:
        (st.success if rep == good else st.error)(f"Réponse : **{good}**")
    if st.button("Variable suivante", key="rd_next"):
        st.session_state["rd_i"] = i + 1
        st.rerun()
    ui.warn("Un score ordinal codé avec des chiffres (MRC 0 à 5) n'est pas une vraie mesure : passer de 2 à 3 n'est "
            "pas le même « écart » que de 4 à 5. On calcule plutôt la médiane que la moyenne.")


def ch_methodes():
    ui.md(r"""
| Méthode | Données | Points forts | Limites |
|---|---|---|---|
| Expérimentation | quantitatives | montre la causalité (groupe contrôle, hasard) | lourd, situation artificielle |
| Enquête par questionnaire | quanti (ou quali, questions ouvertes) | beaucoup de participants, pas cher | désirabilité sociale, compréhension des questions |
| Entretien (directif, semi-directif, libre) | qualitatives | profondeur, vécu | peu de participants, chronophage |
| [[focus group\|Focus group]] | qualitatives | dynamique de groupe, idées variées | certains dominent, pas d'anonymat |
| Observation (participante ou non) | quali ou quanti | comportement réel | [[effet hawthorne\|effet Hawthorne]], interprétation |
| Étude de cas | quali surtout | richesse, cas rares | pas généralisable |
| Analyse de documents | secondaires | rapide, rétrospectif | données incomplètes |

**L'échantillonnage** : l'[[échantillonnage aléatoire]] est la référence. En pratique, on recrute souvent par
**commodité** (les patients de son cabinet, les étudiants de sa promo) : c'est plus simple, mais les résultats
se généralisent moins bien.

**Construire un questionnaire** : questions courtes, une seule idée par question, pas de double négation, pas de
question qui suggère la réponse, échelles de **Likert** (de « pas du tout d'accord » à « tout à fait d'accord »),
et toujours un **pré-test** sur quelques personnes.
""")
    ui.tip("En kiné, on utilise beaucoup de questionnaires **validés** (KOOS pour le genou, Oswestry pour le dos, "
           "DASH pour le membre supérieur). Utilise-les plutôt que d'inventer ton propre questionnaire : leurs "
           "qualités sont connues.")


def ch_biais():
    ui.md(r"""
Un **biais** est une erreur **systématique**, qui fausse toujours dans le même sens (contrairement à l'erreur
aléatoire, qui se compense sur de grands nombres).

| Biais | Exemple |
|---|---|
| [[biais de sélection\|Sélection]] | étudier la lombalgie chez les seuls patients des kinés : on rate ceux qui ne consultent pas |
| Non-réponse / attrition | les patients que le traitement n'a pas aidés abandonnent l'étude et ne sont pas analysés |
| [[biais de mesure\|Mesure]] | goniomètre mal placé ; évaluateur qui sait quel patient a reçu le traitement |
| Mémoire | « Combien de fois êtes-vous tombé l'an dernier ? » : on oublie |
| [[biais de désirabilité sociale\|Désirabilité sociale]] | sur-déclarer l'activité physique, sous-déclarer l'alcool |
| [[effet hawthorne\|Hawthorne]] | les participants font plus d'efforts parce qu'ils sont observés |
| Confusion | un facteur non mesuré explique le lien observé |
""")
    st.markdown("#### À toi : fiabilité et validité")
    st.caption("Chaque point est une mesure répétée ; le centre est la vraie valeur.")
    c1, c2 = st.columns([1, 2])
    with c1:
        biais = st.slider("Biais (erreur systématique)", 0.0, 2.0, 0.0, 0.1, key="rd_biais")
        bruit = st.slider("Dispersion (erreur aléatoire)", 0.05, 1.5, 0.3, 0.05, key="rd_bruit")
    rng = np.random.default_rng(3)
    pts = rng.normal(0, bruit, (25, 2)) + np.array([biais * 0.7, biais * 0.7])
    with c2:
        fig = go.Figure()
        for r in (2.5, 1.7, 0.9):
            fig.add_shape(type="circle", x0=-r, y0=-r, x1=r, y1=r, line_color="rgba(128,128,128,0.6)")
        fig.add_trace(go.Scatter(x=pts[:, 0], y=pts[:, 1], mode="markers", marker=dict(size=9, color="#4d5f92")))
        fig.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10), showlegend=False,
                          xaxis=dict(visible=False, range=[-3, 3]), yaxis=dict(visible=False, scaleanchor="x", range=[-3, 3]))
        ui.chart(fig, "recolte_donnees_0")
    fiable = "fiable" if bruit < 0.4 else "peu fiable"
    valide = "valide" if biais < 0.3 and bruit < 0.6 else "peu valide"
    st.markdown(f"Mesure **{fiable}** et **{valide}**.")
    ui.memo("La [[fiabilité]], c'est **viser toujours au même endroit** (points groupés). La [[validité]], c'est "
            "**viser au centre**. Une mesure peut être fiable mais fausse (balance qui ajoute toujours 2 kg). Une "
            "mesure non fiable ne peut pas être valide.")


def ch_ethique():
    ui.md(r"""
**Principes éthiques de la recherche** (Déclaration d'Helsinki) : consentement libre et éclairé, droit de se
retirer à tout moment sans conséquence, balance bénéfices/risques, avis d'un **comité d'éthique** avant de
commencer.

**Le [[rgpd|RGPD]]** : les données de santé sont des données **sensibles**. Il faut une base légale, informer les
participants, ne récolter que le **nécessaire** (minimisation), sécuriser le stockage, et définir une durée de
conservation.

- **Confidentialité** : les données ne sont accessibles qu'aux personnes autorisées.
- **[[pseudonymisation|Pseudonymisation]]** : on remplace le nom par un code (P01, P02…), la table de
  correspondance est gardée à part. C'est le cas le plus courant en recherche clinique.
- **[[anonymisation|Anonymisation]]** : plus aucun moyen de retrouver la personne, même en croisant les données.
  Plus difficile qu'il n'y paraît : âge + commune + profession suffisent parfois à identifier quelqu'un.
""")
    ui.warn("Remplacer le nom par un code, ce n'est **pas** anonymiser : c'est pseudonymiser. Les données restent "
            "soumises au RGPD.")
    ui.md(r"""
**La synthèse critique d'articles** (ton travail du cours) : pour chaque article, résume la question, la
population, la méthode de récolte, les résultats principaux, et surtout les **biais** et **limites**. Puis compare
les articles entre eux : se rejoignent-ils ? Pourquoi divergent-ils ?
""")


CHAPTERS = [
    ("Sources et types de données", ch_types),
    ("Méthodes de récolte", ch_methodes),
    ("Biais, fiabilité, validité", ch_biais),
    ("Éthique et RGPD", ch_ethique),
]


def _q_var(rng):
    v, good = rng.choice(VARIABLES)
    return (f"De quel type est la variable **{v}** ?", good, ["Nominale", "Ordinale", "Quantitative discrète",
            "Quantitative continue"], "")


BIAIS_EX = [
    ("On recrute les participants d'une étude sur la sédentarité parmi les membres d'un club de sport.", "Biais de sélection"),
    ("Les patients déclarent faire leurs exercices quotidiennement, alors que l'appli montre le contraire.", "Biais de désirabilité sociale"),
    ("Les ouvriers deviennent plus productifs dès qu'ils savent qu'on les observe.", "Effet Hawthorne"),
    ("L'évaluateur, qui sait quels patients ont reçu le traitement, les juge un peu plus favorablement.", "Biais de mesure"),
]


def _q_biais(rng):
    t, good = rng.choice(BIAIS_EX)
    return (f"Quel biais ? {t}", good, [g for _, g in BIAIS_EX] + ["Biais de mémoire"], "")


QUESTIONS = [
    gen_qcm(1, _q_var),
    qcm(1, "Des données issues de dossiers médicaux existants sont des données…", "secondaires",
        ["primaires", "qualitatives uniquement", "expérimentales"]),
    vf(1, "Remplacer le nom des participants par un code revient à anonymiser les données.", False,
       "C'est de la pseudonymisation : la correspondance existe encore."),
    qcm(1, "Quelle méthode permet le mieux de montrer une relation de cause à effet ?", "L'expérimentation contrôlée",
        ["Le focus group", "L'étude de cas", "L'analyse de documents"]),
    gen_qcm(2, _q_biais),
    qcm(2, "Une mesure qui donne toujours le même résultat, mais décalé de la vraie valeur, est…",
        "fiable mais non valide", ["valide mais non fiable", "fiable et valide", "ni fiable ni valide"]),
    multi(2, "Quelles sont des bonnes pratiques pour un questionnaire ?", ["Une seule idée par question",
          "Faire un pré-test", "Éviter les doubles négations"], ["Suggérer la réponse attendue", "Questions très longues"]),
    qcm(2, "Pour une variable ordinale (douleur faible/modérée/forte), on résume plutôt avec…", "la médiane",
        ["la moyenne", "l'écart type", "la variance"]),
    qcm(2, "Que dit le principe de minimisation du RGPD ?", "Ne récolter que les données nécessaires",
        ["Récolter le moins de participants possible", "Réduire la taille des fichiers", "Supprimer les données après 1 jour"]),
    qcm(3, "Dans un essai, 30 % des patients du groupe traité abandonnent parce qu'ils ne vont pas mieux ; on n'analyse "
        "que ceux qui restent. Quel biais ?", "Un biais d'attrition qui surestime l'effet du traitement",
        ["Un biais de mémoire", "Aucun biais", "Un biais qui sous-estime l'effet"]),
    qcm(3, "Pourquoi l'âge, la commune et la profession peuvent-ils suffire à réidentifier un participant ?",
        "Leur combinaison peut être unique dans une petite population", ["Parce qu'ils sont nominatifs",
        "Parce qu'ils sont toujours publics", "Ce n'est pas possible"]),
    qcm(3, "Tu veux comprendre pourquoi des patients arrêtent leur programme d'exercices. Quelle méthode choisir ?",
        "Des entretiens semi-directifs ou un focus group", ["Un essai contrôlé randomisé", "Un goniomètre",
        "Une analyse de la prévalence"]),
    qcm(3, "Comment limiter le biais de mesure dans un essai clinique ?", "Utiliser un évaluateur qui ne sait pas dans quel groupe est le patient (aveugle)",
        ["Augmenter le nombre de mesures", "Choisir des patients motivés", "Ne mesurer qu'une fois"]),
]

CARDS = [
    ("Donnée primaire / secondaire", "Récoltée pour l'étude / déjà existante"),
    ("Variable nominale", "Catégories sans ordre"),
    ("Variable ordinale", "Catégories ordonnées (Likert, MRC)"),
    ("Fiabilité", "Même résultat quand on répète"),
    ("Validité", "Mesure bien ce qu'elle prétend mesurer"),
    ("Biais", "Erreur systématique"),
    ("Effet Hawthorne", "Changer parce qu'on est observé"),
    ("Désirabilité sociale", "Répondre ce qui est bien vu"),
    ("Pseudonymisation", "Code + table de correspondance séparée"),
    ("Anonymisation", "Réidentification impossible, irréversible"),
    ("RGPD et données de santé", "Données sensibles : base légale, minimisation, sécurité"),
    ("Focus group", "Entretien de groupe de 6 à 10 personnes"),
]

VIDEOS = [
    ("Fiabilité et validité d'une mesure", "fiabilité validité mesure explication cible"),
    ("Les biais en recherche clinique", "biais recherche clinique sélection mesure confusion"),
    ("Construire un bon questionnaire", "construire un questionnaire de recherche conseils"),
    ("RGPD et recherche en santé", "RGPD recherche santé pseudonymisation anonymisation"),
]

LINKS = [("Déclaration d'Helsinki (Association médicale mondiale)", "https://www.wma.net/fr/policies-post/declaration-dhelsinki-de-lamm-principes-ethiques-applicables-a-la-recherche-medicale-impliquant-des-etres-humains/")]
