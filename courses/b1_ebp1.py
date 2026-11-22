"""LKNR1105 Evidence based practice (EBP) / Raisonnement clinique 1."""

import streamlit as st

from app import ui
from app.course import Course
from app.quiz import gen_qcm, multi, qcm, vf

COURSE = Course(
    code="LKNR1105", title="Evidence based practice / Raisonnement clinique 1", short="EBP et raisonnement 1",
    bloc=1, quad=2, credits=3, hours="30 h", icon=":material/psychology_alt:",
    intro="Comment un kiné décide-t-il quoi faire ? En combinant ce que disent les études, son expérience et ce que "
          "veut le patient : c'est l'EBP. Et en suivant une démarche de raisonnement clinique structurée, en se "
          "méfiant de ses propres biais. La suite au bloc 2 (LKNR1210).",
    acquis=[
        "Comprendre les principes de la démarche EBP.",
        "Décrire les étapes du raisonnement clinique et argumenter une décision.",
        "Connaître les principes de la récolte d'informations et la structure d'une prise en charge.",
        "Identifier les biais cognitifs en soins de santé.",
    ],
)

TERMS = {
    "pico": ("PICO", "Structure d'une question clinique : Patient (population), Intervention, Comparaison, "
             "Outcome (critère de résultat).", "PICO"),
    "raisonnement hypothético-déductif": ("Raisonnement hypothético-déductif", "Formuler tôt des hypothèses "
                                          "diagnostiques, puis les tester une à une par l'anamnèse et l'examen.",
                                          None),
    "reconnaissance de schéma": ("Reconnaissance de schéma (pattern recognition)", "Raisonnement rapide et intuitif "
                                 "de l'expert, qui reconnaît une situation déjà vue. Efficace mais exposé aux biais.",
                                 None),
    "validité interne": ("Validité interne", "Degré auquel les résultats d'une étude sont dus à l'intervention et "
                         "non à des biais.", "Validité interne"),
    "validité externe": ("Validité externe", "Degré auquel les résultats d'une étude peuvent s'appliquer à d'autres "
                         "patients et contextes (généralisation).", "Validité externe"),
    "drapeau rouge": ("Drapeau rouge", "Signe d'alerte d'une pathologie grave (fracture, cancer, infection, "
                      "atteinte neurologique) qui impose de réorienter vers le médecin.", None),
    "drapeau jaune": ("Drapeau jaune", "Facteur psychosocial (peur, croyances, catastrophisme, dépression) qui "
                      "augmente le risque de chronicisation.", None),
    "fermeture prématurée": ("Fermeture prématurée", "Biais qui consiste à arrêter de réfléchir dès qu'une "
                             "hypothèse semble convenir, sans envisager les autres.", None),
}

BIAIS = [
    ("Dès la lecture de « tendinite » sur la prescription, l'étudiant n'examine plus que le tendon.", "Ancrage"),
    ("Le kiné a trouvé une explication et arrête l'examen sans chercher d'autres causes.", "Fermeture prématurée"),
    ("Après un cas de syndrome de la queue de cheval la semaine passée, le kiné le suspecte chez tous ses lombalgiques.",
     "Disponibilité"),
    ("Le kiné ne retient que les tests qui vont dans le sens de son hypothèse.", "Confirmation"),
]


