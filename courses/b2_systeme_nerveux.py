"""LKNR1206 Pathologies et kinésithérapie du système nerveux."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from app import ui
from app.course import Course
from app.quiz import gen_qcm, multi, num, qcm, table_qcm, vf

COURSE = Course(
    code="LKNR1206", title="Pathologies et kinésithérapie du système nerveux", short="Neurologie",
    bloc=2, quad=2, credits=5, hours="30 h + 37,5 h", icon=":material/neurology:",
    intro="AVC, lésions de la moelle, traumatismes crâniens, Parkinson, sclérose en plaques, atteintes "
          "périphériques, myopathies et neuropédiatrie : reconnaître les syndromes, évaluer avec les bonnes "
          "échelles, et rééduquer en s'appuyant sur la plasticité.",
    acquis=[
        "Décrire l'épidémiologie, la physiopathologie et la présentation clinique des pathologies neurologiques.",
        "Utiliser les tests et outils cliniques ; mener l'examen et poser le diagnostic kiné.",
        "Référer si nécessaire, établir un pronostic, évaluer et adapter en continu.",
        "Choisir les actes techniques, exercices et l'éducation thérapeutique selon les stades.",
        "Prendre en compte les troubles associés (sensitifs, visuels, équilibre, déglutition, sphinctériens).",
    ],
)

TERMS = {
    "avc": ("AVC", "Accident vasculaire cérébral : arrêt brutal de la circulation dans une partie du cerveau, par "
            "obstruction (ischémique, ≈ 80 %) ou rupture (hémorragique).", "Accident vasculaire cérébral"),
    "spasticité": ("Spasticité", "Augmentation du tonus qui dépend de la vitesse d'étirement, liée à une lésion du "
                   "motoneurone supérieur (voie pyramidale).", "Spasticité"),
    "rigidité": ("Rigidité", "Augmentation du tonus constante quelle que soit la vitesse, souvent « en roue dentée », "
                 "typique de la maladie de Parkinson.", "Rigidité (neurologie)"),
    "signe de babinski": ("Signe de Babinski", "Extension du gros orteil quand on frotte le bord externe de la plante : "
                          "signe d'atteinte de la voie pyramidale (normal chez le nourrisson).", "Signe de Babinski"),
    "ataxie": ("Ataxie", "Trouble de la coordination des mouvements, sans paralysie (cervelet, proprioception).", "Ataxie"),
    "hémiplégie": ("Hémiplégie", "Paralysie d'une moitié du corps, du côté opposé à la lésion cérébrale.", "Hémiplégie"),
    "asia": ("Échelle ASIA", "Classification des lésions médullaires de A (complète, rien sous la lésion) à E "
             "(normale).", "Échelle de l'ASIA"),
    "glasgow": ("Score de Glasgow", "Évaluation de la conscience de 3 à 15 (yeux, verbal, moteur).", "Échelle de Glasgow"),
    "parkinson": ("Maladie de Parkinson", "Maladie neurodégénérative (perte des neurones à dopamine) : lenteur, "
                  "rigidité, tremblement de repos, troubles de la marche et de l'équilibre.", "Maladie de Parkinson"),
    "sclérose en plaques": ("Sclérose en plaques", "Maladie auto-immune qui détruit la myéline du SNC, souvent par "
                            "poussées, chez le jeune adulte.", "Sclérose en plaques"),
    "paralysie cérébrale": ("Paralysie cérébrale", "Troubles du mouvement et de la posture dus à une lésion du cerveau "
                            "en développement (avant, pendant ou peu après la naissance). Non évolutive.", "Paralysie cérébrale"),
    "ashworth modifiée": ("Échelle d'Ashworth modifiée", "Cotation de la spasticité de 0 (pas d'augmentation du tonus) "
                          "à 4 (segment rigide).", "Échelle d'Ashworth"),
    "freezing": ("Freezing", "Blocage soudain de la marche (« pieds collés au sol ») dans la maladie de Parkinson.", None),
    "cimt": ("CIMT", "Thérapie par contrainte induite : contraindre le membre sain pour forcer l'utilisation intensive "
             "du membre parétique.", None),
}

GCS_Y = {4: "Spontanée", 3: "Au bruit / à la demande", 2: "À la douleur", 1: "Aucune"}
GCS_V = {5: "Orientée", 4: "Confuse", 3: "Mots inappropriés", 2: "Sons incompréhensibles", 1: "Aucune"}
GCS_M = {6: "Obéit aux ordres", 5: "Localise la douleur", 4: "Retrait à la douleur", 3: "Flexion anormale (décortication)",
         2: "Extension anormale (décérébration)", 1: "Aucune"}


def ch_syndromes():
    ui.md(r"""
