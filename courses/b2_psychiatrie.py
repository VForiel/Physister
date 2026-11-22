"""LKNR1209 Psychiatrie."""

import streamlit as st

from app import ui
from app.course import Course
from app.quiz import gen_qcm, multi, qcm, vf

COURSE = Course(
    code="LKNR1209", title="Psychiatrie", short="Psychiatrie",
    bloc=2, quad=1, credits=2, hours="22,5 h", icon=":material/self_improvement:",
    intro="Beaucoup de patients de kiné ont aussi une souffrance psychique, et certains troubles (dépression, "
          "anxiété, troubles alimentaires) changent la façon de les prendre en charge. Le kiné n'est pas "
          "psychiatre, mais il doit savoir repérer, communiquer et orienter.",
    acquis=[
        "Décrire les caractéristiques cliniques des souffrances psychologiques et des affections psychiatriques.",
        "Repérer les stéréotypes et les biais dans le raisonnement clinique.",
        "Connaître les principes du projet thérapeutique et le rôle du psychiatre.",
        "Savoir quand orienter vers des soins spécialisés.",
    ],
)

TERMS = {
    "examen mental": ("Examen de l'état mental", "Description structurée de la présentation, du comportement, de "
                      "l'humeur, de la pensée, des perceptions, de la cognition et du jugement d'un patient.",
                      "Examen de l'état mental"),
    "dsm-5": ("DSM-5", "Manuel diagnostique et statistique des troubles mentaux (Association américaine de "
              "psychiatrie). La CIM-11 de l'OMS est l'autre classification de référence.",
              "Manuel diagnostique et statistique des troubles mentaux"),
    "anhédonie": ("Anhédonie", "Perte de la capacité à éprouver du plaisir.", "Anhédonie"),
    "épisode dépressif caractérisé": ("Épisode dépressif caractérisé", "Au moins 5 symptômes sur 9 pendant au moins "
                                      "2 semaines, dont l'humeur triste ou l'anhédonie, avec retentissement.",
                                      "Trouble dépressif majeur"),
    "trouble bipolaire": ("Trouble bipolaire", "Alternance d'épisodes dépressifs et d'épisodes maniaques ou "
                          "hypomaniaques (humeur exaltée, moins de sommeil, idées rapides).", "Trouble bipolaire"),
    "attaque de panique": ("Attaque de panique", "Crise brutale de peur intense avec palpitations, souffle court, "
                           "vertiges, peur de mourir ; culmine en quelques minutes.", "Attaque de panique"),
    "psychose": ("Psychose", "Perte de contact avec la réalité : délires (idées fausses inébranlables) et "
                 "hallucinations.", "Psychose"),
    "symptômes négatifs": ("Symptômes négatifs", "Dans la schizophrénie : apathie, retrait social, pauvreté du "
                           "discours et des émotions.", None),
    "anorexie mentale": ("Anorexie mentale", "Restriction alimentaire, peur intense de grossir, perception "
                         "déformée du corps, poids anormalement bas.", "Anorexie mentale"),
    "somatisation": ("Symptômes somatiques", "Symptômes physiques (douleur, fatigue) avec une détresse et des "
                     "préoccupations excessives à leur sujet.", "Trouble à symptomatologie somatique"),
    "stigmatisation": ("Stigmatisation", "Étiquetage négatif d'une personne à cause de son trouble, qui mène à la "
                       "discrimination et retarde les soins.", "Stigmatisation"),
}

VIGNETTES = [
    ("Depuis un mois, Léa, 34 ans, ne prend plus plaisir à rien, dort mal, a perdu l'appétit, se sent inutile et "
     "fatiguée en permanence.", "Trouble dépressif"),
    ("Marc, 22 ans, a des crises brutales de palpitations, d'étouffement et de peur de mourir, qui durent 10 minutes, "
     "et il évite maintenant les transports.", "Trouble panique"),
    ("Sophie, 17 ans, gymnaste, mange très peu, a un IMC de 16, et se trouve encore trop grosse.", "Anorexie mentale"),
    ("Thomas, 25 ans, entend des voix qui commentent ses actes, et pense que ses voisins l'espionnent par la télé.",
     "Trouble psychotique"),
    ("Depuis 6 mois, Anne s'inquiète de tout (travail, santé, enfants), a du mal à se détendre, est tendue et irritable.",
     "Anxiété généralisée"),
    ("Après un grave accident de voiture, Paul revit la scène en cauchemars et en flashs, et évite de conduire.",
     "Trouble de stress post-traumatique"),
]


