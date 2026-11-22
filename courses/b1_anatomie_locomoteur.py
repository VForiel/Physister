"""LFSM1003 Anatomie du système locomoteur et analyse du mouvement."""

import math

import plotly.graph_objects as go
import streamlit as st

from app import ui
from app.course import Course
from app.quiz import gen_qcm, multi, qcm, vf

COURSE = Course(
    code="LFSM1003", title="Anatomie du système locomoteur et analyse du mouvement", short="Anatomie locomotrice",
    bloc=1, quad=2, credits=6, hours="52,5 h", icon=":material/directions_run:",
    intro="Le cœur de métier : chaque articulation, ses mouvements et leurs amplitudes, les muscles qui les "
          "produisent et les nerfs qui les commandent. L'explorateur de muscles et les quiz générés t'aident à "
          "mémoriser ce gros volume, et la dernière partie apprend à analyser un mouvement.",
    acquis=[
        "Nommer et décrire les structures du système locomoteur.",
        "Connaître la fonction des muscles, les amplitudes articulaires et les axes de rotation.",
        "Expliquer un mouvement à partir des structures anatomiques.",
        "Analyser des postures statiques et des gestes sportifs.",
        "Résoudre des cas concrets.",
    ],
)

TERMS = {
    "chaîne cinétique ouverte": ("Chaîne cinétique ouverte", "Mouvement où l'extrémité distale est libre "
                                 "(leg extension, lever le bras).", None),
    "chaîne cinétique fermée": ("Chaîne cinétique fermée", "Mouvement où l'extrémité distale est fixée (squat, "
                                "pompes) : plusieurs articulations bougent ensemble.", None),
    "muscle biarticulaire": ("Muscle biarticulaire", "Muscle qui croise deux articulations (droit fémoral, "
                             "ischio-jambiers, gastrocnémien, biceps brachial). Son action dépend de la position des "
                             "deux.", None),
    "insuffisance active": ("Insuffisance active", "Un muscle biarticulaire, raccourci sur ses deux articulations à "
                            "la fois, ne peut plus produire beaucoup de force (fermer fort le poing, poignet fléchi).",
                            None),
    "insuffisance passive": ("Insuffisance passive", "Un muscle biarticulaire, étiré sur ses deux articulations à la "
                             "fois, limite le mouvement (difficile de fléchir la hanche genou tendu : ischio-jambiers).",
                             None),
    "coiffe des rotateurs": ("Coiffe des rotateurs", "Quatre muscles qui stabilisent la tête humérale : "
                             "supra-épineux, infra-épineux, petit rond, subscapulaire.", "Coiffe des rotateurs"),
    "rythme scapulo-huméral": ("Rythme scapulo-huméral", "Coordination entre la gléno-humérale et la scapula lors "
                               "de l'élévation du bras : environ 2° gléno-huméral pour 1° scapulo-thoracique.",
                               None),
    "verrouillage du genou": ("Verrouillage du genou", "Rotation automatique (screw-home) du tibia en fin "
                              "d'extension, qui stabilise le genou ; le poplité le déverrouille.", None),
    "goniomètre": ("Goniomètre", "Rapporteur articulé qui mesure les amplitudes articulaires en degrés.",
                   "Goniomètre"),
    "nerf fémoral": ("Nerf fémoral", "Nerf du plexus lombaire (L2-L4) : quadriceps, ilio-psoas (en partie), "
                     "sartorius ; sensibilité de la face antérieure de la cuisse.", "Nerf fémoral"),
    "nerf sciatique": ("Nerf sciatique", "Plus gros nerf du corps (L4-S3), qui se divise en nerfs tibial et "
                       "fibulaire commun.", "Nerf sciatique"),
    "nerf radial": ("Nerf radial", "Nerf du plexus brachial (C5-T1) : tous les extenseurs du membre supérieur "
                    "(triceps, extenseurs du poignet et des doigts).", "Nerf radial"),
    "nerf médian": ("Nerf médian", "Nerf du plexus brachial : la plupart des fléchisseurs de l'avant-bras et les "
                    "muscles du pouce (éminence thénar). Comprimé dans le canal carpien.", "Nerf médian"),
    "nerf ulnaire": ("Nerf ulnaire", "Nerf du plexus brachial : la plupart des petits muscles de la main ; "
                     "superficiel au coude (« petit juif »).", "Nerf ulnaire"),
}

