"""LKNR1202 Techniques de base en kinésithérapie."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from app import ui
from app.course import Course
from app.quiz import gen_qcm, multi, num, qcm, table_qcm, vf

COURSE = Course(
    code="LKNR1202", title="Techniques de base en kinésithérapie", short="Techniques de base",
    bloc=2, quad=1, credits=6, hours="30 h + 67,5 h", icon=":material/fitness_center:",
    intro="Le premier vrai cours « de kiné » : comment les tissus (muscle, tendon, articulation, nerf) réagissent "
          "aux contraintes et cicatrisent, comment les évaluer, et comment doser exercices, étirements, "
          "mobilisations et massage. Beaucoup de pratique en TP : ce chapitre t'aide à comprendre le pourquoi.",
    acquis=[
        "Expliquer les mécanismes patho-biologiques des tissus musculaires, tendineux, articulaires et nerveux.",
        "Connaître les principes des actes techniques, des exercices et des conseils.",
        "Réaliser et interpréter une évaluation musculo-squelettique.",
        "Évaluer, adapter ou arrêter une intervention.",
        "Extraire les informations pertinentes d'une vignette clinique.",
    ],
)

TERMS = {
    "mécanotransduction": ("Mécanotransduction", "Transformation d'une contrainte mécanique en signal biologique "
                           "par les cellules (fibroblastes, ténocytes, ostéocytes) : la charge pilote la réparation.",
                           "Mécanotransduction"),
    "1rm": ("1RM", "Une répétition maximale : la charge la plus lourde qu'on peut soulever une seule fois avec une "
            "bonne technique.", "Une répétition maximale"),
    "hypertrophie": ("Hypertrophie", "Augmentation du volume des fibres musculaires.", "Hypertrophie musculaire"),
    "viscoélasticité": ("Viscoélasticité", "Comportement des tissus à la fois élastiques (ils reprennent leur forme) "
                        "et visqueux (leur réponse dépend du temps et de la vitesse) : fluage, relaxation.", "Viscoélasticité"),
    "fluage": ("Fluage", "Allongement progressif d'un tissu sous une charge constante.", "Fluage"),
    "grades de maitland": ("Grades de Maitland", "Échelle (I à IV) des mobilisations articulaires selon l'amplitude "
                           "et la position dans l'amplitude disponible.", None),
    "neurodynamique": ("Neurodynamique", "Étude et traitement de la mobilité et de la mécanosensibilité du système "
                       "nerveux (tests de mise en tension comme le Lasègue ou l'ULNT).", None),
    "testing mrc": ("Échelle MRC", "Cotation de la force musculaire de 0 (aucune contraction) à 5 (force normale).",
                    "Échelle MRC"),
    "goniométrie": ("Goniométrie", "Mesure des amplitudes articulaires avec un goniomètre.", None),
    "étirement statique": ("Étirement statique", "Maintenir le muscle en position allongée (en général 15 à 60 s).", None),
    "pnf": ("PNF (contracter-relâcher)", "Technique d'étirement où l'on contracte le muscle étiré quelques secondes "
            "avant de gagner de l'amplitude.", "Facilitation neuromusculaire proprioceptive"),
    "endfeel": ("Sensation de fin de mouvement (end-feel)", "Qualité de la résistance perçue en fin d'amplitude "
                "passive : osseuse (dure), capsulaire (ferme élastique), tissulaire (molle), vide (douleur, sans "
                "résistance).", None),
}

MRC = {0: "aucune contraction visible ni palpable", 1: "contraction palpable sans mouvement",
       2: "mouvement complet sans la pesanteur", 3: "mouvement complet contre la pesanteur",
       4: "mouvement contre la pesanteur et une résistance modérée", 5: "force normale"}

PRESCRIPTION = {  # objectif : (%1RM, répétitions, séries, repos)
    "Force maximale": ("≥ 85 %", "1 à 6", "2 à 6", "2 à 5 min"),
    "Hypertrophie": ("65 à 85 %", "6 à 12", "3 à 6", "1 à 2 min"),
    "Endurance musculaire": ("< 65 %", "≥ 15", "2 à 3", "≤ 30 s à 1 min"),
    "Puissance": ("30 à 60 % (vitesse maximale)", "1 à 5", "3 à 5", "2 à 5 min"),
}


def ch_tissus():
    ui.md(r"""