**Trois grands syndromes moteurs centraux**

| | Pyramidal | Extrapyramidal | Cérébelleux |
|---|---|---|---|
| Lésion | voie corticospinale | noyaux gris centraux | cervelet |
| Tonus | [[spasticité]] (dépend de la vitesse) | [[rigidité]] (constante, roue dentée) | hypotonie |
| Réflexes | vifs, [[signe de babinski\|Babinski]] | normaux | normaux ou pendulaires |
| Mouvement | faiblesse, perte de la sélectivité | lenteur, rareté, tremblement de repos | [[ataxie]], dysmétrie, tremblement d'action |
| Exemple | AVC | Parkinson | lésion cérébelleuse, SEP |
""")
    st.markdown("#### À toi : spasticité ou rigidité ?")
    st.caption("Résistance ressentie quand on étire passivement un muscle, selon la vitesse de l'étirement.")
    v = np.linspace(0, 300, 100)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=v, y=1 + 0.012 * v + 0.00004 * v ** 2, name="Spasticité (pyramidal)"))
    fig.add_trace(go.Scatter(x=v, y=np.full_like(v, 2.6), name="Rigidité (extrapyramidal)"))
    fig.add_trace(go.Scatter(x=v, y=np.full_like(v, 1.0), name="Tonus normal", line=dict(dash="dot")))
    fig.update_layout(height=270, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="Vitesse d'étirement (°/s)",
                      yaxis_title="Résistance (relative)", legend=dict(orientation="h", y=-0.3))
    st.plotly_chart(fig, width="stretch")
    ui.memo("**Spasticité** = **S**peed : plus tu étires **vite**, plus ça résiste (« comme un canif » : ça cède "
            "parfois d'un coup). **Rigidité** = résistance **égale** dans tout le mouvement (« tuyau de plomb », "
            "avec des à-coups en roue dentée).")
    ui.md("Cotation clinique de la spasticité : l'[[ashworth modifiée|échelle d'Ashworth modifiée]] (0, 1, 1+, 2, 3, 4).")


def ch_avc():
    ui.md(r"""
**L'[[avc|AVC]]** : première cause de handicap acquis de l'adulte. Ischémique dans environ 80 % des cas,
hémorragique dans 20 %. Le territoire le plus touché est celui de l'**artère cérébrale moyenne** :
[[hémiplégie]] controlatérale à prédominance brachio-faciale, troubles sensitifs, et selon le côté : **aphasie**
(hémisphère gauche, en général) ou **héminégligence** (hémisphère droit).

**Reconnaître un AVC : « VITE » (FAST en anglais)** : **V**isage paralysé, **I**ncapacité à lever un bras,
**T**rouble de la parole, **E**n urgence : appeler le 112. Chaque minute compte (thrombolyse, thrombectomie).

**La rééducation** s'appuie sur la plasticité : beaucoup de **pratique**, **intensive**, **orientée vers des tâches**
qui ont du sens pour le patient (s'habiller, marcher, prendre un verre). La [[cimt|thérapie par contrainte
induite]] pour le membre supérieur, l'entraînement à la marche (sur tapis, avec ou sans support), l'équilibre. La
récupération est la plus rapide dans les **3 à 6 premiers mois**, mais des progrès restent possibles ensuite.
""")
    ui.clinic("L'épaule de l'hémiplégique est fragile (subluxation, douleur) : on ne tire **jamais** sur le bras "
              "parétique pour aider le patient à se lever ou à se retourner, et on le positionne avec soin.")


def ch_moelle_tc():
    ui.md(r"""
**Les lésions médullaires** : traumatiques (accident, chute, plongeon) ou non (tumeur, ischémie). Le niveau
détermine le tableau : **tétraplégie** (cervicale) ou **paraplégie** (thoracique et en dessous). L'[[asia|échelle
ASIA]] classe la lésion de **A** (complète) à **E** (normale). Au-dessus de C3-C5, le diaphragme est touché
(ventilation assistée).

Complications à prévenir : escarres, troubles respiratoires, raideurs, ostéoporose, troubles urinaires et
intestinaux, **dysréflexie autonome** (au-dessus de T6 : poussée hypertensive brutale déclenchée par une vessie
pleine, une escarre… : urgence).

