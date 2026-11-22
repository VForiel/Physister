"""LFSM1102 Anatomie générale, systématique et fonctionnelle."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from app import ui
from app.course import Course
from app.quiz import gen_qcm, multi, qcm, table_qcm, vf

COURSE = Course(
    code="LFSM1102", title="Anatomie générale, systématique et fonctionnelle", short="Anatomie générale",
    bloc=1, quad=1, credits=5, hours="37,5 h", icon=":material/skeleton:",
    intro="L'anatomie, c'est la langue commune de tous les soignants. Ce cours fait le tour du corps entier, "
          "système par système, en reliant toujours la **forme** à la **fonction**. Le détail du système "
          "locomoteur viendra au Q2 (LFSM1003).",
    acquis=[
        "Décrire les structures du corps humain en trois dimensions.",
        "Expliquer la relation entre forme et fonction.",
        "Utiliser la nomenclature scientifique et médicale.",
        "Utiliser la description du système locomoteur pour expliquer le mouvement.",
        "Identifier les principaux repères anatomiques et palpatoires.",
    ],
)

TERMS = {
    "position anatomique": ("Position anatomique de référence", "Debout, regard à l'horizontale, bras le long du "
                            "corps, paumes vers l'avant, pieds parallèles. Toutes les descriptions s'y réfèrent.",
                            "Position anatomique"),
    "plan sagittal": ("Plan sagittal", "Plan vertical qui coupe le corps en une partie droite et une partie gauche. "
                      "On y fait la flexion et l'extension.", "Plan sagittal"),
    "plan frontal": ("Plan frontal (coronal)", "Plan vertical qui sépare l'avant (antérieur) de l'arrière "
                     "(postérieur). On y fait l'abduction et l'adduction.", "Plan frontal"),
    "plan transversal": ("Plan transversal (horizontal)", "Plan horizontal qui sépare le haut du bas. On y fait "
                         "les rotations.", "Plan transverse"),
    "médial": ("Médial", "Plus proche du plan médian du corps. Le pouce est latéral, l'auriculaire médial "
               "(en position anatomique).", None),
    "latéral": ("Latéral", "Plus éloigné du plan médian du corps.", None),
    "articulation synoviale": ("Articulation synoviale", "Articulation mobile avec une cavité articulaire, du "
                               "cartilage hyalin, une capsule et du liquide synovial (genou, épaule, hanche…).",
                               "Articulation synoviale"),
    "diaphyse": ("Diaphyse", "Corps (partie centrale, tubulaire) d'un os long.", "Diaphyse"),
    "épiphyse": ("Épiphyse", "Extrémité d'un os long, recouverte de cartilage articulaire.", "Épiphyse"),
    "périoste": ("Périoste", "Membrane qui entoure l'os (sauf au niveau du cartilage). Très innervée et "
                 "vascularisée, elle participe à la consolidation des fractures.", "Périoste"),
    "agoniste": ("Agoniste", "Muscle principal qui réalise un mouvement donné.", None),
    "antagoniste": ("Antagoniste", "Muscle qui produit le mouvement inverse de l'agoniste. Il se relâche (ou freine) "
                    "pendant que l'agoniste se contracte.", None),
    "système nerveux autonome": ("Système nerveux autonome", "Partie du système nerveux qui règle les viscères sans "
                                 "contrôle volontaire : sympathique (action, « fight or flight ») et "
                                 "parasympathique (repos, digestion).", "Système nerveux autonome"),
    "plexus": ("Plexus", "Réseau de nerfs qui s'échangent des fibres avant de donner les nerfs des membres "
               "(plexus brachial, plexus lombaire, plexus sacral).", "Plexus nerveux"),
    "dermatome": ("Dermatome", "Zone de peau innervée par une seule racine nerveuse spinale.", "Dermatome (anatomie)"),
    "myotome": ("Myotome", "Ensemble des muscles innervés par une seule racine nerveuse spinale.", "Myotome"),
    "alvéole": ("Alvéole pulmonaire", "Petit sac au bout des bronchioles où se font les échanges gazeux entre "
                "l'air et le sang.", "Alvéole pulmonaire"),
    "néphron": ("Néphron", "Unité fonctionnelle du rein (environ un million par rein) qui filtre le sang et "
                "forme l'urine.", "Néphron"),
    "péritoine": ("Péritoine", "Membrane séreuse qui tapisse la cavité abdominale et enveloppe une partie des "
                  "viscères.", "Péritoine"),
}

DIRECTIONS = {
    "Supérieur (crânial)": "vers la tête",
    "Inférieur (caudal)": "vers les pieds",
    "Antérieur (ventral)": "vers l'avant",
    "Postérieur (dorsal)": "vers l'arrière",
    "Médial": "vers le plan médian",
    "Latéral": "vers le côté, loin du plan médian",
    "Proximal": "vers la racine du membre",
    "Distal": "vers l'extrémité du membre",
    "Superficiel": "vers la surface du corps",
    "Profond": "vers l'intérieur du corps",
}

PLANES = {
    "Sagittal": ("x", "Coupe droite / gauche. Mouvements : flexion et extension (ex. hocher la tête « oui », "
                      "lever le bras vers l'avant)."),
    "Frontal": ("y", "Coupe avant / arrière. Mouvements : abduction et adduction, inclinaisons latérales "
                     "(ex. jumping jack)."),
    "Transversal": ("z", "Coupe haut / bas. Mouvements : rotations (ex. tourner la tête « non », rotation du "
                         "tronc)."),
}


def _stick_figure():
    # bonhomme en 3D : x = gauche-droite, y = avant-arrière, z = haut
    segs = [
        [(0, 0, 0.9), (0, 0, 1.45)],  # tronc
        [(0, 0, 1.45), (0, 0, 1.75)],  # tête
        [(-0.2, 0, 1.4), (0.2, 0, 1.4)],  # épaules
        [(-0.2, 0, 1.4), (-0.25, 0, 0.85)], [(0.2, 0, 1.4), (0.25, 0, 0.85)],  # bras
        [(-0.1, 0, 0.9), (0.1, 0, 0.9)],  # bassin
        [(-0.1, 0, 0.9), (-0.12, 0, 0.05)], [(0.1, 0, 0.9), (0.12, 0, 0.05)],  # jambes
        [(-0.12, 0, 0.05), (-0.12, 0.15, 0.0)], [(0.12, 0, 0.05), (0.12, 0.15, 0.0)],  # pieds
    ]
    xs, ys, zs = [], [], []
    for a, b in segs:
        xs += [a[0], b[0], None]
        ys += [a[1], b[1], None]
        zs += [a[2], b[2], None]
    return go.Scatter3d(x=xs, y=ys, z=zs, mode="lines", line=dict(width=8, color="#6b7280"), name="Corps",
                        hoverinfo="skip")


def ch_conventions():
    ui.md(r"""