**La cicatrisation** suit trois phases qui se chevauchent :

1. **Inflammation** (0 à ~5 jours) : saignement, caillot, cellules inflammatoires. Signes : rougeur, chaleur,
   gonflement, douleur, perte de fonction. **Nécessaire** à la réparation.
2. **Prolifération** (~3 jours à 3-6 semaines) : les fibroblastes fabriquent un tissu cicatriciel de collagène
   **désorganisé** (type III), fragile.
3. **Remodelage** (de 3 semaines à 1 an et plus) : le collagène se réorganise (type I) et s'**aligne** dans le sens
   des contraintes. C'est là que la charge est indispensable.
""")
    fig = go.Figure()
    for i, (name, a, b) in enumerate([("Inflammation", 0, 5), ("Prolifération", 3, 42), ("Remodelage", 21, 365)]):
        fig.add_trace(go.Bar(y=[name], x=[b - a], base=[a], orientation="h", name=name))
    fig.update_layout(height=200, margin=dict(l=10, r=10, t=10, b=10), showlegend=False,
                      xaxis=dict(type="log", title="Jours après la lésion (échelle logarithmique)", range=[-0.1, 2.7]),
                      yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, width="stretch")
    ui.md(r"""
Les cellules des tissus conjonctifs **sentent** les contraintes et y répondent ([[mécanotransduction]]) : c'est
la base de la **mécanothérapie**. Trop peu de charge (immobilisation) : le tissu s'affaiblit et la cicatrice est
désorganisée. Trop de charge trop tôt : la cicatrice se rompt. Le kiné cherche la **charge optimale**.

**Comportement mécanique** : tendons et ligaments ont une courbe contrainte-déformation caractéristique.
""")
    st.markdown("#### À toi : la courbe contrainte-déformation d'un ligament")
    d = st.slider("Déformation (%)", 0.0, 10.0, 2.0, 0.1, key="tb_def")
    x = np.linspace(0, 10, 300)

    def stress(e):
        e = np.asarray(e, dtype=float)
        toe = 8 * e ** 2
        lin = 32 + 30 * (e - 2)
        plast = 152 + 30 * (e - 6) - 9 * (e - 6) ** 2
        y = np.where(e < 2, toe, np.where(e < 6, lin, np.where(e < 8, plast, 0)))
        return y

    fig = go.Figure(go.Scatter(x=x, y=stress(x), mode="lines"))
    fig.add_trace(go.Scatter(x=[d], y=[float(stress(d))], mode="markers", marker=dict(size=13)))
    for x0, x1, txt in ((0, 2, "pied"), (2, 6, "élastique"), (6, 8, "plastique"), (8, 10, "rupture")):
        fig.add_vrect(x0=x0, x1=x1, opacity=0.06 if txt != "rupture" else 0.12, line_width=0,
                      annotation_text=txt, annotation_position="top left")
    fig.update_layout(height=280, margin=dict(l=10, r=10, t=20, b=10), showlegend=False,
                      xaxis_title="Déformation (%)", yaxis_title="Contrainte (unités arbitraires)")
    st.plotly_chart(fig, width="stretch")
    zone = ("zone du pied : les fibres ondulées se déplissent, peu de force" if d < 2 else
            "zone élastique : réversible, c'est la zone des activités normales" if d < 6 else
            "zone plastique : microruptures, le tissu ne revient pas à sa longueur (entorse grave)" if d < 8 else
            "rupture complète")
    st.caption(f"{d:.1f} % : {zone}. Valeurs schématiques.")
    ui.md(r"""
Ces tissus sont aussi [[viscoélasticité|viscoélastiques]] : maintenus étirés, ils s'allongent lentement
([[fluage]]) ; plus on les étire vite, plus ils sont raides.
""")


def ch_muscle():
    ui.md(r"""
