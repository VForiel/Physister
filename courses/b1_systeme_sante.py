"""LKNR1104 Système de santé et modèle médical."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from app import ui
from app.course import Course
from app.quiz import gen_qcm, multi, num, qcm, table_qcm, vf

COURSE = Course(
    code="LKNR1104", title="Système de santé et modèle médical", short="Système de santé",
    bloc=1, quad=2, credits=6, hours="45 h", icon=":material/account_balance:",
    intro="Qui paie la séance de kiné ? Qui indemnise un ouvrier blessé ? Que veut dire « prévention secondaire » ? "
          "Ce cours situe le kiné dans le système de santé belge, présente les modèles de la santé et les bases "
          "de l'épidémiologie.",
    acquis=[
        "Distinguer le modèle biopsychosocial du modèle médical.",
        "Connaître le rôle des acteurs et la place du kiné (interprofessionnalité).",
        "Connaître le cadre légal et le système de santé publique belge.",
        "Comprendre la prévention primaire, secondaire et tertiaire, et la réparation des dommages liés au travail.",
        "Analyser les risques liés à une activité professionnelle (ergonomie).",
    ],
)

TERMS = {
    "déterminants de la santé": ("Déterminants de la santé", "Facteurs qui influencent la santé : biologie, "
                                 "comportements, réseau social, conditions de vie et de travail, contexte "
                                 "socio-économique (modèle de Dahlgren et Whitehead).", "Déterminants de la santé"),
    "promotion de la santé": ("Promotion de la santé", "Processus qui donne aux populations les moyens d'agir sur "
                              "leur santé (Charte d'Ottawa, OMS, 1986).", "Promotion de la santé"),
    "prévention primaire": ("Prévention primaire", "Éviter qu'une maladie apparaisse (vaccination, activité "
                            "physique, ergonomie).", "Prévention"),
    "prévention secondaire": ("Prévention secondaire", "Dépister et traiter tôt une maladie déjà présente mais "
                              "encore discrète (dépistage).", "Prévention"),
    "prévention tertiaire": ("Prévention tertiaire", "Limiter les complications, les rechutes et le handicap d'une "
                             "maladie installée (réadaptation).", "Prévention"),
    "prévention quaternaire": ("Prévention quaternaire", "Protéger le patient des soins inutiles ou excessifs "
                               "(surdiagnostic, surtraitement).", "Prévention quaternaire"),
    "inami": ("INAMI", "Institut national d'assurance maladie-invalidité : organise le remboursement des soins, "
              "fixe la nomenclature et les tarifs, contrôle.", "Institut national d'assurance maladie-invalidité"),
    "mutualité": ("Mutualité", "Organisme assureur auprès duquel chaque personne est affiliée ; elle rembourse les "
                  "soins selon les règles de l'INAMI.", "Mutualité en Belgique"),
    "ticket modérateur": ("Ticket modérateur", "Part du tarif d'un soin qui reste à charge du patient après "
                          "remboursement.", "Ticket modérateur"),
    "bim": ("BIM", "Bénéficiaire de l'intervention majorée : statut qui donne un meilleur remboursement aux "
            "personnes à faibles revenus.", None),
    "nomenclature": ("Nomenclature", "Liste officielle des prestations remboursables par l'INAMI, avec leur code, "
                     "leurs conditions et leur tarif.", None),
    "fedris": ("FEDRIS", "Agence fédérale des risques professionnels : accidents du travail et maladies "
               "professionnelles.", None),
    "aviq": ("AVIQ", "Agence pour une Vie de Qualité : organisme wallon compétent pour la santé, le handicap, les "
             "familles et les aînés.", "Agence pour une vie de qualité"),
    "phare": ("PHARE", "Personne Handicapée Autonomie Recherchée : service de la COCOF pour les personnes "
              "handicapées à Bruxelles.", None),
    "axxon": ("AXXON", "Association professionnelle des kinésithérapeutes en Belgique.", None),
    "interprofessionnalité": ("Interprofessionnalité", "Collaboration de plusieurs professions autour d'un même "
                              "patient, avec des objectifs partagés.", None),
    "ergonomie": ("Ergonomie", "Adaptation du travail (poste, outils, organisation) à l'humain pour préserver sa "
                  "santé et son efficacité.", "Ergonomie"),
}

PREVENTION = [
    ("Programme d'exercices d'équilibre pour éviter les chutes chez des seniors en bonne santé.", "Primaire"),
    ("Dépistage de l'ostéoporose par densitométrie chez une femme ménopausée.", "Secondaire"),
    ("Réadaptation cardiaque après un infarctus.", "Tertiaire"),
    ("Éviter de prescrire une IRM inutile pour une lombalgie aiguë sans signe d'alerte.", "Quaternaire"),
    ("Formation des ouvriers aux bonnes postures de port de charges.", "Primaire"),
    ("Rééducation d'un patient après un AVC pour limiter le handicap.", "Tertiaire"),
    ("Test de dépistage du cancer colorectal à 50 ans.", "Secondaire"),
]

ACTEURS = {
    "INAMI": "organise le remboursement des soins et fixe la nomenclature",
    "Mutualité": "rembourse les soins à ses affiliés",
    "FEDRIS": "gère les accidents du travail et maladies professionnelles",
    "AVIQ": "santé, handicap et aînés en Wallonie",
    "PHARE": "aide aux personnes handicapées à Bruxelles (COCOF)",
    "AXXON": "association professionnelle des kinés",
    "SPF Santé publique": "délivre le visa d'exercice des professions de santé",
}


def ch_modeles():
    ui.md(r"""