Toute description anatomique part de la **[[position anatomique|position anatomique de référence]]** :
debout, face à toi, bras le long du corps, **paumes vers l'avant**. Même si le patient est couché ou a le bras
levé, on décrit toujours comme s'il était dans cette position. C'est ce qui permet à deux soignants de se
comprendre sans ambiguïté.

**Trois plans, trois axes.** Chaque mouvement se fait *dans* un plan, *autour* d'un axe perpendiculaire à ce plan.
""")
    c1, c2 = st.columns([1, 2])
    with c1:
        plane = st.radio("Plan à afficher", list(PLANES), key="ag_plane")
        st.markdown(PLANES[plane][1])
    with c2:
        fig = go.Figure(_stick_figure())
        u = np.linspace(-0.5, 0.5, 2)
        v = np.linspace(0, 1.8, 2)
        axis = PLANES[plane][0]
        if axis == "x":
            Y, Z = np.meshgrid(u, v)
            fig.add_trace(go.Surface(x=np.zeros_like(Y), y=Y, z=Z, opacity=0.35, showscale=False,
                                     colorscale=[[0, "#4d5f92"], [1, "#4d5f92"]], name="Plan sagittal"))
        elif axis == "y":
            X, Z = np.meshgrid(u, v)
            fig.add_trace(go.Surface(x=X, y=np.zeros_like(X), z=Z, opacity=0.35, showscale=False,
                                     colorscale=[[0, "#4d5f92"], [1, "#4d5f92"]]))
        else:
            X, Y = np.meshgrid(u, u)
            fig.add_trace(go.Surface(x=X, y=Y, z=np.full_like(X, 1.0), opacity=0.35, showscale=False,
                                     colorscale=[[0, "#4d5f92"], [1, "#4d5f92"]]))
        fig.update_layout(height=430, margin=dict(l=0, r=0, t=0, b=0), showlegend=False,
                          scene=dict(xaxis_title="gauche ↔ droite", yaxis_title="arrière ↔ avant", zaxis_title="",
                                     aspectmode="manual", aspectratio=dict(x=0.7, y=0.7, z=1.1),
                                     xaxis_range=[-0.6, 0.6], yaxis_range=[-0.6, 0.6], zaxis_range=[0, 1.85],
                                     camera=dict(eye=dict(x=1.4, y=1.4, z=0.6))))
        ui.chart(fig, "anatomie_generale_0")
        st.caption("Fais tourner la figure avec la souris (ou le doigt).")
    ui.memo("Flexion/extension → **sagittal** ; abduction/adduction → **frontal** ; rotation → **transversal**. "
            "Pour l'axe : il est toujours **perpendiculaire** au plan. La flexion du coude se fait dans le plan "
            "sagittal, autour d'un axe frontal (gauche-droite).")
    ui.md("**Les termes de position** se disent toujours par paires :")
    ui.table([[k, v] for k, v in DIRECTIONS.items()], headers=["Terme", "Signification"])
    ui.warn("**Proximal/distal** ne s'emploient que pour les membres (et quelques organes tubulaires). Pour le "
            "tronc, on dit supérieur/inférieur. Et le pouce est **latéral** : en position anatomique, la paume "
            "regarde vers l'avant.")


def ch_squelette():
    ui.md(r"""
