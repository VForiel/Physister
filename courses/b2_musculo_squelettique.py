"""LKNR1204 Pathologies et kinésithérapie du système musculo-squelettique."""

import streamlit as st

from app import ui
from app.course import Course
from app.quiz import gen_qcm, multi, qcm, table_qcm, vf

COURSE = Course(
    code="LKNR1204", title="Pathologies et kinésithérapie du système musculo-squelettique", short="Musculo-squelettique",
    bloc=2, quad=2, credits=7, hours="45 h + 37,5 h", icon=":material/orthopedics:",
    intro="Le plus gros cours du bloc 2 et le cœur de la pratique libérale : traumatismes, tendinopathies, arthrose, "
          "lombalgies et cervicalgies, épaule, genou, cheville, post-opératoire. Pour chaque problème : comprendre, "
          "examiner, savoir quand référer, et traiter.",
    acquis=[
        "Décrire l'épidémiologie, la physiopathologie et la présentation clinique des pathologies.",
        "Utiliser les tests et outils cliniques en connaissant leurs qualités psychométriques.",
        "Mener l'examen clinique, poser un diagnostic kiné et un pronostic.",
        "Référer le patient quand c'est nécessaire.",
        "Choisir et adapter actes techniques, exercices et éducation thérapeutique.",
    ],
)

TERMS = {
    "consolidation": ("Consolidation osseuse", "Réparation d'une fracture : hématome, cal mou, cal dur, remodelage. "
                      "Environ 6 à 12 semaines chez l'adulte.", "Consolidation osseuse"),
    "tendinopathie": ("Tendinopathie", "Douleur et perte de fonction d'un tendon liées à la charge, avec "
                      "modifications de sa structure. Pas vraiment une inflammation (d'où l'abandon du mot « tendinite »).",
                      "Tendinopathie"),
    "arthrose": ("Arthrose", "Maladie de toute l'articulation (cartilage, os, synoviale, capsule, muscles) : douleur "
                 "mécanique, raideur matinale courte, perte de fonction.", "Arthrose"),
    "lombalgie commune": ("Lombalgie commune (non spécifique)", "Douleur lombaire sans cause précise identifiable "
                          "(environ 90 % des lombalgies).", "Lombalgie"),
    "radiculopathie": ("Radiculopathie", "Atteinte d'une racine nerveuse (souvent par une hernie discale) : douleur "
                       "dans un dermatome, parfois déficit moteur, sensitif ou réflexe.", "Radiculopathie"),
    "lca": ("LCA", "Ligament croisé antérieur : empêche le tibia de partir en avant et contrôle les rotations. Lésé "
            "lors des pivots, souvent sans contact.", "Ligament croisé antérieur"),
    "test de lachman": ("Test de Lachman", "Test de la laxité du LCA, genou fléchi à environ 20-30° : on tire le tibia "
                        "vers l'avant.", "Test de Lachman"),
    "conflit sous-acromial": ("Douleur d'épaule liée à la coiffe", "Douleur à l'élévation du bras, longtemps "
                              "expliquée par un « conflit » mécanique sous l'acromion ; on parle aujourd'hui plutôt de "
                              "douleur de la coiffe des rotateurs liée à la charge.", None),
    "capsulite rétractile": ("Capsulite rétractile", "Épaule gelée : inflammation puis rétraction de la capsule, "
                             "avec perte surtout de la rotation latérale passive. Évolue sur 1 à 3 ans.", "Capsulite rétractile"),
    "règles d'ottawa": ("Règles d'Ottawa", "Critères cliniques qui indiquent quand faire une radio après un "
                        "traumatisme de cheville ou de pied.", "Règles d'Ottawa"),
    "emg": ("EMG", "Électromyographie : enregistrement de l'activité électrique des muscles et étude de la "
            "conduction nerveuse.", "Électromyographie"),
}