**Le modèle biomédical** : la maladie est une lésion ou un dysfonctionnement biologique ; le soignant la
diagnostique et la traite. Très efficace pour les maladies aiguës (infection, fracture), il est insuffisant pour
les maladies **chroniques** et la **douleur** persistante.

**Le modèle [[biopsychosocial]]** (Engel, 1977) : la santé résulte de l'interaction de facteurs **biologiques**
(lésion, génétique), **psychologiques** (croyances, peur, humeur) et **sociaux** (travail, famille, revenus).
La [[cif|CIF]] (OMS, 2001) le met en pratique : on décrit une personne par ses **fonctions et structures**, ses
**activités**, sa **participation**, et les facteurs **environnementaux** et **personnels**.

**Les [[déterminants de la santé]]** (Dahlgren et Whitehead) sont souvent représentés en couches autour de la
personne : âge, sexe, hérédité → mode de vie → réseaux sociaux → conditions de vie et de travail → contexte
socio-économique, culturel et environnemental.
""")
    ui.clinic("Deux patients avec la même hernie discale : l'un reprend le travail en 6 semaines, l'autre est en "
              "invalidité depuis un an. La différence tient souvent à la peur du mouvement, au soutien de "
              "l'employeur, au type de travail. Le modèle biopsychosocial explique ce que le modèle biomédical ne "
              "voit pas.")


def ch_prevention():
    ui.md(r"""