**Les qualités musculaires** : la **force** (produire une tension maximale), l'**endurance** (répéter ou tenir
longtemps), la **puissance** (force × vitesse), et le volume (**[[hypertrophie]]**). Chacune se travaille avec des
paramètres différents.
""")
    ui.table([[k, *v] for k, v in PRESCRIPTION.items()], headers=["Objectif", "Charge (% 1RM)", "Répétitions", "Séries", "Repos"])
    st.caption("Repères inspirés des recommandations de l'ACSM et de la NSCA ; à adapter au patient.")
    st.markdown("#### À toi : estimer la 1RM sans la tester")
    st.caption("Tester une vraie 1RM chez un patient est risqué. On l'estime à partir d'une série jusqu'à l'échec.")
    c1, c2 = st.columns([1, 2])
    with c1:
        load = st.number_input("Charge soulevée (kg)", 1.0, 300.0, 40.0, 2.5, key="tb_load")
        reps = st.slider("Répétitions jusqu'à l'échec", 1, 12, 8, key="tb_reps")
    epley = load * (1 + reps / 30)
    brzycki = load * 36 / (37 - reps)
    with c2:
        k1, k2 = st.columns(2)
        k1.metric("1RM (Epley)", f"{epley:.1f} kg")
        k2.metric("1RM (Brzycki)", f"{brzycki:.1f} kg")
        rm = (epley + brzycki) / 2
        st.markdown(f"Pour de l'hypertrophie (≈ 70-80 % 1RM) : **{0.7 * rm:.0f} à {0.8 * rm:.0f} kg**. "
                    f"Pour l'endurance (< 65 %) : **moins de {0.65 * rm:.0f} kg**.")
    ui.tip("En clinique, on dose souvent avec la **perception de l'effort** : « il doit te rester 2 ou 3 répétitions "
           "en réserve » (RIR), ou l'échelle de Borg. Plus simple et plus sûr que le pourcentage de 1RM.")
    ui.md(r"""
**Le tendon** s'adapte lentement (des mois) mais très bien à la charge : renforcement **lent et lourd** (heavy
slow resistance), isométrie, excentrique. Le repos complet l'affaiblit.

**Les étirements** : [[étirement statique|statique]] (tenir 15 à 60 s), dynamique (mouvements amples contrôlés),
[[pnf|PNF contracter-relâcher]]. Ils augmentent l'amplitude surtout en améliorant la **tolérance à l'étirement**
(le système nerveux accepte d'aller plus loin), un peu par effets viscoélastiques. Ils ne préviennent pas
clairement les blessures, et un long étirement statique juste avant un effort explosif peut diminuer un peu la
performance.
""")


def ch_articulation():
    ui.md(r"""
**Le cartilage** se nourrit par le **mouvement** : la compression et le relâchement font circuler le liquide
synovial (comme une éponge). Une articulation immobilisée s'abîme.

**La capsule et les ligaments** se rétractent avec l'immobilisation ; la mobilisation leur redonne de la longueur.

**L'évaluation passive** : amplitude ([[goniométrie]]), qualité de la [[endfeel|sensation de fin de mouvement]],
douleur. Une limitation dans un **schéma capsulaire** (par exemple l'épaule : rotation latérale la plus limitée,
puis abduction, puis rotation médiale) oriente vers une atteinte de toute la capsule.

**Les [[grades de maitland|mobilisations de Maitland]]**
""")
    ui.table([
        ["I", "petite amplitude, au début de l'amplitude", "douleur"],
        ["II", "grande amplitude, sans atteindre la résistance", "douleur"],
        ["III", "grande amplitude, jusque dans la résistance", "raideur"],
        ["IV", "petite amplitude, en fin d'amplitude, dans la résistance", "raideur"],
    ], headers=["Grade", "Mouvement", "Indication principale"])
    ui.memo("Grades **I et II** pour la **douleur** (on ne touche pas la résistance), **III et IV** pour la "
            "**raideur** (on va dans la résistance). Plus le chiffre est grand, plus on va loin.")


def ch_nerf():
    ui.md(r"""
Les nerfs doivent **glisser** et s'**allonger** avec les mouvements (le nerf médian glisse d'environ 1 cm au
poignet quand on étend le coude et le poignet). Un nerf comprimé ou irrité devient **mécanosensible** : il fait mal
quand on le met en tension.

**Les tests [[neurodynamique|neurodynamiques]]** mettent un nerf progressivement en tension :
- **Lasègue** (SLR, jambe tendue levée) : nerf sciatique et racines L5-S1 ;
- **Slump** (assis, flexion du rachis + extension du genou + flexion dorsale) ;
- **ULNT** (tests de tension du membre supérieur) : médian, radial, ulnaire.