def ch_ebp():
    ui.md(r"""
**L'[[ebp|EBP]]** (Sackett, 1996) : « l'utilisation consciencieuse, explicite et judicieuse des meilleures preuves
actuelles pour prendre des décisions concernant les soins de chaque patient ». Elle repose sur **trois piliers** :

1. les **meilleures preuves** de la recherche ;
2. l'**expertise clinique** du soignant ;
3. les **valeurs et préférences** du patient,

le tout dans un **contexte** (ressources, temps, remboursement).
""")
    ui.warn("L'EBP n'est **pas** « appliquer ce que dit la dernière étude ». Si le patient refuse l'exercice "
            "recommandé, ou si l'étude porte sur de jeunes sportifs et que ton patient a 85 ans, il faut adapter.")
    ui.md(r"""
**Les 5 étapes (les « 5 A »)**
1. **Ask** : formuler une question clinique précise ([[pico|PICO]]).
2. **Acquire** : chercher les preuves (PEDro, PubMed, guides de pratique).
3. **Appraise** : évaluer leur qualité et leur pertinence.
4. **Apply** : décider avec le patient.
5. **Assess** : évaluer le résultat, et ajuster.
""")
    ui.memo("**3 piliers, 5 A** : Ask, Acquire, Appraise, Apply, Assess. En français : Demander, Chercher, Critiquer, "
            "Appliquer, Évaluer.")


def ch_pico():
    ui.md(r"""
Une bonne question clinique suit la structure **[[pico|PICO]]** :
- **P**atient / population : qui ? (âge, pathologie, stade)
- **I**ntervention : quel traitement ou test ?
- **C**omparaison : par rapport à quoi ? (autre traitement, placebo, rien)
- **O**utcome : quel résultat mesurer ? (douleur, fonction, retour au travail)
""")
    st.markdown("#### À toi : construis ta question et ta recherche")
    c1, c2 = st.columns(2)
    p = c1.text_input("P (en anglais pour la recherche)", "older adults with knee osteoarthritis", key="ebp_p")
    i = c2.text_input("I", "resistance training", key="ebp_i")
    c = c1.text_input("C", "usual care", key="ebp_c")
    o = c2.text_input("O", "pain", key="ebp_o")
    st.markdown(f"**Question** : chez des *{p}*, est-ce que *{i}*, comparé à *{c}*, améliore *{o}* ?")
    terms = [f'"{x}"' if " " in x else x for x in (p, i, o) if x]
    query = " AND ".join(f"({t})" for t in terms)
    st.code(query, language=None)
    st.caption("On met en général P, I et O dans la recherche, la comparaison moins souvent. Ajoute des synonymes "
               "avec OR, puis colle la requête dans PubMed ou PEDro.")
    st.link_button("Chercher sur PubMed", f"https://pubmed.ncbi.nlm.nih.gov/?term={query.replace(' ', '+')}")
    ui.md(r"""
**Validité interne et externe** : une étude bien faite (bonne [[validité interne]]) ne s'applique pas forcément à
ton patient. La [[validité externe]] demande : les participants ressemblent-ils à mon patient ? L'intervention
est-elle faisable dans mon cabinet ? Le résultat mesuré compte-t-il pour lui ?
""")


def ch_raisonnement():
    ui.md(r"""
Le **raisonnement clinique**, ce sont les processus de pensée qui mènent de la plainte du patient à une décision.

**Deux grands types**
- Le [[raisonnement hypothético-déductif|raisonnement **hypothético-déductif**]] : on génère des hypothèses dès
  les premières minutes, puis on les teste. Lent, analytique, typique du débutant (et de l'expert face à un cas
  difficile).
- La [[reconnaissance de schéma|**reconnaissance de schéma**]] : l'expert reconnaît un tableau déjà vu. Rapide et
  souvent juste, mais exposé aux biais.

Il existe aussi le raisonnement **narratif** (comprendre l'histoire et le vécu du patient), **collaboratif** (décider
avec lui), **éthique**, et le raisonnement sur la **procédure** (comment faire l'exercice).

**Les étapes d'une prise en charge en kiné**
1. **[[anamnèse|Anamnèse]]** : plainte, histoire, antécédents, [[drapeau rouge|drapeaux rouges]] et
   [[drapeau jaune|jaunes]], attentes.
2. **Examen clinique** : observation, tests, mesures.
3. **Diagnostic kiné** (en termes de fonction, selon la CIF) et **pronostic**.
4. **Objectifs** fixés avec le patient.
5. **Traitement** : actes, exercices, éducation.
6. **Réévaluation** continue, et adaptation.
""")
    ui.tip("Dès l'anamnèse, note **2 ou 3 hypothèses**. À chaque question et chaque test, demande-toi : « est-ce que "
           "ça renforce ou affaiblit chacune de mes hypothèses ? ». C'est ce qu'on attend en vignette clinique.")
    ui.clinic("Les **drapeaux rouges** d'une lombalgie : antécédent de cancer, perte de poids inexpliquée, fièvre, "
              "traumatisme important, douleur nocturne non mécanique, troubles urinaires ou anesthésie en selle "
              "(syndrome de la queue de cheval : urgence !). Si présents : on réoriente vers le médecin.")