La **[[promotion de la santé]]** (Charte d'Ottawa, 1986) vise à donner aux gens les moyens d'agir sur leur santé :
politiques publiques, environnements favorables, action communautaire, aptitudes individuelles, réorientation
des services de santé.

| Niveau | But | Exemple en kiné |
|---|---|---|
| [[prévention primaire\|Primaire]] | éviter l'apparition | échauffement et renforcement pour prévenir les blessures |
| [[prévention secondaire\|Secondaire]] | dépister tôt | repérer une scoliose chez un ado |
| [[prévention tertiaire\|Tertiaire]] | limiter les conséquences | réadaptation après un AVC |
| [[prévention quaternaire\|Quaternaire]] | éviter les soins inutiles | ne pas multiplier les séances passives sans effet |
""")
    st.markdown("#### À toi : classe l'action")
    i = st.session_state.setdefault("ss_prev_i", 0) % len(PREVENTION)
    txt, good = PREVENTION[i]
    st.markdown(f"> {txt}")
    rep = st.radio("Niveau de prévention", ["Primaire", "Secondaire", "Tertiaire", "Quaternaire"], index=None,
                   horizontal=True, key=f"ss_prev_{i}")
    if rep:
        (st.success if rep == good else st.error)(f"Réponse : **{good}**")
    if st.button("Exemple suivant", key="ss_prev_next"):
        st.session_state["ss_prev_i"] = i + 1
        st.rerun()


def ch_epidemio():
    ui.md(r"""
L'**épidémiologie** étudie la fréquence des maladies et leurs facteurs.

- L'**[[incidence]]** : nouveaux cas pendant une période / population à risque. Elle mesure le **risque** de tomber
  malade.
- La **[[prévalence]]** : tous les cas (anciens et nouveaux) à un moment / population. Elle mesure le **poids** de
  la maladie.

Pour une maladie stable, **prévalence ≈ incidence × durée moyenne**. Une maladie fréquente mais courte (rhume) a
une forte incidence et une prévalence modérée ; une maladie rare mais chronique (diabète) s'accumule et a une forte
prévalence.
""")
    st.markdown("#### À toi : la baignoire de la prévalence")
    st.caption("Les nouveaux cas remplissent la baignoire (incidence), les guérisons et décès la vident. Le niveau "
               "d'eau, c'est la prévalence.")
    c1, c2 = st.columns([1, 2])
    with c1:
        inc = st.slider("Incidence (nouveaux cas pour 1000 personnes par an)", 1, 100, 10, key="ss_inc")
        dur = st.slider("Durée moyenne de la maladie (années)", 0.1, 30.0, 5.0, 0.1, key="ss_dur")
    years = np.arange(0, 40.1, 0.5)
    prev = inc * dur * (1 - np.exp(-years / dur))
    with c2:
        fig = go.Figure(go.Scatter(x=years, y=prev, mode="lines", fill="tozeroy"))
        fig.update_layout(height=260, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="Années",
                          yaxis_title="Prévalence (pour 1000)")
        st.plotly_chart(fig, width="stretch")
        st.metric("Prévalence à l'équilibre", f"≈ {inc * dur:.0f} pour 1000")
    ui.warn("Ne confonds pas : « 10 % des adultes **ont** mal au dos aujourd'hui » est une **prévalence** ; « 2 % des "
            "adultes **commencent** une lombalgie chaque mois » est une **incidence**.")
    ui.md(r"""
**Santé publique et pays à revenus faibles** : la charge des maladies y est différente (infections, malnutrition,
traumatismes), l'accès à la réadaptation très limité. L'OMS estime qu'environ une personne sur trois dans le monde
aurait besoin de réadaptation au cours de sa vie (initiative « Réadaptation 2030 »).
""")


def ch_belgique():
    ui.md(r"""
**La sécurité sociale** belge protège contre les risques de la vie : maladie et invalidité, chômage, pensions,
accidents du travail, maladies professionnelles, allocations familiales, vacances annuelles. Elle est financée par
les cotisations sociales et l'impôt.

**L'assurance soins de santé**
- L'**[[inami|INAMI]]** organise le système : il fixe la **[[nomenclature]]** (liste des prestations remboursables
  avec leurs codes et tarifs), négocie avec les représentants des prestataires et des mutualités, et contrôle.
- Chaque personne est affiliée à une **[[mutualité]]**, qui rembourse les soins.
- Le patient paie un **[[ticket modérateur]]**, réduit pour les **[[bim|BIM]]** (intervention majorée). Le
  **maximum à facturer** plafonne ce que dépense un ménage sur une année.

**La kiné dans la nomenclature** : le remboursement dépend de la **prescription** et de la situation du patient.
Il existe des situations « courantes » (nombre limité de séances remboursées par an) et des **listes de
pathologies** donnant droit à plus de séances : la liste **F** (pathologies aiguës et chroniques, Fa et Fb) et la
liste **E** (pathologies lourdes). Les règles détaillées changent régulièrement : vérifie toujours sur le site de
l'INAMI.

**Exercer** : il faut un **diplôme**, un **visa** (SPF Santé publique), un **agrément**, puis un **numéro INAMI**.
L'**[[axxon|AXXON]]** représente la profession.

