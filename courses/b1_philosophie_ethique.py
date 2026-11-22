"""LFSM1106 Philosophie et éthique en sciences de la motricité."""

import streamlit as st

from app import ui
from app.course import Course
from app.quiz import gen_qcm, multi, qcm, table_qcm, vf

COURSE = Course(
    code="LFSM1106", title="Philosophie et éthique en sciences de la motricité", short="Philosophie et éthique",
    bloc=1, quad=1, credits=3, hours="30 h", icon=":material/balance:",
    intro="Qu'est-ce qu'un corps « normal » ? Être en bonne santé, c'est quoi ? Peut-on forcer un patient à "
          "faire ses exercices ? Ce cours montre que derrière chaque geste de soin, il y a une idée du corps "
          "et des valeurs, et apprend à argumenter face à un dilemme.",
    acquis=[
        "Situer la place des valeurs dans la conception du corps et de la santé.",
        "Connaître les conceptions du rapport âme-corps qui influencent encore la pratique.",
        "Différencier éthique et déontologie.",
        "Construire une argumentation éthique et défendre un point de vue face à un dilemme.",
    ],
)

TERMS = {
    "dualisme": ("Dualisme", "Conception (Descartes) où l'esprit et le corps sont deux substances distinctes : "
                 "la pensée d'un côté, la matière étendue de l'autre.", "Dualisme (philosophie de l'esprit)"),
    "monisme": ("Monisme", "Conception où il n'y a qu'une seule réalité : l'esprit et le corps sont deux aspects "
                "d'une même chose (Spinoza) ou l'esprit est produit par le corps (matérialisme).", "Monisme"),
    "corps propre": ("Corps propre", "Chez Merleau-Ponty : le corps tel que je le vis de l'intérieur, par lequel "
                     "je perçois et j'agis, et pas seulement un objet que l'on observe.", "Maurice Merleau-Ponty"),
    "éthique": ("Éthique", "Réflexion critique sur les valeurs et sur ce qu'il est bon de faire dans une "
                "situation donnée, surtout quand les règles ne suffisent pas.", "Éthique"),
    "morale": ("Morale", "Ensemble de règles et de valeurs partagées par un groupe ou une culture, qui disent "
               "ce qui est bien ou mal.", "Morale"),
    "déontologie": ("Déontologie", "Ensemble des devoirs d'une profession, écrits dans un code (code de "
                    "déontologie des kinésithérapeutes).", "Déontologie"),
    "conséquentialisme": ("Conséquentialisme", "Théorie éthique qui juge une action à ses conséquences : la "
                          "bonne action produit le plus de bien (utilitarisme de Bentham et Mill).",
                          "Conséquentialisme"),
    "déontologisme": ("Déontologisme", "Théorie éthique qui juge une action selon qu'elle respecte ou non un "
                      "devoir, indépendamment de ses conséquences (Kant).", "Déontologisme"),
    "éthique des vertus": ("Éthique des vertus", "Théorie éthique (Aristote) centrée sur le caractère : agir comme "
                           "le ferait une personne vertueuse (prudente, juste, courageuse).", "Éthique de la vertu"),
    "autonomie": ("Autonomie", "Principe éthique : respecter la capacité de la personne à décider pour elle-même "
                  "(consentement libre et éclairé).", None),
    "bienfaisance": ("Bienfaisance", "Principe éthique : agir pour le bien du patient.", None),
    "non-malfaisance": ("Non-malfaisance", "Principe éthique : ne pas nuire (primum non nocere).", None),
    "justice": ("Justice", "Principe éthique : répartir équitablement les soins et les ressources.", None),
    "paternalisme": ("Paternalisme", "Attitude où le soignant décide « pour le bien » du patient à sa place, "
                     "sans respecter son autonomie.", "Paternalisme"),
    "normal et pathologique": ("Le normal et le pathologique", "Livre de Georges Canguilhem (1943) : la maladie "
                               "n'est pas un simple écart à une moyenne, mais une nouvelle norme de vie, plus "
                               "étroite ; la santé est la capacité à créer de nouvelles normes.",
                               "Le Normal et le Pathologique"),
}