SYNDROMES = {
    "Lombalgie non spécifique": "douleur lombaire mécanique sans signe neurologique ni drapeau rouge",
    "Radiculopathie L5": "douleur jusqu'au dos du pied, faiblesse de l'extension du gros orteil",
    "Radiculopathie S1": "douleur jusqu'à la plante et au bord latéral du pied, réflexe achilléen diminué",
    "Tendinopathie de la coiffe": "douleur à l'élévation et contre résistance, amplitude passive conservée",
    "Capsulite rétractile": "perte de la rotation latérale passive, douleur nocturne",
    "Rupture du LCA": "pivot, craquement, gonflement rapide (hémarthrose), instabilité",
    "Lésion méniscale": "douleur sur l'interligne, blocages, gonflement retardé",
    "Entorse latérale de cheville": "inversion forcée, douleur sous la malléole latérale",
    "Tendinopathie d'Achille": "raideur matinale du tendon, douleur au début de l'effort",
    "Gonarthrose": "douleur mécanique, raideur matinale de moins de 30 minutes, plus de 45 ans",
}


def ch_principes():
    ui.md(r"""
**Les grandes familles**
- **Traumatismes** : fractures ([[consolidation]] en 6 à 12 semaines), lésions musculaires (du simple
  étirement à la rupture), entorses (ligaments, grades I à III), lésions tendineuses.
- **[[tendinopathie|Tendinopathies]]** : liées à la charge ; un continuum de la tendinopathie réactive
  (surcharge brutale) à la tendinopathie dégénérative.
- **[[arthrose|Arthrose]]** : très fréquente après 50 ans (genou, hanche, main). L'exercice est le traitement de
  première ligne, avec l'éducation et le contrôle du poids.
- **Pathologies non spécifiques** : douleur sans lésion précise (lombalgie, cervicalgie).

**Les examens paracliniques** : la **radiographie** (os, arthrose), l'**échographie** (tendons, muscles, liquide),
l'**IRM** (tissus mous, disques, ménisques, ligaments), le **scanner** (os en détail), les **tests sanguins**
(inflammation, infection), l'[[emg|EMG]] (nerfs, muscles).
""")
    ui.warn("L'imagerie montre beaucoup d'anomalies **chez des gens sans douleur** : hernies discales, arthrose, "
            "« usure » de la coiffe sont fréquentes après 40 ans et n'expliquent pas forcément la douleur. Une image "
            "ne remplace jamais l'examen clinique.")
    ui.md(r"""
**Les principes de traitement** : éducation (expliquer, rassurer, gérer la charge), **exercice** progressif adapté
(c'est le cœur du traitement), techniques manuelles en complément, retour progressif aux activités. Et toujours :
**chercher les drapeaux rouges**, et référer si besoin.
""")
    ui.clinic("Hygiène : désinfection des mains et du matériel entre chaque patient, attention aux plaies "
              "post-opératoires (pas de massage sur une cicatrice non fermée), et aux patients immunodéprimés.")


def ch_rachis():
    ui.md(r"""
**La [[lombalgie commune]]** : presque tout le monde en fait une un jour ; c'est la première cause d'années vécues
avec un handicap dans le monde. Elle guérit le plus souvent en quelques semaines, mais récidive souvent.

**Le tri diagnostique** (triage) :
1. **Pathologie grave** (drapeaux rouges : fracture, cancer, infection, syndrome de la queue de cheval) : < 1 à 2 %.
2. **[[radiculopathie|Radiculopathie]]** (douleur dans la jambe, sous le genou, dans un dermatome) : environ 5 à 10 %.
3. **Lombalgie non spécifique** : environ 90 %.

**Le traitement de la lombalgie non spécifique** : rassurer (« le dos est solide »), rester **actif**, éviter le
repos au lit, exercice, et dépister les **drapeaux jaunes** (peur, catastrophisme, stress au travail) qui
prédisent la chronicité. Pas d'imagerie en routine.

**La cervicalgie** suit la même logique : surtout non spécifique, exercice et éducation, attention aux drapeaux
rouges (traumatisme, signes neurologiques, insuffisance vertébro-basilaire avant les manipulations cervicales).
""")
    ui.table([
        ["L4", "face antérieure de la jambe, bord médial du pied", "extension du genou (quadriceps)", "rotulien"],
        ["L5", "face latérale de la jambe, dos du pied, gros orteil", "extension du gros orteil, flexion dorsale", "aucun fiable"],
        ["S1", "plante et bord latéral du pied", "flexion plantaire (marche sur les pointes)", "achilléen"],
    ], headers=["Racine", "Douleur et sensibilité", "Faiblesse", "Réflexe"])


