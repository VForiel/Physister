"""LFSM1104 Biologie et éléments d'histologie."""

import random

import streamlit as st

from app import ui
from app.course import Course
from app.quiz import gen_qcm, multi, num, qcm, table_qcm, vf

COURSE = Course(
    code="LFSM1104", title="Biologie et éléments d'histologie", short="Biologie et histologie",
    bloc=1, quad=2, credits=5, hours="45 h", icon=":material/biotech:",
    intro="De la cellule aux tissus : comment une cellule fonctionne, comment l'information génétique devient une "
          "protéine, comment les cellules se divisent, et de quoi sont faits les tissus que tu soigneras (muscle, "
          "tendon, cartilage, os, nerf).",
    acquis=[
        "Comprendre l'unicité et la diversité du monde vivant.",
        "Décrire la structure et le fonctionnement de la cellule et du génome humain.",
        "Expliquer la division cellulaire et les bases du développement embryonnaire.",
        "Décrire la structure des principaux tissus humains, en particulier ceux liés au mouvement.",
    ],
)

TERMS = {
    "eucaryote": ("Eucaryote", "Cellule avec un vrai noyau entouré d'une membrane et des organites (animaux, "
                  "plantes, champignons). Les bactéries sont procaryotes : pas de noyau.", "Eucaryote"),
    "mitochondrie": ("Mitochondrie", "Organite qui produit l'essentiel de l'ATP par la respiration cellulaire. "
                     "Elle a son propre ADN, transmis par la mère.", "Mitochondrie"),
    "réticulum endoplasmique": ("Réticulum endoplasmique", "Réseau de membranes : rugueux (avec ribosomes, "
                                "fabrique des protéines) ou lisse (lipides, et stock de calcium dans le muscle, "
                                "où il s'appelle réticulum sarcoplasmique).", "Réticulum endoplasmique"),
    "appareil de golgi": ("Appareil de Golgi", "Organite qui modifie, trie et emballe les protéines avant de les "
                          "envoyer à leur destination.", "Appareil de Golgi"),
    "ribosome": ("Ribosome", "Machine qui lit l'ARN messager et assemble les acides aminés en protéine.", "Ribosome"),
    "transcription": ("Transcription", "Copie d'un gène de l'ADN en ARN messager, dans le noyau.",
                      "Transcription (biologie)"),
    "traduction": ("Traduction", "Lecture de l'ARN messager par le ribosome pour fabriquer une protéine, codon par "
                   "codon.", "Traduction génétique"),
    "codon": ("Codon", "Groupe de trois nucléotides de l'ARN messager qui code un acide aminé (ou un arrêt).", "Codon"),
    "mitose": ("Mitose", "Division d'une cellule en deux cellules filles identiques (même nombre de chromosomes).",
               "Mitose"),
    "méiose": ("Méiose", "Double division qui produit les gamètes : quatre cellules à 23 chromosomes, toutes "
               "génétiquement différentes.", "Méiose"),
    "gamète": ("Gamète", "Cellule reproductrice (spermatozoïde ou ovocyte), haploïde (23 chromosomes).", "Gamète"),
    "feuillets embryonnaires": ("Feuillets embryonnaires", "Les trois couches de cellules de l'embryon : "
                                "ectoderme (peau, système nerveux), mésoderme (muscles, os, sang, cœur), endoderme "
                                "(tube digestif, poumons).", "Feuillet embryonnaire"),
    "épithélium": ("Épithélium", "Tissu de cellules jointives qui recouvre les surfaces (peau) ou tapisse les "
                   "cavités, ou forme les glandes.", "Épithélium"),
    "tissu conjonctif": ("Tissu conjonctif", "Tissu de soutien fait de cellules dispersées dans une matrice "
                         "extracellulaire (fibres + substance fondamentale) : tendon, ligament, cartilage, os, "
                         "graisse.", "Tissu conjonctif"),
    "fibroblaste": ("Fibroblaste", "Cellule du tissu conjonctif qui fabrique le collagène et la matrice.", "Fibroblaste"),
    "chondrocyte": ("Chondrocyte", "Cellule du cartilage, enfermée dans sa matrice.", "Chondrocyte"),
    "ostéoblaste": ("Ostéoblaste", "Cellule qui fabrique l'os. L'ostéoclaste le résorbe ; l'ostéocyte est un "
                    "ostéoblaste emmuré dans l'os.", "Ostéoblaste"),
    "neurone": ("Neurone", "Cellule nerveuse qui reçoit (dendrites), intègre (corps cellulaire) et transmet "
                "(axone) l'influx nerveux.", "Neurone"),
    "cellule gliale": ("Cellule gliale", "Cellule de soutien du système nerveux (astrocytes, oligodendrocytes, "
                       "cellules de Schwann qui forment la myéline…).", "Cellule gliale"),
}