THEORIES = {
    "Conséquentialisme (utilitarisme)": "Juger l'action à ses conséquences : le plus grand bien pour le plus grand nombre.",
    "Déontologisme (Kant)": "Respecter le devoir et la dignité, quelles que soient les conséquences ; ne jamais traiter "
                            "une personne seulement comme un moyen.",
    "Éthique des vertus (Aristote)": "Se demander ce que ferait un soignant prudent, juste, honnête et bienveillant.",
    "Principisme (Beauchamp et Childress)": "Peser autonomie, bienfaisance, non-malfaisance et justice dans la situation.",
}


def ch_philo():
    ui.md(r"""
La **philosophie** pose les questions que les sciences ne tranchent pas seules : qu'est-ce qu'être vivant, en
bonne santé, libre ? Qu'est-ce qu'un bon soin ? Elle examine aussi les **présupposés** des sciences.

La médecine moderne est née d'une façon de voir le corps comme une **machine** qu'on peut démonter. Cette
vision a permis des progrès immenses (anatomie, chirurgie), mais elle risque d'oublier que le patient **vit** son
corps, avec son histoire, ses peurs et ses projets. Toute la tension entre modèle biomédical et modèle
[[biopsychosocial]] vient de là.
""")
    ui.tip("Philosopher n'est pas donner son avis : c'est **argumenter**, définir ses termes et examiner les "
           "objections. « Je trouve que » ne suffit pas, il faut « parce que ».")


def ch_corps():
    ui.md(r"""
| Penseur | Idée du corps | Ce qu'il en reste en santé |
|---|---|---|
| **Platon** (Ve-IVe s. av. J.-C.) | Le corps est le « tombeau » de l'âme, qui est supérieure | la méfiance envers le corps et les plaisirs |
| **Aristote** | L'âme est la « forme » du corps vivant, inséparable de lui | l'unité de l'être vivant |
| **Descartes** (XVIIe) | [[dualisme\|Dualisme]] : l'esprit pense, le corps est une machine | le corps-machine de la médecine moderne |
| **Spinoza** | [[monisme\|Monisme]] : corps et esprit sont deux aspects d'une même réalité | les émotions et le corps vont ensemble |
| **Merleau-Ponty** (XXe) | Le [[corps propre]] : je ne *possède* pas un corps, je *suis* mon corps | le corps vécu, la perception, le geste |
""")
    ui.md(r"""
**Le mouvement et l'action** : pour Merleau-Ponty, le geste habile n'est pas une suite d'ordres envoyés par
l'esprit à des muscles ; le corps « sait » faire avant que je le pense (le schéma corporel). C'est très proche de
ce que la neurophysiologie appelle aujourd'hui les **automatismes moteurs**.

**Plaisir et douleur** : depuis Épicure (le plaisir comme absence de douleur), la douleur est pensée comme un
signal mais aussi comme une **expérience vécue** qui envahit tout. La définition actuelle de la douleur (IASP)
insiste sur ce caractère d'**expérience** sensorielle *et* émotionnelle.
""")
    ui.clinic("Un patient qui dit « mon genou ne m'obéit plus » parle de son corps comme d'un objet étranger. "
              "La rééducation, c'est aussi l'aider à **se réapproprier** ce corps : pas seulement gagner des degrés "
              "d'amplitude.")