# muscle : (région, action principale, nerf, racines)
MUSCLES = {
    "Deltoïde": ("Épaule", "abduction de l'épaule (faisceau moyen)", "nerf axillaire", "C5-C6"),
    "Supra-épineux": ("Épaule", "initiation de l'abduction, stabilisation de la tête humérale", "nerf supra-scapulaire", "C5-C6"),
    "Infra-épineux": ("Épaule", "rotation latérale de l'épaule", "nerf supra-scapulaire", "C5-C6"),
    "Petit rond": ("Épaule", "rotation latérale de l'épaule", "nerf axillaire", "C5-C6"),
    "Subscapulaire": ("Épaule", "rotation médiale de l'épaule", "nerfs subscapulaires", "C5-C6"),
    "Grand pectoral": ("Épaule", "adduction et rotation médiale de l'épaule", "nerfs pectoraux médial et latéral", "C5-T1"),
    "Grand dorsal": ("Épaule", "extension, adduction et rotation médiale de l'épaule", "nerf thoraco-dorsal", "C6-C8"),
    "Dentelé antérieur": ("Épaule", "protraction et sonnette latérale de la scapula", "nerf thoracique long", "C5-C7"),
    "Trapèze": ("Épaule", "élévation (supérieur), rétraction (moyen) et sonnette latérale de la scapula", "nerf accessoire (XI)", "XI (C3-C4)"),
    "Rhomboïdes": ("Épaule", "rétraction et sonnette médiale de la scapula", "nerf dorsal de la scapula", "C4-C5"),
    "Biceps brachial": ("Coude", "flexion du coude et supination", "nerf musculo-cutané", "C5-C6"),
    "Brachial": ("Coude", "flexion du coude", "nerf musculo-cutané", "C5-C6"),
    "Brachio-radial": ("Coude", "flexion du coude en position neutre", "nerf radial", "C5-C6"),
    "Triceps brachial": ("Coude", "extension du coude", "nerf radial", "C6-C8"),
    "Rond pronateur": ("Coude", "pronation de l'avant-bras", "nerf médian", "C6-C7"),
    "Supinateur": ("Coude", "supination de l'avant-bras", "nerf radial (branche profonde)", "C5-C6"),
    "Fléchisseur radial du carpe": ("Poignet et main", "flexion et inclinaison radiale du poignet", "nerf médian", "C6-C7"),
    "Fléchisseur ulnaire du carpe": ("Poignet et main", "flexion et inclinaison ulnaire du poignet", "nerf ulnaire", "C7-T1"),
    "Long extenseur radial du carpe": ("Poignet et main", "extension et inclinaison radiale du poignet", "nerf radial", "C6-C7"),
    "Fléchisseur profond des doigts": ("Poignet et main", "flexion des interphalangiennes distales", "nerfs médian et ulnaire", "C8-T1"),
    "Interosseux dorsaux": ("Poignet et main", "abduction des doigts", "nerf ulnaire", "C8-T1"),
    "Court abducteur du pouce": ("Poignet et main", "abduction du pouce", "nerf médian", "C8-T1"),
    "Ilio-psoas": ("Hanche", "flexion de la hanche", "nerf fémoral et branches du plexus lombaire", "L1-L3"),
    "Grand fessier": ("Hanche", "extension et rotation latérale de la hanche", "nerf glutéal inférieur", "L5-S2"),
    "Moyen fessier": ("Hanche", "abduction de la hanche, stabilisation du bassin en appui unipodal", "nerf glutéal supérieur", "L4-S1"),
    "Tenseur du fascia lata": ("Hanche", "abduction, flexion et rotation médiale de la hanche", "nerf glutéal supérieur", "L4-S1"),
    "Long adducteur": ("Hanche", "adduction de la hanche", "nerf obturateur", "L2-L4"),
    "Piriforme": ("Hanche", "rotation latérale de la hanche", "nerf du piriforme", "S1-S2"),
    "Sartorius": ("Hanche", "flexion, abduction et rotation latérale de hanche, flexion du genou", "nerf fémoral", "L2-L3"),
    "Quadriceps": ("Genou", "extension du genou", "nerf fémoral", "L2-L4"),
    "Ischio-jambiers": ("Genou", "flexion du genou et extension de la hanche", "nerf sciatique (partie tibiale surtout)", "L5-S2"),
    "Gracile": ("Genou", "adduction de hanche et flexion du genou", "nerf obturateur", "L2-L3"),
    "Poplité": ("Genou", "déverrouillage du genou (rotation médiale du tibia)", "nerf tibial", "L4-S1"),
    "Tibial antérieur": ("Cheville et pied", "flexion dorsale et inversion du pied", "nerf fibulaire profond", "L4-L5"),
    "Long extenseur de l'hallux": ("Cheville et pied", "extension du gros orteil", "nerf fibulaire profond", "L5"),
    "Long et court fibulaires": ("Cheville et pied", "éversion du pied", "nerf fibulaire superficiel", "L5-S1"),
    "Triceps sural": ("Cheville et pied", "flexion plantaire de la cheville", "nerf tibial", "S1-S2"),
    "Tibial postérieur": ("Cheville et pied", "inversion du pied, soutien de l'arche médiale", "nerf tibial", "L4-L5"),
    "Diaphragme": ("Tronc et cou", "inspiration", "nerf phrénique", "C3-C5"),
    "Droit de l'abdomen": ("Tronc et cou", "flexion du tronc", "nerfs intercostaux", "T7-T12"),
    "Transverse de l'abdomen": ("Tronc et cou", "gainage (augmente la pression intra-abdominale)", "nerfs intercostaux et ilio-hypogastrique", "T7-L1"),
    "Obliques de l'abdomen": ("Tronc et cou", "rotation et inclinaison du tronc", "nerfs intercostaux", "T7-T12"),
    "Érecteurs du rachis": ("Tronc et cou", "extension du rachis", "rameaux dorsaux des nerfs spinaux", "segmentaire"),
    "Multifides": ("Tronc et cou", "stabilisation segmentaire du rachis", "rameaux dorsaux des nerfs spinaux", "segmentaire"),
    "Sterno-cléido-mastoïdien": ("Tronc et cou", "flexion du cou, rotation de la tête du côté opposé", "nerf accessoire (XI)", "XI (C2-C3)"),
}

