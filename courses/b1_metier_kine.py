"""LKNR1103 Introduction au métier de kinésithérapeute."""

import streamlit as st

from app import ui
from app.course import Course
from app.quiz import gen_qcm, multi, num, qcm, vf

COURSE = Course(
    code="LKNR1103", title="Introduction au métier de kinésithérapeute", short="Métier de kiné",
    bloc=1, quad=1, credits=4, hours="30 h", icon=":material/badge:",
    intro="Avant les techniques, il y a la relation : écouter, expliquer, obtenir le consentement, respecter le "
          "secret. Ce cours pose aussi les bons réflexes d'hygiène et les premiers gestes face aux petits "
          "traumatismes et aux brûlures.",
    acquis=[
        "Analyser son projet de formation de façon réflexive.",
        "Communiquer en favorisant l'empowerment du patient ; pratiquer l'écoute active.",
        "Tenir compte du vécu spécifique du patient (handicap, maladie chronique).",
        "Connaître les gestes d'urgence de base et les règles d'hygiène.",
        "Respecter le consentement éclairé, le cadre éthique, le secret professionnel et la juste distance.",
    ],
)

TERMS = {
    "écoute active": ("Écoute active", "Écouter en montrant qu'on comprend : silences, relances, reformulation, "
                      "questions ouvertes, sans juger ni interrompre (Carl Rogers).", "Écoute active"),
    "reformulation": ("Reformulation", "Redire avec ses mots ce que le patient a dit, pour vérifier qu'on a "
                      "compris et lui montrer qu'on l'écoute.", None),
    "empowerment": ("Empowerment", "Processus par lequel le patient gagne du pouvoir d'agir sur sa santé : il "
                    "comprend, décide et agit (on parle aussi d'autonomisation ou de patient acteur).",
                    "Empowerment"),
    "consentement éclairé": ("Consentement éclairé", "Accord libre donné par le patient après avoir reçu une "
                             "information claire sur le soin, ses bénéfices, ses risques et les alternatives. "
                             "Il peut être retiré à tout moment.", "Consentement éclairé"),
    "secret professionnel": ("Secret professionnel", "Obligation de ne pas révéler ce qu'on apprend sur un patient "
                             "dans le cadre de sa profession (article 458 du Code pénal belge).",
                             "Secret professionnel en Belgique"),
    "juste distance": ("Juste distance", "Posture du soignant ni trop distante (froide) ni trop proche "
                       "(fusionnelle), pour rester empathique et efficace.", None),
    "infection nosocomiale": ("Infection associée aux soins", "Infection contractée lors d'un soin (à l'hôpital "
                              "ou ailleurs), absente à l'admission.", "Infection nosocomiale"),
    "friction hydroalcoolique": ("Friction hydroalcoolique", "Désinfection des mains par une solution à base "
                                 "d'alcool, pendant 20 à 30 secondes. Méthode de référence sauf mains souillées.",
                                 "Solution hydroalcoolique"),
    "phlyctène": ("Phlyctène", "Cloque remplie de liquide, typique d'une brûlure du 2e degré.", "Phlyctène"),
    "peace & love": ("PEACE & LOVE", "Recommandations (Dubois et Esculier, 2020) pour les lésions des tissus mous : "
                     "Protéger, Élever, Éviter les anti-inflammatoires, Compresser, Éduquer ; puis Load (charger), "
                     "Optimisme, Vascularisation, Exercice.", None),
}

AREAS = {  # règle des 9 de Wallace (adulte)
    "Tête et cou": 9, "Membre supérieur droit": 9, "Membre supérieur gauche": 9,
    "Face antérieure du tronc": 18, "Face postérieure du tronc": 18,
    "Membre inférieur droit": 18, "Membre inférieur gauche": 18, "Périnée": 1,
}