def ch_demarche():
    ui.md(r"""
**Le psychiatre** est un médecin : il pose un diagnostic, prescrit des médicaments, coordonne les soins et peut
hospitaliser. Le **psychologue** n'est pas médecin : il évalue et fait des psychothérapies.

**La démarche diagnostique** : entretien, [[examen mental|examen de l'état mental]], anamnèse (antécédents,
contexte, substances), examens pour exclure une cause physique (thyroïde, médicaments, tumeur…), puis
**diagnostic différentiel**.

L'examen mental décrit : la **présentation** (tenue, contact), le **comportement** (agitation, ralentissement),
l'**humeur** et les affects, le **cours et le contenu de la pensée** (idées suicidaires, délires), les
**perceptions** (hallucinations), la **cognition** (orientation, mémoire, attention), le **jugement** et
l'**insight** (conscience du trouble).

**Normal ou pathologique ?** La tristesse, l'anxiété et le stress sont normaux. On parle de trouble quand
c'est **intense**, **durable**, et que ça entraîne une **souffrance** importante ou un **retentissement** sur la vie
(travail, relations). La santé mentale fait partie de la santé : « il n'y a pas de santé sans santé mentale » (OMS).
""")


def ch_troubles():
    ui.md(r"""
**L'approche catégorielle** classe les troubles selon des critères (le [[dsm-5|DSM-5]], la CIM-11).

**Troubles de l'humeur**
- **[[épisode dépressif caractérisé|Dépression]]** : au moins 5 symptômes sur 9 pendant au moins 2 semaines, dont
  **humeur triste** ou **[[anhédonie]]** : troubles du sommeil, de l'appétit, fatigue, ralentissement ou agitation,
  culpabilité, troubles de la concentration, idées de mort.
- **[[trouble bipolaire|Trouble bipolaire]]** : épisodes dépressifs et épisodes **maniaques** (exaltation, moins
  besoin de dormir, projets démesurés).

**Troubles anxieux** : anxiété généralisée (inquiétudes excessives sur tout, au moins 6 mois), trouble panique
([[attaque de panique|attaques de panique]] répétées et peur d'en refaire), phobies (spécifiques, sociale),
agoraphobie. Le **stress post-traumatique** (cauchemars, reviviscences, évitement, hypervigilance après un
traumatisme) est classé à part dans le DSM-5.

**Troubles psychotiques** : la **schizophrénie** associe des symptômes **positifs** (délires, hallucinations,
désorganisation) et des [[symptômes négatifs|symptômes **négatifs**]] (apathie, retrait).

**Troubles liés à l'usage de substances** : alcool, cannabis, opioïdes… avec perte de contrôle, envie
irrépressible (craving), tolérance et sevrage.

**Troubles des conduites alimentaires** : [[anorexie mentale|anorexie]], boulimie (crises puis vomissements ou
compensations), hyperphagie boulimique (crises sans compensation).
""")
    st.markdown("#### À toi : oriente le diagnostic")
    i = st.session_state.setdefault("psy_i", 0) % len(VIGNETTES)
    txt, good = VIGNETTES[i]
    st.markdown(f"> {txt}")
    rep = st.radio("Ce tableau évoque…", sorted({g for _, g in VIGNETTES}), index=None, key=f"psy_v_{i}")
    if rep:
        (st.success if rep == good else st.error)(f"Réponse : **{good}**")
    if st.button("Vignette suivante", key="psy_next"):
        st.session_state["psy_i"] = i + 1
        st.rerun()
    st.caption("Exercice de reconnaissance : en vrai, c'est le médecin qui pose le diagnostic, après un examen complet.")


