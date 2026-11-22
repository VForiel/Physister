"""LANGL1851A et B : English for Movement and Rehabilitation Sciences."""

import streamlit as st

from app import ui
from app.course import Course
from app.quiz import gen_qcm, qcm, table_qcm, vf

COURSE = Course(
    code="LANGL1851", title="English for Movement and Rehabilitation Sciences (A et B)", short="Anglais",
    bloc=2, quad=1, credits=4, hours="15 h (A, Q1) + 30 h (B, Q2)", icon=":material/translate:",
    intro="La plupart des articles et des guides de pratique sont en anglais. Ces deux cours (A au Q1, B au Q2) "
          "visent la lecture d'articles (niveau B1) et une communication simple à l'oral (A2). Ici : le "
          "vocabulaire du métier, les faux amis, et comment lire un abstract.",
    acquis=[
        "Maîtriser le vocabulaire spécifique aux sciences de la motricité en anglais.",
        "Comprendre une littérature scientifique et de vulgarisation (B1) et la résumer en français.",
        "Décrire en français le contenu d'un document audiovisuel.",
        "Communiquer et dialoguer au niveau A2, adapté au public et au contexte (partie B).",
    ],
)

TERMS = {
    "faux ami": ("Faux ami", "Mot qui ressemble à un mot français mais n'a pas le même sens (« actually » = en fait, "
                 "pas « actuellement »).", "Faux-ami"),
    "hedging": ("Hedging", "Atténuation prudente d'une affirmation dans un texte scientifique (may, might, suggest, "
                "appear to).", None),
}

VOCAB = {
    # anatomie
    "shoulder blade": "omoplate (scapula)", "collarbone": "clavicule", "elbow": "coude", "wrist": "poignet",
    "knee": "genou", "kneecap": "rotule (patella)", "ankle": "cheville", "heel": "talon", "hip": "hanche",
    "thigh": "cuisse", "calf": "mollet", "shin": "tibia (face antérieure de la jambe)", "spine": "colonne vertébrale",
    "lower back": "bas du dos (région lombaire)", "neck": "cou", "rib": "côte", "skull": "crâne",
    "tendon": "tendon", "ligament": "ligament", "cartilage": "cartilage", "joint": "articulation",
    "bone": "os", "muscle strength": "force musculaire", "hamstrings": "ischio-jambiers",
    "rotator cuff": "coiffe des rotateurs", "pelvic floor": "plancher pelvien", "toe": "orteil",
    "big toe": "gros orteil (hallux)", "thumb": "pouce",
    # mouvements et clinique
    "range of motion (ROM)": "amplitude articulaire", "to bend": "plier, fléchir", "to straighten": "tendre, étendre",
    "to stretch": "étirer", "to strengthen": "renforcer", "to lift": "soulever", "weight-bearing": "mise en charge",
    "gait": "marche (façon de marcher)", "balance": "équilibre", "fall": "chute", "sprain": "entorse",
    "strain": "élongation, claquage (muscle)", "fracture": "fracture", "swelling": "gonflement, œdème",
    "bruise": "hématome, bleu", "pain": "douleur", "ache": "douleur sourde", "sore": "douloureux, endolori",
    "stiffness": "raideur", "numbness": "engourdissement", "tingling": "fourmillements",
    "weakness": "faiblesse", "shortness of breath": "essoufflement (dyspnée)", "stroke": "AVC",
    "spinal cord injury": "lésion de la moelle épinière", "physiotherapist (physical therapist)": "kinésithérapeute",
    "outpatient": "patient ambulatoire", "inpatient": "patient hospitalisé", "home exercise programme": "programme d'exercices à domicile",
    "walking aid": "aide à la marche", "crutches": "béquilles", "wheelchair": "fauteuil roulant",
    "to recover": "récupérer, guérir", "rehabilitation": "réadaptation, rééducation", "warm-up": "échauffement",
    "cool-down": "retour au calme", "sets and reps": "séries et répétitions", "physical activity": "activité physique",
    # recherche
    "randomised controlled trial (RCT)": "essai contrôlé randomisé", "systematic review": "revue systématique",
    "outcome measure": "critère de jugement, mesure de résultat", "sample size": "taille de l'échantillon",
    "follow-up": "suivi", "dropout": "abandon (participant qui quitte l'étude)", "baseline": "mesure initiale",
    "evidence": "preuves, données probantes", "finding": "résultat (d'une étude)", "bias": "biais",
    "significant": "significatif (statistiquement)", "to assess": "évaluer", "reliability": "fiabilité",
    "validity": "validité", "guideline": "recommandation, guide de pratique",
}