def ch_membre_sup():
    ui.md(r"""
**L'épaule douloureuse** (souvent tendinopathie de la coiffe des rotateurs) : douleur à l'élévation (arc
douloureux entre 60 et 120°), à la résistance ; amplitudes **passives** conservées. Traitement : exercices de
renforcement progressifs de la coiffe et des muscles de la scapula, gestion de la charge. La chirurgie
d'acromioplastie ne fait pas mieux que l'exercice dans la plupart des cas.

**L'épaule raide** : la [[capsulite rétractile]] (perte de la rotation latérale **passive**, douleur nocturne,
souvent chez les 40-60 ans, diabétiques). Évolution en phases (douloureuse, raide, récupération) sur 1 à 3 ans.

**L'épaule instable** : luxation (le plus souvent antérieure, bras en abduction et rotation latérale), récidives
fréquentes chez le jeune sportif. Renforcement, proprioception, parfois chirurgie de stabilisation.
""")
    ui.memo("Pour différencier : **tendinopathie** = l'actif fait mal, le **passif est libre**. **Capsulite** = le "
            "**passif est limité** (surtout la rotation latérale). C'est l'examen passif qui tranche.")


def ch_membre_inf():
    ui.md(r"""
**Le genou traumatique**
- **Rupture du [[lca|LCA]]** : pivot sans contact, craquement, gonflement rapide (sang dans l'articulation),
  sensation que le genou « lâche ». Test clé : le [[test de lachman|Lachman]]. Traitement : rééducation seule ou
  ligamentoplastie, puis 9 à 12 mois avant le retour au pivot.
- **Lésion méniscale** : douleur sur l'interligne, blocages, gonflement plus progressif. On préserve le ménisque
  (réparation plutôt qu'ablation, ou rééducation seule chez la personne d'âge moyen à lésion dégénérative).

**L'entorse de cheville** : la plus fréquente des blessures sportives, souvent l'inversion, avec lésion du ligament
talo-fibulaire antérieur. Les [[règles d'ottawa|règles d'Ottawa]] disent quand une radio est utile. Traitement :
PEACE & LOVE, mise en charge précoce, puis proprioception et renforcement (le meilleur moyen d'éviter les récidives).

**L'arthrose de hanche et de genou** : exercice (renforcement, aérobie), perte de poids si surpoids, éducation. Si
échec : prothèse totale de hanche (PTH) ou de genou (PTG), avec rééducation post-opératoire.

**Post-opératoire** : respecter les consignes du chirurgien (mise en charge, amplitudes autorisées, précautions de
la PTH selon la voie d'abord), prévenir les complications (thrombose, raideur), récupérer amplitude, force et marche.
""")
    st.markdown("#### À toi : faut-il une radio de la cheville ? (règles d'Ottawa)")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Cheville** : douleur dans la zone malléolaire **et** au moins un critère :")
        a = st.checkbox("Douleur à la palpation du bord postérieur ou de la pointe de la malléole latérale (6 derniers cm)", key="ot_a")
        b = st.checkbox("Douleur à la palpation du bord postérieur ou de la pointe de la malléole médiale (6 derniers cm)", key="ot_b")
    with c2:
        st.markdown("**Pied** : douleur dans le médio-pied **et** au moins un critère :")
        c = st.checkbox("Douleur à la palpation de la base du 5e métatarsien", key="ot_c")
        d = st.checkbox("Douleur à la palpation de l'os naviculaire", key="ot_d")
    e = st.checkbox("Incapacité à faire 4 pas (en boitant, c'est permis) juste après le traumatisme et à l'examen", key="ot_e")
    if a or b or e:
        st.error("Radiographie de la **cheville** indiquée.")
    if c or d or e:
        st.error("Radiographie du **pied** indiquée.")
    if not any((a, b, c, d, e)):
        st.success("Aucun critère : la radio n'est pas nécessaire (sensibilité proche de 100 % pour exclure une fracture).")
    ui.tip("Les règles d'Ottawa sont très **sensibles** : quand elles sont négatives, on peut exclure une fracture "
           "en toute confiance (SnNout). Elles sont moins **spécifiques** : positives, elles ne prouvent pas la "
           "fracture. On en reparle en EBP 2.")