**Le traumatisme crânien** : de léger (commotion) à grave. On évalue la conscience avec le [[glasgow|score de
Glasgow]] : 13 à 15 = léger, 9 à 12 = modéré, 3 à 8 = grave (coma).
""")
    st.markdown("#### À toi : calcule un score de Glasgow")
    c1, c2, c3 = st.columns(3)
    y = c1.selectbox("Ouverture des yeux", list(GCS_Y), format_func=lambda k: f"{k} · {GCS_Y[k]}", key="sn_y")
    vv = c2.selectbox("Réponse verbale", list(GCS_V), format_func=lambda k: f"{k} · {GCS_V[k]}", key="sn_v")
    m = c3.selectbox("Réponse motrice", list(GCS_M), format_func=lambda k: f"{k} · {GCS_M[k]}", key="sn_m")
    total = y + vv + m
    sev = "grave (coma)" if total <= 8 else "modéré" if total <= 12 else "léger"
    st.metric("Score de Glasgow", f"{total} / 15", help="E + V + M")
    st.markdown(f"Traumatisme crânien **{sev}**.")
    ui.memo("Les maxima : **4** pour les yeux, **5** pour le verbal, **6** pour le moteur (« 4, 5, 6 »). Le minimum "
            "est 3, pas 0.")


def ch_degeneratives():
    ui.md(r"""
**La [[parkinson|maladie de Parkinson]]** : perte des neurones à dopamine de la substance noire.
- Signes cardinaux : **bradykinésie** (lenteur), **rigidité**, **tremblement de repos**, puis **instabilité
  posturale**.
