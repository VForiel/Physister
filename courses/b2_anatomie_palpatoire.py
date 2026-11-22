"""LKNR1203 Anatomie palpatoire."""

import streamlit as st

from app import ui
from app.course import Course
from app.quiz import gen_qcm, multi, qcm, vf

COURSE = Course(
    code="LKNR1203", title="Anatomie palpatoire", short="Anatomie palpatoire",
    bloc=2, quad=1, credits=3, hours="7,5 h + 30 h", icon=":material/back_hand:",
    intro="Trouver sous ses doigts ce qu'on a appris dans les livres : os, tendons, muscles, artères, nerfs. "
          "C'est surtout de la pratique en binôme ; ce chapitre te donne la méthode, les repères région par région "
          "et des fiches pour réviser avant les TP.",
    acquis=[
        "Réaliser les actes techniques de palpation sur un pair.",
        "Identifier les structures osseuses et les tissus mous.",
        "Décrire le mouvement, les muscles en action et les limitations.",
        "Analyser le mouvement sur des vignettes simples et en faire une synthèse fonctionnelle.",
    ],
)

TERMS = {
    "palpation": ("Palpation", "Examen par le toucher pour localiser et apprécier une structure (forme, consistance, "
                  "sensibilité, chaleur).", "Palpation"),
    "repère osseux": ("Repère osseux", "Relief osseux facile à palper qui sert de point de départ pour trouver les "
                      "autres structures.", None),
    "tabatière anatomique": ("Tabatière anatomique", "Creux à la base du pouce, entre les tendons du long extenseur "
                             "et du court extenseur du pouce ; on y palpe le scaphoïde et l'artère radiale.",
                             "Tabatière anatomique"),
    "triangle de scarpa": ("Triangle fémoral (de Scarpa)", "Zone du pli de l'aine où passent le nerf, l'artère et la "
                           "veine fémorale (de dehors en dedans : NAV).", "Triangle fémoral"),
}