Le squelette adulte compte environ **206 os**. Il soutient, protège (crâne, cage thoracique), sert de levier aux
muscles, stocke le calcium et le phosphore, et fabrique les cellules sanguines (moelle rouge).

**Squelette axial** (crâne, colonne, côtes, sternum) et **squelette appendiculaire** (ceintures et membres).

**Formes des os** : longs (fémur, humérus), courts (os du carpe), plats (scapula, os du crâne), irréguliers
(vertèbres), sésamoïdes, logés dans un tendon (patella).

**Anatomie d'un os long** : la [[diaphyse]] (corps, tube d'os **compact** avec la cavité médullaire), deux
[[épiphyse|épiphyses]] (extrémités en os **spongieux**, coiffées de cartilage), et chez l'enfant la
**plaque de croissance** (cartilage de conjugaison) entre les deux, la **métaphyse**. Le tout entouré par le
[[périoste]].
""")
    ui.md(r"""
**Les articulations** se classent selon ce qui unit les os :

| Type | Tissu d'union | Mobilité | Exemples |
|---|---|---|---|
| Fibreuses | tissu fibreux | quasi nulle | sutures du crâne, syndesmose tibio-fibulaire |
| Cartilagineuses | cartilage | faible | symphyse pubienne, disques intervertébraux |
| Synoviales | capsule + liquide synovial | grande | épaule, genou, hanche |

Les [[articulation synoviale|articulations synoviales]] se classent selon la **forme des surfaces** et donc le nombre de **degrés de liberté** :

| Forme | Degrés de liberté | Exemple |
|---|---|---|
| Plane | glissements | articulations entre os du carpe, acromio-claviculaire |
| Trochléenne (ginglyme, charnière) | 1 | huméro-ulnaire (coude) |
| Trochoïde (pivot) | 1 | radio-ulnaire proximale, atlas-axis |
| Condylienne (ellipsoïde) | 2 | radio-carpienne (poignet) |
| En selle | 2 | trapézo-métacarpienne (pouce) |
| Sphéroïde (énarthrose) | 3 | épaule, hanche |
""")
    ui.clinic("Chez l'enfant, la plaque de croissance est **plus fragile** que les ligaments. Une torsion qui "
              "donnerait une entorse chez l'adulte peut donner un **décollement épiphysaire** chez l'enfant : on "
              "ne parle jamais trop vite d'« entorse » chez un enfant.")


def ch_muscles():
    ui.md(r"""
Trois types de tissu musculaire :

| | Strié squelettique | Strié cardiaque | Lisse |
|---|---|---|---|
| Où | attaché aux os | cœur | parois des viscères et vaisseaux |
| Commande | volontaire | involontaire (automatisme) | involontaire |
| Aspect | fibres longues multinucléées, striées | cellules ramifiées, disques intercalaires | cellules fusiformes, non striées |

