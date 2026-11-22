"""LFSM1107 Psychologie générale."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from app import ui
from app.course import Course
from app.quiz import gen_qcm, multi, qcm, table_qcm, vf

COURSE = Course(
    code="LFSM1107", title="Psychologie générale", short="Psychologie",
    bloc=1, quad=1, credits=3, hours="30 h", icon=":material/psychology:",
    intro="Un patient qui ne fait pas ses exercices, qui a peur de bouger, qui apprend un nouveau geste : la "
          "psychologie est partout en kiné. Ce cours donne les grandes théories de la perception, de la mémoire, "
          "de l'apprentissage, de la motivation et de la santé.",
    acquis=[
        "Décrire les concepts et théories de base de la psychologie.",
        "Définir les concepts de l'apprentissage et de la motivation.",
        "Identifier ces concepts dans des cas concrets.",
    ],
)

TERMS = {
    "attention sélective": ("Attention sélective", "Capacité à se concentrer sur une information en ignorant les "
                            "autres (effet cocktail party).", "Attention"),
    "mémoire de travail": ("Mémoire de travail", "Mémoire à court terme active, de capacité limitée (environ 4 à 7 "
                           "éléments), qui maintient et manipule l'information pendant quelques secondes.",
                           "Mémoire de travail"),
    "mémoire procédurale": ("Mémoire procédurale", "Mémoire des savoir-faire (faire du vélo, un geste technique), "
                            "implicite et durable.", "Mémoire procédurale"),
    "mémoire déclarative": ("Mémoire déclarative", "Mémoire des faits (sémantique) et des événements vécus "
                            "(épisodique), qu'on peut verbaliser.", "Mémoire déclarative"),
    "conditionnement classique": ("Conditionnement classique", "Apprentissage par association (Pavlov) : un "
                                  "stimulus neutre finit par déclencher la réponse d'un autre stimulus auquel il "
                                  "a été associé.", "Conditionnement classique"),
    "conditionnement opérant": ("Conditionnement opérant", "Apprentissage par les conséquences (Skinner) : un "
                                "comportement suivi d'une conséquence agréable augmente, d'une conséquence "
                                "désagréable diminue.", "Conditionnement opérant"),
    "renforcement": ("Renforcement", "Conséquence qui augmente la fréquence d'un comportement. Positif : on "
                     "ajoute quelque chose d'agréable ; négatif : on retire quelque chose de désagréable.",
                     "Renforcement"),
    "apprentissage vicariant": ("Apprentissage vicariant", "Apprentissage par l'observation d'un modèle "
                                "(Bandura).", "Apprentissage social"),
    "sentiment d'efficacité personnelle": ("Sentiment d'efficacité personnelle", "Croyance d'une personne en sa "
                                           "capacité à réussir une tâche (Bandura). Prédit fortement l'adhésion "
                                           "à un programme d'exercices.", "Auto-efficacité"),
    "motivation intrinsèque": ("Motivation intrinsèque", "Faire une activité pour le plaisir ou l'intérêt qu'elle "
                               "procure en elle-même.", "Motivation intrinsèque et extrinsèque"),
    "autodétermination": ("Théorie de l'autodétermination", "Théorie de Deci et Ryan : la motivation de qualité "
                          "naît de trois besoins, autonomie, compétence et lien social.",
                          "Théorie de l'autodétermination"),
    "stress": ("Stress", "Réaction de l'organisme face à une situation perçue comme menaçante ou dépassant ses "
               "ressources.", "Stress (biologie)"),
    "coping": ("Coping", "Stratégies d'ajustement pour faire face au stress : centrées sur le problème ou sur "
               "l'émotion.", "Coping"),
    "kinésiophobie": ("Kinésiophobie", "Peur excessive du mouvement, par crainte de se blesser ou d'avoir mal. "
                      "Elle entretient la douleur chronique.", "Kinésiophobie"),
}

OPERANT = [
    ("Le patient reçoit des félicitations après avoir fait ses exercices, et il les refait.", "Renforcement positif"),
    ("Faire ses étirements fait disparaître la raideur matinale, alors il continue.", "Renforcement négatif"),
    ("Un enfant reçoit une remarque sévère quand il triche à l'exercice, et il arrête.", "Punition positive"),
    ("Un sportif perd son temps de jeu quand il saute l'échauffement, et il ne le saute plus.", "Punition négative"),
    ("Une patiente évite de se pencher et sa peur de la douleur disparaît sur le moment : elle évite de plus en plus.",
     "Renforcement négatif"),
    ("Un joueur reçoit un badge sur son appli après 10 jours de marche, et marche davantage.", "Renforcement positif"),
]
STADES = {
    "Précontemplation": "« Je n'ai pas de problème, je ne vois pas pourquoi je ferais du sport. »",
    "Contemplation": "« Je sais que je devrais bouger plus, mais pas maintenant. »",
    "Préparation": "« Je me suis inscrite à la salle, je commence lundi. »",
    "Action": "« Je marche 30 minutes par jour depuis 2 mois. »",
    "Maintien": "« Je cours trois fois par semaine depuis plus d'un an. »",
}


def ch_methodes():
    ui.md(r"""