def ch_dimension():
    ui.md(r"""
**L'approche dimensionnelle** : plutôt que « malade ou pas », on situe la personne sur des continuums (niveau
d'anxiété, d'humeur). Plus proche de la réalité clinique.

**La psychosomatique et le modèle biopsychosocial** : le corps et le psychisme interagissent. Le stress chronique
augmente la douleur, la dépression la rend plus intense, la douleur chronique favorise la dépression. Certains
patients ont des [[somatisation|symptômes physiques]] importants sans lésion expliquant tout : ils ont réellement
mal, ce n'est pas « dans la tête » au sens de « imaginaire ».

**La [[stigmatisation]]** : « les schizophrènes sont dangereux », « la dépression, c'est un manque de volonté ».
Ces stéréotypes sont faux (les personnes avec un trouble psychique sont plus souvent **victimes** de violence que
auteurs), font souffrir et retardent les soins. Ils biaisent aussi le raisonnement des soignants : on risque de
**mettre une plainte physique sur le compte du trouble psychique** et de rater une vraie maladie.
""")
    ui.warn("Chez un patient avec un diagnostic psychiatrique, une douleur thoracique reste une douleur thoracique : "
            "elle doit être explorée comme chez tout le monde. C'est le biais d'**ombrage diagnostique**.")


def ch_kine():
    ui.md(r"""
**Le projet thérapeutique** est multidisciplinaire : psychiatre, psychologue, infirmier, ergothérapeute, kiné,
assistant social, médecin généraliste. Il combine selon les cas médicaments, psychothérapies (par exemple les
thérapies cognitivo-comportementales), activité physique et soutien social.

**Ce que le kiné peut apporter**
- L'**activité physique** a un effet antidépresseur et anxiolytique démontré, comparable à d'autres traitements
  dans les formes légères à modérées de dépression. Il existe même une spécialité : la kinésithérapie en santé
  mentale (psychomotricité).
- Le **corps** comme porte d'entrée : relaxation, conscience corporelle, respiration.
- Le repérage : un patient qui ne vient plus, qui a perdu tout intérêt, qui parle de « ne plus en pouvoir ».

**Quand orienter ?** Toujours en cas d'**idées suicidaires** (en parler ne les fait pas apparaître : poser la
question directement protège), de signes psychotiques, de perte de poids importante, de consommation de
substances qui inquiète, ou quand la souffrance dépasse ce que l'on peut accompagner.
""")
    ui.clinic("Si un patient évoque des idées de mort : écoute sans juger, demande directement s'il pense au suicide, "
              "ne le laisse pas seul s'il y a un danger immédiat, et oriente (médecin traitant, urgences, ligne d'écoute : "
              "**Centre de prévention du suicide, 0800 32 123** en Belgique francophone, ou le **112** en urgence).")


CHAPTERS = [
    ("Démarche diagnostique", ch_demarche),
    ("Les grands troubles", ch_troubles),
    ("Approche dimensionnelle et stigmatisation", ch_dimension),
    ("Le kiné et la santé mentale", ch_kine),
]


def _q_vignette(rng):
    t, good = rng.choice(VIGNETTES)
    return (f"{t} Quel trouble ce tableau évoque-t-il ?", good, [g for _, g in VIGNETTES], "")