Un test est positif s'il **reproduit les symptômes** du patient et si un mouvement à distance (la **différenciation
structurelle**, comme la flexion du cou au Slump) les modifie : ça montre que c'est le nerf, et pas le muscle.

**Le contrôle du mouvement** : au-delà des tissus, on évalue la **qualité** du mouvement (coordination,
compensations). Et tout s'inscrit dans la [[cif|CIF]] : on relie l'atteinte des fonctions (force, amplitude) aux
limitations d'**activités** et de **participation** du patient.
""")
    ui.clinic("Les techniques de **glissement** neural (on tend un bout du nerf pendant qu'on relâche l'autre) sont "
              "mieux tolérées que la mise en tension quand le nerf est très irrité.")


def ch_evaluation():
    ui.md(r"""
**L'évaluation musculo-squelettique** suit un ordre : inspection, palpation, amplitudes actives puis passives,
force, tests spécifiques, tests fonctionnels.

**La force : l'[[testing mrc|échelle MRC]]**
""")
    ui.table([[k, v] for k, v in MRC.items()], headers=["Cotation", "Définition"])
    ui.tip("Les cotations 4 et 5 sont subjectives : pour suivre un patient, un **dynamomètre manuel** donne des "
           "newtons et détecte des progrès que la cotation MRC rate.")
    ui.md(r"""
**Les techniques de relâchement** : le **massage** (effleurage, pétrissage, frictions) et les approches
myofasciales agissent surtout sur la **douleur** et la **détente** (effets neurophysiologiques et contextuels),
beaucoup moins sur la structure des tissus. Ils sont utiles en **complément** de l'exercice, rarement seuls.

