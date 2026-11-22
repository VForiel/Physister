"""LKNR1208 Gériatrie."""

import streamlit as st

from app import ui
from app.course import Course
from app.quiz import gen_qcm, multi, num, qcm, vf

COURSE = Course(
    code="LKNR1208", title="Gériatrie", short="Gériatrie",
    bloc=2, quad=1, credits=2, hours="22,5 h", icon=":material/elderly:",
    intro="La population vieillit et une grande partie des patients d'un kiné ont plus de 65 ans. Ce cours distingue "
          "le vieillissement normal du pathologique, présente la fragilité, les chutes, les troubles cognitifs, "
          "l'évaluation gériatrique standardisée et le travail en équipe.",
    acquis=[
        "Identifier les syndromes liés au vieillissement physiologique et pathologique.",
        "Repérer les stéréotypes sur les personnes âgées.",
        "Utiliser les outils d'évaluation gériatrique standardisée.",
        "Élaborer un projet thérapeutique dans une démarche interprofessionnelle.",
        "Connaître les recommandations de l'OMS (exercice, aides techniques, séances de groupe).",
    ],
)

TERMS = {
    "fragilité": ("Fragilité", "État de vulnérabilité accrue dû à la baisse des réserves de plusieurs systèmes : un "
                  "petit stress (grippe, chute) entraîne une perte d'autonomie disproportionnée.", "Fragilité (gériatrie)"),
    "sarcopénie": ("Sarcopénie", "Perte de masse et de force musculaires liée à l'âge, avec baisse de la "
                   "performance physique.", "Sarcopénie"),
    "âgisme": ("Âgisme", "Stéréotypes, préjugés et discriminations envers les personnes en raison de leur âge.", "Âgisme"),
    "egs": ("Évaluation gériatrique standardisée", "Évaluation globale et interdisciplinaire de la personne âgée : "
            "médicale, fonctionnelle, cognitive, thymique, nutritionnelle, sociale.", "Évaluation gériatrique standardisée"),
    "adl": ("ADL / AVQ", "Activités de base de la vie quotidienne : se laver, s'habiller, aller aux toilettes, se "
            "déplacer, être continent, manger (échelle de Katz).", "Activités de la vie quotidienne"),
    "iadl": ("IADL / AIVQ", "Activités instrumentales : téléphoner, faire les courses, préparer les repas, gérer "
             "ses médicaments et son argent (échelle de Lawton).", None),
    "delirium": ("Delirium (syndrome confusionnel aigu)", "Trouble aigu et fluctuant de l'attention et de la conscience, "
                 "souvent déclenché par une infection, un médicament, une déshydratation. C'est une urgence.", "Delirium"),
    "démence": ("Trouble neurocognitif majeur (démence)", "Déclin cognitif progressif qui retentit sur l'autonomie "
                "(Alzheimer, vasculaire, à corps de Lewy…).", "Démence"),
    "polymédication": ("Polymédication", "Prise de nombreux médicaments (souvent 5 ou plus), qui augmente le risque "
                       "d'effets indésirables, de chutes et de confusion.", "Polymédication"),
    "tug": ("Timed Up and Go", "Test : se lever d'une chaise, marcher 3 m, faire demi-tour, revenir s'asseoir, "
            "chronométré.", "Timed up and go test"),
}

FRIED = [
    "Perte de poids involontaire (≥ 4,5 kg ou 5 % en un an)",
    "Épuisement ressenti (fatigue)",
    "Faible force de préhension (dynamomètre)",
    "Vitesse de marche lente",
    "Faible niveau d'activité physique",
]


