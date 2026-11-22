"""LTECO1004 Sociétés, cultures, religions : questions éthiques."""

import streamlit as st

from app import ui
from app.course import Course
from app.quiz import gen_qcm, multi, qcm, vf

COURSE = Course(
    code="LTECO1004", title="Sociétés, cultures, religions : questions éthiques", short="Questions éthiques",
    bloc=1, quad=1, credits=2, hours="15 h", icon=":material/diversity_3:",
    intro="Le cours de sciences religieuses conseillé aux étudiants en kiné. Deux volets : la délibération éthique "
          "face aux conflits de valeurs en clinique, et la place du corps, de la maladie et de la spiritualité "
          "dans le soin. Il prolonge le cours de philosophie et éthique.",
    acquis=[
        "Connaître les catégories fondamentales de la réflexion éthique : liberté, dignité, responsabilité, justice.",
        "Construire une argumentation éthique qui tient compte de la complexité des situations.",
        "Exercer son esprit critique et se positionner personnellement.",
    ],
)

TERMS = {
    "dignité": ("Dignité", "Valeur inconditionnelle de toute personne humaine, qui ne dépend ni de son état de "
                "santé, ni de ses capacités, ni de son utilité.", "Dignité humaine"),
    "liberté": ("Liberté", "Capacité de la personne à faire ses propres choix ; en santé, elle se traduit par "
                "l'autonomie et le consentement.", "Liberté"),
    "responsabilité": ("Responsabilité", "Le fait de répondre de ses actes et de leurs conséquences, et de "
                       "prendre soin de ceux qui dépendent de nous (Hans Jonas, Emmanuel Levinas).",
                       "Responsabilité morale"),
    "délibération éthique": ("Délibération éthique", "Démarche collective et argumentée pour décider dans une "
                             "situation où des valeurs entrent en conflit.", None),
    "spiritualité": ("Spiritualité", "Façon dont une personne cherche et exprime le sens de sa vie, ses valeurs "
                     "et son lien à ce qui la dépasse, religieuse ou non.", "Spiritualité"),
    "maladie vécue": ("Maladie vécue (illness)", "La maladie telle que la personne l'éprouve et lui donne sens, "
                      "distincte de la maladie comme diagnostic biologique (disease).", None),
    "laïcité": ("Neutralité", "En Belgique, l'État reconnaît plusieurs cultes et la laïcité organisée ; dans les "
                "soins, le soignant respecte les convictions du patient sans imposer les siennes.", "Laïcité"),
}


def ch_categories():
    ui.md(r"""
Quatre catégories reviennent dans toute réflexion éthique :

- **[[liberté|Liberté]]** : le patient choisit pour lui-même. Elle suppose qu'il soit informé et capable de décider.
- **[[dignité|Dignité]]** : toute personne a une valeur, même dépendante, désorientée, en fin de vie. On ne la
  « perd » pas ; c'est le regard ou le traitement qu'on lui porte qui peut la respecter ou non.
- **[[responsabilité|Responsabilité]]** : je réponds de mes actes, et j'ai une responsabilité particulière envers
  celui qui est vulnérable. Pour **Levinas**, le visage de l'autre m'oblige ; pour **Hans Jonas**, la
  responsabilité s'étend aux générations futures.
- **[[justice|Justice]]** : répartir équitablement des ressources limitées (temps de soin, lits, remboursements).

Ces valeurs entrent régulièrement en **conflit** : respecter la liberté d'un patient peut aller contre ce qu'on
pense être son bien ; soigner longuement un patient peut retirer du temps aux autres.
""")
    ui.memo("**LDRJ** : Liberté, Dignité, Responsabilité, Justice. Elles recoupent les principes de Beauchamp et "
            "Childress vus en philosophie (autonomie ≈ liberté, justice = justice).")