def ch_raisonnement():
    st.markdown("Associe chaque tableau clinique à son syndrome : c'est l'entraînement aux vignettes de l'examen.")
    ui.table([[k, v] for k, v in SYNDROMES.items()], headers=["Syndrome", "Tableau typique"])
    ui.md(r"""
**Démarche pour une vignette**
1. Repérer les éléments clés : âge, mécanisme, localisation, comportement de la douleur (mécanique ou non),
   signes neurologiques, drapeaux.
2. Formuler 2 ou 3 hypothèses et les tests qui les départagent.
3. Diagnostic kiné en termes de **fonction** (CIF) : « limitation de la montée des escaliers due à une faiblesse du
   quadriceps et une douleur fémoro-patellaire ».
4. Pronostic, objectifs, plan de traitement, critères de réévaluation.
""")


CHAPTERS = [
    ("Principes et grandes pathologies", ch_principes),
    ("Rachis lombaire et cervical", ch_rachis),
    ("Épaule", ch_membre_sup),
    ("Genou et cheville", ch_membre_inf),
    ("Raisonnement sur vignettes", ch_raisonnement),
]


def _q_ottawa(rng):
    cas = [
        ("Après une entorse, la patiente marche 4 pas en boitant ; douleur seulement en avant de la malléole latérale.", "Non"),
        ("Douleur à la palpation de la pointe de la malléole latérale.", "Oui, radio de la cheville"),
        ("Douleur à la palpation de la base du 5e métatarsien.", "Oui, radio du pied"),
        ("Le patient ne peut pas faire 4 pas, même en boitant.", "Oui, radio de la cheville et du pied"),
    ]
    t, good = rng.choice(cas)
    return (f"Règles d'Ottawa. {t} Une radio est-elle indiquée ?", good, [g for _, g in cas], "")