**Les risques professionnels** : [[fedris|FEDRIS]] gère les **accidents du travail** (y compris sur le chemin du
travail) et les **maladies professionnelles** (liste reconnue, par exemple certaines atteintes du dos ou des
tendons liées aux vibrations ou aux gestes répétitifs).

**Le handicap** est une compétence des entités fédérées : l'**[[aviq|AVIQ]]** en Wallonie, **[[phare|PHARE]]** à
Bruxelles (COCOF), le VAPH en Flandre.
""")
    ui.tip("Les institutions changent souvent de nom en Belgique (FEDRIS est née en 2017 de la fusion du Fonds des "
           "accidents du travail et du Fonds des maladies professionnelles). Retiens surtout **qui fait quoi**.")


def ch_travail():
    ui.md(r"""
**Les risques professionnels** : physiques (charges, postures, vibrations, gestes répétitifs), chimiques,
biologiques, psychosociaux (stress, burn-out). Les **troubles musculo-squelettiques** (dos, épaule, poignet) sont la
première cause de maladie professionnelle en Europe.

**Prévention au travail** : la loi belge sur le **bien-être au travail** (1996) oblige l'employeur à analyser les
risques et à les prévenir, avec un **conseiller en prévention** et la **médecine du travail**.

**L'[[ergonomie]] d'un poste de travail sur écran**
- Haut de l'écran à hauteur des yeux, à environ une longueur de bras ;
- coudes à 90°, avant-bras soutenus, poignets dans l'axe ;
- pieds à plat, dossier qui soutient le bas du dos ;
- et surtout : **bouger souvent**. La meilleure posture est la suivante.

**Le port de charges** : charge près du corps, jambes fléchies, dos gainé, pas de torsion du tronc, pieds écartés.
Mais les études montrent que la formation seule aux « bonnes postures » prévient peu les lombalgies : il faut
surtout **adapter le travail** (aides techniques, poids des charges, organisation) et garder les travailleurs
**actifs et forts**.