FAUX_AMIS = {
    "actually": "en fait (et non « actuellement » = currently)",
    "eventually": "finalement (et non « éventuellement » = possibly)",
    "sensible": "raisonnable (et non « sensible » = sensitive)",
    "to achieve": "atteindre, réussir (et non « achever » = to finish)",
    "library": "bibliothèque (et non « librairie » = bookshop)",
    "to attend": "assister à (et non « attendre » = to wait)",
    "injury": "blessure (et non « injure » = insult)",
    "physician": "médecin (et non « physicien » = physicist)",
    "to support": "soutenir (et non « supporter » = to bear, to stand)",
    "lecture": "cours magistral (et non « lecture » = reading)",
    "to resume": "reprendre (et non « résumer » = to summarise)",
    "chronic": "qui dure longtemps (et non « grave ») : chronic pain ≠ severe pain",
}

ABSTRACT = """**Background:** Knee osteoarthritis is a leading cause of pain and disability in older adults.
**Objective:** To compare the effect of a 12-week resistance training programme with usual care on pain and function.
**Methods:** Eighty participants aged 60 to 80 years were randomly allocated to resistance training (n = 40) or usual
care (n = 40). The primary outcome was pain intensity (0-10 scale) at 12 weeks.
**Results:** Pain decreased more in the training group (mean difference −1.8 points, 95% CI −2.6 to −1.0).
Six participants dropped out.
**Conclusion:** Resistance training may reduce pain in older adults with knee osteoarthritis.
These findings suggest that it should be considered as a first-line treatment."""


def ch_vocab():
    st.markdown("Recherche dans le lexique (anglais ou français). Le même lexique alimente les fiches mémo et le quiz.")
    q = st.text_input("Rechercher", placeholder="ex. genou, sprain, échantillon", key="en_q")
    rows = [[en, fr] for en, fr in VOCAB.items() if not q or q.lower() in en.lower() or q.lower() in fr.lower()]
    ui.table(rows, headers=["English", "Français"])
    ui.tip("Apprends les mots **en contexte** : « She sprained her ankle playing basketball » se retient mieux que "
           "« sprain = entorse ». Et lis un abstract par semaine sur PEDro ou PubMed : c'est le meilleur entraînement.")


def ch_faux_amis():
    ui.md("Les [[faux ami|faux amis]] les plus piégeux en sciences de la santé :")
    ui.table([[k, v] for k, v in FAUX_AMIS.items()], headers=["Anglais", "Sens réel"])
    ui.warn("« The patient eventually recovered » veut dire « le patient a **finalement** guéri », pas « éventuellement ». "
            "Et « chronic pain » veut dire une douleur qui **dure** (plus de 3 mois), pas une douleur grave.")