**Évaluer, adapter ou arrêter** : à chaque séance, on vérifie la réponse (douleur pendant et dans les 24 h,
gonflement, progrès fonctionnels). Une douleur qui reste modérée et revient à son niveau de base en 24 h est en
général acceptable ; une aggravation durable impose de diminuer la charge.
""")


CHAPTERS = [
    ("Tissus et cicatrisation", ch_tissus),
    ("Muscle et tendon", ch_muscle),
    ("Articulation et mobilisation", ch_articulation),
    ("Nerf et neurodynamique", ch_nerf),
    ("Évaluer et doser", ch_evaluation),
]


def _q_1rm(rng):
    load = rng.choice([20, 30, 40, 50, 60])
    reps = rng.choice([5, 6, 8, 10])
    rm = load * (1 + reps / 30)
    return dict(prompt=f"Un patient soulève {load} kg {reps} fois jusqu'à l'échec. Estime sa 1RM avec la formule "
                       f"d'Epley : 1RM = charge × (1 + reps/30).",
                answer=rm, unit="kg", tol=0.02, why=f"{load} × (1 + {reps}/30) = {rm:.1f} kg.")


def _q_pct(rng):
    rm = rng.choice([50, 60, 80, 100])
    pct = rng.choice([60, 70, 75, 80])
    return dict(prompt=f"La 1RM est de {rm} kg. Quelle charge correspond à {pct} % de la 1RM (kg) ?",
                answer=rm * pct / 100, unit="kg", tol=0.01, why=f"{rm} × {pct}/100 = {rm * pct / 100:g} kg.")


QUESTIONS = [
    qcm(1, "Quelles sont les trois phases de la cicatrisation, dans l'ordre ?", "Inflammation, prolifération, remodelage",
        ["Prolifération, inflammation, remodelage", "Remodelage, inflammation, prolifération", "Inflammation, remodelage, prolifération"]),
    table_qcm(1, {str(k): v for k, v in MRC.items()}, "Que signifie une cotation MRC de **{k}** ?",
              "Quelle cotation MRC correspond à : {v} ?"),
    qcm(1, "Les grades de Maitland I et II sont surtout indiqués pour…", "la douleur", ["la raideur", "la force", "l'endurance"]),
    vf(1, "L'immobilisation prolongée renforce le cartilage articulaire.", False, "Le cartilage se nourrit par le mouvement."),
    qcm(1, "Que signifie 1RM ?", "La charge maximale soulevable une seule fois", ["Une répétition par minute",
        "La charge pour 10 répétitions", "Le repos minimal"]),
    table_qcm(2, {k: v[1] for k, v in PRESCRIPTION.items()}, "Combien de répétitions par série pour l'objectif **{k}** ?"),
    qcm(2, "Le test de Lasègue met en tension…", "le nerf sciatique et les racines L5-S1",
        ["le nerf fémoral", "le nerf médian", "le plexus brachial"]),
    multi(2, "Quels effets explique surtout le gain d'amplitude après étirements ?",
          ["Meilleure tolérance à l'étirement (système nerveux)", "Effets viscoélastiques temporaires"],
          ["Allongement permanent des os", "Disparition des sarcomères"]),
    qcm(2, "Dans la phase de remodelage, le collagène…", "s'aligne dans le sens des contraintes et devient de type I",
        ["disparaît", "reste désorganisé", "devient du cartilage"]),
    num(2, _q_pct),
    qcm(2, "Que se passe-t-il dans la zone plastique de la courbe contrainte-déformation ?",
        "Des microruptures : le tissu ne revient plus à sa longueur initiale", ["Le tissu est totalement réversible",
        "Les fibres se déplissent seulement", "Rien, le tissu est au repos"]),
    num(3, _q_1rm),
    qcm(3, "Au test du Slump, la douleur du patient dans la jambe diminue quand il relève la tête. Que conclure ?",
        "Le nerf est probablement impliqué (différenciation structurelle positive)", ["C'est forcément musculaire",
        "Le test est raté", "C'est une atteinte articulaire de hanche"]),
    qcm(3, "Après une séance de renforcement pour une tendinopathie, la douleur passe de 2/10 à 4/10 et revient à 2/10 "
        "le lendemain. Que faire ?", "Continuer : la réponse est acceptable", ["Arrêter tout exercice",
        "Doubler la charge", "Passer au massage seul"]),
    qcm(3, "Pourquoi éviter l'immobilisation stricte d'une entorse de cheville bénigne ?",
        "La charge précoce et dosée oriente le collagène et améliore la cicatrisation",
        ["Parce que le plâtre coûte cher", "Parce que les ligaments ne cicatrisent jamais", "Parce que l'inflammation est inutile"]),
    qcm(3, "Une épaule a la rotation latérale la plus limitée, puis l'abduction, puis la rotation médiale. Cela évoque…",
        "un schéma capsulaire (atteinte de toute la capsule)", ["une tendinopathie du biceps", "une lésion nerveuse",
        "une épaule normale"]),
]

CARDS = [
    ("Phases de la cicatrisation", "Inflammation (0-5 j), prolifération (→ 6 sem), remodelage (→ 1 an)"),
    ("Mécanotransduction", "Les cellules transforment la charge en signal de réparation"),
    ("Zones de la courbe contrainte-déformation", "Pied, élastique, plastique, rupture"),
    ("Force maximale", "≥ 85 % 1RM, 1-6 reps"),
    ("Hypertrophie", "65-85 % 1RM, 6-12 reps"),
    ("Endurance musculaire", "< 65 % 1RM, ≥ 15 reps"),
    ("Formule d'Epley", "1RM = charge × (1 + reps/30)"),
    ("Maitland I-II / III-IV", "Douleur / raideur"),
    ("MRC 3", "Mouvement complet contre la pesanteur"),
    ("Lasègue", "Sciatique, L5-S1"),
    ("Différenciation structurelle", "Bouger un segment à distance pour savoir si c'est le nerf"),
    ("Fluage", "Allongement sous charge constante"),
]

VIDEOS = [
    ("Les phases de la cicatrisation tissulaire", "phases cicatrisation tissulaire inflammation prolifération remodelage"),
    ("Grades de mobilisation de Maitland", "grades mobilisation Maitland kinésithérapie"),
    ("Tests neurodynamiques : Slump et ULNT", "test slump ULNT neurodynamique kiné"),
    ("Échelle MRC et testing musculaire", "testing musculaire échelle MRC cotation"),
]

LINKS = [("Physiopedia : Tissue healing", "https://www.physio-pedia.com/Soft_Tissue_Healing")]