QUESTIONS = [
    table_qcm(1, SYNDROMES, "Quel tableau correspond à : **{k}** ?", "Quel syndrome évoque ce tableau : {v} ?"),
    qcm(1, "Quelle proportion des lombalgies est non spécifique ?", "Environ 90 %", ["Environ 10 %", "Environ 50 %", "100 %"]),
    qcm(1, "Quel test évalue le ligament croisé antérieur ?", "Le test de Lachman", ["Le test de Lasègue",
        "Le test de Romberg", "Le test de Trendelenburg"]),
    vf(1, "Le repos au lit est recommandé dans la lombalgie aiguë commune.", False, "Rester actif est recommandé."),
    qcm(1, "Quel est le traitement de première ligne de l'arthrose du genou ?", "L'exercice et l'éducation",
        ["La prothèse", "Le repos complet", "Les infiltrations systématiques"]),
    gen_qcm(2, _q_ottawa),
    qcm(2, "Une épaule a une rotation latérale passive très limitée et des douleurs nocturnes. On pense à…",
        "une capsulite rétractile", ["une tendinopathie de la coiffe", "une luxation antérieure", "une arthrose acromio-claviculaire"]),
    qcm(2, "Une douleur jusqu'au gros orteil avec faiblesse de son extension évoque une atteinte de…", "la racine L5",
        ["la racine S1", "la racine L3", "la racine C7"]),
    multi(2, "Quels éléments évoquent une rupture du LCA ?", ["Pivot sans contact", "Gonflement rapide", "Sensation d'instabilité"],
          ["Douleur uniquement à la palpation de la malléole", "Raideur matinale de 2 heures"]),
    vf(2, "Une hernie discale vue à l'IRM explique forcément la douleur du patient.", False,
       "On en trouve souvent chez des personnes sans douleur."),
    qcm(2, "Pourquoi a-t-on abandonné le mot « tendinite » ?", "Parce que la tendinopathie n'est pas principalement une inflammation",
        ["Parce qu'il est trop long", "Parce que les tendons ne font jamais mal", "Parce qu'il désigne une fracture"]),
    qcm(3, "Un homme de 65 ans, lombalgique, a des antécédents de cancer de la prostate et des douleurs nocturnes. Que faire ?",
        "Le référer au médecin : drapeaux rouges d'une possible métastase", ["Commencer les exercices",
        "Lui conseiller du repos", "Masser la zone douloureuse"]),
    qcm(3, "Pourquoi des règles d'Ottawa négatives permettent-elles d'éviter une radio ?",
        "Leur sensibilité est très élevée : un test négatif exclut presque toujours une fracture (SnNout)",
        ["Leur spécificité est parfaite", "Parce que les fractures de cheville sont impossibles", "Parce que la radio est dangereuse"]),
    qcm(3, "Quelle intervention réduit le plus les récidives d'entorse de cheville ?", "Le travail proprioceptif et le renforcement",
        ["Le repos prolongé", "Le massage", "Les ultrasons"]),
    qcm(3, "Patient de 35 ans, douleur d'épaule à l'élévation et contre résistance, passif complet et indolore. Plan de traitement ?",
        "Éducation et renforcement progressif de la coiffe et des muscles scapulaires", ["Mobilisations passives intensives pour gagner de l'amplitude",
        "Immobilisation stricte", "Chirurgie d'emblée"]),
]

CARDS = list(SYNDROMES.items()) + [
    ("Tri de la lombalgie", "Pathologie grave < 2 %, radiculopathie 5-10 %, non spécifique ≈ 90 %"),
    ("Racine L5", "Dos du pied, gros orteil ; faiblesse de l'extension de l'hallux"),
    ("Racine S1", "Plante, bord latéral ; réflexe achilléen"),
    ("Règles d'Ottawa (cheville)", "Pointe/bord post. des malléoles, 4 pas impossibles"),
    ("Règles d'Ottawa (pied)", "Base du 5e métatarsien, naviculaire, 4 pas impossibles"),
    ("Consolidation osseuse", "6 à 12 semaines chez l'adulte"),
    ("Tendinopathie vs capsulite", "Actif douloureux, passif libre vs passif limité (RL)"),
]

VIDEOS = [
    ("Lombalgie : ce que dit la science", "lombalgie commune recommandations kinésithérapie rester actif"),
    ("Test de Lachman", "test de Lachman démonstration"),
    ("Règles d'Ottawa cheville", "règles d'Ottawa cheville explication"),
    ("Rééducation d'une tendinopathie", "tendinopathie rééducation renforcement charge"),
]

LINKS = [
    ("KCE : recommandations lombalgie et douleur radiculaire (Belgique)", "https://kce.fgov.be/fr"),
    ("Physiopedia : Ottawa ankle rules", "https://www.physio-pedia.com/Ottawa_Ankle_Rules"),
]