def ch_lire():
    ui.md(r"""
**Lire un abstract en anglais** : repère les sous-titres (Background, Objective, Methods, Results, Conclusion)
et cherche d'abord la **question**, la **population**, l'**intervention** et le **résultat principal** (le PICO
du cours d'EBP).

**Le [[hedging]]** : les scientifiques nuancent. *may, might, could, suggest, appear to, is likely to*
signalent une conclusion prudente. *demonstrate, show, prove* sont plus affirmatifs. Repérer ces mots, c'est
comprendre le degré de certitude des auteurs.

**Grammaire en contexte** : les articles utilisent beaucoup le **passif** (*participants were randomly allocated*,
« les participants ont été répartis au hasard ») et le **prétérit** pour décrire ce qui a été fait (*pain
decreased*).
""")
    st.markdown("#### À toi : lis cet abstract (fictif)")
    st.markdown(ABSTRACT)
    c1, c2 = st.columns(2)
    p = c1.radio("Quelle est la population ?", ["Des sportifs de 20 à 30 ans", "Des personnes de 60 à 80 ans avec arthrose du genou",
                                                 "Des patients opérés du genou"], index=None, key="en_p")
    h = c2.radio("Le mot « may » dans la conclusion indique…", ["une certitude", "une prudence (hedging)", "une obligation"],
                 index=None, key="en_h")
    d = c1.radio("Que veut dire « Six participants dropped out » ?", ["Six participants ont abandonné l'étude",
                                                                      "Six participants sont tombés", "Six participants ont guéri"],
                 index=None, key="en_d")
    if p:
        (c1.success if p.startswith("Des personnes") else c1.error)("Population : 80 personnes de 60 à 80 ans avec gonarthrose.")
    if h:
        (c2.success if "prudence" in h else c2.error)("« May » atténue la conclusion : c'est du hedging.")
    if d:
        (c1.success if "abandonné" in d else c1.error)("« To drop out » = abandonner (dropout = abandon).")
    ui.md(r"""
**Pour la partie B (oral, A2)** : savoir se présenter, accueillir un patient, poser des questions simples
(*Where does it hurt? When did it start? Does it hurt when you bend your knee?*), donner une consigne
(*Lie on your back. Lift your leg slowly. Hold for five seconds.*).
""")


CHAPTERS = [
    ("Vocabulaire", ch_vocab),
    ("Faux amis", ch_faux_amis),
    ("Lire un article", ch_lire),
]

QUESTIONS = [
    table_qcm(1, {k: v for k, v in list(VOCAB.items())[:30]}, "Que veut dire **{k}** ?", "Comment dit-on « {v} » en anglais ?"),
    table_qcm(2, {k: v for k, v in list(VOCAB.items())[30:65]}, "Que veut dire **{k}** ?", "Comment dit-on « {v} » en anglais ?"),
    table_qcm(3, {k: v for k, v in list(VOCAB.items())[65:]}, "Que veut dire **{k}** ?", "Comment dit-on « {v} » en anglais ?"),
    table_qcm(2, FAUX_AMIS, "Que veut vraiment dire **{k}** ?"),
    qcm(1, "« Physiotherapist » se traduit par…", "kinésithérapeute", ["physicien", "médecin", "psychologue"]),
    vf(1, "« Actually » veut dire « actuellement ».", False, "Il veut dire « en fait » ; actuellement = currently."),
    qcm(1, "« Where does it hurt? » signifie…", "Où avez-vous mal ?", ["Quand avez-vous mal ?", "Avez-vous chaud ?",
        "Pourquoi avez-vous mal ?"]),
    qcm(2, "Dans un article, « participants were randomly allocated » est au…", "passif", ["futur", "présent continu", "conditionnel"]),
    qcm(2, "Quel mot exprime le plus de prudence ?", "may", ["demonstrate", "prove", "show"]),
    qcm(3, "« Chronic low back pain » désigne…", "une douleur lombaire qui dure depuis longtemps (plus de 3 mois)",
        ["une douleur lombaire très intense", "une douleur lombaire aiguë", "une douleur au cou"]),
    qcm(3, "« The intervention did not achieve a clinically meaningful effect » signifie…",
        "L'intervention n'a pas atteint un effet cliniquement important", ["L'intervention n'a pas été terminée",
        "L'intervention a été un succès clinique", "L'intervention a été arrêtée pour effets indésirables"]),
    qcm(3, "Quelle consigne correspond à « Allongez-vous sur le dos et levez lentement la jambe » ?",
        "Lie on your back and lift your leg slowly", ["Lie on your stomach and bend your knee",
        "Stand up and lift your arm", "Sit down and hold your breath"]),
]

CARDS = list(VOCAB.items()) + list(FAUX_AMIS.items())

VIDEOS = [
    ("Vocabulaire anglais du corps humain", "English vocabulary body parts physiotherapy"),
    ("Anglais pour kinés : consultation", "English for physiotherapists patient conversation"),
    ("Lire un article scientifique en anglais", "how to read a scientific paper abstract"),
]

LINKS = [("PEDro (abstracts en anglais pour s'entraîner)", "https://pedro.org.au/")]