QUESTIONS = [
    gen_qcm(1, _q_vignette),
    qcm(1, "Combien de temps doivent durer les symptômes pour parler d'épisode dépressif caractérisé ?", "Au moins 2 semaines",
        ["Au moins 2 jours", "Au moins 6 mois", "Au moins 1 an"]),
    qcm(1, "Que signifie l'anhédonie ?", "La perte de la capacité à éprouver du plaisir", ["L'absence de sommeil",
        "La peur de grossir", "Une hallucination"]),
    vf(1, "Le psychologue est un médecin qui peut prescrire des médicaments.", False, "C'est le psychiatre."),
    qcm(1, "Quelles sont les deux grandes classifications des troubles mentaux ?", "Le DSM-5 et la CIM-11",
        ["Le MMSE et la GDS", "La CIF et la CIM-11", "Le DSM-5 et l'échelle de Berg"]),
    multi(2, "Quels sont des symptômes positifs de la schizophrénie ?", ["Hallucinations", "Idées délirantes"],
          ["Apathie", "Retrait social", "Pauvreté du discours"], "Les autres sont des symptômes négatifs."),
    qcm(2, "Quelle différence entre boulimie et hyperphagie boulimique ?",
        "Dans la boulimie, les crises sont suivies de comportements compensatoires (vomissements…)",
        ["Il n'y en a pas", "L'hyperphagie concerne uniquement les enfants", "La boulimie n'a pas de crises"]),
    vf(2, "Demander directement à un patient s'il pense au suicide augmente le risque qu'il passe à l'acte.", False,
       "Au contraire, en parler protège et permet d'orienter."),
    qcm(2, "L'insight, dans l'examen mental, désigne…", "la conscience que le patient a de son trouble",
        ["son niveau d'intelligence", "son humeur", "sa mémoire"]),
    qcm(2, "L'activité physique dans la dépression légère à modérée…", "a un effet antidépresseur démontré",
        ["n'a aucun effet", "aggrave les symptômes", "est contre-indiquée"]),
    qcm(3, "Un patient suivi pour schizophrénie se plaint d'une douleur au mollet gonflé. Le risque principal est…",
        "d'attribuer la plainte à son trouble psychique et de rater une thrombose (ombrage diagnostique)",
        ["qu'il simule", "de le vexer", "aucun"]),
    qcm(3, "Une patiente lombalgique chronique a perdu tout intérêt, dort mal et se dit « inutile » depuis un mois. "
        "Que faire ?", "En parler avec elle et l'orienter vers son médecin pour évaluer une dépression",
        ["Ignorer, ce n'est pas le rôle du kiné", "Augmenter les séances de massage", "Lui dire de se secouer"]),
    qcm(3, "Pourquoi la stigmatisation des troubles psychiques est-elle un problème de santé ?",
        "Elle fait souffrir, isole et retarde l'accès aux soins", ["Elle n'a aucune conséquence",
        "Elle protège la société", "Elle aide à poser le diagnostic"]),
    qcm(3, "Une jeune sportive très mince a des fractures de fatigue à répétition et refuse de manger plus. Que suspecter ?",
        "Un trouble des conduites alimentaires (déficit énergétique relatif dans le sport)", ["Une simple maladresse",
        "Un manque de calcium uniquement", "Un trouble psychotique"]),
]

CARDS = [
    ("Épisode dépressif caractérisé", "≥ 5 symptômes / 9, ≥ 2 semaines, dont humeur triste ou anhédonie"),
    ("Anhédonie", "Perte du plaisir"),
    ("Trouble bipolaire", "Épisodes dépressifs + maniaques"),
    ("Anxiété généralisée", "Inquiétudes excessives sur tout, ≥ 6 mois"),
    ("Trouble panique", "Attaques de panique répétées + peur d'en refaire"),
    ("TSPT", "Reviviscences, évitement, hypervigilance après un traumatisme"),
    ("Symptômes positifs / négatifs", "Délires, hallucinations / apathie, retrait"),
    ("Anorexie mentale", "Restriction, peur de grossir, image du corps déformée"),
    ("Insight", "Conscience du trouble"),
    ("Ombrage diagnostique", "Attribuer une plainte physique au trouble psychique"),
    ("Idées suicidaires", "Poser la question directement, ne pas laisser seul, orienter"),
]

VIDEOS = [
    ("Reconnaître la dépression", "reconnaître dépression symptômes explication psychiatre"),
    ("L'attaque de panique expliquée", "attaque de panique explication"),
    ("Activité physique et santé mentale", "activité physique dépression anxiété effets"),
    ("Stigmatisation en santé mentale", "stigmatisation santé mentale idées reçues"),
]

LINKS = [("Centre de prévention du suicide (Belgique)", "https://www.preventionsuicide.be/")]