def ch_biais():
    ui.md(r"""
Même les experts se trompent, souvent à cause de **biais cognitifs** :

| Biais | Ce qui se passe | Antidote |
|---|---|---|
| Ancrage | la première information pèse trop | relire le cas à froid, se demander « et si c'était autre chose ? » |
| [[fermeture prématurée\|Fermeture prématurée]] | on s'arrête dès qu'une hypothèse convient | toujours avoir au moins une hypothèse alternative |
| Disponibilité | on surestime ce qu'on a vu récemment | penser en termes de fréquence réelle (prévalence) |
| Confirmation | on cherche ce qui confirme | chercher activement ce qui **infirmerait** |
| Excès de confiance | on se croit plus sûr qu'on ne l'est | réévaluer, demander un avis |
""")
    st.markdown("#### À toi : quel biais ?")
    i = st.session_state.setdefault("ebp_b_i", 0) % len(BIAIS)
    txt, good = BIAIS[i]
    st.markdown(f"> {txt}")
    rep = st.radio("Biais", ["Ancrage", "Fermeture prématurée", "Disponibilité", "Confirmation"], index=None,
                   horizontal=True, key=f"ebp_b_{i}")
    if rep:
        (st.success if rep == good else st.error)(f"Réponse : **{good}**")
    if st.button("Cas suivant", key="ebp_b_next"):
        st.session_state["ebp_b_i"] = i + 1
        st.rerun()


CHAPTERS = [
    ("L'evidence based practice", ch_ebp),
    ("Poser la bonne question (PICO)", ch_pico),
    ("Le raisonnement clinique", ch_raisonnement),
    ("Les biais cognitifs", ch_biais),
]


def _q_biais(rng):
    t, good = rng.choice(BIAIS)
    return (f"Quel biais ? {t}", good, ["Ancrage", "Fermeture prématurée", "Disponibilité", "Confirmation"], "")


PICO_EX = [
    ("Chez des coureurs avec tendinopathie d'Achille, le renforcement excentrique comparé au repos réduit-il la douleur ?",
     {"P": "coureurs avec tendinopathie d'Achille", "I": "renforcement excentrique", "C": "repos", "O": "douleur"}),
    ("Chez des patients BPCO, la réhabilitation à l'effort comparée aux soins usuels améliore-t-elle la distance de marche ?",
     {"P": "patients BPCO", "I": "réhabilitation à l'effort", "C": "soins usuels", "O": "distance de marche"}),
]


def _q_pico(rng):
    q, d = rng.choice(PICO_EX)
    k = rng.choice(list(d))
    return (f"Dans la question « {q} », quel est le **{k}** du PICO ?", d[k], [v for kk, v in d.items() if kk != k], "")