La psychologie est l'étude **scientifique** du comportement et des processus mentaux. Elle utilise :
- l'**observation** (en milieu naturel ou en laboratoire) ;
- les **questionnaires** et entretiens (attention à la désirabilité sociale) ;
- les **études corrélationnelles** (liens entre variables, sans causalité) ;
- les **expériences** (on manipule une variable, avec un groupe contrôle et l'assignation au hasard) : seule
  méthode qui montre une causalité ;
- les **études de cas** (riches mais peu généralisables).
""")
    ui.tip("Le grand piège : prendre son intuition (« je connais les gens ») pour une connaissance. La psychologie "
           "scientifique montre souvent que le bon sens se trompe.")


def ch_perception():
    ui.md(r"""
**Sensation et perception** : la sensation est la détection d'un stimulus par un récepteur ; la **perception** est
son interprétation par le cerveau, influencée par nos attentes et notre expérience. On ne voit pas le monde tel
qu'il est, mais tel que le cerveau le **reconstruit** (illusions d'optique, douleur modulée par le contexte).

**Attention** : ressource **limitée**. L'[[attention sélective]] filtre ; l'attention **partagée** (double tâche)
fait baisser les performances. La **cécité attentionnelle** : on ne voit pas un gorille qui traverse la scène si
l'on compte des passes de ballon (Simons et Chabris, 1999).

