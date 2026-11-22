"""LKNR1207 Introduction à la pathologie."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from app import ui
from app.course import Course
from app.quiz import gen_qcm, multi, num, qcm, table_qcm, vf

COURSE = Course(
    code="LKNR1207", title="Introduction à la pathologie", short="Introduction à la pathologie",
    bloc=2, quad=2, credits=3, hours="30 h", icon=":material/medical_information:",
    intro="Les grands mécanismes de la maladie (tumeurs, inflammation, auto-immunité, infections, troubles "
          "métaboliques), la composition corporelle comme paramètre du soin (obésité, sarcopénie, ostéoporose), "
          "et comment raisonner chez un patient qui cumule plusieurs maladies.",
    acquis=[
        "Décrire les différents aspects des pathologies.",
        "Mobiliser les sciences fondamentales pour évaluer la personne (vignettes).",
        "Intégrer les informations de l'anamnèse et évaluer l'état de santé.",
        "Connaître les principes du dépistage (screening).",
    ],
)

TERMS = {
    "imc": ("IMC", "Indice de masse corporelle : poids (kg) / taille² (m²). Normal entre 18,5 et 25 chez l'adulte.",
            "Indice de masse corporelle"),
    "tour de taille": ("Tour de taille", "Mesure de la graisse abdominale, plus liée au risque cardiovasculaire que "
                       "l'IMC. Risque accru au-delà de 94 cm (homme) et 80 cm (femme) selon l'OMS.", None),
    "syndrome métabolique": ("Syndrome métabolique", "Association d'obésité abdominale, hypertension, glycémie "
                             "élevée et troubles des lipides, qui multiplie le risque cardiovasculaire et de diabète.",
                             "Syndrome métabolique"),
    "diabète de type 2": ("Diabète de type 2", "Hyperglycémie chronique due surtout à une résistance à l'insuline, "
                          "favorisée par la sédentarité et l'excès de poids.", "Diabète de type 2"),
    "diabète de type 1": ("Diabète de type 1", "Destruction auto-immune des cellules du pancréas qui fabriquent "
                          "l'insuline ; traitement par insuline à vie.", "Diabète de type 1"),
    "hta": ("Hypertension artérielle", "Pression artérielle de repos ≥ 140/90 mmHg (au cabinet), de façon répétée.",
            "Hypertension artérielle"),
    "ostéoporose": ("Ostéoporose", "Diminution de la masse et de la qualité de l'os qui augmente le risque de "
                    "fracture. Diagnostic : T-score ≤ −2,5 à la densitométrie.", "Ostéoporose"),
    "tumeur maligne": ("Tumeur maligne (cancer)", "Prolifération de cellules anormales qui envahit les tissus voisins "
                       "et peut donner des métastases.", "Cancer"),
    "métastase": ("Métastase", "Foyer de cancer à distance de la tumeur d'origine (os, poumon, foie, cerveau).", "Métastase"),
    "auto-immunité": ("Maladie auto-immune", "Le système immunitaire attaque les tissus de l'organisme (polyarthrite "
                      "rhumatoïde, diabète de type 1, SEP).", "Maladie auto-immune"),
    "iatrogène": ("Iatrogène", "Causé par un soin ou un médicament (effet indésirable, infection liée aux soins).",
                  "Iatrogénèse"),
    "valeur prédictive positive": ("Valeur prédictive positive", "Probabilité d'être malade quand le test est "
                                   "positif. Elle dépend de la prévalence de la maladie.", "Valeur prédictive"),
    "multimorbidité": ("Multimorbidité", "Présence de plusieurs maladies chroniques chez une même personne.", None),
}

TAA = [(0, 120, 80, "Optimale"), (1, 130, 85, "Normale"), (2, 140, 90, "Normale haute"), (3, 160, 100, "HTA grade 1"),
       (4, 180, 110, "HTA grade 2"), (5, 999, 999, "HTA grade 3")]


def ch_composition():
    ui.md(r"""
La masse et la composition du corps changent la façon de soigner : charge sur les articulations, tolérance à
l'effort, dosage des exercices, risques associés.