Un muscle squelettique s'attache par ses **tendons** à une **origine** (souvent proximale, plus fixe) et à une
**terminaison** (souvent distale, plus mobile). Il ne fait que **tirer** : pour revenir, il faut un autre muscle.

**Rôles dans un mouvement** : l'[[agoniste]] réalise le mouvement, l'[[antagoniste]] fait l'inverse, les
**synergistes** aident l'agoniste, les **stabilisateurs** (fixateurs) tiennent les segments voisins.

**Forme et fonction** : les fibres parallèles (fusiformes, comme le biceps) donnent de l'amplitude et de la vitesse ;
les fibres **pennées** (obliques sur le tendon, comme le quadriceps ou le deltoïde) donnent de la **force**, parce
qu'on loge beaucoup plus de fibres dans le même volume.
""")
    ui.memo("Le nom d'un muscle raconte souvent sa forme ou son rôle : **deltoïde** (en forme de Δ), "
            "**biceps** (deux chefs), **long fléchisseur du pouce** (taille + action + cible), "
            "**sterno-cléido-mastoïdien** (ses insertions : sternum, clavicule, processus mastoïde).")


def ch_nerveux():
    ui.md(r"""
**Organisation**
- **Système nerveux central (SNC)** : l'encéphale (cerveau, tronc cérébral, cervelet) et la moelle spinale.
- **Système nerveux périphérique (SNP)** : 12 paires de nerfs crâniens et 31 paires de nerfs spinaux
  (8 cervicales, 12 thoraciques, 5 lombaires, 5 sacrales, 1 coccygienne).

Chaque nerf spinal naît de deux racines : la racine **ventrale (motrice)** et la racine **dorsale (sensitive)**,
avec son ganglion. Les nerfs des membres passent par des [[plexus]] : **brachial** (C5-T1) pour le membre
supérieur, **lombaire** (L1-L4) et **sacral** (L4-S4) pour le membre inférieur.

Une racine innerve une bande de peau, le [[dermatome]], et un groupe de muscles, le [[myotome]]. C'est la base
de l'examen neurologique.

**Somatique et autonome** : le système somatique commande les muscles squelettiques (volontaire) et ramène les
sensations conscientes. Le [[système nerveux autonome]] règle les viscères :
- **sympathique** (centres thoraco-lombaires) : fuir ou combattre. Cœur plus rapide, bronches dilatées, pupilles
  dilatées, digestion ralentie.
- **parasympathique** (centres crânio-sacrés, surtout le nerf vague X) : repos et digestion.
""")
    st.markdown("#### Les 12 nerfs crâniens")
    ui.table([
        ["I", "Olfactif", "sensitif", "odorat"], ["II", "Optique", "sensitif", "vision"],
        ["III", "Oculomoteur", "moteur", "la plupart des muscles de l'œil, pupille"],
        ["IV", "Trochléaire", "moteur", "muscle oblique supérieur de l'œil"],
        ["V", "Trijumeau", "mixte", "sensibilité du visage, muscles de la mastication"],
        ["VI", "Abducens", "moteur", "muscle droit latéral de l'œil"],
        ["VII", "Facial", "mixte", "muscles de la mimique, goût (2/3 antérieurs de la langue)"],
        ["VIII", "Vestibulo-cochléaire", "sensitif", "audition et équilibre"],
        ["IX", "Glosso-pharyngien", "mixte", "pharynx, goût (1/3 postérieur)"],
        ["X", "Vague", "mixte", "viscères thoraciques et abdominaux (parasympathique)"],
        ["XI", "Accessoire", "moteur", "trapèze et sterno-cléido-mastoïdien"],
        ["XII", "Hypoglosse", "moteur", "muscles de la langue"],
    ], headers=["N°", "Nom", "Type", "Rôle principal"])
    ui.memo("Pour le type (Sensitif, Moteur, Both = mixte), dans l'ordre de I à XII : « **S**ome **S**ay **M**arry "
            "**M**oney, **B**ut **M**y **B**rother **S**ays **B**ig **B**rains **M**atter **M**ore ».")
    ui.clinic("Le nerf accessoire (XI) peut être lésé lors d'une chirurgie du cou : le trapèze s'affaiblit, la "
              "scapula « décolle » et l'élévation du bras devient difficile. Le kiné repère ça à l'inspection.")


def ch_circulation():
    ui.md(r"""