def ch_sante():
    ui.md(r"""
**Définition de l'OMS (1946)** : « La santé est un état de complet bien-être physique, mental et social, et ne
consiste pas seulement en une absence de maladie ou d'infirmité. »

Elle a été une révolution (la santé n'est pas que biologique), mais on la critique : un état « complet » est
inatteignable, et la définition fait de presque tout le monde un malade.

**Normal ou pathologique ?**
- Pour une vision **statistique**, le normal est la **moyenne** : est anormal ce qui s'en écarte trop. Mais le
  champion olympique est très loin de la moyenne, et il n'est pas malade.
- Pour **Georges Canguilhem** ([[normal et pathologique|*Le normal et le pathologique*]]), le vivant crée ses
  propres **normes**. Être en santé, c'est pouvoir **s'adapter** et créer de nouvelles normes face aux
  changements. La maladie, c'est une norme de vie plus **étroite**, moins tolérante aux écarts.
- La définition **fonctionnelle** : la maladie est une fonction biologique qui ne marche plus comme elle devrait.

**Handicap** : avec la [[cif|CIF]], le handicap n'est plus une propriété de la personne, mais le résultat de
l'interaction entre ses limitations et son **environnement**. Une personne en fauteuil n'est pas « handicapée »
dans un bâtiment accessible.
""")
    ui.memo("Canguilhem : **santé = pouvoir de changer de normes**. Un genou opéré qui ne supporte que la marche à plat "
            "vit avec une norme « plus étroite » qu'un genou qui encaisse le foot.")


def ch_ethique():
    ui.md(r"""
Quatre mots qu'on confond souvent :

| | Ce que c'est | Exemple |
|---|---|---|
| [[morale\|Morale]] | règles et valeurs partagées par un groupe | « on ne ment pas » |
| [[éthique\|Éthique]] | réflexion critique sur ce qu'il faut faire, surtout quand les règles entrent en conflit | « dois-je dire toute la vérité à ce patient très anxieux ? » |
| [[déontologie\|Déontologie]] | devoirs écrits d'une profession | le secret professionnel du kiné |
| Droit | règles imposées par l'État, avec sanctions | la loi belge sur les droits du patient (2002) |
""")
    st.markdown("#### Les grandes théories éthiques")
    ui.table([[k, v] for k, v in THEORIES.items()], headers=["Théorie", "Question qu'elle pose"])
    ui.md(r"""
**Les quatre principes de Beauchamp et Childress** (le cadre le plus utilisé en santé) :
1. **[[autonomie|Autonomie]]** : respecter les choix d'un patient informé ;
2. **[[bienfaisance|Bienfaisance]]** : agir pour son bien ;
3. **[[non-malfaisance|Non-malfaisance]]** : ne pas nuire ;
4. **[[justice|Justice]]** : traiter équitablement.

Un dilemme éthique apparaît quand ces principes **se contredisent**. L'excès de bienfaisance sans autonomie
donne le [[paternalisme]].
""")
    ui.memo("**ABNJ** : **A**utonomie, **B**ienfaisance, **N**on-malfaisance, **J**ustice. "
            "« **A**vant **B**ien **N**ous **J**uger ».")