CODONS = {
    "UUU": "Phe", "UUC": "Phe", "UUA": "Leu", "UUG": "Leu", "CUU": "Leu", "CUC": "Leu", "CUA": "Leu", "CUG": "Leu",
    "AUU": "Ile", "AUC": "Ile", "AUA": "Ile", "AUG": "Met", "GUU": "Val", "GUC": "Val", "GUA": "Val", "GUG": "Val",
    "UCU": "Ser", "UCC": "Ser", "UCA": "Ser", "UCG": "Ser", "CCU": "Pro", "CCC": "Pro", "CCA": "Pro", "CCG": "Pro",
    "ACU": "Thr", "ACC": "Thr", "ACA": "Thr", "ACG": "Thr", "GCU": "Ala", "GCC": "Ala", "GCA": "Ala", "GCG": "Ala",
    "UAU": "Tyr", "UAC": "Tyr", "UAA": "STOP", "UAG": "STOP", "CAU": "His", "CAC": "His", "CAA": "Gln", "CAG": "Gln",
    "AAU": "Asn", "AAC": "Asn", "AAA": "Lys", "AAG": "Lys", "GAU": "Asp", "GAC": "Asp", "GAA": "Glu", "GAG": "Glu",
    "UGU": "Cys", "UGC": "Cys", "UGA": "STOP", "UGG": "Trp", "CGU": "Arg", "CGC": "Arg", "CGA": "Arg", "CGG": "Arg",
    "AGU": "Ser", "AGC": "Ser", "AGA": "Arg", "AGG": "Arg", "GGU": "Gly", "GGC": "Gly", "GGA": "Gly", "GGG": "Gly",
}
COMPL = {"A": "U", "T": "A", "C": "G", "G": "C"}  # brin matrice d'ADN → ARNm


def ch_cellule():
    ui.md(r"""
**L'unicité du vivant** : tous les êtres vivants sont faits de cellules, utilisent l'ADN comme support de
l'information, le même code génétique, et l'ATP comme monnaie énergétique. **La diversité** vient de
l'évolution : variation (mutations) + sélection naturelle.

La cellule humaine est **[[eucaryote]]** : un noyau et des organites, chacun avec sa fonction.

| Organite | Fonction |
|---|---|
| Membrane plasmique | bicouche de phospholipides avec protéines : barrière sélective, récepteurs |
| Noyau | contient l'ADN (46 chromosomes), lieu de la transcription |
| [[ribosome\|Ribosomes]] | fabriquent les protéines |
| [[réticulum endoplasmique\|Réticulum endoplasmique]] | rugueux : protéines ; lisse : lipides, stock de Ca²⁺ |
| [[appareil de golgi\|Appareil de Golgi]] | modifie, trie et expédie les protéines |
| [[mitochondrie\|Mitochondries]] | produisent l'ATP (respiration cellulaire) |
| Lysosomes | digestion des déchets (« estomac » de la cellule) |
| Cytosquelette | charpente et transport (microtubules, filaments d'actine, filaments intermédiaires) |
""")
    ui.memo("Le trajet d'une protéine à exporter (par exemple le collagène) : **ADN → ARNm → ribosome sur le "
            "réticulum rugueux → Golgi → vésicule → membrane → dehors**. Comme une usine : plan, chaîne de "
            "montage, emballage, expédition.")
    ui.clinic("Les fibres musculaires ont énormément de **mitochondries**, et l'entraînement en endurance en augmente "
              "le nombre. C'est une des raisons pour lesquelles un muscle entraîné se fatigue moins vite.")