def ch_sante():
    ui.md(r"""
Le kiné est un **modèle** : difficile de convaincre un patient de bouger quand on est soi-même sédentaire, et
sa propre santé (dos, sommeil, stress) conditionne la qualité des soins. Ce cours commence donc par toi.

**Les recommandations d'activité physique (OMS, adultes de 18 à 64 ans)**
- **150 à 300 minutes** par semaine d'activité d'intensité **modérée** (on peut parler mais pas chanter),
  ou **75 à 150 minutes** d'intensité **soutenue**, ou un mélange des deux ;
- du **renforcement musculaire** au moins **2 jours** par semaine ;
- **limiter** le temps assis et le couper régulièrement.
""")
    ui.tip("Apprendre le métier, c'est aussi apprendre à **réfléchir sur sa pratique** (métacognition) : après un "
           "stage ou un TP, note ce qui a marché, ce qui t'a mise mal à l'aise, et ce que tu changerais. "
           "C'est ce qu'on attend dans les portfolios réflexifs.")
    ui.clinic("Les kinés ont un risque élevé de **troubles musculo-squelettiques** (dos, pouces, poignets) : "
              "ergonomie de la table (hauteur réglable), utilisation du poids du corps plutôt que de la force des "
              "bras, pauses. Prends ces habitudes dès les TP.")


def ch_communication():
    ui.md(r"""
**L'[[écoute active]]** (Carl Rogers) repose sur :
- des **questions ouvertes** au début (« Racontez-moi ce qui vous amène »), plus fermées ensuite pour préciser ;
- des **silences** et des relances (« Hm hm », « Et alors ? ») ;
- la **[[reformulation]]** (« Si je comprends bien, c'est surtout le matin que votre dos est raide ? ») ;
- l'**empathie** : comprendre ce que vit l'autre, sans forcément le partager ni le juger ;
- l'attention au **non-verbal** (posture, regard, ton).
""")
    st.markdown("#### À toi : quelle réponse est la plus aidante ?")
    st.markdown("> Le patient : « Ça fait trois mois que j'ai mal, personne ne trouve ce que j'ai, j'en ai marre. »")
    rep = st.radio("Tu réponds…", [
        "« Ne vous inquiétez pas, ça va passer. »",
        "« Vous devriez faire plus de sport. »",
        "« Trois mois sans réponse, ça doit être épuisant. Qu'est-ce qui vous inquiète le plus ? »",
        "« Moi aussi j'ai eu mal au dos, c'est pénible. »",
    ], index=None, key="mk_comm")
    if rep:
        if rep.startswith("« Trois"):
            st.success("Oui : tu reformules l'émotion (empathie) et tu ouvres avec une question ouverte.")
        else:
            st.error("Cette réponse rassure trop vite, conseille sans écouter, ou ramène la conversation à toi. "
                     "La bonne : reformuler l'émotion, puis poser une question ouverte.")
    ui.md(r"""
**Le patient acteur** : on ne soigne pas *un* patient passif, on soigne *avec* lui. L'[[empowerment]] passe par
l'**éducation thérapeutique** (comprendre sa pathologie), des **objectifs décidés ensemble** et l'autonomie dans
les exercices.

**Les patients au vécu spécifique** (handicap, maladie chronique) sont souvent **experts** de leur situation :
on leur demande comment ils font, ce qui les aide. On parle à la personne, pas à l'accompagnant, et on ne
présume pas de ses limites.
""")


def ch_ethique():
    ui.md(r"""
**Le [[consentement éclairé]]** (loi belge du 22 août 2002 relative aux droits du patient) : avant un soin, le
patient doit recevoir une information **claire, compréhensible**, sur le but, les bénéfices, les risques et les
alternatives. Il est **libre** d'accepter ou de refuser, et peut **retirer** son consentement à tout moment.
Il est particulièrement important avant un **toucher** dans une zone intime ou sensible.

**Le [[secret professionnel]]** (article 458 du Code pénal) : tout ce que tu apprends sur un patient dans ton
travail est couvert, y compris en stage. Pas de nom ni de détail reconnaissable dans les conversations entre
amis, sur les réseaux sociaux, dans les travaux. Il existe des exceptions strictement prévues par la loi
(témoignage en justice, état de nécessité, danger grave pour un enfant…).

**La [[juste distance]]** : être chaleureux et empathique sans devenir l'ami ou le confident du patient. Pas de
relation privée avec un patient, pas de cadeaux importants, attention aux réseaux sociaux.
""")
    ui.warn("Même « juste raconter » un cas marrant à des amis peut violer le secret si la personne est "
            "reconnaissable (petite ville, club de sport). Dans le doute : on ne raconte pas.")