QUESTIONS = [
    multi(1, "Quels sont les trois piliers de l'EBP ?", ["Meilleures preuves de la recherche", "Expertise clinique",
          "Valeurs et préférences du patient"], ["Avis de la famille", "Coût de la séance"]),
    qcm(1, "Que signifie le O de PICO ?", "Outcome (critère de résultat)", ["Objectif", "Observation", "Opinion"]),
    vf(1, "L'EBP consiste à appliquer strictement le résultat de la dernière étude publiée.", False,
       "Elle intègre aussi l'expertise et les préférences du patient."),
    qcm(1, "Quelle est la première étape de l'EBP ?", "Formuler une question clinique (Ask)",
        ["Chercher des articles", "Appliquer le traitement", "Évaluer le résultat"]),
    gen_qcm(1, _q_pico),
    gen_qcm(2, _q_biais),
    qcm(2, "Le raisonnement rapide d'un expert qui reconnaît un tableau clinique s'appelle…",
        "la reconnaissance de schéma", ["le raisonnement hypothético-déductif", "le raisonnement narratif", "l'ancrage"]),
    qcm(2, "La validité externe d'une étude concerne…", "la possibilité d'appliquer ses résultats à d'autres patients",
        ["l'absence de biais dans l'étude", "la qualité statistique", "le nombre d'auteurs"]),
    multi(2, "Lesquels sont des drapeaux rouges d'une lombalgie ?", ["Anesthésie en selle", "Antécédent de cancer",
          "Fièvre"], ["Douleur qui augmente en se penchant", "Raideur matinale de 10 minutes"]),
    qcm(2, "Un drapeau jaune est…", "un facteur psychosocial qui favorise la chronicisation",
        ["un signe de pathologie grave", "une contre-indication absolue", "un résultat de test"]),
    qcm(3, "Une étude sur de jeunes footballeurs montre l'efficacité d'un programme. Ta patiente a 78 ans. Que fais-tu ?",
        "Tu tiens compte de la validité externe limitée et tu adaptes, en discutant avec elle",
        ["Tu appliques le programme tel quel", "Tu ignores l'étude", "Tu refuses de la traiter"]),
    qcm(3, "Quel est le meilleur antidote au biais de confirmation ?", "Chercher activement ce qui infirmerait son hypothèse",
        ["Faire plus de tests qui confirment", "Écouter son intuition", "Lire la prescription plus attentivement"]),
    qcm(3, "Un patient lombalgique signale des troubles urinaires récents et une anesthésie du périnée. Que faire ?",
        "Réorienter en urgence vers un médecin (suspicion de syndrome de la queue de cheval)",
        ["Commencer des exercices de McKenzie", "Revoir le patient la semaine prochaine", "Appliquer de la chaleur"]),
    qcm(3, "Dans le raisonnement hypothético-déductif, à quel moment formule-t-on les premières hypothèses ?",
        "Très tôt, dès les premières informations de l'anamnèse", ["Uniquement après tous les tests",
        "Jamais, on observe sans hypothèse", "À la fin du traitement"]),
]

CARDS = [
    ("Définition de l'EBP (Sackett)", "Utilisation consciencieuse, explicite et judicieuse des meilleures preuves pour chaque patient"),
    ("3 piliers de l'EBP", "Preuves, expertise clinique, préférences du patient"),
    ("5 A", "Ask, Acquire, Appraise, Apply, Assess"),
    ("PICO", "Patient, Intervention, Comparaison, Outcome"),
    ("Validité interne", "Résultats dus à l'intervention, pas aux biais"),
    ("Validité externe", "Généralisation à d'autres patients"),
    ("Hypothético-déductif", "Hypothèses précoces testées une à une"),
    ("Drapeau rouge", "Signe de pathologie grave → médecin"),
    ("Drapeau jaune", "Facteur psychosocial de chronicisation"),
    ("Fermeture prématurée", "S'arrêter à la première hypothèse qui convient"),
]

VIDEOS = [
    ("L'evidence based practice en kinésithérapie", "evidence based practice kinésithérapie explication"),
    ("Formuler une question PICO", "question PICO exemple"),
    ("Le raisonnement clinique en kiné", "raisonnement clinique kinésithérapie"),
    ("Biais cognitifs en médecine", "biais cognitifs diagnostic médecine"),
]

LINKS = [("PEDro : guide pour chercher (en français)", "https://pedro.org.au/french/learn/")]