Le cœur est **deux pompes côte à côte** :
- le **cœur droit** envoie le sang pauvre en O₂ vers les poumons (**petite circulation**, pulmonaire) ;
- le **cœur gauche** envoie le sang riche en O₂ vers tout le corps (**grande circulation**, systémique).

Les **artères** partent du cœur (parois épaisses et élastiques, haute pression), les **veines** y reviennent
(parois fines, valvules, basse pression), les **capillaires** font les échanges avec les tissus.
""")
    ui.warn("Artère = **part** du cœur, pas forcément « sang rouge ». L'artère pulmonaire transporte du sang **pauvre** "
            "en O₂, et les veines pulmonaires du sang **riche** en O₂.")
    st.markdown("#### À toi : suis une goutte de sang")
    path = [
        ("Veines caves supérieure et inférieure", "Le sang pauvre en O₂ revient du corps."),
        ("Atrium (oreillette) droit", "Il se remplit, puis se contracte."),
        ("Valve tricuspide", "Empêche le retour vers l'atrium."),
        ("Ventricule droit", "Paroi assez fine : la pression pulmonaire est basse."),
        ("Valve pulmonaire", "Entre le ventricule droit et le tronc pulmonaire."),
        ("Artères pulmonaires", "Sang pauvre en O₂ vers les poumons."),
        ("Capillaires pulmonaires (alvéoles)", "Le sang capte l'O₂ et rejette le CO₂."),
        ("Veines pulmonaires (4)", "Sang riche en O₂ vers le cœur gauche."),
        ("Atrium (oreillette) gauche", "Il se remplit, puis se contracte."),
        ("Valve mitrale (bicuspide)", "Deux cuspides, comme une mitre d'évêque."),
        ("Ventricule gauche", "Paroi très épaisse : il pousse le sang dans tout le corps."),
        ("Valve aortique", "Entre le ventricule gauche et l'aorte."),
        ("Aorte puis artères", "Distribution à tout le corps, sous haute pression."),
        ("Capillaires des tissus", "Le sang livre l'O₂ et récupère le CO₂, puis repart par les veines."),
    ]
    step = st.slider("Étape", 1, len(path), 1, key="ag_sang")
    name, desc = path[step - 1]
    rich = 7 <= step <= 13
    st.markdown(f"**{step}. {name}** : {desc}")
    st.progress(step / len(path), text="Sang riche en O₂" if rich else "Sang pauvre en O₂")
    ui.memo("Valves dans l'ordre : « **T**ry **P**ulling **M**y **A**orta » : **T**ricuspide, **P**ulmonaire, "
            "**M**itrale, **A**ortique.")


def ch_visceres():
    ui.md(r"""
**Respiratoire** : voies aériennes supérieures (nez, pharynx, larynx) puis inférieures (trachée, bronches,
bronchioles), jusqu'aux [[alvéole|alvéoles]] (environ 300 millions, 70 à 100 m² d'échanges). Le poumon droit a
**3 lobes**, le gauche **2** (la place du cœur). Chaque poumon est entouré par la **plèvre** (deux feuillets qui
glissent l'un sur l'autre). Le **diaphragme** est le muscle principal de l'inspiration.

**Digestif** : bouche, pharynx, œsophage, estomac, intestin grêle (duodénum, jéjunum, iléon ; c'est là que
se fait l'essentiel de l'absorption), côlon, rectum. Glandes annexes : foie (bile, métabolisme), vésicule
biliaire, pancréas (enzymes digestives et insuline). La cavité abdominale est tapissée par le [[péritoine]].

**Urinaire** : deux reins (rétropéritonéaux, à hauteur de T12-L3), qui filtrent le sang grâce aux
[[néphron|néphrons]], puis uretères, vessie, urètre.