def ch_hygiene():
    ui.md(r"""
Les **[[infection nosocomiale|infections associées aux soins]]** se transmettent surtout **par les mains** des
soignants. L'hygiène des mains est donc le geste de prévention n°1.

**Les 5 moments de l'hygiène des mains (OMS)**
1. **Avant** de toucher un patient ;
2. **Avant** un geste aseptique (pansement, aspiration…) ;
3. **Après** un risque d'exposition à un liquide biologique ;
4. **Après** avoir touché un patient ;
5. **Après** avoir touché l'environnement du patient (lit, table, matériel).

**Comment** : la [[friction hydroalcoolique]] (20 à 30 secondes, jusqu'à séchage) est la méthode de référence.
Le **lavage à l'eau et au savon** est obligatoire si les mains sont visiblement **souillées** (et pour certains
germes comme *Clostridioides difficile*, que l'alcool ne tue pas).

**Prérequis** : ongles courts, sans vernis ni faux ongles, **pas de bijoux** aux mains et poignets (ni montre, ni
bague, ni bracelet), avant-bras dégagés.
""")
    ui.memo("Deux moments **avant**, trois moments **après** : « avant le patient, avant l'aseptique ; après le liquide, "
            "après le patient, après son environnement ».")
    ui.clinic("Désinfecte aussi la **table** et le **matériel** (élastiques, ballons) entre chaque patient, et utilise "
              "un drap ou un papier propre par patient.")


def ch_urgence():
    ui.md(r"""
**Lésions des tissus mous (entorse, contusion)** : l'ancien protocole RICE (repos, glace, compression,
élévation) a été remplacé par **[[peace & love|PEACE & LOVE]]** (Dubois et Esculier, 2020) :

| Immédiatement : **PEACE** | Ensuite : **LOVE** |
|---|---|
| **P**rotéger (limiter les mouvements douloureux 1 à 3 jours) | **L**oad : remettre en charge progressivement, guidé par la douleur |
| **É**lever le membre | **O**ptimisme : un discours positif améliore la récupération |
| **É**viter les anti-inflammatoires (**A**void), qui gênent la cicatrisation | **V**ascularisation : activité cardio sans douleur |
| **C**ompresser (bandage) | **E**xercice : mobilité, force, proprioception |
| **É**duquer : expliquer, éviter les traitements passifs inutiles | |

La glace soulage la douleur mais son effet sur la guérison n'est pas démontré, d'où son absence de PEACE & LOVE.

**Plaie** : se protéger (gants), nettoyer à l'eau, désinfecter, couvrir. Saignement abondant : **compression
directe**. Saignement de nez : tête **penchée en avant** (pas en arrière !) et pincer les narines 10 minutes.
""")
    st.markdown("#### Les brûlures")
    ui.md(r"""
| Degré | Profondeur | Aspect | Douleur |
|---|---|---|---|
| 1er | épiderme | rouge, sec (coup de soleil) | oui |
| 2e superficiel | derme superficiel | [[phlyctène\|cloques]], rouge, suintant | très douloureux |
| 2e profond | derme profond | cloques, fond pâle | peu douloureux |
| 3e | toute la peau | blanc, brun ou noir, cartonné | **indolore** (nerfs détruits) |

**Premier geste** : refroidir à l'**eau tempérée** (environ 15 à 25 °C) pendant **20 minutes**, le plus vite
possible. Pas de glace, pas de beurre ni de dentifrice. Retirer les bijoux, ne pas percer les cloques. Appeler
le 112 si la brûlure est étendue, profonde, au visage, aux mains, au périnée, ou chez un enfant.
""")
    st.markdown("#### À toi : la règle des 9 (Wallace)")
    st.caption("Chez l'adulte, chaque zone représente un multiple de 9 % de la surface du corps. Coche les zones brûlées.")
    cols = st.columns(2)
    total = 0
    for i, (zone, pct) in enumerate(AREAS.items()):
        if cols[i % 2].checkbox(f"{zone} ({pct} %)", key=f"mk_burn_{i}"):
            total += pct
    st.metric("Surface brûlée", f"{total} %")
    if total >= 10:
        st.error("Brûlure grave chez l'adulte (≥ 10 % de la surface) : appel au 112.")
    elif total:
        st.info("Astuce pour les petites zones : la paume de la main du patient (doigts compris) fait environ 1 %.")
    ui.warn("La règle des 9 est faite pour les **adultes**. L'enfant a une tête proportionnellement plus grande et des "
            "jambes plus petites : on utilise des tables adaptées (Lund et Browder).")