def ch_vieillissement():
    ui.md(r"""
**Démographie** : en Belgique, environ une personne sur cinq a plus de 65 ans, et la part des plus de 85 ans
augmente vite. L'**espérance de vie** dépasse 80 ans, mais l'espérance de vie **en bonne santé** est nettement plus
courte : l'enjeu est d'ajouter de la vie aux années.

**Vieillissement normal des organes** (variable d'une personne à l'autre !)
- **Muscles** : perte de masse et surtout de force et de puissance ([[sarcopénie]]), plus marquée sans activité.
- **Os** : perte de densité (ostéoporose, surtout après la ménopause).
- **Cœur et vaisseaux** : artères plus rigides, FC maximale plus basse (≈ 220 − âge, en moyenne).
- **Poumons** : moins d'élasticité, capacité vitale qui diminue.
- **Système nerveux** : réflexes et temps de réaction plus lents, équilibre moins bon, sommeil plus fragmenté.
- **Sens** : presbytie, presbyacousie, sensibilité plantaire réduite.
- **Reins** : élimination des médicaments plus lente.

**Le vieillissement actif** (OMS) : optimiser la santé, la participation et la sécurité pour garder sa qualité de
vie. L'activité physique est l'intervention la plus efficace sur presque tous ces points.
""")
    ui.warn("Ne mets pas tout sur le compte de l'âge : une fatigue, une confusion ou une chute ont souvent une "
            "**cause traitable** (infection, médicament, anémie, déshydratation). « C'est l'âge » est un piège.")
    ui.md(r"""
**L'[[âgisme]]** : « les vieux sont fragiles, tous pareils, ne peuvent plus progresser ». Faux : une personne de
90 ans peut gagner beaucoup de force avec un entraînement adapté. Les soignants âgistes proposent moins de
rééducation, avec des objectifs trop bas. Et ils parlent à l'accompagnant plutôt qu'au patient.
""")


def ch_fragilite():
    ui.md(r"""
La **[[fragilité]]** est un état intermédiaire entre la robustesse et la dépendance. Elle est **réversible**, en
particulier par l'exercice et la nutrition : c'est donc le moment idéal pour intervenir.
""")
    st.markdown("#### À toi : le phénotype de fragilité de Fried")
    n = sum(st.checkbox(c, key=f"ger_fried_{i}") for i, c in enumerate(FRIED))
    if n >= 3:
        st.error(f"{n}/5 critères : **fragile**. Évaluation globale et programme d'exercices multicomposantes recommandés.")
    elif n >= 1:
        st.warning(f"{n}/5 critères : **pré-fragile**. Le moment idéal pour prévenir.")
    else:
        st.success("0/5 critère : **robuste**.")
    ui.md(r"""
**Les grands syndromes gériatriques** : chutes, [[delirium|confusion aiguë]], troubles cognitifs, incontinence,
dénutrition, [[polymédication]], dépression, perte d'autonomie. Ils ont souvent **plusieurs causes**
qui s'additionnent.

**Les troubles cognitifs** : il faut distinguer
- le [[delirium]] : **brutal**, **fluctuant**, avec trouble de l'**attention**, souvent réversible si on trouve la
  cause. C'est une urgence médicale.
- la [[démence|démence (trouble neurocognitif majeur)]] : **progressive**, sur des mois ou des années.
- la **dépression**, qui peut ressembler à une démence chez la personne âgée.

**La dénutrition** : fréquente (perte d'appétit, difficultés à mâcher, isolement), elle aggrave la sarcopénie.
Exercice **et** apport en protéines vont ensemble.
""")


def ch_chutes():
    ui.md(r"""
Environ **une personne sur trois** de plus de 65 ans chute au moins une fois par an (une sur deux après 80 ans).
Les chutes sont la première cause de décès par traumatisme chez les personnes âgées, et la **peur de tomber**
pousse à moins bouger, ce qui augmente encore le risque.

**Facteurs de risque** : antécédent de chute (le plus fort), faiblesse des membres inférieurs, troubles de
l'équilibre et de la marche, médicaments (somnifères, psychotropes, antihypertenseurs), troubles de la vue,
hypotension orthostatique, troubles cognitifs, environnement (tapis, éclairage, escaliers), chaussures.
""")
    st.markdown("#### À toi : le Timed Up and Go")
    c1, c2 = st.columns([1, 2])
    with c1:
        t = st.slider("Temps au TUG (s)", 5.0, 40.0, 11.0, 0.5, key="ger_tug")
        vit = st.slider("Vitesse de marche (m/s)", 0.2, 1.6, 1.0, 0.05, key="ger_vit")
    with c2:
        if t >= 13.5:
            st.error(f"TUG {t:.1f} s : risque de chute augmenté (seuil souvent cité : ≥ 13,5 s ; ≥ 12 s dans le programme STEADI).")
        elif t >= 12:
            st.warning(f"TUG {t:.1f} s : zone limite, à surveiller.")
        else:
            st.success(f"TUG {t:.1f} s : dans les normes.")
        if vit < 0.8:
            st.warning(f"Vitesse de marche {vit:.2f} m/s : moins de 0,8 m/s, signe de fragilité et de mauvais pronostic.")
        else:
            st.info(f"Vitesse de marche {vit:.2f} m/s : la vitesse de marche est un vrai « signe vital » chez la personne âgée.")
    ui.warn("Un test isolé ne prédit pas bien les chutes : on combine anamnèse (chutes passées), plusieurs tests "
            "(TUG, Berg, vitesse de marche, lever de chaise) et l'avis de l'équipe.")
    ui.clinic("Les programmes qui marchent le mieux pour prévenir les chutes combinent **équilibre** (exercices "
              "progressivement plus difficiles, au moins 3 heures par semaine en cumulé selon les études) et "
              "**renforcement** des membres inférieurs, par exemple les programmes Otago ou le tai-chi. Et on "
              "apprend au patient à **se relever du sol**.")