# articulation : [(mouvement, amplitude normale indicative en degrés, muscles principaux)]
JOINTS = {
    "Épaule": [("Flexion", 180, "deltoïde antérieur, grand pectoral (chef claviculaire), coraco-brachial"),
               ("Extension", 60, "grand dorsal, grand rond, deltoïde postérieur"),
               ("Abduction", 180, "deltoïde moyen, supra-épineux (+ trapèze et dentelé pour la scapula)"),
               ("Rotation latérale", 90, "infra-épineux, petit rond"),
               ("Rotation médiale", 70, "subscapulaire, grand pectoral, grand dorsal, grand rond")],
    "Coude": [("Flexion", 145, "biceps brachial, brachial, brachio-radial"),
              ("Extension", 0, "triceps brachial, anconé"),
              ("Pronation", 80, "rond pronateur, carré pronateur"),
              ("Supination", 80, "supinateur, biceps brachial")],
    "Poignet": [("Flexion", 80, "fléchisseurs radial et ulnaire du carpe, long palmaire"),
                ("Extension", 70, "extenseurs radiaux (long et court) et ulnaire du carpe"),
                ("Inclinaison radiale", 20, "fléchisseur radial et long extenseur radial du carpe"),
                ("Inclinaison ulnaire", 30, "fléchisseur et extenseur ulnaires du carpe")],
    "Hanche": [("Flexion (genou fléchi)", 120, "ilio-psoas, droit fémoral, tenseur du fascia lata, sartorius"),
               ("Extension", 20, "grand fessier, ischio-jambiers"),
               ("Abduction", 45, "moyen et petit fessiers, tenseur du fascia lata"),
               ("Adduction", 30, "long, court et grand adducteurs, gracile, pectiné"),
               ("Rotation latérale", 45, "piriforme, obturateurs, jumeaux, carré fémoral, grand fessier"),
               ("Rotation médiale", 45, "petit et moyen fessiers (fibres antérieures), tenseur du fascia lata")],
    "Genou": [("Flexion", 140, "ischio-jambiers, gastrocnémien, gracile, sartorius"),
              ("Extension", 0, "quadriceps")],
    "Cheville": [("Flexion dorsale", 20, "tibial antérieur, long extenseur des orteils, long extenseur de l'hallux"),
                 ("Flexion plantaire", 50, "triceps sural, tibial postérieur, fibulaires, longs fléchisseurs"),
                 ("Inversion", 35, "tibial postérieur, tibial antérieur"),
                 ("Éversion", 15, "long et court fibulaires")],
    "Rachis cervical": [("Flexion", 45, "sterno-cléido-mastoïdiens, longs du cou"),
                        ("Extension", 60, "trapèze supérieur, splénius, semi-épineux"),
                        ("Rotation (de chaque côté)", 70, "SCM controlatéral, splénius homolatéral")],
    "Rachis lombaire": [("Flexion", 60, "droit de l'abdomen, obliques"),
                        ("Extension", 25, "érecteurs du rachis, multifides"),
                        ("Inclinaison latérale", 25, "carré des lombes, obliques")],
}