# région : [(structure, comment la trouver)]
REPERES = {
    "Épaule": [
        ("Acromion", "Suivre l'épine de la scapula vers le dehors jusqu'à son bord plat au sommet de l'épaule."),
        ("Articulation acromio-claviculaire", "Petite marche entre le bout de la clavicule et l'acromion ; bouger le bras en avant pour la sentir."),
        ("Processus coracoïde", "Sous la clavicule, environ 2 cm en dedans de la tête humérale, dans le creux delto-pectoral ; profond, sensible."),
        ("Tubercule majeur", "Sous l'acromion, en dehors ; insertion du supra-épineux, mieux accessible bras en rotation médiale derrière le dos."),
        ("Sillon intertuberculaire", "Entre les tubercules majeur et mineur ; contient le long chef du biceps, roule sous les doigts en rotation."),
        ("Angle inférieur de la scapula", "En bas de la scapula, vers T7 ; suit la sonnette quand on lève le bras."),
    ],
    "Coude et avant-bras": [
        ("Épicondyle latéral", "Relief externe de l'humérus distal ; origine des extenseurs du poignet (épicondylalgie)."),
        ("Épicondyle médial", "Relief interne, plus saillant ; origine des fléchisseurs et du rond pronateur."),
        ("Olécrâne", "Pointe du coude ; forme un triangle avec les épicondyles, coude fléchi à 90°."),
        ("Tête radiale", "2 cm sous l'épicondyle latéral ; elle tourne sous le doigt en prono-supination."),
        ("Nerf ulnaire", "Dans la gouttière derrière l'épicondyle médial (« petit juif ») ; le presser donne des fourmillements."),
    ],
    "Poignet et main": [
        ("Processus styloïde du radius", "Relief externe du poignet, plus bas que celui de l'ulna."),
        ("Processus styloïde de l'ulna", "Relief interne et postérieur du poignet."),
        ("Scaphoïde", "Au fond de la tabatière anatomique, poignet en inclinaison ulnaire ; douleur à ce niveau après une chute = fracture à exclure."),
        ("Pisiforme", "Petit os rond à la base de l'éminence hypothénar, côté ulnaire ; tendon du fléchisseur ulnaire du carpe."),
        ("Artère radiale", "Pouls à la face antérieure du poignet, en dehors du tendon du fléchisseur radial du carpe."),
    ],
    "Bassin et hanche": [
        ("Crête iliaque", "Bord supérieur de l'os coxal ; le sommet des crêtes est au niveau de L4-L5."),
        ("Épine iliaque antéro-supérieure (EIAS)", "Bout antérieur de la crête iliaque ; origine du sartorius."),
        ("Épine iliaque postéro-supérieure (EIPS)", "Sous les fossettes lombaires (de Vénus), au niveau de S2."),
        ("Grand trochanter", "Relief latéral de la cuisse, une main sous la crête iliaque ; il tourne en rotation de hanche."),
        ("Tubérosité ischiatique", "Sous le pli de la fesse, hanche fléchie ; origine des ischio-jambiers."),
        ("Artère fémorale", "Pouls au pli de l'aine, à mi-chemin entre EIAS et symphyse pubienne (triangle fémoral)."),
    ],
    "Genou": [
        ("Patella", "Os sésamoïde devant le genou ; mobile genou tendu et relâché."),
        ("Tubérosité tibiale", "Relief sous la patella où s'insère le tendon patellaire."),
        ("Interligne fémoro-tibial", "Creux de part et d'autre du tendon patellaire, genou fléchi ; on y palpe les ménisques."),
        ("Tête de la fibula", "Face latérale, sous le genou, au niveau de la tubérosité tibiale ; insertion du biceps fémoral."),
        ("Nerf fibulaire commun", "Contourne le col de la fibula, juste sous sa tête : zone de compression (plâtre, jambes croisées)."),
        ("Artère poplitée", "Pouls profond au creux poplité, genou légèrement fléchi et relâché."),
    ],
    "Cheville et pied": [
        ("Malléole latérale", "Bout distal de la fibula, plus bas et plus en arrière que la malléole médiale."),
        ("Malléole médiale", "Bout distal du tibia."),
        ("Ligament talo-fibulaire antérieur", "En avant et sous la malléole latérale ; le plus souvent lésé dans l'entorse."),
        ("Base du 5e métatarsien", "Relief au bord latéral du pied ; insertion du court fibulaire ; à palper dans les règles d'Ottawa."),
        ("Tendon calcanéen (d'Achille)", "Gros tendon derrière la cheville, du triceps sural au calcanéus."),
        ("Artère dorsale du pied (pédieuse)", "Pouls sur le dos du pied, en dehors du tendon du long extenseur de l'hallux."),
        ("Artère tibiale postérieure", "Pouls derrière la malléole médiale."),
    ],
    "Rachis": [
        ("C7 (vertèbre proéminente)", "Le processus épineux le plus saillant à la base du cou ; il reste en place en extension du cou, alors que C6 s'enfonce."),
        ("Épine de la scapula", "Au niveau de T3."),
        ("Angle inférieur de la scapula", "Au niveau de T7."),
        ("Sommet des crêtes iliaques", "Au niveau de L4-L5."),
        ("EIPS", "Au niveau de S2."),
    ],
}


def ch_methode():
    ui.md(r"""
**Le toucher** n'est pas neutre : il informe le kiné, mais il communique aussi (confiance, respect, ou au contraire
inconfort). Toujours **prévenir** et expliquer avant de toucher, demander le **consentement**, respecter la pudeur,
avoir les mains propres et tièdes.

**La méthode de [[palpation]]**
1. Partir d'un **[[repère osseux]]** facile (on n'arrive jamais directement sur une petite structure).
2. Se déplacer de proche en proche, en connaissant les **distances** et les directions.
3. Adapter la **pression** : légère pour la peau, plus profonde pour un muscle profond.
4. **Faire bouger** : une contraction fait saillir un muscle ou un tendon (contracter contre résistance), un
   mouvement passif fait rouler un relief osseux sous le doigt.
5. Comparer avec le **côté opposé**.
6. Vérifier : si c'est la bonne structure, elle doit réagir comme prévu (tendon qui se tend, os qui tourne).
""")
    ui.tip("Pour identifier un muscle : demande l'**action** de ce muscle contre une légère résistance, et palpe "
           "là où il doit se contracter. S'il ne se contracte pas, tu n'es pas sur le bon muscle (ou pas dans la "
           "bonne action).")
    ui.memo("Au pli de l'aine, de **dehors en dedans** : **N**erf, **A**rtère, **V**eine fémoraux (« **NAV**ire », "
            "puis les lymphatiques). Dans le [[triangle de scarpa|triangle fémoral]].")