def ch_evaluation():
    ui.md(r"""
**L'[[egs|évaluation gériatrique standardisée]]** couvre tous les domaines, avec des outils validés :

| Domaine | Outils |
|---|---|
| Autonomie de base | [[adl\|ADL]] (Katz) |
| Autonomie instrumentale | [[iadl\|IADL]] (Lawton) |
| Mobilité, équilibre, chutes | [[tug\|TUG]], échelle de Berg, vitesse de marche, test de lever de chaise, SPPB |
| Cognition | MMSE, MoCA, test de l'horloge |
| Humeur | échelle de dépression gériatrique (GDS) |
| Nutrition | MNA (Mini Nutritional Assessment) |
| Fragilité | critères de Fried, échelle clinique de fragilité |
| Social | entourage, logement, aides |

**La démarche interprofessionnelle** : gériatre, infirmier, kiné, ergothérapeute, diététicien, logopède,
psychologue, assistant social. Le **projet thérapeutique** est construit avec le patient (et ses proches) autour
de **ses** priorités : rentrer chez soi, continuer à jardiner, aller voir ses petits-enfants.

**Questions éthiques fréquentes** : respecter les choix d'une personne qui prend des risques, contention,
annonce d'un diagnostic, fin de vie.
""")
    ui.md(r"""
**Les recommandations de l'OMS pour les 65 ans et plus**
- **150 à 300 min** d'activité modérée par semaine (ou 75 à 150 min soutenue) ;
- **renforcement musculaire** au moins **2 jours** par semaine ;
- activité **multicomposante** (équilibre + force) au moins **3 jours** par semaine pour prévenir les chutes ;
- adapter à ses capacités : « un peu, c'est mieux que rien ».

Les **séances de groupe** motivent et rompent l'isolement ; les **aides techniques** (canne, déambulateur) se
choisissent, se règlent et s'apprennent avec le kiné.
""")


CHAPTERS = [
    ("Le vieillissement", ch_vieillissement),
    ("Fragilité et syndromes gériatriques", ch_fragilite),
    ("Les chutes", ch_chutes),
    ("Évaluer et accompagner", ch_evaluation),
]

OUTILS = {"Échelle de Katz": "Autonomie de base (ADL)", "Échelle de Lawton": "Autonomie instrumentale (IADL)",
          "MMSE": "Cognition", "MNA": "Nutrition", "Échelle de Berg": "Équilibre", "GDS": "Humeur (dépression)"}


def _q_outil(rng):
    k = rng.choice(list(OUTILS))
    return (f"Que mesure l'outil **{k}** ?", OUTILS[k], list(OUTILS.values()), "")


def _q_fc(rng):
    age = rng.choice([65, 70, 75, 80, 85])
    return dict(prompt=f"Estime la fréquence cardiaque maximale théorique d'une personne de {age} ans avec la formule "
                       f"220 − âge.", answer=220 - age, unit="bpm", tol=0.0, why=f"220 − {age} = {220 - age} bpm.")