**Génital** : gonades (testicules, ovaires) qui produisent les gamètes et les hormones sexuelles, et voies génitales.
""")
    ui.clinic("Le **plancher pelvien** (muscles qui ferment le bas du bassin) soutient la vessie, l'utérus et le "
              "rectum. Sa rééducation (incontinence après un accouchement ou une chirurgie de la prostate) est une "
              "spécialité de la kiné.")
    ui.tip("Une douleur viscérale peut être **projetée** sur la peau d'un dermatome qui partage la même racine : "
           "l'infarctus qui fait mal au bras gauche, la vésicule biliaire à l'épaule droite. Le kiné doit y penser "
           "devant une douleur d'épaule qui ne varie pas avec les mouvements.")


CHAPTERS = [
    ("Conventions et vocabulaire", ch_conventions),
    ("Os et articulations", ch_squelette),
    ("Muscles", ch_muscles),
    ("Système nerveux", ch_nerveux),
    ("Cœur et circulation", ch_circulation),
    ("Viscères", ch_visceres),
]

MVT_PLAN = {
    "flexion du coude": "sagittal", "abduction de l'épaule": "frontal", "rotation de la tête (« non »)": "transversal",
    "extension du genou": "sagittal", "inclinaison latérale du tronc": "frontal", "rotation latérale de hanche": "transversal",
    "flexion dorsale de cheville": "sagittal", "adduction de hanche": "frontal",
}
NERFS_CRANIENS = {"I": "Olfactif", "II": "Optique", "III": "Oculomoteur", "IV": "Trochléaire", "V": "Trijumeau",
                  "VI": "Abducens", "VII": "Facial", "VIII": "Vestibulo-cochléaire", "IX": "Glosso-pharyngien",
                  "X": "Vague", "XI": "Accessoire", "XII": "Hypoglosse"}
ARTICULATIONS = {"hanche": "sphéroïde (3 degrés de liberté)", "épaule (gléno-humérale)": "sphéroïde (3 degrés de liberté)",
                 "huméro-ulnaire": "trochléenne (1 degré de liberté)", "radio-ulnaire proximale": "trochoïde (1 degré de liberté)",
                 "radio-carpienne": "condylienne (2 degrés de liberté)", "trapézo-métacarpienne": "en selle (2 degrés de liberté)"}


def _q_direction(rng):
    pairs = [("le genou", "la cheville", "proximal"), ("la main", "le coude", "distal"),
             ("le sternum", "le bras", "médial"), ("le pouce", "l'auriculaire", "latéral"),
             ("la tête", "le thorax", "supérieur"), ("le nez", "les oreilles", "antérieur"),
             ("la peau", "les muscles", "superficiel"), ("la colonne vertébrale", "le sternum", "postérieur")]
    a, b, good = rng.choice(pairs)
    return (f"En position anatomique, {a} est … par rapport à {b}.", good,
            ["proximal", "distal", "médial", "latéral", "supérieur", "antérieur", "postérieur", "superficiel"],
            "Raisonne toujours en position anatomique (paumes vers l'avant).")


QUESTIONS = [
    qcm(1, "En position anatomique de référence, les paumes de main sont tournées…", "vers l'avant",
        ["vers l'arrière", "vers le corps", "vers le sol"]),
    table_qcm(1, MVT_PLAN, "Dans quel plan se fait la **{k}** ?", why="Flexion/extension : sagittal ; abd/adduction : frontal ; rotations : transversal."),
    gen_qcm(1, _q_direction),
    qcm(1, "Combien de paires de nerfs spinaux possède l'être humain ?", "31", ["12", "24", "33"],
        "8 cervicales, 12 thoraciques, 5 lombaires, 5 sacrales, 1 coccygienne."),
    vf(1, "Le poumon gauche a trois lobes.", False, "Il en a deux (le cœur prend de la place) ; le droit en a trois."),
    qcm(1, "Quel type de tissu musculaire est volontaire ?", "Strié squelettique", ["Strié cardiaque", "Lisse", "Aucun"]),
    table_qcm(2, NERFS_CRANIENS, "Comment s'appelle le nerf crânien **{k}** ?", "Quel est le numéro du nerf **{v}** ?"),
    table_qcm(2, ARTICULATIONS, "Quel type d'articulation synoviale est l'articulation **{k}** ?"),
    qcm(2, "La valve entre l'atrium gauche et le ventricule gauche est la valve…", "mitrale",
        ["tricuspide", "aortique", "pulmonaire"], "Tricuspide à droite, mitrale (bicuspide) à gauche."),
    vf(2, "Les artères pulmonaires transportent du sang riche en oxygène.", False,
       "Elles partent du cœur droit vers les poumons : sang pauvre en O₂."),
    multi(2, "Quels effets sont dus au système sympathique ?", ["Accélération du cœur", "Dilatation des bronches",
          "Dilatation des pupilles"], ["Augmentation de la digestion", "Constriction des bronches"],
          "Le sympathique prépare à l'action."),
    qcm(2, "Une racine nerveuse innerve une bande de peau appelée…", "dermatome", ["myotome", "sclérotome", "plexus"]),
    qcm(2, "Le plexus brachial est formé par les racines…", "C5 à T1", ["C1 à C4", "T1 à T12", "L1 à L4"]),
    qcm(3, "Un enfant tombe en torsion sur la cheville. Pourquoi faut-il se méfier avant de parler d'entorse ?",
        "La plaque de croissance est plus fragile que les ligaments : elle peut se décoller",
        ["Les enfants n'ont pas de ligaments", "Les os de l'enfant ne cassent jamais",
         "Le périoste de l'enfant est absent"]),
    qcm(3, "Pourquoi le quadriceps a-t-il des fibres pennées ?", "Pour loger plus de fibres et produire plus de force",
        ["Pour avoir plus d'amplitude", "Pour contracter plus vite", "Pour être innervé par plusieurs nerfs"]),
    qcm(3, "Lors de la flexion du coude, autour de quel axe se fait le mouvement ?",
        "Un axe frontal (gauche-droite)", ["Un axe sagittal (avant-arrière)", "Un axe vertical", "Un axe oblique"],
        "Le mouvement est dans le plan sagittal, l'axe est perpendiculaire à ce plan."),
    qcm(3, "Une patiente a une douleur à l'épaule droite qui ne varie pas avec les mouvements, après un repas gras. "
        "Que suspecter ?", "Une douleur projetée d'origine viscérale (vésicule biliaire)",
        ["Une tendinopathie de la coiffe", "Une capsulite rétractile", "Une entorse acromio-claviculaire"],
        "Une douleur mécanique varie avec les mouvements ; ici, il faut réorienter vers le médecin."),
    multi(3, "Quels nerfs crâniens sont purement moteurs ?", ["III Oculomoteur", "XI Accessoire", "XII Hypoglosse"],
          ["V Trijumeau", "VII Facial", "II Optique"], "V et VII sont mixtes, II est sensitif."),
]

CARDS = [
    ("Position anatomique", "Debout, regard horizontal, bras le long du corps, paumes vers l'avant"),
    ("Plan des flexions/extensions", "Sagittal (axe frontal)"),
    ("Plan des abductions/adductions", "Frontal (axe sagittal)"),
    ("Plan des rotations", "Transversal (axe vertical)"),
    ("Nombre de paires de nerfs spinaux", "31 : 8 C, 12 T, 5 L, 5 S, 1 Co"),
    ("Plexus brachial", "C5 à T1"),
    ("Plexus lombaire / sacral", "L1-L4 / L4-S4"),
    ("Articulation sphéroïde", "3 degrés de liberté (épaule, hanche)"),
    ("Articulation en selle", "Trapézo-métacarpienne (pouce), 2 degrés"),
    ("Valves du cœur dans l'ordre", "Tricuspide, pulmonaire, mitrale, aortique"),
    ("Lobes pulmonaires", "3 à droite, 2 à gauche"),
    ("Nerf crânien X", "Vague : parasympathique des viscères"),
    ("Nerf crânien XI", "Accessoire : trapèze et SCM"),
    ("Dermatome", "Zone de peau innervée par une racine"),
    ("Myotome", "Muscles innervés par une racine"),
    ("Sympathique", "Centres thoraco-lombaires, action (« fight or flight »)"),
]

VIDEOS = [
    ("Plans et axes anatomiques", "plans axes anatomiques sagittal frontal transversal"),
    ("Les nerfs crâniens", "12 nerfs crâniens anatomie explication"),
    ("La circulation sanguine dans le cœur", "circulation sanguine cœur trajet du sang anatomie"),
    ("Classification des articulations", "classification articulations synoviales types anatomie"),
]

LINKS = [
    ("Kenhub : atlas et articles d'anatomie (FR)", "https://www.kenhub.com/fr"),
    ("Complete Anatomy / Zygote Body : anatomie en 3D", "https://www.zygotebody.com/"),
]