def ch_generalites():
    ui.md(r"""
**Arthrologie : ce qui permet et limite un mouvement**
- La **forme des surfaces** (une trochlée n'autorise qu'un mouvement, une sphère trois).
- Les **ligaments et la capsule** : ils se tendent en fin de mouvement.
- Les **muscles** (actifs ou étirés) et le **contact des parties molles** (la flexion du genou s'arrête quand le
  mollet touche la cuisse).

**Myologie : comment lire l'action d'un muscle**
1. Repère son trajet : par où passe-t-il **par rapport à l'axe** de l'articulation ?
2. Un muscle qui passe **en avant** de l'axe de flexion-extension (au membre supérieur et à la hanche) fléchit ;
   en arrière, il étend. Au genou c'est l'inverse : le quadriceps, en avant, étend.
3. Son action peut **changer selon la position** : les adducteurs de hanche fléchissent la hanche quand elle est
   étendue, et l'étendent quand elle est très fléchie.

**[[chaîne cinétique ouverte|Chaîne ouverte]] ou [[chaîne cinétique fermée|fermée]]** ? Dans un leg extension
(ouverte), le quadriceps bouge le tibia ; dans un squat (fermée), il contrôle la descente du corps entier, en
excentrique.

**Les [[muscle biarticulaire|muscles biarticulaires]]** ont une longueur qui dépend de deux articulations, d'où
l'[[insuffisance active]] (trop court pour bien tirer) et l'[[insuffisance passive]] (trop long, il freine).
""")
    ui.tip("Teste l'insuffisance active : fléchis fort ton poignet, puis essaie de serrer le poing. Les fléchisseurs "
           "des doigts, déjà raccourcis au poignet, ne peuvent plus serrer fort. C'est pour ça qu'on désarme "
           "quelqu'un en lui fléchissant le poignet.")
    ui.memo("Pour retrouver l'action d'un muscle : « **d'où il part, où il arrive, par où il passe** ». Tire "
            "mentalement sur la terminaison vers l'origine : le mouvement obtenu est son action.")


def _joint_section(names):
    for j in names:
        st.markdown(f"#### {j}")
        ui.table([[m, f"{a}°", mus] for m, a, mus in JOINTS[j]], headers=["Mouvement", "Amplitude indicative", "Muscles principaux"])