CHAPTERS = [
    ("Ta santé et ton projet", ch_sante),
    ("Communiquer avec le patient", ch_communication),
    ("Consentement, secret, juste distance", ch_ethique),
    ("Hygiène", ch_hygiene),
    ("Petites urgences et brûlures", ch_urgence),
]


def _q_wallace(rng):
    zones = rng.sample(list(AREAS), rng.choice([2, 3]))
    total = sum(AREAS[z] for z in zones)
    return dict(prompt=f"Selon la règle des 9 (adulte), quel pourcentage de surface corporelle représentent : "
                       f"{', '.join(z.lower() for z in zones)} ?",
                answer=total, unit="%", tol=0.0, why=" + ".join(f"{AREAS[z]}" for z in zones) + f" = {total} %.")


BRULURES = [
    ("Peau rouge et sèche, douloureuse, après une journée à la plage.", "1er degré"),
    ("Cloques remplies de liquide, très douloureuses, après une éclaboussure d'eau bouillante.", "2e degré superficiel"),
    ("Peau blanche et cartonnée, que le patient ne sent presque pas.", "3e degré"),
]


def _q_brulure(rng):
    d, good = rng.choice(BRULURES)
    return (f"{d} De quel degré de brûlure s'agit-il ?", good, ["1er degré", "2e degré superficiel", "2e degré profond", "3e degré"], "")