L'[[imc|IMC]] est simple mais imparfait : il ne distingue pas le muscle de la graisse (un rugbyman peut être
« obèse » selon l'IMC). Le [[tour de taille]] renseigne sur la graisse **abdominale**, la plus dangereuse.
""")
    st.markdown("#### À toi : IMC et tour de taille")
    c1, c2 = st.columns([1, 2])
    with c1:
        poids = st.slider("Poids (kg)", 35, 160, 70, key="ip_poids")
        taille = st.slider("Taille (cm)", 140, 210, 170, key="ip_taille")
        sexe = st.radio("Sexe", ["Femme", "Homme"], horizontal=True, key="ip_sexe")
        tt = st.slider("Tour de taille (cm)", 55, 160, 80, key="ip_tt")
    imc = poids / (taille / 100) ** 2
    classes = [(18.5, "Maigreur"), (25, "Corpulence normale"), (30, "Surpoids"), (35, "Obésité classe I"),
               (40, "Obésité classe II"), (999, "Obésité classe III")]
    cls = next(n for lim, n in classes if imc < lim)
    seuil = 80 if sexe == "Femme" else 94
    with c2:
        st.metric("IMC", f"{imc:.1f} kg/m²", help=cls)
        st.markdown(f"Catégorie : **{cls}**.")
        if tt >= seuil + (8 if sexe == "Femme" else 8):
            st.error(f"Tour de taille {tt} cm : risque cardio-métabolique **nettement augmenté**.")
        elif tt >= seuil:
            st.warning(f"Tour de taille {tt} cm : risque **augmenté** (seuil OMS : {seuil} cm).")
        else:
            st.success(f"Tour de taille sous le seuil de risque ({seuil} cm).")
    ui.md(r"""
**L'obésité** s'accompagne souvent de [[diabète de type 2]], d'[[hta|hypertension]], d'arthrose (genou), d'apnées
du sommeil : c'est le [[syndrome métabolique]]. L'exercice améliore ces facteurs **même sans perte de poids**.

**La maigreur** chez la personne âgée annonce souvent la **sarcopénie** et l'**[[ostéoporose]]** (T-score ≤ −2,5),
avec un risque de fracture (poignet, vertèbres, col du fémur). Le renforcement et les exercices en charge
protègent l'os.
""")
    ui.clinic("Chez un patient diabétique sous insuline ou sulfamides : vérifier la glycémie avant l'effort, avoir du "
              "sucre à portée de main, connaître les signes d'**hypoglycémie** (tremblements, sueurs, pâleur, confusion). "
              "Et surveiller les **pieds** (neuropathie, plaies).")


def ch_processus():
    ui.md(r"""
**Les grands types de processus pathologiques**

| Processus | Mécanisme | Exemples |
|---|---|---|
| Inflammatoire | réaction de défense : rougeur, chaleur, gonflement, douleur, perte de fonction | entorse, bursite, arthrite |
| [[auto-immunité\|Auto-immun]] | l'immunité attaque le soi | polyarthrite rhumatoïde, spondylarthrite, diabète de type 1 |
| Infectieux | bactéries, virus, champignons | pneumonie, arthrite septique, COVID-19 |
| Tumoral | prolifération cellulaire anormale, bénigne ou [[tumeur maligne\|maligne]] | lipome (bénin), cancer du sein, myélome |
| Métabolique | dérèglement du métabolisme | diabète, goutte, ostéoporose |
| Toxique et [[iatrogène]] | substance ou soin | alcool, effets indésirables des corticoïdes, chute sous somnifère |
| Dégénératif | usure, vieillissement des tissus | arthrose, maladies neurodégénératives |
| Vasculaire | défaut d'irrigation | infarctus, AVC, artériopathie |
""")
    ui.memo("Les 5 signes de l'inflammation en latin : **rubor** (rougeur), **calor** (chaleur), **tumor** (gonflement), "
            "**dolor** (douleur), **functio laesa** (perte de fonction).")
    ui.md(r"""
**Bénin ou malin ?** Une tumeur bénigne grossit lentement, reste bien limitée et ne donne pas de métastases. Une
tumeur maligne envahit et peut donner des [[métastase|métastases]], souvent **osseuses** (sein, prostate, poumon,
rein, thyroïde) : d'où l'importance des drapeaux rouges devant une douleur osseuse ou rachidienne.
""")
    ui.clinic("Une douleur inflammatoire est souvent **nocturne** et **matinale**, avec une raideur de plus de 30 minutes "
              "qui s'améliore en bougeant (spondylarthrite) ; une douleur mécanique augmente à l'effort et se calme au "
              "repos. Cette différence oriente toute l'anamnèse.")


def ch_depistage():
    ui.md(r"""
**Le dépistage (screening)** cherche une maladie chez des personnes **sans symptômes**. Il n'est utile que si la
maladie est fréquente et grave, si on dispose d'un test fiable et acceptable, et si un traitement précoce change
l'évolution (critères de Wilson et Jungner, OMS).