def ch_membre_sup():
    ui.md(r"""
**L'épaule** est un **complexe** de 4 articulations : gléno-humérale, acromio-claviculaire, sterno-claviculaire, et
la « fausse » articulation scapulo-thoracique (glissement de la scapula sur le thorax). La gléno-humérale est la
plus mobile du corps, au prix d'une stabilité faible : la petite glène tient la grosse tête humérale grâce au
labrum, à la capsule et surtout à la [[coiffe des rotateurs]].

Lever le bras jusqu'à 180° demande environ 120° de gléno-humérale et 60° de rotation de la scapula : c'est le
[[rythme scapulo-huméral]] (2 pour 1).
""")
    ui.memo("Coiffe des rotateurs : **SIPS** (dans l'ordre, du haut vers l'arrière puis l'avant) : **S**upra-épineux, "
            "**I**nfra-épineux, **P**etit rond, **S**ubscapulaire. Le seul rotateur **médial** est le "
            "**S**ubscapulaire, le seul à l'avant.")
    _joint_section(["Épaule", "Coude", "Poignet"])
    ui.md(r"""
**Les trois nerfs de la main** : le [[nerf radial|radial]] commande **tous les extenseurs** ; le
[[nerf médian|médian]], la plupart des **fléchisseurs** de l'avant-bras et l'**éminence thénar** (pouce) ; le
[[nerf ulnaire|ulnaire]], la plupart des **petits muscles de la main** (interosseux, adducteur du pouce).
""")
    ui.clinic("Lésion du nerf radial (fracture de la diaphyse humérale) : **main tombante**, impossible d'étendre le "
              "poignet. Compression du médian au **canal carpien** : fourmillements des 3 premiers doigts la nuit, "
              "puis fonte de l'éminence thénar. Atteinte du thoracique long : **scapula alata** (décollée) quand on "
              "pousse contre un mur.")


def ch_membre_inf():
    ui.md(r"""
**La hanche** est une sphéroïde très **stable** (cotyle profond, labrum, ligaments puissants) : elle porte le
poids du corps. **Le genou** est surtout une charnière (flexion-extension) avec un peu de rotation genou fléchi.
Sa stabilité dépend des **ligaments** (croisés antérieur et postérieur, collatéraux), des **ménisques** et des
muscles. En fin d'extension, le tibia tourne latéralement : c'est le [[verrouillage du genou]].

**La cheville** (talo-crurale) fait la flexion dorsale et plantaire ; l'**inversion** et l'**éversion** se font
surtout dans la subtalaire, sous le talus.
""")
    _joint_section(["Hanche", "Genou", "Cheville"])
    ui.md(r"""
**Les nerfs** : le [[nerf fémoral|fémoral]] (L2-L4) en avant (quadriceps) ; l'**obturateur** (L2-L4) en dedans
(adducteurs) ; les **glutéaux** pour les fessiers ; le [[nerf sciatique|sciatique]] en arrière, qui se divise en
**tibial** (loge postérieure de jambe : flexion plantaire) et **fibulaire commun**, lui-même divisé en
**profond** (loge antérieure : flexion dorsale) et **superficiel** (loge latérale : éversion).
""")
    ui.memo("Les tendons de la **patte d'oie** (face médiale du genou), d'avant en arrière : « **S**er**G**en**T** » : "
            "**S**artorius, **G**racile, semi-**T**endineux. Trois muscles, trois nerfs différents (fémoral, "
            "obturateur, sciatique).")


def ch_rachis():
    ui.md(r"""
**La colonne** : 7 cervicales, 12 thoraciques, 5 lombaires, le sacrum (5 vertèbres soudées) et le coccyx. Elle
présente des **courbures** : lordose cervicale, cyphose thoracique, lordose lombaire. Ces courbures augmentent sa
résistance aux charges verticales.

Chaque **segment mobile** = deux vertèbres + le **disque** (anneau fibreux autour d'un noyau gélatineux) + deux
**articulations zygapophysaires** (facettes) + les ligaments. L'orientation des facettes dicte les mouvements :
- **cervical** : très mobile dans tous les plans ; C1-C2 assure la moitié de la rotation de la tête ;
- **thoracique** : rotations, mais flexion-extension limitée par les côtes ;
- **lombaire** : flexion-extension, très peu de rotation (facettes dans le plan sagittal).
""")
    _joint_section(["Rachis cervical", "Rachis lombaire"])
    ui.md(r"""
**Les muscles du tronc** travaillent en **caisson** : le transverse de l'abdomen, le diaphragme, le plancher
pelvien et les multifides augmentent la pression intra-abdominale et stabilisent le rachis pendant les mouvements
des membres.
""")
    ui.memo("**C3, C4, C5 keep the diaphragm alive** : le nerf phrénique vient de C3-C5. Une lésion médullaire "
            "au-dessus de C3 nécessite une ventilation assistée.")