QUESTIONS = [
    qcm(1, "Combien de moments compte l'hygiène des mains selon l'OMS ?", "5", ["3", "4", "7"]),
    qcm(1, "Combien de temps faut-il refroidir une brûlure ?", "20 minutes à l'eau tempérée",
        ["2 minutes à l'eau glacée", "1 heure avec de la glace", "Il ne faut pas la refroidir"]),
    vf(1, "En cas de saignement de nez, il faut pencher la tête en arrière.", False,
       "En avant, pour ne pas avaler le sang, et pincer les narines."),
    vf(1, "Un patient peut retirer son consentement à tout moment.", True),
    qcm(1, "Dans PEACE & LOVE, que signifie le A de PEACE ?", "Éviter les anti-inflammatoires",
        ["Appliquer de la glace", "Arrêter tout mouvement", "Analgésiques systématiques"]),
    gen_qcm(1, _q_brulure),
    qcm(2, "Quand faut-il se laver les mains à l'eau et au savon plutôt qu'utiliser une friction hydroalcoolique ?",
        "Quand les mains sont visiblement souillées", ["Toujours", "Jamais", "Seulement le matin"]),
    multi(2, "Quels éléments font partie de l'écoute active ?", ["La reformulation", "Les questions ouvertes",
          "Les silences et relances"], ["Donner rapidement des conseils", "Raconter sa propre expérience"]),
    qcm(2, "Le secret professionnel en Belgique est prévu par…", "l'article 458 du Code pénal",
        ["la Constitution, article 1", "le règlement de l'UCLouvain", "le code de la route"]),
    qcm(2, "Une brûlure du 3e degré est souvent…", "indolore, car les terminaisons nerveuses sont détruites",
        ["la plus douloureuse", "couverte de cloques", "limitée à l'épiderme"]),
    num(2, _q_wallace),
    qcm(2, "Que veut dire « empowerment » en santé ?", "Renforcer le pouvoir d'agir du patient sur sa santé",
        ["Augmenter la force musculaire", "Donner plus d'autorité au soignant", "Prescrire plus de séances"]),
    qcm(3, "Pendant ton stage, un ami te demande des nouvelles de son voisin, que tu soignes. Que fais-tu ?",
        "Tu ne dis rien, même pas que tu le soignes", ["Tu donnes des nouvelles générales sans détails",
        "Tu le dis car c'est un proche", "Tu demandes d'abord à ton maître de stage"],
        "Même le fait d'être soigné est couvert par le secret."),
    qcm(3, "Une entorse de cheville date de la veille. Quelle prise en charge suit les recommandations actuelles ?",
        "Protéger, élever, comprimer, éduquer, éviter les anti-inflammatoires, puis recharger progressivement",
        ["Repos strict trois semaines avec glace", "Anti-inflammatoires et immobilisation plâtrée systématique",
         "Reprise immédiate du sport à pleine charge"]),
    qcm(3, "Un patient dit : « De toute façon, rien ne marche pour moi. » La réponse la plus adaptée est…",
        "« Vous avez l'impression d'avoir tout essayé… qu'est-ce que vous avez déjà essayé ? »",
        ["« Mais si, ça va marcher, vous verrez. »", "« Vous devez être plus motivé. »",
         "« Les autres patients s'en sortent bien, eux. »"]),
    multi(3, "Quelles brûlures justifient un appel au 112 ?", ["Brûlure de 15 % de la surface chez un adulte",
          "Brûlure profonde des mains", "Brûlure étendue chez un jeune enfant"],
          ["Coup de soleil de 2 % sur l'épaule"]),
]

CARDS = [
    ("5 moments de l'hygiène des mains", "Avant patient, avant geste aseptique, après liquide biologique, après patient, après environnement"),
    ("Friction hydroalcoolique", "20 à 30 s ; eau + savon si mains souillées"),
    ("PEACE", "Protéger, Élever, Éviter les anti-inflammatoires, Compresser, Éduquer"),
    ("LOVE", "Load, Optimisme, Vascularisation, Exercice"),
    ("Brûlure : premier geste", "Eau tempérée 20 minutes"),
    ("Règle des 9 (adulte)", "Tête 9, chaque bras 9, tronc avant 18, arrière 18, chaque jambe 18, périnée 1"),
    ("Brûlure du 3e degré", "Blanche/cartonnée, indolore"),
    ("Consentement éclairé", "Information claire, accord libre, retrait possible à tout moment"),
    ("Secret professionnel (Belgique)", "Article 458 du Code pénal"),
    ("Recommandations OMS adultes", "150-300 min/sem modéré ou 75-150 min soutenu + renforcement 2 j/sem"),
    ("Saignement de nez", "Tête en avant, pincer 10 minutes"),
]

VIDEOS = [
    ("Les 5 moments de l'hygiène des mains (OMS)", "5 moments hygiène des mains OMS"),
    ("Technique de friction hydroalcoolique", "friction hydroalcoolique technique OMS"),
    ("PEACE & LOVE expliqué", "PEACE and LOVE entorse Dubois Esculier"),
    ("Écoute active et reformulation", "écoute active reformulation soignant"),
]

LINKS = [
    ("PEACE & LOVE, l'article original (British Journal of Sports Medicine, 2020)",
     "https://bjsm.bmj.com/content/54/2/72"),
    ("Croix-Rouge de Belgique : premiers secours", "https://www.croix-rouge.be/"),
]