def ch_genetique():
    ui.md(r"""
**L'ADN** est une double hélice de [[nucléotide|nucléotides]] (bases A, T, C, G ; A–T et C–G). Un **gène** est
un segment d'ADN qui code une protéine (ou un ARN). Le génome humain compte environ **20 000 gènes**, répartis
sur **23 paires de chromosomes** (22 paires d'autosomes + XX ou XY).

**Le dogme central** : ADN → (**[[transcription]]** dans le noyau) → ARN messager → (**[[traduction]]** par le
ribosome) → protéine.

L'ARN messager est lu par **[[codon|codons]]** de 3 bases. Il y a 64 codons pour 20 acides aminés : le code est
**redondant** (plusieurs codons pour un même acide aminé). **AUG** (méthionine) donne le départ ; **UAA, UAG,
UGA** sont des codons **stop**.
""")
    st.markdown("#### À toi : du gène à la protéine")
    st.caption("Entre le brin matrice d'ADN (celui qui est lu). L'ARNm est complémentaire, avec U à la place de T.")
    if "bh_seq" not in st.session_state:
        st.session_state["bh_seq"] = "TACGGTCTTAAACGAATT"
    c1, c2 = st.columns([3, 1], vertical_alignment="bottom")
    with c2:
        if st.button("Séquence au hasard", key="bh_rand"):
            body = "".join(random.choice("ACGT") for _ in range(15))
            st.session_state["bh_seq"] = "TAC" + body + "ATT"
    with c1:
        seq = st.text_input("Brin matrice d'ADN (3' → 5')", key="bh_seq").upper().replace(" ", "")
    if seq and set(seq) <= set("ACGT"):
        arn = "".join(COMPL[b] for b in seq)
        codons = [arn[i:i + 3] for i in range(0, len(arn) - len(arn) % 3, 3)]
        prot = []
        for c in codons:
            aa = CODONS[c]
            prot.append(aa)
            if aa == "STOP":
                break
        st.markdown(f"**ARN messager (5' → 3')** : `{' '.join(codons)}`")
        st.markdown(f"**Protéine** : {' – '.join(prot)}")
        if prot and prot[0] != "Met":
            st.caption("Dans une vraie cellule, la traduction commence au premier AUG (Met).")
    else:
        st.warning("Uniquement les lettres A, C, G, T.")
    ui.md(r"""
**Les mutations** : un changement d'une base peut ne rien changer (code redondant : mutation **silencieuse**),
changer un acide aminé (**faux-sens**, comme dans la drépanocytose) ou créer un stop précoce (**non-sens**).
L'insertion ou la délétion d'une base **décale** toute la lecture : c'est souvent grave. La myopathie de
Duchenne est due à des mutations du gène de la **dystrophine**, une protéine qui ancre l'appareil contractile à
la membrane du muscle.
""")