def ch_explorateur():
    st.markdown("Choisis une région ou cherche un muscle. Les amplitudes et innervations sont celles du cours, "
                "à vérifier dans ton syllabus si ton prof donne d'autres valeurs (elles varient selon les sources).")
    c1, c2 = st.columns(2)
    region = c1.selectbox("Région", ["Toutes"] + sorted({v[0] for v in MUSCLES.values()}), key="al_region")
    query = c2.text_input("Recherche (muscle, nerf, action, racine)", key="al_q", placeholder="ex. fibulaire, L5, rotation")
    rows = []
    for name, (reg, action, nerf, racines) in MUSCLES.items():
        if region != "Toutes" and reg != region:
            continue
        hay = f"{name} {action} {nerf} {racines}".lower()
        if query and query.lower() not in hay:
            continue
        rows.append([name, action, nerf, racines])
    ui.table(rows, headers=["Muscle", "Action principale", "Innervation", "Racines"])

    st.markdown("#### Goniomètre virtuel")
    st.caption("Visualise l'amplitude normale d'un mouvement et compare-la à une mesure.")
    c1, c2 = st.columns([1, 2])
    with c1:
        joint = st.selectbox("Articulation", list(JOINTS), key="al_gonio_j")
        mvt = st.selectbox("Mouvement", [m for m, _, _ in JOINTS[joint]], key="al_gonio_m")
        normal = dict((m, a) for m, a, _ in JOINTS[joint])[mvt]
        mesure = st.slider("Amplitude mesurée chez ton patient (°)", 0, 180, min(normal, 180) // 2, key="al_gonio_v")
    with c2:
        def arc(angle, r):
            pts = [i * angle / 40 for i in range(41)]
            return [0] + [r * math.cos(math.radians(p)) for p in pts] + [0], \
                   [0] + [r * math.sin(math.radians(p)) for p in pts] + [0]
        fig = go.Figure()
        x, y = arc(max(normal, 1), 1.0)
        fig.add_trace(go.Scatter(x=x, y=y, fill="toself", name=f"Normal : {normal}°", opacity=0.3))
        x, y = arc(max(mesure, 1), 0.8)
        fig.add_trace(go.Scatter(x=x, y=y, fill="toself", name=f"Mesuré : {mesure}°", opacity=0.6))
        fig.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10), xaxis=dict(visible=False, range=[-1.1, 1.1]),
                          yaxis=dict(visible=False, scaleanchor="x", range=[-0.2, 1.1]), legend=dict(orientation="h"))
        st.plotly_chart(fig, width="stretch")
        if normal:
            st.metric("Pourcentage de l'amplitude normale", f"{mesure / normal:.0%}")