QUESTIONS = [
    qcm(1, "Combien de critères compte le phénotype de fragilité de Fried ?", "5", ["3", "4", "10"]),
    qcm(1, "Quelle proportion des plus de 65 ans chute au moins une fois par an ?", "Environ un tiers",
        ["Environ 5 %", "Environ 90 %", "Personne"]),
    vf(1, "La fragilité est un état irréversible.", False, "Elle est réversible, surtout par l'exercice et la nutrition."),
    gen_qcm(1, _q_outil),
    qcm(1, "Que signifie la sarcopénie ?", "Perte de masse et de force musculaires liée à l'âge",
        ["Perte de densité osseuse", "Perte de mémoire", "Perte d'appétit"]),
    num(1, _q_fc),
    multi(2, "Quels sont des critères de fragilité de Fried ?", ["Vitesse de marche lente", "Faible force de préhension",
          "Perte de poids involontaire"], ["Hypertension artérielle", "Âge supérieur à 80 ans"]),
    qcm(2, "Qu'est-ce qui distingue le delirium de la démence ?", "Son début brutal et fluctuant, avec trouble de l'attention",
        ["Sa lenteur d'installation", "Son caractère toujours définitif", "L'absence de cause"]),
    qcm(2, "Quel est le facteur de risque de chute le plus fort ?", "Un antécédent de chute", ["Être une femme",
        "Porter des lunettes", "Vivre en ville"]),
    qcm(2, "Selon l'OMS, combien de jours par semaine une personne âgée devrait-elle faire des exercices "
        "d'équilibre et de force ?", "Au moins 3 jours", ["1 jour", "Jamais, c'est dangereux", "7 jours obligatoirement"]),
    vf(2, "Une vitesse de marche inférieure à 0,8 m/s est un signe de fragilité.", True),
    qcm(3, "Une dame de 84 ans devient soudain confuse en 24 h, avec une attention fluctuante. Que faire ?",
        "Alerter le médecin : c'est probablement un delirium avec une cause à trouver (infection, médicament…)",
        ["Conclure à une maladie d'Alzheimer", "Attendre que ça passe", "Augmenter l'intensité des exercices"]),
    qcm(3, "Un patient âgé chute depuis l'ajout d'un somnifère. Quel est le rôle du kiné ?",
        "Signaler le lien possible au médecin, en plus du travail d'équilibre", ["Arrêter lui-même le médicament",
        "Ne rien dire, ce n'est pas son domaine", "Immobiliser le patient au lit"]),
    qcm(3, "Pourquoi apprendre à une personne âgée à se relever du sol ?",
        "Rester longtemps au sol après une chute entraîne de graves complications et entretient la peur de tomber",
        ["Pour renforcer les bras", "Pour éviter la sarcopénie", "Ce n'est pas utile"]),
    qcm(3, "Un soignant s'adresse à la fille plutôt qu'à son père de 88 ans, lucide. C'est un exemple de…",
        "âgisme", ["paternalisme bienveillant justifié", "bonne pratique", "secret professionnel"]),
]

CARDS = [
    ("Phénotype de Fried", "Perte de poids, épuisement, faible préhension, marche lente, faible activité ; ≥ 3 = fragile"),
    ("Sarcopénie", "Perte de masse et de force musculaires"),
    ("Delirium", "Brutal, fluctuant, trouble de l'attention : urgence"),
    ("Démence", "Déclin cognitif progressif avec perte d'autonomie"),
    ("TUG", "Lever, 3 m, demi-tour, retour ; ≥ 13,5 s = risque de chute"),
    ("Vitesse de marche", "< 0,8 m/s = fragilité"),
    ("Katz / Lawton", "ADL de base / IADL instrumentales"),
    ("MNA", "Évaluation nutritionnelle"),
    ("Chutes", "1/3 des > 65 ans par an ; facteur n°1 : chute antérieure"),
    ("OMS, ≥ 65 ans", "150-300 min modéré, force 2 j, équilibre + force 3 j par semaine"),
    ("Âgisme", "Stéréotypes et discrimination liés à l'âge"),
]

VIDEOS = [
    ("Le Timed Up and Go en pratique", "Timed Up and Go test démonstration"),
    ("La fragilité chez la personne âgée", "fragilité personne âgée Fried explication"),
    ("Programme Otago de prévention des chutes", "programme Otago exercices prévention chutes"),
    ("Apprendre à se relever du sol", "apprendre à se relever du sol personne âgée kiné"),
]

LINKS = [("OMS : lignes directrices sur l'activité physique (2020)", "https://www.who.int/fr/publications/i/item/9789240015128")]