def ch_division():
    ui.md(r"""
**Le cycle cellulaire** : interphase (G1 : croissance ; S : **réplication** de l'ADN ; G2 : préparation) puis
division (M).

**La [[mitose]]** donne deux cellules **identiques** à 46 chromosomes. Elle sert à la croissance et à la
réparation des tissus. Ses phases :
""")
    phases = [
        ("Prophase", "Les chromosomes (déjà dupliqués, en deux chromatides) se condensent ; le fuseau se forme."),
        ("Métaphase", "Les chromosomes s'alignent au milieu de la cellule (plaque équatoriale)."),
        ("Anaphase", "Les chromatides sœurs se séparent et migrent vers les pôles opposés."),
        ("Télophase", "Deux noyaux se reforment ; la cytokinèse coupe la cellule en deux."),
    ]
    step = st.select_slider("Phase de la mitose", [p for p, _ in phases], key="bh_mitose")
    st.info(dict(phases)[step])
    ui.memo("**PMAT** : Prophase, Métaphase (au **M**ilieu), Anaphase (**A**part, ils s'éloignent), Télophase "
            "(deux noyaux, **T**erminé).")
    ui.md(r"""
**La [[méiose]]** produit les [[gamète|gamètes]] : deux divisions successives, quatre cellules **haploïdes**
(23 chromosomes), toutes différentes grâce au **brassage** (échange de segments entre chromosomes homologues,
le *crossing-over*, et répartition au hasard des chromosomes).

**Gamétogenèse** : chez l'homme, la spermatogenèse est continue dès la puberté, quatre spermatozoïdes par cellule
de départ. Chez la femme, l'ovogenèse commence avant la naissance, se bloque, et chaque cycle libère un ovocyte
(une seule cellule utile, les autres produits deviennent des globules polaires).

**Fécondation** : spermatozoïde (23) + ovocyte (23) = zygote (46), dans la trompe utérine.
""")


def ch_embryo():
    ui.md(r"""
**Les premières semaines**
- Semaine 1 : divisions du zygote (morula), puis blastocyste qui s'**implante** dans l'utérus.
- Semaine 2 : disque embryonnaire à deux feuillets.
- Semaine 3 : **gastrulation**, formation des trois [[feuillets embryonnaires]], puis début de formation du tube
  neural.
- Semaines 4 à 8 : **organogenèse**, tous les organes s'ébauchent. C'est la période la plus sensible aux agents
  toxiques (alcool, certains médicaments, infections).

| Feuillet | Ce qu'il donne |
|---|---|
| **Ectoderme** (externe) | épiderme, système nerveux |
| **Mésoderme** (milieu) | muscles, os, cartilage, tissus conjonctifs, cœur, vaisseaux, sang, reins |
| **Endoderme** (interne) | revêtement du tube digestif, foie, pancréas, poumons |

Le mésoderme se découpe en **somites** de part et d'autre de la future colonne : ils donnent les vertèbres, les
muscles du tronc et le derme. C'est pour ça que muscles et peau sont organisés par segments (myotomes,
dermatomes) !
""")
    ui.memo("**Ecto = extérieur** (peau, et le système nerveux qui « vient de la peau » en s'enroulant en tube), "
            "**Méso = milieu** (tout ce qui bouge et soutient), **Endo = dedans** (tubes digestif et respiratoire).")
    ui.clinic("Le **spina bifida** est un défaut de fermeture du tube neural (semaine 4). L'acide folique pris "
              "avant et au début de la grossesse en réduit fortement le risque. Les enfants atteints sont souvent "
              "suivis en kiné (paralysies des membres inférieurs).")