Le piège : même un bon test donne beaucoup de **faux positifs** quand la maladie est **rare**. La [[valeur prédictive positive]]
dépend de la prévalence.
""")
    st.markdown("#### À toi : le paradoxe du dépistage")
    c1, c2 = st.columns([1, 2])
    with c1:
        prev = st.slider("Prévalence de la maladie (%)", 0.1, 50.0, 1.0, 0.1, key="ip_prev") / 100
        se = st.slider("Sensibilité du test (%)", 50, 100, 90, key="ip_se") / 100
        sp = st.slider("Spécificité du test (%)", 50, 100, 95, key="ip_sp") / 100
    n = 10000
    malades = prev * n
    vp, fn = se * malades, (1 - se) * malades
    fp, vn = (1 - sp) * (n - malades), sp * (n - malades)
    vpp = vp / (vp + fp) if vp + fp else 0
    vpn = vn / (vn + fn) if vn + fn else 0
    with c2:
        k1, k2 = st.columns(2)
        k1.metric("Valeur prédictive positive", f"{vpp:.0%}")
        k2.metric("Valeur prédictive négative", f"{vpn:.1%}")
        st.markdown(f"Sur {n:,} personnes : **{vp:.0f}** vrais positifs et **{fp:.0f}** faux positifs.".replace(",", " "))
        xs = np.linspace(0.001, 0.5, 200)
        vpps = se * xs / (se * xs + (1 - sp) * (1 - xs))
        fig = go.Figure(go.Scatter(x=xs * 100, y=vpps * 100, mode="lines"))
        fig.add_trace(go.Scatter(x=[prev * 100], y=[vpp * 100], mode="markers", marker=dict(size=12)))
        fig.update_layout(height=240, margin=dict(l=10, r=10, t=10, b=10), showlegend=False,
                          xaxis_title="Prévalence (%)", yaxis_title="VPP (%)",
                          xaxis_range=[0, 50], yaxis_range=[0, 100])
        ui.chart(fig, "intro_pathologie_0")
    ui.tip("Avec une prévalence de 1 %, un test sensible à 90 % et spécifique à 95 % : sur 100 positifs, seuls 15 "
           "environ sont vraiment malades. C'est pourquoi on ne fait pas passer n'importe quel test à tout le monde.")


def ch_polypathologie():
    ui.md(r"""
**La [[multimorbidité]]** est la règle chez la personne âgée : arthrose + diabète + insuffisance cardiaque +
dépression, par exemple. Chaque maladie modifie la prise en charge des autres, et les traitements interagissent
(polymédication).

**Un cadre de réflexion**
1. **Lister** les problèmes de santé et les traitements (anamnèse, dossier).
2. Pour chacun : quel **impact** sur l'exercice (contre-indications, précautions, dosage) ?
3. Quelles **priorités** pour le patient (ses objectifs à lui) ?
4. Quels **risques** surveiller pendant les séances (glycémie, PA, dyspnée, douleur thoracique, chute) ?
5. Quand **référer** ou communiquer avec le médecin ?

**Les paramètres à connaître avant l'effort**
""")
    ui.table([[n, f"< {s}/{d}" if s < 999 else "≥ 180/110"] for _, s, d, n in TAA], headers=["Catégorie de PA (mmHg, cabinet)", "Seuil"])
    st.caption("Classification européenne (ESH). Les catégories sont définies par la PA systolique et/ou diastolique.")
    ui.md(r"""