def ch_dilemmes():
    ui.md(r"""
**Construire une argumentation éthique**
1. **Décrire** les faits (qui, quoi, quel contexte) sans juger.
2. **Identifier** les valeurs et principes en tension.
3. **Lister** les options possibles (souvent plus de deux !).
4. **Peser** chaque option avec plusieurs théories : conséquences, devoirs, ce que ferait un bon soignant.
5. **Décider** et justifier, en reconnaissant ce qu'on sacrifie.
""")
    st.markdown("#### À toi : un dilemme")
    st.markdown(
        "> Une patiente de 82 ans, lucide, refuse de marcher avec son déambulateur dans le couloir de la maison de "
        "repos : elle préfère rester au fauteuil. Sa fille insiste pour que tu la « forces », sinon elle va perdre la "
        "marche."
    )
    option = st.radio("Que fais-tu ?", [
        "Je la force : c'est pour son bien.",
        "Je respecte son refus sans rien faire d'autre.",
        "Je cherche à comprendre son refus et je négocie un objectif qui a du sens pour elle.",
    ], index=None, key="pe_dilemme")
    if option:
        analyses = {
            "Je la force : c'est pour son bien.":
                "Bienfaisance forte, mais **autonomie** violée : c'est du paternalisme. Une patiente lucide a le droit "
                "de refuser un soin (loi belge sur les droits du patient). Et à long terme, la contrainte casse la "
                "confiance.",
            "Je respecte son refus sans rien faire d'autre.":
                "Autonomie respectée, mais la **bienfaisance** est oubliée : un refus peut cacher une peur (de chuter, "
                "d'avoir mal, d'être vue avec un déambulateur). Respecter, ce n'est pas abandonner.",
            "Je cherche à comprendre son refus et je négocie un objectif qui a du sens pour elle.":
                "C'est l'option la plus défendable : elle respecte l'**autonomie** tout en cherchant le **bien** de la "
                "patiente. Peut-être qu'elle acceptera de marcher pour aller au jardin ou voir son amie à l'autre "
                "étage. C'est aussi ce que ferait un soignant **vertueux** (prudent et bienveillant).",
        }
        st.info(analyses[option])
    ui.md(r"""
**Quelques controverses autour du corps** : le **dopage** (égalité des chances, santé de l'athlète, liberté), le
**corps augmenté** (prothèses plus performantes qu'un membre, stimulants cognitifs), l'**inclusion** dans le sport
(catégories de genre, handisport), l'usage des **données de santé** des objets connectés.
""")


CHAPTERS = [
    ("Philosophie et sciences", ch_philo),
    ("Le corps dans l'histoire des idées", ch_corps),
    ("Santé, normal et pathologique", ch_sante),
    ("Éthique, morale, déontologie", ch_ethique),
    ("Argumenter face à un dilemme", ch_dilemmes),
]

PENSEURS = {"Descartes": "Dualisme : l'esprit pense, le corps est une machine",
            "Merleau-Ponty": "Le corps propre : je suis mon corps",
            "Spinoza": "Monisme : corps et esprit, deux aspects d'une même réalité",
            "Platon": "Le corps est le tombeau de l'âme",
            "Canguilhem": "La santé est le pouvoir d'instituer de nouvelles normes"}

SITUATIONS = [
    ("Un kiné refuse de donner des infos sur un patient à son employeur.", "Déontologie (secret professionnel)"),
    ("Un kiné prolonge les séances d'un patient alors qu'elles ne servent plus, pour facturer.", "Non-malfaisance et justice"),
    ("Un patient bien informé refuse une technique, et le kiné en propose une autre.", "Autonomie"),
    ("Un kiné décide seul de l'objectif sans demander l'avis du patient, « pour son bien ».", "Paternalisme"),
]


def _q_situation(rng):
    s, good = rng.choice(SITUATIONS)
    return (f"Quel principe ou notion est principalement en jeu ? {s}", good, [g for _, g in SITUATIONS], "")