def ch_regions():
    region = st.selectbox("Région", list(REPERES), key="ap_region")
    ui.table([[s, h] for s, h in REPERES[region]], headers=["Structure", "Comment la trouver"])
    if region == "Poignet et main":
        ui.md("La [[tabatière anatomique]] est un excellent point de départ pour le scaphoïde et l'artère radiale.")
    if region == "Rachis":
        ui.clinic("Ces repères aident à compter les vertèbres, mais ils sont **imprécis** (on se trompe souvent d'un "
                  "niveau). Combine-en plusieurs et vérifie par le mouvement.")
    st.markdown("#### Les pouls à connaître")
    ui.table([
        ["Carotidien", "sur le côté du cou, en avant du sterno-cléido-mastoïdien (jamais des deux côtés à la fois)"],
        ["Radial", "face antérieure du poignet, côté pouce"],
        ["Brachial", "face médiale du bras, au pli du coude en dedans du tendon du biceps"],
        ["Fémoral", "pli de l'aine, triangle fémoral"],
        ["Poplité", "creux du genou, profond"],
        ["Tibial postérieur", "derrière la malléole médiale"],
        ["Dorsal du pied", "dos du pied, en dehors du tendon du long extenseur de l'hallux"],
    ], headers=["Pouls", "Où le prendre"])
    ui.warn("Ne prends jamais le pouls avec le **pouce** : il a son propre pouls, et tu risques de sentir le tien. "
            "Utilise l'index et le majeur.")


def ch_mouvement():
    ui.md(r"""
La palpation sert aussi à **analyser le mouvement** : sentir quel muscle se contracte, à quel moment, dans quel
ordre, et où se situe la limitation.

**Grille d'analyse d'un mouvement simple** (comme en vignette)
1. Dans quel **plan** et autour de quel **axe** se fait le mouvement ?
2. Quelle **amplitude** (comparée à la norme et au côté opposé) ?
3. Quels **muscles** sont en action, et en quel mode (concentrique, excentrique, isométrique) ? Comment le vérifier
   à la palpation ?
4. Quelle est la **limitation** : douleur, raideur (capsule, muscle), faiblesse, peur ?
5. **Synthèse** : comment ces éléments expliquent-ils la gêne fonctionnelle du patient ?

**Exemple** : lever le bras en abduction. Plan frontal, axe sagittal. Amplitude normale 180°. Le deltoïde moyen et
le supra-épineux en concentrique, le trapèze et le dentelé antérieur font tourner la scapula (palpe l'angle
inférieur qui part en dehors). Si la scapula bouge trop tôt et trop fort (« haussement d'épaule »), la
gléno-humérale est probablement limitée ou douloureuse.
""")
    ui.clinic("Toucher une zone douloureuse peut aussi apaiser : le toucher calme, rassure, et active des mécanismes "
              "de modulation de la douleur. C'est un effet réel, mais à ne pas confondre avec un effet sur la "
              "structure palpée.")


CHAPTERS = [
    ("Le toucher et la méthode", ch_methode),
    ("Repères région par région", ch_regions),
    ("Palper pour analyser le mouvement", ch_mouvement),
]

ALL = [(s, h, r) for r, items in REPERES.items() for s, h in items]
NIVEAUX = {"C7 (vertèbre proéminente)": "C7", "Épine de la scapula": "T3", "Angle inférieur de la scapula": "T7",
           "Sommet des crêtes iliaques": "L4-L5", "EIPS": "S2"}