- Marche : petits pas, peu de ballant des bras, demi-tours difficiles, [[freezing]], festination.
- Kiné : exercices **amples** et rapides, renforcement, équilibre, entraînement à la marche avec **indices**
  externes (rythme d'un métronome, lignes au sol) qui contournent les noyaux gris centraux, stratégies contre le
  freezing, prévention des chutes. L'exercice ralentit la perte de fonction.

**La [[sclérose en plaques]]** : jeunes adultes (plus souvent des femmes), évolution par poussées ou progressive.
Symptômes très variés : faiblesse, spasticité, ataxie, troubles visuels, sensitifs, vésicaux, **fatigue** très
fréquente. Kiné : exercice adapté (aérobie, renforcement, équilibre), gestion de l'énergie, éviter la chaleur
excessive.

**Les lésions neurologiques périphériques** : un nerf (radial, fibulaire commun…), un plexus, ou une
**polyneuropathie** (diabète : en « chaussettes », d'abord aux pieds). Signes : faiblesse et amyotrophie dans le
territoire, réflexes diminués, troubles sensitifs. Pas de spasticité (c'est le motoneurone **inférieur**).

**Les myopathies** (dystrophie de Duchenne…) : faiblesse surtout proximale, progressive. Kiné : maintenir
amplitudes, fonction et respiration, éviter l'épuisement.

**Neuropédiatrie** : la [[paralysie cérébrale]] (lésion non évolutive du cerveau en développement, mais des
troubles qui évoluent avec la croissance : spasticité, rétractions, déformations), le spina bifida, les retards de
développement moteur.
""")
    ui.table([
        ["Motoneurone supérieur (central)", "spasticité, hyperréflexie, Babinski, peu d'amyotrophie", "AVC, lésion médullaire, SEP"],
        ["Motoneurone inférieur (périphérique)", "hypotonie, aréflexie, amyotrophie, fasciculations", "lésion d'un nerf, d'une racine, polyneuropathie"],
    ], headers=["Atteinte", "Signes", "Exemples"])


CHAPTERS = [
    ("Les grands syndromes", ch_syndromes),
    ("L'AVC", ch_avc),
    ("Moelle et traumatisme crânien", ch_moelle_tc),
    ("Maladies neurodégénératives et périphériques", ch_degeneratives),
]

SIGNES = {
    "Spasticité et signe de Babinski": "Syndrome pyramidal",
    "Rigidité en roue dentée et tremblement de repos": "Syndrome extrapyramidal",
    "Dysmétrie et tremblement d'action": "Syndrome cérébelleux",
    "Amyotrophie, aréflexie et fasciculations": "Atteinte du motoneurone inférieur",
}


def _q_gcs(rng):
    y, v, m = rng.choice(list(GCS_Y)), rng.choice(list(GCS_V)), rng.choice(list(GCS_M))
    return dict(prompt=f"Un patient ouvre les yeux : « {GCS_Y[y].lower()} », réponse verbale : « {GCS_V[v].lower()} », "
                       f"réponse motrice : « {GCS_M[m].lower()} ». Quel est son score de Glasgow ?",
                answer=y + v + m, tol=0.0, why=f"E{y} + V{v} + M{m} = {y + v + m}.")


QUESTIONS = [
    table_qcm(1, SIGNES, "Ces signes évoquent quel syndrome : {k} ?", "Quels signes caractérisent : **{v}** ?"),
    qcm(1, "Quelle proportion des AVC est ischémique ?", "Environ 80 %", ["Environ 20 %", "Environ 50 %", "100 %"]),
    qcm(1, "Quel est le score de Glasgow minimal ?", "3", ["0", "1", "5"]),
    vf(1, "La paralysie cérébrale est une lésion évolutive du cerveau.", False, "La lésion n'évolue pas, mais les troubles changent avec la croissance."),
    qcm(1, "Que signifie le V de « VITE » pour reconnaître un AVC ?", "Visage paralysé", ["Vertiges", "Vomissements", "Vision double"]),
    num(2, _q_gcs),
    qcm(2, "Une lésion de l'hémisphère gauche chez un droitier donne souvent…", "une hémiplégie droite et une aphasie",
        ["une hémiplégie gauche et une héminégligence", "une ataxie bilatérale", "une paraplégie"]),
    qcm(2, "La classification ASIA A signifie…", "lésion médullaire complète", ["lésion incomplète motrice", "fonction normale",
        "lésion du nerf périphérique"]),
    multi(2, "Quels sont des signes cardinaux de la maladie de Parkinson ?", ["Bradykinésie", "Rigidité", "Tremblement de repos"],
          ["Spasticité", "Signe de Babinski"]),
    qcm(2, "Pourquoi utilise-t-on des indices externes (métronome, lignes au sol) dans la maladie de Parkinson ?",
        "Ils aident à initier et rythmer la marche en contournant les noyaux gris centraux déficients",
        ["Pour distraire le patient", "Pour mesurer la vitesse", "Ils n'ont pas d'effet"]),
    qcm(3, "Un patient tétraplégique C6 devient brutalement rouge, avec céphalée et PA à 200/110. Que suspecter ?",
        "Une dysréflexie autonome (chercher une vessie pleine, une escarre) : urgence", ["Une crise d'angoisse",
        "Un effet normal de l'exercice", "Un AVC hémorragique sans lien"]),
    qcm(3, "Pour aider un patient hémiplégique à se redresser au lit, que faut-il éviter ?",
        "Tirer sur son bras parétique", ["Le faire participer", "Lui expliquer le mouvement", "Utiliser le côté sain"]),
    qcm(3, "Un diabétique a une faiblesse et des troubles sensitifs « en chaussettes » avec réflexes achilléens abolis. Il s'agit…",
        "d'une polyneuropathie (atteinte périphérique)", ["d'un AVC", "d'une sclérose en plaques", "d'une myopathie"]),
    qcm(3, "Pourquoi la rééducation après un AVC doit-elle être intensive et orientée vers des tâches ?",
        "Parce que la plasticité dépend de la quantité, de l'intensité et de la spécificité de la pratique",
        ["Parce que le patient s'ennuie sinon", "Parce que la lésion disparaît", "Ce n'est pas utile après 1 semaine"]),
    qcm(3, "Une patiente SEP voit ses symptômes s'aggraver pendant une séance en piscine chaude. Explication ?",
        "La chaleur aggrave temporairement les blocs de conduction des fibres démyélinisées (phénomène d'Uhthoff)",
        ["Une nouvelle poussée certaine", "Une hypoglycémie", "Une réaction allergique au chlore"]),
]

CARDS = list(SIGNES.items()) + [
    ("Spasticité", "Dépend de la vitesse ; motoneurone supérieur"),
    ("Rigidité", "Constante, roue dentée ; Parkinson"),
    ("AVC sylvien gauche", "Hémiplégie droite + aphasie"),
    ("VITE / FAST", "Visage, Incapacité du bras, Trouble de la parole, En urgence 112"),
    ("Score de Glasgow", "Yeux 4 + Verbal 5 + Moteur 6 ; ≤ 8 = grave"),
    ("ASIA A / E", "Complète / normale"),
    ("Dysréflexie autonome", "Lésion > T6 : poussée hypertensive, urgence"),
    ("Parkinson : kiné", "Mouvements amples, indices externes, équilibre, prévention des chutes"),
    ("Motoneurone inférieur", "Hypotonie, aréflexie, amyotrophie"),
    ("Phénomène d'Uhthoff", "SEP : la chaleur aggrave temporairement les symptômes"),
]

VIDEOS = [
    ("Spasticité et rigidité : la différence", "différence spasticité rigidité examen neurologique"),
    ("Rééducation après un AVC", "rééducation AVC kinésithérapie tâche orientée"),
    ("Marche et freezing dans le Parkinson", "freezing Parkinson stratégies kiné indices"),
    ("Le score de Glasgow", "score de Glasgow explication"),
]

LINKS = [("Physiopedia : Stroke", "https://www.physio-pedia.com/Stroke")]
