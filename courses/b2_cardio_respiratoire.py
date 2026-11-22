"""LKNR1205 Pathologies et kinésithérapie du système cardio-respiratoire."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from app import ui
from app.course import Course
from app.quiz import gen_qcm, multi, num, qcm, table_qcm, vf

COURSE = Course(
    code="LKNR1205", title="Pathologies et kinésithérapie du système cardio-respiratoire", short="Cardio-respiratoire",
    bloc=2, quad=2, credits=5, hours="45 h + 22,5 h", icon=":material/pulmonology:",
    intro="Comprendre comment on respire et ce qui se dérègle (BPCO, asthme, encombrement, maladies restrictives), "
          "évaluer un patient (spirométrie, examen clinique), et choisir les techniques de kiné respiratoire et de "
          "réadaptation cardiaque, en les analysant de façon critique.",
    acquis=[
        "Décrire l'épidémiologie, la physiopathologie et la présentation clinique (y compris chez l'enfant et la personne âgée).",
        "Réaliser l'examen clinique et le diagnostic kiné ; référer si nécessaire ; établir un pronostic.",
        "Choisir les actes techniques, exercices et l'éducation thérapeutique.",
        "Appliquer les règles d'hygiène des actes respiratoires.",
        "Analyser et ressentir des patterns respiratoires.",
    ],
)

TERMS = {
    "spirométrie": ("Spirométrie", "Mesure des volumes et des débits d'air lors d'une expiration forcée.", "Spirométrie"),
    "cvf": ("CVF", "Capacité vitale forcée : volume total expiré lors d'une expiration forcée après une inspiration "
            "maximale.", None),
    "tiffeneau": ("Rapport de Tiffeneau", "VEMS/CVF. Inférieur à 0,70 (ou à la limite inférieure de la normale), il "
                  "signe une obstruction bronchique.", "Coefficient de Tiffeneau"),
    "syndrome obstructif": ("Syndrome obstructif", "Les bronches sont rétrécies : l'air sort lentement. VEMS/CVF bas "
                            "(BPCO, asthme).", None),
    "syndrome restrictif": ("Syndrome restrictif", "Le poumon ou le thorax se distend mal : les volumes sont petits "
                            "mais le rapport VEMS/CVF est normal (fibrose, maladies neuromusculaires, obésité).", None),
    "encombrement": ("Encombrement bronchique", "Accumulation de sécrétions dans les bronches (mucoviscidose, "
                     "bronchiectasies, BPCO en exacerbation, post-opératoire).", None),
    "afe": ("Augmentation du flux expiratoire (AFE)", "Technique de désencombrement qui modifie la vitesse "
            "d'expiration pour mobiliser les sécrétions.", None),
    "drainage autogène": ("Drainage autogène", "Technique où le patient respire à différents volumes pulmonaires "
                          "pour décoller puis remonter les sécrétions, de façon autonome.", None),
    "mmrc": ("Échelle mMRC", "Échelle de dyspnée de 0 (essoufflé seulement à l'effort intense) à 4 (trop essoufflé "
             "pour quitter la maison ou s'habiller).", None),
    "réhabilitation respiratoire": ("Réhabilitation respiratoire", "Programme global (exercice, éducation, soutien) "
                                    "pour les patients respiratoires chroniques ; améliore la dyspnée, la tolérance "
                                    "à l'effort et la qualité de vie.", "Réhabilitation respiratoire"),
    "bronchiolite": ("Bronchiolite", "Infection virale des petites bronches du nourrisson (souvent le VRS).", "Bronchiolite"),
    "réadaptation cardiaque": ("Réadaptation cardiaque", "Programme d'exercices, d'éducation et de gestion des "
                               "facteurs de risque après un événement cardiaque.", "Réadaptation cardiaque"),
}

MMRC = {0: "Essoufflé seulement lors d'un effort intense", 1: "Essoufflé en marchant vite à plat ou en montant une légère pente",
        2: "Marche plus lentement que les gens de son âge, ou doit s'arrêter à son propre rythme",
        3: "S'arrête pour respirer après environ 100 m ou quelques minutes", 4: "Trop essoufflé pour sortir ou pour s'habiller"}


def ch_mecanique():
    ui.md(r"""