def ch_analyse():
    ui.md(r"""
**Méthode d'analyse d'un mouvement** (posture ou geste sportif)
1. **Découper** le geste en phases (préparation, action, suivi).
2. Pour chaque articulation et chaque phase : quel **mouvement**, dans quel **plan**, quelle **amplitude** ?
3. Quelle **force** extérieure (gravité, charge, sol) ? Elle crée un moment que les muscles doivent contrer.
4. Quels **muscles** travaillent, et en quel **mode** : concentrique (ils raccourcissent), excentrique (ils freinent
   en s'allongeant), isométrique ?
5. Où sont les **contraintes** (articulation, tendon) et les **risques** ?
""")
    st.markdown("#### Exemple : le squat")
    ui.table([
        ["Descente", "Hanche", "Flexion", "Grand fessier, ischio-jambiers", "Excentrique"],
        ["Descente", "Genou", "Flexion", "Quadriceps", "Excentrique"],
        ["Descente", "Cheville", "Flexion dorsale", "Triceps sural", "Excentrique"],
        ["Remontée", "Hanche", "Extension", "Grand fessier, ischio-jambiers", "Concentrique"],
        ["Remontée", "Genou", "Extension", "Quadriceps", "Concentrique"],
        ["Remontée", "Cheville", "Flexion plantaire", "Triceps sural", "Concentrique"],
        ["Tout le long", "Tronc", "Maintien", "Érecteurs du rachis, abdominaux", "Isométrique"],
    ], headers=["Phase", "Articulation", "Mouvement", "Muscles moteurs", "Mode"])
    ui.warn("Piège classique : à la descente du squat, ce ne sont **pas** les fléchisseurs du genou qui travaillent ! "
            "C'est la gravité qui fléchit, et le **quadriceps** freine en excentrique. Demande-toi toujours : "
            "qui fait le mouvement, la gravité ou le muscle ?")
    ui.md(r"""
**Analyse posturale** (vue de profil) : la ligne de gravité passe normalement par le lobe de l'oreille, l'acromion,
un peu en arrière de la hanche, un peu en avant du genou et en avant de la malléole latérale. Les écarts
(tête en avant, hyperlordose, genu recurvatum) indiquent quelles structures sont surchargées.
""")


CHAPTERS = [
    ("Généralités", ch_generalites),
    ("Membre supérieur", ch_membre_sup),
    ("Membre inférieur", ch_membre_inf),
    ("Rachis et tronc", ch_rachis),
    ("Explorateur et goniomètre", ch_explorateur),
    ("Analyse du mouvement", ch_analyse),
]

_NERFS = sorted({v[2] for v in MUSCLES.values()})
_ACTIONS = sorted({v[1] for v in MUSCLES.values()})


def _q_nerf(rng):
    m = rng.choice(list(MUSCLES))
    good = MUSCLES[m][2]
    return (f"Quel nerf innerve le muscle **{m}** ?", good, [n for n in _NERFS if n != good],
            f"{m} : {good} ({MUSCLES[m][3]}).")


def _q_action(rng):
    m = rng.choice(list(MUSCLES))
    good = MUSCLES[m][1]
    return (f"Quelle est l'action principale du muscle **{m}** ?", good, [a for a in _ACTIONS if a != good], "")


def _q_muscle(rng):
    m = rng.choice(list(MUSCLES))
    reg, action, _, _ = MUSCLES[m]
    bad = [k for k, v in MUSCLES.items() if v[1] != action and v[0] == reg] or [k for k in MUSCLES if k != m]
    return (f"Quel muscle a pour action principale : **{action}** ?", m, bad, "")


def _q_amplitude(rng):
    j = rng.choice(list(JOINTS))
    mvt, a, _ = rng.choice(JOINTS[j])
    opts = sorted({x for x in [a, a + 30, max(0, a - 30), a + 60, 0, 90] if x != a})
    return (f"Quelle est l'amplitude normale indicative de **{mvt.lower()}** ({j.lower()}) ?", f"{a}°",
            [f"{x}°" for x in opts], "Valeurs indicatives (AAOS), elles varient un peu selon les sources.")


def _q_racine(rng):
    m = rng.choice([k for k, v in MUSCLES.items() if v[3][0] in "CLS" and "-" in v[3]])
    good = MUSCLES[m][3]
    return (f"De quelles racines vient principalement l'innervation du muscle **{m}** ?", good,
            sorted({v[3] for v in MUSCLES.values() if v[3] != good and v[3][0] in "CLS"}), "")