QUESTIONS = [
    table_qcm(1, PENSEURS, "Quelle idée est associée à **{k}** ?", "Quel penseur défend l'idée : « {v} » ?"),
    qcm(1, "Quels sont les quatre principes de Beauchamp et Childress ?",
        "Autonomie, bienfaisance, non-malfaisance, justice",
        ["Liberté, égalité, fraternité, solidarité", "Autonomie, vérité, secret, dignité",
         "Bienfaisance, prudence, courage, tempérance"]),
    vf(1, "La déontologie désigne les devoirs écrits d'une profession.", True),
    qcm(1, "Quelle théorie juge une action uniquement à ses conséquences ?", "Le conséquentialisme",
        ["Le déontologisme", "L'éthique des vertus", "Le dualisme"]),
    vf(1, "Selon la définition de l'OMS (1946), la santé est l'absence de maladie.", False,
       "C'est « un état de complet bien-être physique, mental et social », pas seulement l'absence de maladie."),
    gen_qcm(2, _q_situation),
    qcm(2, "Quelle est la principale critique adressée à la définition de la santé de l'OMS ?",
        "Un bien-être « complet » est inatteignable : presque tout le monde serait malade",
        ["Elle ne parle que du corps", "Elle oublie la dimension sociale", "Elle est trop récente"]),
    qcm(2, "Pour Kant, il ne faut jamais traiter une personne…", "seulement comme un moyen, mais aussi comme une fin",
        ["avec bienveillance", "selon ses conséquences", "comme un être autonome"]),
    qcm(2, "Le modèle du corps-machine de la médecine moderne vient surtout de…", "Descartes",
        ["Merleau-Ponty", "Aristote", "Canguilhem"]),
    multi(2, "Dans la CIF, quels éléments participent au handicap ?",
          ["Les limitations de la personne", "L'environnement (accessibilité, aides)", "Les facteurs personnels"],
          ["Uniquement le diagnostic médical"], "Le handicap naît de l'interaction personne-environnement."),
    qcm(3, "Un sportif de haut niveau a un cœur très éloigné de la moyenne (bradycardie à 38/min). Que montre cet exemple ?",
        "Que le normal ne peut pas se réduire à la moyenne statistique",
        ["Qu'il est forcément malade", "Que la statistique suffit à définir la maladie", "Que la norme est fixée par l'OMS"],
        "C'est l'argument de Canguilhem contre la définition statistique."),
    qcm(3, "Une patiente lucide refuse un exercice. Lui imposer « pour son bien » privilégie…",
        "la bienfaisance au détriment de l'autonomie (paternalisme)",
        ["la justice au détriment de la bienfaisance", "l'autonomie au détriment de la non-malfaisance",
         "la non-malfaisance au détriment de la justice"]),
    qcm(3, "Quelle est la première étape d'une délibération éthique rigoureuse ?",
        "Décrire les faits de la situation sans juger", ["Choisir l'option la plus rapide",
        "Appliquer le code de déontologie mot à mot", "Demander l'avis de la famille"]),
    qcm(3, "Quelle différence fait-on entre éthique et déontologie ?",
        "La déontologie fixe des devoirs écrits ; l'éthique réfléchit quand les règles ne suffisent pas ou se contredisent",
        ["Ce sont des synonymes", "L'éthique est imposée par l'État", "La déontologie concerne la vie privée"]),
]

CARDS = [
    ("Dualisme cartésien", "Esprit (pensée) et corps (machine) sont deux substances distinctes"),
    ("Corps propre (Merleau-Ponty)", "Le corps vécu, par lequel je perçois et j'agis"),
    ("Canguilhem", "La santé est la capacité de créer de nouvelles normes"),
    ("Définition OMS de la santé (1946)", "État de complet bien-être physique, mental et social"),
    ("4 principes de Beauchamp et Childress", "Autonomie, bienfaisance, non-malfaisance, justice"),
    ("Conséquentialisme", "Juger aux conséquences (utilitarisme : Bentham, Mill)"),
    ("Déontologisme", "Juger selon le devoir (Kant)"),
    ("Éthique des vertus", "Agir comme une personne vertueuse (Aristote)"),
    ("Paternalisme", "Décider à la place du patient « pour son bien »"),
    ("Morale vs éthique", "Règles partagées vs réflexion critique sur ce qu'il faut faire"),
    ("Déontologie", "Devoirs écrits d'une profession"),
]

VIDEOS = [
    ("Descartes et le dualisme corps-esprit", "Descartes dualisme corps esprit explication"),
    ("Canguilhem : le normal et le pathologique", "Canguilhem le normal et le pathologique"),
    ("Les principes de l'éthique médicale", "principes éthique médicale Beauchamp Childress autonomie bienfaisance"),
    ("Les théories éthiques : Kant, utilitarisme, vertus", "théories éthiques Kant utilitarisme éthique des vertus"),
]

LINKS = [("Loi belge relative aux droits du patient (SPF Santé publique)",
          "https://www.health.belgium.be/fr/sante/organisation-des-soins-de-sante/qualite-des-soins/droits-du-patient")]