**La pompe ventilatoire** : les muscles inspiratoires (surtout le **diaphragme**, aidé par les intercostaux externes
et, à l'effort ou en détresse, par les muscles accessoires : scalènes, sterno-cléido-mastoïdiens) créent une
dépression qui fait entrer l'air. L'expiration de repos est passive ; l'expiration active utilise les abdominaux.

**Deux grandes difficultés**
- vaincre la **résistance des voies aériennes** (bronches rétrécies) ;
- distendre un poumon ou un thorax **rigide** (compliance diminuée).

**La sémiologie respiratoire** : fréquence respiratoire (12 à 20/min au repos chez l'adulte), utilisation des
muscles accessoires, tirage, cyanose, toux (sèche ou productive), expectorations (couleur, quantité), dyspnée
(échelle [[mmrc|mMRC]], Borg), saturation (SpO₂), auscultation (murmure vésiculaire, sibilances, crépitants,
ronchi).
""")
    ui.table([[k, v] for k, v in MMRC.items()], headers=["mMRC", "Description"])
    ui.tip("Pour « ressentir » un pattern obstructif : inspire normalement, puis expire à travers une paille fine. "
           "L'expiration devient longue et pénible, et tu as tendance à garder de l'air : c'est la **distension** du "
           "patient BPCO.")


def ch_spiro():
    ui.md(r"""
**La [[spirométrie]]** : le patient inspire au maximum puis souffle le plus fort et le plus longtemps possible.
On mesure la [[cvf|CVF]] et le [[vems|VEMS]], et on calcule le [[tiffeneau|rapport de Tiffeneau]] VEMS/CVF.

| Profil | VEMS/CVF | CVF | Exemples |
|---|---|---|---|
| Normal | ≥ 0,70 | ≥ 80 % prédit | |
| [[syndrome obstructif\|Obstructif]] | **< 0,70** | normale ou ↓ | BPCO, asthme (réversible sous bronchodilatateur) |
| [[syndrome restrictif\|Restrictif]] (suspicion) | normal ou ↑ | **< 80 %** | fibrose, maladies neuromusculaires, déformation thoracique, obésité |
""")
    st.markdown("#### À toi : le spiromètre virtuel")
    c1, c2 = st.columns([1, 2])
    with c1:
        cvf = st.slider("CVF (% de la valeur prédite)", 30, 130, 95, key="cr_cvf")
        ratio = st.slider("VEMS/CVF", 0.30, 0.95, 0.80, 0.01, key="cr_ratio")
        pred = 4.5
    cvf_l = pred * cvf / 100
    vems_l = cvf_l * ratio
    t = np.linspace(0, 6, 300)
    k = -np.log(1 - ratio) if ratio < 0.999 else 5
    vol = cvf_l * (1 - np.exp(-k * t))
    with c2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=t, y=pred * (1 - np.exp(-1.9 * t)), name="Normal prédit", line=dict(dash="dot")))
        fig.add_trace(go.Scatter(x=t, y=vol, name="Patient"))
        fig.add_trace(go.Scatter(x=[1], y=[vems_l], mode="markers", marker=dict(size=11), name="VEMS (à 1 s)"))
        fig.update_layout(height=290, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="Temps (s)",
                          yaxis_title="Volume expiré (L)", legend=dict(orientation="h", y=-0.25))
        st.plotly_chart(fig, width="stretch")
    if ratio < 0.70:
        st.error(f"VEMS/CVF = {ratio:.2f} < 0,70 : **syndrome obstructif**. Le VEMS vaut {vems_l / (0.8 * pred):.0%} du prédit "
                 f"(VEMS prédit simplifié ici à 80 % de la CVF prédite).")
    elif cvf < 80:
        st.warning(f"Rapport normal ({ratio:.2f}) mais CVF à {cvf} % : **suspicion de syndrome restrictif** (à confirmer "
                   "par la mesure de la capacité pulmonaire totale).")
    else:
        st.success("Spirométrie normale.")
    ui.warn("Le seuil fixe de 0,70 surestime l'obstruction chez les personnes âgées : les recommandations récentes "
            "préfèrent la **limite inférieure de la normale**. Pour un examen de bloc 2, retiens 0,70.")


def ch_syndromes():
    ui.md(r"""
**[[bpco|BPCO]]** : surtout due au **tabac**. Obstruction persistante, toux et expectorations chroniques,
dyspnée d'effort qui s'aggrave, exacerbations. Spirale du déconditionnement : essoufflé → moins actif →
muscles plus faibles → encore plus essoufflé. La [[réhabilitation respiratoire]] est l'un des traitements les
plus efficaces de la BPCO.

**Asthme** : inflammation bronchique, obstruction **variable et réversible**, crises déclenchées par allergènes,
effort, froid. Le kiné éduque (inhalateurs, reconnaissance des crises), encourage l'activité physique.

**[[encombrement|Encombrement bronchique]]** : mucoviscidose (maladie génétique, kiné quotidienne), bronchiectasies,
post-opératoire, patients neuromusculaires qui toussent mal.

**Syndromes restrictifs** : fibrose pulmonaire, maladies neuromusculaires (SLA, myopathies), cyphoscoliose, obésité.

**Insuffisance respiratoire** : quand les échanges ne suffisent plus (hypoxémie, parfois hypercapnie) ; peut
nécessiter oxygénothérapie ou ventilation non invasive.

**Chez l'enfant** : la [[bronchiolite]] du nourrisson ; les recommandations actuelles ne soutiennent **pas** la
kiné respiratoire de routine dans la bronchiolite, sauf situations particulières. Chez la **personne âgée** : moins
de réserve, toux moins efficace, risque de pneumopathie d'inhalation.
""")


def ch_techniques():
    ui.md(r"""
**Buts de la kiné respiratoire** : désencombrer, améliorer la ventilation, diminuer le travail respiratoire,
améliorer la tolérance à l'effort, éduquer.

| Technique | Principe | Indication |
|---|---|---|
| [[afe\|AFE]] (augmentation du flux expiratoire) | modifier la vitesse de l'expiration pour déplacer les sécrétions | encombrement |
| [[drainage autogène\|Drainage autogène]] | respirer à bas, moyen puis haut volume pulmonaire | encombrement, autonomie du patient (mucoviscidose) |
| ELTGOL | expiration lente, glotte ouverte, couché sur le côté | sécrétions périphériques |
| Toux dirigée, huffing | expiration forcée glotte ouverte | évacuer les sécrétions proximales |
| PEP (pression expiratoire positive), flutter | expirer contre une résistance qui garde les bronches ouvertes | encombrement |
| Ventilation dirigée, lèvres pincées | ralentir et allonger l'expiration | BPCO, dyspnée |
| Spirométrie incitative | inspirations profondes guidées | post-opératoire (prévention des atélectasies) |
| Entraînement à l'effort | aérobie + renforcement | BPCO, insuffisance cardiaque, presque tous |
""")
    ui.tip("Le niveau de preuve des techniques de désencombrement est souvent **modeste**. Celui de "
           "l'**entraînement à l'effort** (réhabilitation) est **élevé**. Ton raisonnement critique doit en tenir compte.")
    ui.clinic("**Hygiène** : masque chirurgical (ou FFP2 selon le germe), protection des yeux en cas de toux "
              "provoquée, mouchoirs et crachoirs, désinfection du matériel (embouts, PEP individuels), hygiène des "
              "mains avant et après. La toux projette des gouttelettes.")


def ch_cardiaque():
    ui.md(r"""
**La même démarche pour le cœur** : cardiopathie ischémique (angor, infarctus), insuffisance cardiaque, après
chirurgie cardiaque (pontage, valve).

**La [[réadaptation cardiaque]]** se fait en phases :
1. **Phase I** (hospitalisation) : mobilisation précoce, lever, marche, éducation.
2. **Phase II** (quelques semaines à quelques mois, en centre ou en ambulatoire) : entraînement supervisé
   (aérobie + renforcement), éducation sur les facteurs de risque (tabac, alimentation, stress), retour au travail.
3. **Phase III** (à vie) : maintien de l'activité physique en autonomie.

Elle réduit la mortalité cardiovasculaire et les réhospitalisations, et améliore la qualité de vie.

**Doser l'effort** : à partir d'une épreuve d'effort (FC, puissance, seuil), ou de la méthode de Karvonen (40 à
80 % de la FC de réserve), ou de l'échelle de **Borg** (12 à 14 sur 20, « un peu difficile »), surtout sous
bêtabloquants.

**Signes d'arrêt** : douleur thoracique, dyspnée disproportionnée, malaise, vertiges, pâleur, chute de la pression
à l'effort, troubles du rythme.
""")
    ui.warn("Une douleur thoracique pendant l'effort chez un patient cardiaque : on arrête immédiatement, on le met au "
            "repos, on alerte. On ne « termine » jamais la série.")


CHAPTERS = [
    ("Mécanique et sémiologie", ch_mecanique),
    ("La spirométrie", ch_spiro),
    ("Grands syndromes respiratoires", ch_syndromes),
    ("Techniques de kiné respiratoire", ch_techniques),
    ("Le cœur et la réadaptation cardiaque", ch_cardiaque),
]


def _q_spiro(rng):
    cvf = rng.choice([60, 70, 90, 100, 110])
    ratio = rng.choice([0.50, 0.60, 0.65, 0.78, 0.85])
    if ratio < 0.70:
        good = "Syndrome obstructif"
    elif cvf < 80:
        good = "Suspicion de syndrome restrictif"
    else:
        good = "Spirométrie normale"
    return (f"CVF = {cvf} % du prédit, VEMS/CVF = {ratio:.2f}. Interprétation ?", good,
            ["Syndrome obstructif", "Suspicion de syndrome restrictif", "Spirométrie normale"], "Tiffeneau < 0,70 → obstructif ; rapport normal et CVF < 80 % → restrictif suspecté.")


def _q_tiff(rng):
    vems = rng.choice([1.2, 1.8, 2.4, 3.0, 3.4])
    cvf = rng.choice([3.0, 3.5, 4.0, 4.5])
    return dict(prompt=f"VEMS = {vems} L et CVF = {cvf} L. Calcule le rapport de Tiffeneau (VEMS/CVF).",
                answer=vems / cvf, tol=0.01, why=f"{vems}/{cvf} = {vems / cvf:.2f} ({'obstructif' if vems / cvf < 0.7 else 'pas d obstruction'}).")


QUESTIONS = [
    qcm(1, "Quel est le muscle principal de l'inspiration ?", "Le diaphragme", ["Les abdominaux", "Le grand dorsal", "Le trapèze"]),
    qcm(1, "Le rapport de Tiffeneau, c'est…", "VEMS / CVF", ["CVF / VEMS", "FC / FR", "VEMS × CVF"]),
    table_qcm(1, {str(k): v for k, v in MMRC.items()}, "Que décrit le stade mMRC **{k}** ?", "Quel stade mMRC : « {v} » ?"),
    vf(1, "L'obstruction de l'asthme est en général réversible.", True),
    qcm(1, "Quelle est la cause principale de la BPCO ?", "Le tabac", ["Le sport", "L'asthme de l'enfance", "Les allergies"]),
    gen_qcm(2, _q_spiro),
    num(2, _q_tiff),
    qcm(2, "Quel traitement de la BPCO a le plus haut niveau de preuve en kiné ?", "La réhabilitation respiratoire (entraînement à l'effort)",
        ["Le clapping", "Le massage thoracique", "Le repos"]),
    multi(2, "Quelles techniques visent le désencombrement ?", ["AFE", "Drainage autogène", "ELTGOL"],
          ["Lèvres pincées seules", "Spirométrie incitative"]),
    qcm(2, "Quelles sont les phases de la réadaptation cardiaque ?", "Hospitalisation, entraînement supervisé, maintien à vie",
        ["Diagnostic, chirurgie, repos", "Repos, repos, reprise", "Une seule séance d'éducation"]),
    qcm(3, "Un patient atteint de SLA a une CVF à 55 % et un VEMS/CVF à 0,85. Interprétation ?",
        "Profil restrictif (faiblesse des muscles respiratoires)", ["Profil obstructif", "Spirométrie normale", "Asthme"]),
    qcm(3, "Pendant un exercice, un patient cardiaque signale une douleur thoracique. Que faire ?",
        "Arrêter immédiatement, mettre au repos et alerter", ["Finir la série", "Diminuer un peu la vitesse et continuer",
        "Boire de l'eau et reprendre"]),
    qcm(3, "Comment doser l'effort d'un patient cardiaque sous bêtabloquants ?", "Avec l'échelle de Borg (12 à 14/20) ou les données d'une épreuve d'effort",
        ["Avec 220 − âge", "Au maximum dès la 1re séance", "Uniquement avec la saturation"]),
    qcm(3, "Pourquoi le patient BPCO pince-t-il les lèvres à l'expiration ?",
        "Pour maintenir une pression qui garde les petites bronches ouvertes et vider mieux les poumons",
        ["Pour inspirer plus vite", "Pour tousser", "Par habitude sans effet"]),
    qcm(3, "Quel est l'intérêt de la spirométrie incitative après une chirurgie abdominale ?",
        "Favoriser les inspirations profondes pour prévenir les atélectasies", ["Désencombrer les bronches proximales",
        "Mesurer le VEMS", "Renforcer les abdominaux"]),
]

CARDS = [
    ("Tiffeneau", "VEMS/CVF ; < 0,70 = obstructif"),
    ("Syndrome restrictif", "CVF ↓, rapport normal (fibrose, neuromusculaire)"),
    ("mMRC", "Échelle de dyspnée de 0 à 4"),
    ("BPCO", "Obstruction persistante, tabac ; réhabilitation = traitement clé"),
    ("Asthme", "Obstruction variable et réversible"),
    ("AFE", "Modifier la vitesse d'expiration pour déplacer les sécrétions"),
    ("Drainage autogène", "Respirer à bas, moyen, haut volume ; autonomie"),
    ("Lèvres pincées", "Freiner l'expiration, garder les bronches ouvertes"),
    ("Spirométrie incitative", "Post-op : prévenir les atélectasies"),
    ("Réadaptation cardiaque", "Phase I hôpital, II supervisée, III maintien"),
    ("Borg pour le cardiaque", "12 à 14 sur 20"),
    ("Fréquence respiratoire normale (adulte)", "12 à 20 / min"),
]

VIDEOS = [
    ("Comprendre la spirométrie", "spirométrie interprétation VEMS CVF Tiffeneau"),
    ("Techniques de désencombrement bronchique", "kiné respiratoire désencombrement AFE drainage autogène"),
    ("La réhabilitation respiratoire dans la BPCO", "réhabilitation respiratoire BPCO"),
    ("La réadaptation cardiaque", "réadaptation cardiaque phases"),
]

LINKS = [("GOLD : recommandations BPCO", "https://goldcopd.org/")]