def ch_deliberation():
    ui.md(r"""
**La [[délibération éthique]] en clinique** n'est pas l'application d'une règle : c'est une démarche **collective**
(équipe, patient, proches) pour trouver la **meilleure décision possible** quand il n'y a pas de bonne réponse
évidente.

**Une méthode en étapes**
1. **Les faits** : situation médicale, souhaits du patient, contexte familial et social.
2. **Les questions** : où est le conflit de valeurs ? Qui est concerné ?
3. **Les options** : en chercher plus de deux, y compris les compromis.
4. **Les arguments** pour et contre chaque option, en s'appuyant sur les catégories (liberté, dignité…).
5. **La décision**, justifiée, et ce qu'on accepte de perdre.
6. **Le suivi** : revoir la décision si la situation change.
""")
    st.markdown("#### À toi : repère le conflit de valeurs")
    case = st.selectbox("Situation", [
        "Un patient atteint de sclérose en plaques veut continuer à marcher sans aide malgré plusieurs chutes.",
        "Une famille demande de ne pas dire à sa mère âgée que sa maladie est grave.",
        "Le service n'a le temps de faire de la kiné respiratoire qu'à 3 des 5 patients qui en auraient besoin.",
    ], key="qe_case")
    analyses = {
        "Un patient atteint": "**Liberté** (choisir sa façon de vivre et de risquer) contre **responsabilité** du soignant "
                              "face au risque de chute. Pistes : informer clairement, chercher avec lui des adaptations "
                              "acceptables (aide discrète, aménagement du domicile, travail de l'équilibre).",
        "Une famille": "**Liberté** de la patiente (droit d'être informée, loi belge sur les droits du patient) contre "
                       "le désir de **protection** de la famille. Pistes : demander à la patiente ce qu'elle veut savoir, "
                       "à son rythme ; le droit de ne pas savoir existe aussi.",
        "Le service": "Question de **justice** : sur quels critères prioriser (urgence, bénéfice attendu, ordre "
                      "d'arrivée) ? La décision doit être transparente et discutée en équipe, et le manque de moyens "
                      "signalé.",
    }
    st.info(next(v for k, v in analyses.items() if case.startswith(k)))


def ch_corps():
    ui.md(r"""
**Corps, santé, guérison : des représentations variées.** Selon les cultures et les religions, la maladie peut
être vue comme un dérèglement biologique, un déséquilibre (entre le chaud et le froid, les humeurs, les énergies),
une épreuve, une conséquence d'une faute, ou une affaire de relations. Ces représentations influencent ce que le
patient attend du soin, ce qu'il accepte (toucher, nudité, soignant du même sexe) et la façon dont il exprime sa
douleur.

**La [[maladie vécue]]** : les anglophones distinguent *disease* (la maladie que le médecin diagnostique) et
*illness* (la maladie que la personne éprouve, avec son récit). Deux patients avec la même lésion ne vivent pas la
même maladie. En tenir compte, c'est intégrer le récit du patient dans le projet de soin.

**La dimension existentielle et spirituelle** : une maladie grave, un handicap brutal posent des questions de
**sens** (pourquoi moi ? que vaut ma vie maintenant ?). La [[spiritualité]], religieuse ou non, peut être une
ressource. Le soignant n'a pas à y répondre à la place du patient, mais à **l'accueillir**, et à orienter si
besoin (aumônerie, conseiller laïque, psychologue).
""")
    ui.clinic("Respecter une demande liée aux convictions (horaire de séance pendant le ramadan, soignant du même "
              "sexe, pudeur) fait partie du soin, tant qu'elle ne met pas le patient en danger. Le soignant, lui, "
              "garde une attitude de [[laïcité|neutralité]] : il n'impose pas ses propres convictions.")


CHAPTERS = [
    ("Les catégories de l'éthique", ch_categories),
    ("La délibération éthique en clinique", ch_deliberation),
    ("Corps, maladie et spiritualité", ch_corps),
]

CAS = [
    ("Une patiente refuse une transfusion pour des raisons religieuses.", "Liberté"),
    ("Une personne âgée démente est laissée sans toilette dans le couloir.", "Dignité"),
    ("On décide qui reçoit les dernières places en revalidation.", "Justice"),
    ("Un kiné s'engage à prévenir l'équipe d'un risque de chute qu'il a repéré.", "Responsabilité"),
]