def ch_tissus():
    ui.md(r"""
Quatre grands tissus :

**1. [[épithélium|Épithéliums]]** : cellules jointives, posées sur une membrane basale, **sans vaisseaux**.
Revêtement (peau : épithélium pavimenteux stratifié kératinisé ; intestin : prismatique simple) ou glandes.

**2. [[tissu conjonctif|Tissus conjonctifs]]** : des cellules dispersées dans beaucoup de **matrice
extracellulaire**. C'est la matrice qui donne les propriétés mécaniques.

| Tissu | Cellule | Matrice | Propriété | Vascularisation |
|---|---|---|---|---|
| Tendon, ligament (conjonctif dense régulier) | [[fibroblaste\|fibroblastes]] (ténocytes) | collagène I aligné | résistance à la traction | faible |
| Cartilage hyalin (articulaire) | [[chondrocyte\|chondrocytes]] | collagène II + protéoglycanes (beaucoup d'eau) | résistance à la compression, glissement | **aucune** |
| Fibrocartilage (ménisque, disque) | chondrocytes | collagène I et II | traction + compression | faible |
| Os | [[ostéoblaste\|ostéoblastes]], ostéocytes, ostéoclastes | collagène I minéralisé (hydroxyapatite) | rigidité | **riche** |
| Tissu adipeux | adipocytes | peu | réserve, isolation | riche |
| Sang | globules rouges, blancs, plaquettes | plasma (liquide) | transport | (c'est lui) |

**3. Tissu musculaire** : squelettique (strié, volontaire, fibres multinucléées), cardiaque (strié, cellules
reliées par des disques intercalaires), lisse.

**4. Tissu nerveux** : [[neurone|neurones]] et [[cellule gliale|cellules gliales]].
""")
    ui.clinic("La **vascularisation** prédit la **cicatrisation**. L'os, bien vascularisé, se consolide en 6 à 12 "
              "semaines. Le tendon et le ligament, peu vascularisés, mettent des mois. Le cartilage articulaire, "
              "sans vaisseaux, cicatrise très mal : une lésion cartilagineuse est souvent définitive. Et le ménisque "
              "ne cicatrise que dans sa zone périphérique (« zone rouge »).")
    ui.tip("Un tissu s'adapte à la contrainte qu'on lui impose (loi de Wolff pour l'os) : l'exercice renforce os et "
           "tendons, l'immobilisation les affaiblit. C'est la base de la **mécanothérapie** en kiné.")


CHAPTERS = [
    ("La cellule", ch_cellule),
    ("Génétique moléculaire", ch_genetique),
    ("Division cellulaire et gamètes", ch_division),
    ("Embryologie", ch_embryo),
    ("Les tissus", ch_tissus),
]

ORGANITES = {"mitochondrie": "production d'ATP", "ribosome": "synthèse des protéines",
             "appareil de Golgi": "modification et tri des protéines", "lysosome": "digestion des déchets",
             "noyau": "stockage de l'ADN et transcription", "réticulum sarcoplasmique": "stockage du calcium dans le muscle"}
FEUILLETS = {"épiderme": "ectoderme", "moelle spinale": "ectoderme", "muscle squelettique": "mésoderme",
             "os": "mésoderme", "cœur": "mésoderme", "revêtement de l'intestin": "endoderme", "poumons (épithélium)": "endoderme"}


def _q_arn(rng):
    dna = "".join(rng.choice("ACGT") for _ in range(6))
    arn = "".join(COMPL[b] for b in dna)
    bad = ["".join({"A": "T", "T": "A", "C": "G", "G": "C"}[b] for b in dna), dna, arn[::-1]]
    return (f"Le brin matrice d'ADN est **{dna}**. Quel est l'ARN messager transcrit ?", arn, bad,
            "Complémentarité A→U, T→A, C→G, G→C (U remplace T dans l'ARN).")


def _q_codon(rng):
    c = rng.choice([k for k, v in CODONS.items() if v != "STOP"])
    aa = CODONS[c]
    others = sorted({v for v in CODONS.values() if v not in (aa, "STOP")})
    return (f"Le codon **{c}** code quel acide aminé ? (table du code génétique)", aa, rng.sample(others, 3), "")


def _q_chromo(rng):
    n = rng.choice([1, 2, 3])
    cas = {1: ("une cellule de peau après une mitose", 46), 2: ("un spermatozoïde", 23), 3: ("un zygote", 46)}[n]
    return dict(prompt=f"Combien de chromosomes possède {cas[0]} chez l'humain ?", answer=cas[1], tol=0.0)