def _q_repere(rng):
    s, h, r = rng.choice(ALL)
    others = [x for x, _, rr in ALL if x != s and rr == r]
    return (f"Quelle structure trouve-t-on ainsi ? « {h} »", s, others, "")


def _q_niveau(rng):
    k = rng.choice(list(NIVEAUX))
    return (f"À quel niveau vertébral correspond le repère **{k}** ?", NIVEAUX[k], list(NIVEAUX.values()), "")


QUESTIONS = [
    gen_qcm(1, _q_repere),
    qcm(1, "Avec quels doigts prend-on un pouls ?", "Index et majeur", ["Le pouce", "Le petit doigt seul", "La paume"]),
    vf(1, "La malléole latérale descend plus bas que la malléole médiale.", True),
    qcm(1, "Où palpe-t-on le pouls fémoral ?", "Au pli de l'aine", ["Derrière le genou", "Derrière la malléole médiale", "Au cou"]),
    gen_qcm(2, _q_niveau),
    qcm(2, "Au pli de l'aine, de dehors en dedans, on trouve…", "nerf, artère, veine", ["veine, artère, nerf",
        "artère, nerf, veine", "nerf, veine, artère"]),
    qcm(2, "Comment distinguer C7 de C6 à la palpation ?", "En extension du cou, C6 s'enfonce alors que C7 reste en place",
        ["C6 est toujours plus saillante", "C7 bouge en rotation du tronc", "On ne peut pas"]),
    multi(2, "Quelles structures palpe-t-on dans la tabatière anatomique ?", ["Le scaphoïde", "L'artère radiale"],
          ["Le pisiforme", "Le nerf ulnaire"]),
    qcm(2, "Pour bien identifier un muscle à la palpation, que faire ?", "Lui faire réaliser son action contre une légère résistance",
        ["Appuyer très fort", "Le palper au repos uniquement", "Demander au patient de se détendre complètement"]),
    qcm(3, "Après une chute sur la main, un patient a mal au fond de la tabatière anatomique. Que suspecter ?",
        "Une fracture du scaphoïde, à faire vérifier", ["Une épicondylalgie", "Une simple contusion sans importance",
        "Une tendinopathie d'Achille"]),
    qcm(3, "Un patient a un pied tombant après avoir porté un plâtre serré sous le genou. Quel nerf a pu être comprimé ?",
        "Le nerf fibulaire commun, au col de la fibula", ["Le nerf tibial, au creux poplité", "Le nerf fémoral",
        "Le nerf sciatique à la fesse"]),
    qcm(3, "Pendant l'abduction du bras, l'angle inférieur de la scapula ne part pas en dehors. Quel muscle vérifier ?",
        "Le dentelé antérieur", ["Le grand dorsal", "Les rhomboïdes", "Le subscapulaire"],
        "Avec le trapèze, il produit la sonnette latérale."),
    qcm(3, "Quel ligament de la cheville palpe-t-on en avant et sous la malléole latérale, souvent douloureux après une entorse ?",
        "Le talo-fibulaire antérieur", ["Le deltoïde", "Le calcanéo-fibulaire", "Le talo-fibulaire postérieur"]),
]

CARDS = list({s: h for s, h, _ in ALL}.items()) + [
    ("Pli de l'aine (dehors → dedans)", "Nerf, artère, veine (NAV)"),
    ("Pouls tibial postérieur", "Derrière la malléole médiale"),
    ("Pouls dorsal du pied", "En dehors du tendon du long extenseur de l'hallux"),
]

VIDEOS = [
    ("Palpation de l'épaule", "palpation épaule acromion coracoïde kinésithérapie"),
    ("Palpation du genou", "palpation genou interligne tête fibula"),
    ("Palpation de la cheville et du pied", "palpation cheville pied malléole kiné"),
    ("Prise des pouls périphériques", "prise des pouls périphériques technique"),
]

LINKS = [("Physiopedia : Palpation", "https://www.physio-pedia.com/index.php?search=palpation")]