def _q_cat(rng):
    c, good = rng.choice(CAS)
    return (f"Quelle catégorie éthique est principalement en jeu ? {c}", good,
            ["Liberté", "Dignité", "Justice", "Responsabilité"], "")


QUESTIONS = [
    gen_qcm(1, _q_cat),
    multi(1, "Quelles sont les quatre catégories fondamentales de la réflexion éthique vues au cours ?",
          ["Liberté", "Dignité", "Responsabilité", "Justice"], ["Rentabilité", "Obéissance"]),
    vf(1, "La délibération éthique consiste à appliquer mécaniquement une règle.", False,
       "C'est une démarche argumentée, souvent collective, quand les règles ne suffisent pas."),
    vf(1, "La spiritualité peut être non religieuse.", True),
    qcm(1, "Que désigne « illness » par rapport à « disease » ?", "La maladie telle que la personne la vit",
        ["Le diagnostic biologique", "Une maladie infectieuse", "Une maladie mentale"]),
    qcm(2, "Pour Levinas, qu'est-ce qui fonde la responsabilité envers l'autre ?", "Le visage de l'autre, qui m'oblige",
        ["Le contrat signé", "La loi", "L'intérêt personnel"]),
    qcm(2, "Hans Jonas élargit la responsabilité…", "aux générations futures", ["aux seuls soignants",
        "aux animaux uniquement", "à l'État"]),
    qcm(2, "Quelle est la première étape d'une délibération éthique ?", "Rassembler les faits de la situation",
        ["Décider", "Voter en équipe", "Consulter un texte religieux"]),
    vf(2, "Selon la loi belge, un patient a aussi le droit de ne pas savoir.", True,
       "Le droit à l'information comprend le droit de ne pas être informé s'il le demande."),
    qcm(2, "Quelle attitude un soignant doit-il avoir face aux convictions religieuses du patient ?",
        "Les respecter et les accueillir sans imposer les siennes", ["Les ignorer", "Les corriger",
        "Refuser de soigner si elles diffèrent des siennes"]),
    qcm(3, "Une famille demande de cacher un diagnostic grave à leur mère lucide. Quel conflit de valeurs ?",
        "La liberté (droit à l'information) de la patiente contre le désir de protection de la famille",
        ["La justice contre la dignité", "La responsabilité du soignant contre la loi", "Aucun : la famille décide"]),
    qcm(3, "Le temps de kiné est insuffisant pour tous les patients du service. Quelle approche est la plus juste ?",
        "Définir des critères de priorité transparents en équipe et signaler le manque de moyens",
        ["Soigner ceux qu'on préfère", "Soigner ceux qui se plaignent le plus", "Tirer au sort sans en parler"]),
    qcm(3, "Pourquoi intégrer le récit du patient dans le projet de soin ?",
        "Parce que deux patients avec la même lésion ne vivent pas la même maladie, ni les mêmes objectifs",
        ["Parce que le diagnostic n'a aucune importance", "Pour gagner du temps", "Parce que la loi l'impose mot à mot"]),
    multi(3, "Quelles demandes liées aux convictions peut-on en général respecter ?",
          ["Adapter l'horaire de séance", "Respecter la pudeur", "Proposer un soignant du même sexe si possible"],
          ["Arrêter un soin vital sans information ni discussion"]),
]

CARDS = [
    ("4 catégories éthiques", "Liberté, dignité, responsabilité, justice"),
    ("Dignité", "Valeur inconditionnelle de toute personne"),
    ("Levinas", "Le visage de l'autre m'oblige"),
    ("Hans Jonas", "Responsabilité envers les générations futures"),
    ("Disease vs illness", "Maladie diagnostiquée vs maladie vécue"),
    ("Délibération éthique", "Faits, questions, options, arguments, décision, suivi"),
    ("Spiritualité", "Recherche de sens, religieuse ou non"),
]

VIDEOS = [
    ("La délibération éthique en soins de santé", "délibération éthique soins de santé méthode"),
    ("Spiritualité et soins", "spiritualité et soins de santé accompagnement"),
]

LINKS = [("Comité consultatif de bioéthique de Belgique", "https://www.health.belgium.be/fr/comite-consultatif-de-bioethique")]