QUESTIONS = [
    gen_qcm(1, _q_action),
    gen_qcm(1, _q_muscle),
    qcm(1, "Quels muscles forment la coiffe des rotateurs ?", "Supra-épineux, infra-épineux, petit rond, subscapulaire",
        ["Deltoïde, trapèze, rhomboïdes, dentelé", "Grand pectoral, grand dorsal, grand rond, petit rond",
         "Biceps, triceps, brachial, brachio-radial"]),
    qcm(1, "Combien de vertèbres lombaires a-t-on ?", "5", ["7", "12", "4"]),
    vf(1, "Le quadriceps fléchit le genou.", False, "Il l'étend (le droit fémoral fléchit aussi la hanche)."),
    gen_qcm(2, _q_nerf),
    gen_qcm(2, _q_amplitude),
    qcm(2, "Quel est le seul muscle de la coiffe qui fait une rotation médiale ?", "Subscapulaire",
        ["Infra-épineux", "Petit rond", "Supra-épineux"]),
    qcm(2, "Le rythme scapulo-huméral pendant l'élévation du bras est d'environ…",
        "2° gléno-huméral pour 1° scapulo-thoracique", ["1 pour 1", "1 pour 2", "Uniquement gléno-huméral"]),
    multi(2, "Quels muscles sont biarticulaires ?", ["Droit fémoral", "Gastrocnémien", "Ischio-jambiers"],
          ["Soléaire", "Vaste latéral", "Brachial"]),
    qcm(2, "Au rachis lombaire, le mouvement le plus limité est…", "la rotation", ["la flexion", "l'extension",
        "l'inclinaison latérale"], "Les facettes lombaires sont orientées dans le plan sagittal."),
    gen_qcm(3, _q_racine),
    qcm(3, "Pendant la descente d'un squat, quel muscle contrôle la flexion du genou ?",
        "Le quadriceps, en excentrique", ["Les ischio-jambiers, en concentrique", "Le poplité, en isométrique",
        "Le gastrocnémien, en concentrique"]),
    qcm(3, "Un patient ne peut plus étendre le poignet après une fracture de la diaphyse humérale. Quel nerf est atteint ?",
        "Le nerf radial", ["Le nerf médian", "Le nerf ulnaire", "Le nerf axillaire"],
        "Le radial longe la diaphyse humérale dans la gouttière radiale."),
    qcm(3, "Un patient présente une scapula « décollée » quand il pousse contre un mur. Quel muscle est déficient ?",
        "Le dentelé antérieur (nerf thoracique long)", ["Le trapèze moyen", "Le grand pectoral", "Les rhomboïdes"]),
    qcm(3, "Pourquoi est-il difficile de fléchir complètement la hanche genou tendu ?",
        "Insuffisance passive des ischio-jambiers, étirés sur les deux articulations",
        ["Insuffisance active du quadriceps", "Blocage osseux de la hanche", "Contraction du psoas"]),
    qcm(3, "Un patient a un pied tombant et ne peut plus faire l'éversion, mais garde la flexion plantaire. Quel nerf ?",
        "Le nerf fibulaire commun", ["Le nerf tibial", "Le nerf fémoral", "Le nerf obturateur"],
        "Ses deux branches commandent la flexion dorsale (profond) et l'éversion (superficiel)."),
]

CARDS = [(m, f"{v[1]} · {v[2]} ({v[3]})") for m, v in MUSCLES.items()] + [
    ("Coiffe des rotateurs", "Supra-épineux, infra-épineux, petit rond, subscapulaire"),
    ("Rythme scapulo-huméral", "2° gléno-huméral : 1° scapulo-thoracique"),
    ("Nerf phrénique", "C3-C5 (« keep the diaphragm alive »)"),
    ("Verrouillage du genou", "Rotation latérale du tibia en fin d'extension ; déverrouillé par le poplité"),
]

VIDEOS = [
    ("Anatomie de l'épaule et coiffe des rotateurs", "anatomie épaule coiffe des rotateurs muscles"),
    ("Muscles du membre inférieur", "anatomie muscles membre inférieur cuisse jambe"),
    ("Innervation du membre supérieur : radial, médian, ulnaire", "nerf radial médian ulnaire anatomie territoires"),
    ("Analyse biomécanique du squat", "analyse squat muscles excentrique concentrique"),
]

LINKS = [
    ("Kenhub : muscles du membre supérieur", "https://www.kenhub.com/fr/library/anatomie/muscles-du-membre-superieur"),
    ("Physiopedia : Range of motion normative values", "https://www.physio-pedia.com/Range_of_Motion_Normative_Values"),
]