**Mémoire** (modèle d'Atkinson et Shiffrin, puis Baddeley) :
1. **Mémoire sensorielle** : quelques centaines de millisecondes.
2. [[mémoire de travail|Mémoire de travail]] : quelques secondes, environ 4 à 7 éléments.
3. **Mémoire à long terme** : [[mémoire déclarative|déclarative]] (faits, événements) et
   [[mémoire procédurale|procédurale]] (gestes).

**Décision et résolution de problèmes** : on utilise des **heuristiques** (raccourcis) qui produisent des biais
(voir le cours d'esprit critique).
""")
    ui.clinic("Un patient âgé qui marche en parlant ralentit, voire s'arrête : la **double tâche** révèle un risque de "
              "chute. Les tests « marche + compter à rebours » s'en servent. Et pour qu'un patient retienne ses "
              "exercices : **peu** de consignes à la fois, écrites, montrées, et répétées.")


def ch_apprentissage():
    ui.md(r"""
**[[conditionnement classique|Conditionnement classique]] (Pavlov)** : on associe un stimulus neutre (la cloche) à
un stimulus qui déclenche naturellement une réponse (la nourriture → salivation). Après quelques associations, la
cloche seule fait saliver.

**[[conditionnement opérant|Conditionnement opérant]] (Skinner)** : un comportement dépend de ses **conséquences**.

| | On **ajoute** quelque chose | On **retire** quelque chose |
|---|---|---|
| Le comportement **augmente** | [[renforcement\|Renforcement]] positif (récompense) | Renforcement négatif (soulagement) |
| Le comportement **diminue** | Punition positive | Punition négative (privation) |
""")
    ui.warn("« Négatif » ne veut pas dire « mauvais » : il veut dire **retirer**. Le renforcement négatif fait "
            "**augmenter** un comportement en supprimant quelque chose de désagréable (l'antidouleur qui fait "
            "disparaître la douleur renforce le fait d'en prendre).")
    st.markdown("#### À toi : classe la situation")
    i = st.session_state.setdefault("ps_op_i", 0) % len(OPERANT)
    sit, good = OPERANT[i]
    st.markdown(f"> {sit}")
    rep = st.radio("C'est…", ["Renforcement positif", "Renforcement négatif", "Punition positive", "Punition négative"],
                   index=None, key=f"ps_op_{i}", horizontal=True)
    if rep:
        (st.success if rep == good else st.error)(f"Réponse : **{good}**")
    if st.button("Situation suivante", key="ps_op_next"):
        st.session_state["ps_op_i"] = i + 1
        st.rerun()
    ui.md(r"""
**[[apprentissage vicariant|Apprentissage vicariant]] (Bandura)** : on apprend en **observant** un modèle, surtout
s'il nous ressemble et qu'il réussit. Bandura introduit aussi le
[[sentiment d'efficacité personnelle]] : croire qu'on en est capable. Il se nourrit de quatre sources : les
**réussites** personnelles (la plus forte), l'observation de modèles, la persuasion verbale et l'état physiologique.
""")
    ui.clinic("L'**évitement** dans la douleur chronique est un renforcement négatif : éviter de se pencher supprime "
              "la peur sur le moment, donc on évite de plus en plus, on se déconditionne, et la douleur s'installe. "
              "C'est le cercle de la [[kinésiophobie]]. On le casse par une **exposition graduée**.")


def ch_motivation():
    ui.md(r"""
**Pyramide de Maslow** : besoins physiologiques, sécurité, appartenance, estime, accomplissement. Célèbre mais
peu soutenue par les données (on n'attend pas d'avoir satisfait un niveau pour chercher le suivant).

**[[autodétermination|Théorie de l'autodétermination]] (Deci et Ryan)** : la motivation va de l'amotivation à la
[[motivation intrinsèque]], en passant par plusieurs formes de motivation extrinsèque (contrainte, culpabilité,
valeur personnelle). Elle est d'autant plus durable que trois **besoins** sont nourris :
- **autonomie** (je choisis),
- **compétence** (je me sens capable, je progresse),
- **lien social** (je ne suis pas seul).

**Loi de Yerkes-Dodson** : la performance augmente avec l'activation (l'éveil, le stress) jusqu'à un optimum,
puis diminue. L'optimum est plus bas pour les tâches complexes.
""")
    st.markdown("#### À toi : la courbe de Yerkes-Dodson")
    c1, c2 = st.columns([1, 2])
    with c1:
        act = st.slider("Niveau d'activation (stress)", 0.0, 10.0, 5.0, 0.5, key="ps_act")
        cx = st.radio("Tâche", ["Simple (sprint)", "Complexe (geste fin, examen)"], key="ps_task")
    opt = 6.5 if cx.startswith("Simple") else 4.0
    x = np.linspace(0, 10, 200)
    y = np.exp(-((x - opt) / 2.6) ** 2)
    with c2:
        fig = go.Figure(go.Scatter(x=x, y=y, mode="lines"))
        fig.add_trace(go.Scatter(x=[act], y=[np.exp(-((act - opt) / 2.6) ** 2)], mode="markers", marker=dict(size=13)))
        fig.update_layout(height=260, margin=dict(l=10, r=10, t=10, b=10), showlegend=False,
                          xaxis_title="Activation", yaxis_title="Performance",
                          xaxis_range=[0, 10], yaxis_range=[0, 1.1])
        ui.chart(fig, "psychologie_0")


def ch_sante():
    ui.md(r"""
La **psychologie de la santé** cherche à comprendre pourquoi on adopte (ou pas) des comportements de santé.

**Modèle des croyances relatives à la santé** : j'agis si je me sens **vulnérable**, si le problème me paraît
**grave**, si les **bénéfices** de l'action dépassent les **obstacles**, et s'il y a un déclencheur.

**Théorie du comportement planifié (Ajzen)** : l'**intention** d'agir dépend de mon **attitude**, des **normes
sociales** perçues et du **contrôle** que je pense avoir. Mais l'intention ne suffit pas : il y a un fossé entre
intention et action.

**Modèle transthéorique (Prochaska et DiClemente)** : on change par **stades**, avec des rechutes possibles.
""")
    ui.table([[k, v] for k, v in STADES.items()], headers=["Stade", "Ce que dit la personne"])
    ui.md(r"""
**Le [[stress]]** : pour Selye, une réaction en trois phases (alarme, résistance, épuisement). Pour **Lazarus**,
le stress dépend de l'**évaluation** : la situation est-elle menaçante (évaluation primaire) et ai-je les
ressources pour y faire face (évaluation secondaire) ? Puis on met en place un [[coping]], centré sur le
**problème** (agir) ou sur l'**émotion** (se calmer, prendre de la distance).

**Déterminants sociaux** : le comportement dépend aussi du groupe (conformisme : expériences d'**Asch**),
de l'autorité (expériences de **Milgram**), du statut social et des inégalités.

**Psychologie et activité physique** : l'exercice réduit les symptômes dépressifs et anxieux, améliore le
sommeil et certaines fonctions cognitives. C'est une piste de soin à part entière.
""")
    ui.tip("Ne propose pas un programme d'action à quelqu'un en **précontemplation** : il faut d'abord l'aider à "
           "voir l'intérêt du changement (entretien motivationnel). Adapter l'intervention au stade, c'est la clé.")
    ui.md(r"""
**Les troubles psychiques** sont abordés en détail dans le cours de psychiatrie (bloc 2). Retiens qu'ils sont
fréquents (environ une personne sur quatre au cours de sa vie) et que l'**évaluation scientifique** des
interventions psychologiques (thérapies cognitivo-comportementales notamment) a montré leur efficacité.
""")


CHAPTERS = [
    ("Méthodes de la psychologie", ch_methodes),
    ("Perception, attention, mémoire", ch_perception),
    ("Apprentissage", ch_apprentissage),
    ("Motivation", ch_motivation),
    ("Santé, stress et comportements", ch_sante),
]


def _q_operant(rng):
    s, good = rng.choice(OPERANT)
    return (f"{s} Il s'agit de…", good, ["Renforcement positif", "Renforcement négatif", "Punition positive",
                                         "Punition négative"], "Positif = on ajoute ; négatif = on retire.")


QUESTIONS = [
    qcm(1, "Qui a décrit le conditionnement classique ?", "Pavlov", ["Skinner", "Bandura", "Maslow"]),
    qcm(1, "Quelle méthode permet d'établir une relation de cause à effet ?", "L'expérience contrôlée",
        ["L'étude corrélationnelle", "L'étude de cas", "Le questionnaire"]),
    qcm(1, "La mémoire de travail peut contenir environ…", "4 à 7 éléments", ["1 élément", "20 à 30 éléments", "une quantité illimitée"]),
    vf(1, "Le renforcement négatif fait diminuer un comportement.", False,
       "Il le fait augmenter, en retirant quelque chose de désagréable."),
    qcm(1, "Faire du vélo relève de la mémoire…", "procédurale", ["épisodique", "sémantique", "sensorielle"]),
    gen_qcm(2, _q_operant),
    table_qcm(2, STADES, "Quelle phrase correspond au stade **{k}** du modèle transthéorique ?",
              "Selon le modèle transthéorique, à quel stade est cette personne : {v}"),
    multi(2, "Quels sont les trois besoins de la théorie de l'autodétermination ?",
          ["Autonomie", "Compétence", "Lien social"], ["Sécurité", "Estime de soi", "Argent"]),
    qcm(2, "Quelle est la source la plus puissante du sentiment d'efficacité personnelle selon Bandura ?",
        "Les réussites vécues par la personne elle-même", ["La persuasion verbale", "L'observation de modèles",
        "L'état physiologique"]),
    qcm(2, "Selon Lazarus, le stress dépend surtout…", "de l'évaluation que la personne fait de la situation et de ses ressources",
        ["de l'intensité objective du stimulus", "uniquement des hormones", "de la personnalité seule"]),
    vf(2, "Selon la loi de Yerkes-Dodson, plus on est stressé, meilleure est la performance.", False,
       "La relation est en U inversé : il y a un optimum."),
    qcm(3, "Un patient lombalgique évite de se pencher depuis des mois ; sa peur diminue à chaque évitement. Quel "
        "mécanisme entretient son comportement ?", "Un renforcement négatif de l'évitement",
        ["Un renforcement positif", "Une punition négative", "Un conditionnement classique de la douleur"],
        "L'évitement retire la peur (désagréable) : il augmente. D'où l'exposition graduée."),
    qcm(3, "Un patient dit : « Je sais que je devrais faire mes exercices, mais pas cette semaine. » Quelle approche "
        "est la plus adaptée ?", "Explorer avec lui les avantages et inconvénients du changement (entretien motivationnel)",
        ["Lui donner tout de suite un programme détaillé", "Le menacer d'arrêter la prise en charge",
         "Considérer qu'il est en phase de maintien"], "Il est en contemplation."),
    qcm(3, "Pour qu'une personne âgée retienne son programme d'exercices, quelle stratégie est la meilleure ?",
        "Peu de consignes à la fois, démontrées, écrites et répétées",
        ["Tout expliquer oralement en une fois", "Lui donner un livre sur le sujet", "Ne rien écrire pour qu'elle mémorise mieux"],
        "La mémoire de travail est limitée ; on multiplie les canaux et les répétitions."),
    qcm(3, "Pourquoi un test de marche en double tâche est-il utile chez la personne âgée ?",
        "Il révèle des difficultés attentionnelles qui augmentent le risque de chute",
        ["Il mesure la force du quadriceps", "Il remplace l'examen neurologique", "Il évalue la mémoire procédurale seule"]),
]

CARDS = [
    ("Conditionnement classique", "Association de stimuli (Pavlov)"),
    ("Conditionnement opérant", "Apprentissage par les conséquences (Skinner)"),
    ("Renforcement négatif", "Retirer un désagrément → le comportement augmente"),
    ("Punition négative", "Retirer un agrément → le comportement diminue"),
    ("Apprentissage vicariant", "Apprendre en observant un modèle (Bandura)"),
    ("Sentiment d'efficacité personnelle", "Croire en sa capacité à réussir (Bandura)"),
    ("3 besoins de l'autodétermination", "Autonomie, compétence, lien social"),
    ("Stades du modèle transthéorique", "Précontemplation, contemplation, préparation, action, maintien"),
    ("Yerkes-Dodson", "Performance en U inversé selon l'activation"),
    ("Lazarus", "Stress = évaluation de la menace et des ressources ; coping"),
    ("Mémoire procédurale", "Savoir-faire, implicite (vélo, gestes)"),
    ("Kinésiophobie", "Peur du mouvement qui entretient la douleur"),
]

VIDEOS = [
    ("Conditionnement opérant : renforcement et punition", "conditionnement opérant renforcement négatif punition explication"),
    ("Théorie de l'autodétermination", "théorie de l'autodétermination Deci Ryan motivation"),
    ("Le test du gorille invisible (attention sélective)", "gorille invisible Simons Chabris"),
    ("Modèle transthéorique du changement", "modèle transthéorique Prochaska stades du changement"),
]

LINKS = [("Physiopedia : Fear avoidance model", "https://www.physio-pedia.com/Fear_Avoidance_Model")]