QUESTIONS = [
    table_qcm(1, ORGANITES, "Quelle est la fonction principale : **{k}** ?", "Quel organite assure : **{v}** ?"),
    qcm(1, "La mitose produit…", "deux cellules identiques à 46 chromosomes",
        ["quatre cellules à 23 chromosomes", "deux cellules à 23 chromosomes", "une seule cellule"]),
    qcm(1, "Quel est le codon de départ de la traduction ?", "AUG", ["UAA", "UGA", "GGG"]),
    vf(1, "Le cartilage articulaire est richement vascularisé.", False, "Il n'a aucun vaisseau : il cicatrise très mal."),
    qcm(1, "Quel type de collagène domine dans le tendon ?", "Type I", ["Type II", "Type IV", "Il n'y a pas de collagène"]),
    num(1, _q_chromo),
    table_qcm(2, FEUILLETS, "De quel feuillet embryonnaire dérive : **{k}** ?"),
    gen_qcm(2, _q_arn),
    gen_qcm(2, _q_codon),
    qcm(2, "Pendant quelle phase de la mitose les chromosomes s'alignent-ils au centre ?", "Métaphase",
        ["Prophase", "Anaphase", "Télophase"]),
    multi(2, "Quelles caractéristiques décrivent le muscle cardiaque ?", ["Strié", "Involontaire", "Disques intercalaires"],
          ["Multinucléé comme le muscle squelettique", "Commande volontaire"]),
    qcm(2, "Pourquoi les gamètes sont-ils tous génétiquement différents ?",
        "Grâce au crossing-over et à la répartition au hasard des chromosomes pendant la méiose",
        ["Grâce aux mutations à chaque division", "Parce que la mitose les mélange", "Ils sont identiques"]),
    qcm(3, "Une mutation remplace un codon d'acide aminé par un codon STOP. Conséquence ?",
        "Une protéine tronquée, souvent non fonctionnelle (mutation non-sens)",
        ["Aucune conséquence", "Une protéine plus longue", "Un simple changement d'acide aminé"]),
    qcm(3, "Pourquoi une lésion du ménisque en périphérie cicatrise-t-elle mieux qu'au bord interne ?",
        "La périphérie est vascularisée, pas le bord interne", ["Le bord interne a plus de collagène",
        "La périphérie est faite de cartilage hyalin", "Le bord interne est soumis à moins de contraintes"]),
    qcm(3, "Muscles du tronc et derme sont organisés en segments (myotomes, dermatomes). Pourquoi ?",
        "Parce qu'ils dérivent des somites, blocs segmentaires du mésoderme",
        ["Parce qu'ils dérivent de l'endoderme", "À cause de la méiose", "Par hasard"]),
    qcm(3, "Pourquoi l'os consolide-t-il plus vite qu'un ligament ?", "Il est beaucoup mieux vascularisé",
        ["Il contient plus de collagène II", "Il n'a pas de cellules", "Il ne subit pas de contraintes"]),
]

CARDS = [
    ("Mitochondrie", "Production d'ATP ; ADN propre transmis par la mère"),
    ("Dogme central", "ADN → transcription → ARNm → traduction → protéine"),
    ("Codon start", "AUG (méthionine)"),
    ("Codons stop", "UAA, UAG, UGA"),
    ("Mitose", "2 cellules identiques diploïdes (46)"),
    ("Méiose", "4 cellules différentes haploïdes (23)"),
    ("Phases de la mitose", "Prophase, Métaphase, Anaphase, Télophase"),
    ("Ectoderme", "Épiderme et système nerveux"),
    ("Mésoderme", "Muscles, os, cartilage, cœur, sang, reins"),
    ("Endoderme", "Revêtement digestif et respiratoire, foie, pancréas"),
    ("Tendon", "Collagène I aligné, peu vascularisé"),
    ("Cartilage hyalin", "Collagène II + protéoglycanes, non vascularisé"),
    ("Loi de Wolff", "L'os s'adapte aux contraintes qu'on lui impose"),
    ("Ostéoclaste", "Cellule qui résorbe l'os"),
]

VIDEOS = [
    ("Transcription et traduction animées", "transcription traduction ARN messager animation"),
    ("La mitose étape par étape", "mitose étapes animation"),
    ("Mitose et méiose : différences", "différence mitose méiose explication"),
    ("Les tissus conjonctifs en histologie", "histologie tissu conjonctif cartilage os tendon"),
]

LINKS = [("Khan Academy (FR) : biologie", "https://fr.khanacademy.org/science/biology")]