**L'[[interprofessionnalité]]** : le kiné travaille avec le médecin, l'ergothérapeute, l'infirmier, le
psychologue, le logopède… Chacun apporte sa compétence autour d'objectifs **communs** fixés avec le patient.
""")
    ui.memo("La meilleure posture est **la prochaine** : aucune posture n'est mauvaise en soi, c'est l'immobilité "
            "prolongée qui pose problème.")


CHAPTERS = [
    ("Modèles de la santé", ch_modeles),
    ("Promotion et prévention", ch_prevention),
    ("Épidémiologie", ch_epidemio),
    ("Le système belge", ch_belgique),
    ("Santé au travail et ergonomie", ch_travail),
]


def _q_prev(rng):
    t, good = rng.choice(PREVENTION)
    return (f"Quel niveau de prévention ? {t}", good, ["Primaire", "Secondaire", "Tertiaire", "Quaternaire"], "")


def _q_prevalence(rng):
    inc = rng.choice([2, 5, 10, 20])
    dur = rng.choice([0.5, 2, 5, 10])
    return dict(prompt=f"Une maladie stable a une incidence de {inc} nouveaux cas pour 1000 personnes par an et dure en "
                       f"moyenne {dur} ans. Quelle est sa prévalence approximative (pour 1000) ?",
                answer=inc * dur, unit="pour 1000", tol=0.02, why=f"P ≈ I × D = {inc} × {dur} = {inc * dur:g} pour 1000.")


def _q_incidence(rng):
    pop = rng.choice([2000, 5000, 10000])
    new = rng.choice([20, 50, 100])
    return dict(prompt=f"Sur une année, {new} nouveaux cas de tendinopathie apparaissent dans une population de {pop} "
                       f"coureurs. Quelle est l'incidence annuelle (en %) ?",
                answer=new / pop * 100, unit="%", tol=0.02, why=f"{new}/{pop} = {new / pop * 100:.2g} %.")


QUESTIONS = [
    gen_qcm(1, _q_prev),
    qcm(1, "Qui a proposé le modèle biopsychosocial ?", "George Engel (1977)", ["Sigmund Freud", "Hippocrate", "Louis Pasteur"]),
    qcm(1, "La prévalence mesure…", "tous les cas présents à un moment donné", ["les nouveaux cas sur une période",
        "les décès", "les guérisons"]),
    vf(1, "En Belgique, l'INAMI fixe la nomenclature des prestations remboursables.", True),
    qcm(1, "Le ticket modérateur est…", "la part du tarif qui reste à charge du patient",
        ["la prescription du médecin", "le salaire du kiné", "une amende"]),
    table_qcm(2, ACTEURS, "Quel est le rôle de : **{k}** ?", "Quel organisme : {v} ?"),
    qcm(2, "Quel document a fondé la promotion de la santé (OMS, 1986) ?", "La Charte d'Ottawa",
        ["La Déclaration d'Helsinki", "Le serment d'Hippocrate", "Le rapport Brundtland"]),
    multi(2, "Quelles composantes décrit la CIF ?", ["Fonctions et structures", "Activités", "Participation",
          "Facteurs environnementaux"], ["Revenus du soignant"]),
    num(2, _q_incidence),
    qcm(2, "Quelle est la première cause de maladie professionnelle en Europe ?", "Les troubles musculo-squelettiques",
        ["Les allergies", "Les accidents de la route", "Les infections"]),
    num(3, _q_prevalence),
    qcm(3, "Une maladie a une incidence élevée mais une prévalence faible. Qu'en déduire ?",
        "Elle est de courte durée (guérison rapide ou décès)", ["Elle est chronique", "Elle est très rare",
        "L'incidence a été mal mesurée"], "Prévalence ≈ incidence × durée."),
    qcm(3, "Un patient lombalgique aigu sans drapeau rouge réclame une IRM. Ne pas la prescrire relève de…",
        "la prévention quaternaire", ["la prévention primaire", "la prévention secondaire", "la négligence"]),
    qcm(3, "Pourquoi la formation aux « bonnes postures » ne suffit-elle pas à prévenir les lombalgies au travail ?",
        "Il faut surtout adapter le travail (charges, aides techniques, organisation) et garder les travailleurs actifs",
        ["Parce que les postures n'ont aucune importance", "Parce que les lombalgies sont génétiques",
         "Parce que les formations sont interdites"]),
    qcm(3, "Un ouvrier se blesse au dos sur le chemin du travail. Quel organisme est concerné ?",
        "FEDRIS (accident du travail, chemin du travail inclus)", ["L'AVIQ", "AXXON", "Le SPF Finances"]),
]

CARDS = [
    ("Modèle biopsychosocial", "Engel 1977 : biologique + psychologique + social"),
    ("Charte d'Ottawa", "Promotion de la santé (OMS, 1986)"),
    ("Prévention primaire", "Éviter l'apparition"),
    ("Prévention secondaire", "Dépister tôt"),
    ("Prévention tertiaire", "Limiter les conséquences"),
    ("Prévention quaternaire", "Éviter les soins inutiles"),
    ("Incidence", "Nouveaux cas / population à risque / période"),
    ("Prévalence", "Tous les cas à un moment / population"),
    ("Relation prévalence-incidence", "P ≈ I × durée"),
    ("INAMI", "Remboursements, nomenclature, tarifs"),
    ("FEDRIS", "Accidents du travail et maladies professionnelles"),
    ("AVIQ / PHARE", "Handicap en Wallonie / à Bruxelles"),
    ("BIM", "Bénéficiaire de l'intervention majorée"),
    ("Pour exercer la kiné en Belgique", "Diplôme, visa, agrément, numéro INAMI"),
]

VIDEOS = [
    ("Le système de santé belge expliqué", "système de soins de santé belge INAMI mutualité explication"),
    ("Le modèle biopsychosocial", "modèle biopsychosocial Engel explication"),
    ("Incidence et prévalence", "incidence prévalence épidémiologie explication"),
    ("Les niveaux de prévention", "prévention primaire secondaire tertiaire quaternaire"),
]

LINKS = [
    ("INAMI : kinésithérapeutes", "https://www.inami.fgov.be/fr/professionnels/professionnels-de-la-sante/kinesitherapeutes"),
    ("FEDRIS", "https://www.fedris.be/fr"),
    ("AXXON", "https://axxon.be/"),
]