- **Glycémie à jeun** normale < 100 mg/dL ; diabète si ≥ 126 mg/dL à deux reprises (ou HbA1c ≥ 6,5 %).
- **Ostéoporose** : T-score ≤ −2,5 ; ostéopénie entre −1 et −2,5.
- **Saturation** normale ≥ 95 % (souvent un peu moins chez le patient BPCO, selon la cible fixée par le médecin).
""")


CHAPTERS = [
    ("Composition corporelle", ch_composition),
    ("Les processus pathologiques", ch_processus),
    ("Le dépistage", ch_depistage),
    ("Polypathologie et paramètres", ch_polypathologie),
]


def _q_imc(rng):
    p = rng.choice([50, 60, 72, 85, 95, 110])
    t = rng.choice([1.55, 1.65, 1.75, 1.85])
    return dict(prompt=f"Calcule l'IMC d'une personne de {p} kg et {t:.2f} m.", answer=p / t ** 2, unit="kg/m²",
                tol=0.01, why=f"{p} / {t}² = {p / t ** 2:.1f} kg/m².")


def _q_vpp(rng):
    prev = rng.choice([0.01, 0.05, 0.10, 0.20])
    se, sp = rng.choice([(0.9, 0.9), (0.95, 0.9), (0.8, 0.95)])
    vpp = se * prev / (se * prev + (1 - sp) * (1 - prev))
    return dict(prompt=f"Prévalence {prev:.0%}, sensibilité {se:.0%}, spécificité {sp:.0%}. Quelle est la valeur "
                       f"prédictive positive (en %) ?",
                answer=vpp * 100, unit="%", tol=0.03,
                why=f"VPP = Se·P / (Se·P + (1−Sp)(1−P)) = {se}×{prev} / ({se}×{prev} + {1 - sp:.2f}×{1 - prev:.2f}) ≈ {vpp:.0%}.")


PROCESSUS = {"Polyarthrite rhumatoïde": "Auto-immun", "Arthrite septique": "Infectieux", "Lipome": "Tumoral (bénin)",
             "Goutte": "Métabolique", "Fracture vertébrale sous corticoïdes au long cours": "Iatrogène",
             "Arthrose": "Dégénératif"}

QUESTIONS = [
    qcm(1, "Quelle est la formule de l'IMC ?", "poids / taille²", ["poids × taille", "taille / poids", "poids / taille"]),
    qcm(1, "Un IMC normal chez l'adulte est compris entre…", "18,5 et 25", ["15 et 20", "25 et 30", "20 et 35"]),
    table_qcm(1, PROCESSUS, "Quel type de processus pathologique : **{k}** ?"),
    vf(1, "Une tumeur bénigne peut donner des métastases.", False),
    qcm(1, "Quel T-score définit l'ostéoporose ?", "≤ −2,5", ["≥ 0", "entre −1 et −2,5", "≤ −5"]),
    num(2, _q_imc),
    multi(2, "Quels sont des signes cardinaux de l'inflammation ?", ["Rougeur", "Chaleur", "Gonflement", "Douleur"],
          ["Pâleur", "Froid"]),
    qcm(2, "Pourquoi le tour de taille complète-t-il l'IMC ?", "Il mesure la graisse abdominale, plus liée au risque cardio-métabolique",
        ["Il mesure la masse musculaire", "Il remplace la pesée", "Il mesure la densité osseuse"]),
    qcm(2, "À partir de quelle PA (cabinet) parle-t-on d'hypertension ?", "140/90 mmHg", ["120/80 mmHg", "130/85 mmHg", "180/110 mmHg"]),
    qcm(2, "Quels cancers donnent souvent des métastases osseuses ?", "Sein, prostate, poumon, rein, thyroïde",
        ["Peau uniquement", "Aucun", "Uniquement les leucémies"]),
    num(3, _q_vpp),
    qcm(3, "Pourquoi un test très spécifique donne-t-il quand même beaucoup de faux positifs dans une population à faible prévalence ?",
        "Parce que le petit pourcentage d'erreurs s'applique à un très grand nombre de personnes saines",
        ["Parce que le test est mauvais", "Parce que la sensibilité est trop haute", "Ce n'est pas possible"]),
    qcm(3, "Un patient diabétique devient pâle, tremblant et confus pendant la séance. Que faire ?",
        "Suspecter une hypoglycémie : arrêter, lui donner du sucre rapide, surveiller", ["Continuer l'exercice",
        "Lui donner de l'insuline", "Le faire courir pour le réveiller"]),
    qcm(3, "Une raideur matinale de 1 h 30 qui s'améliore en bougeant, chez un homme de 28 ans, évoque…",
        "une douleur inflammatoire (spondylarthrite possible), à référer", ["une lombalgie mécanique banale",
        "une arthrose", "une fracture"]),
    qcm(3, "Face à un patient multimorbide, quelle est la première étape ?", "Lister les problèmes de santé et les traitements",
        ["Commencer l'exercice le plus intense", "Traiter uniquement la plainte principale sans autre question",
         "Refuser la prise en charge"]),
]

CARDS = [
    ("IMC", "poids / taille² ; normal 18,5-25"),
    ("Tour de taille à risque (OMS)", "≥ 94 cm (homme), ≥ 80 cm (femme)"),
    ("Hypertension", "≥ 140/90 mmHg au cabinet"),
    ("Diabète", "Glycémie à jeun ≥ 126 mg/dL (2 fois) ou HbA1c ≥ 6,5 %"),
    ("Ostéoporose", "T-score ≤ −2,5"),
    ("Signes de l'inflammation", "Rubor, calor, tumor, dolor, functio laesa"),
    ("Bénin vs malin", "Limité, pas de métastase vs envahit, métastases"),
    ("Métastases osseuses fréquentes", "Sein, prostate, poumon, rein, thyroïde"),
    ("VPP", "Dépend de la prévalence"),
    ("Iatrogène", "Causé par un soin ou un médicament"),
    ("Hypoglycémie", "Tremblements, sueurs, pâleur, confusion → sucre rapide"),
]

VIDEOS = [
    ("Sensibilité, spécificité et valeurs prédictives", "sensibilité spécificité valeur prédictive positive explication"),
    ("L'inflammation expliquée", "inflammation aiguë mécanismes explication"),
    ("Diabète et activité physique", "diabète exercice physique précautions hypoglycémie"),
    ("Ostéoporose et exercice", "ostéoporose exercices recommandations"),
]

LINKS = [("OMS : obésité et surpoids", "https://www.who.int/fr/news-room/fact-sheets/detail/obesity-and-overweight")]
