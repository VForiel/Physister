"""LKNR1102 Développement durable."""

import plotly.graph_objects as go
import streamlit as st

from app import ui
from app.course import Course
from app.quiz import gen_qcm, multi, num, qcm, vf

COURSE = Course(
    code="LKNR1102", title="Développement durable", short="Développement durable",
    bloc=1, quad=2, credits=2, hours="22,5 h", icon=":material/eco:",
    intro="Le climat change la santé (chaleur, allergies, maladies infectieuses), et les soins de santé pèsent "
          "eux-mêmes sur le climat. Le kiné a un rôle à jouer : la mobilité active et l'exercice sont à la fois "
          "bons pour la santé et pour la planète.",
    acquis=[
        "Comprendre les enjeux du développement durable et de la transition.",
        "Mesurer leur influence sur les choix de prise en charge.",
        "Avoir une approche critique des tensions liées à ces enjeux.",
        "Identifier les liens entre environnement, santé et comportement.",
    ],
)

TERMS = {
    "limites planétaires": ("Limites planétaires", "Neuf seuils (Rockström et al., 2009) au-delà desquels "
                            "l'équilibre de la Terre risque de basculer : climat, biodiversité, cycles de l'azote et "
                            "du phosphore, eau douce, sols, acidification des océans, ozone, aérosols, nouvelles "
                            "entités (plastiques, produits chimiques).", "Limites planétaires"),
    "donut": ("Théorie du Donut", "Modèle de Kate Raworth : l'humanité doit vivre entre un plancher social (besoins "
              "de base pour tous) et un plafond écologique (les limites planétaires).", "Économie du donut"),
    "odd": ("Objectifs de développement durable", "17 objectifs adoptés par l'ONU en 2015 pour 2030 (pauvreté, "
            "santé, éducation, climat…). La santé est l'ODD 3.", "Objectifs de développement durable"),
    "one health": ("One Health", "Approche qui considère que la santé humaine, la santé animale et celle des "
                   "écosystèmes sont liées et doivent être gérées ensemble.", "One Health"),
    "co-bénéfice": ("Co-bénéfice", "Action qui améliore à la fois la santé et l'environnement (vélo, alimentation "
                    "plus végétale…).", None),
    "éco-anxiété": ("Éco-anxiété", "Inquiétude face aux menaces environnementales. Réaction compréhensible, elle "
                    "peut paralyser ou pousser à agir.", "Éco-anxiété"),
    "point de bascule": ("Point de bascule", "Seuil au-delà duquel un système change d'état de façon rapide et "
                         "souvent irréversible (fonte des calottes, mais aussi, côté social, adoption rapide d'une "
                         "nouvelle norme).", "Point de basculement climatique"),
    "scope 3": ("Scope 3", "Émissions indirectes d'une organisation : achats, chaîne d'approvisionnement, "
                "déplacements des patients et du personnel. Pour les soins de santé, c'est la plus grosse part.",
                None),
}

LIMITES = [  # état d'après le bilan Planetary Health Check 2025
    ("Changement climatique", True), ("Intégrité de la biosphère", True), ("Changement d'usage des sols", True),
    ("Eau douce", True), ("Cycles biogéochimiques (azote, phosphore)", True), ("Nouvelles entités", True),
    ("Acidification des océans", True), ("Aérosols atmosphériques", False), ("Couche d'ozone", False),
]

DISCOURS = [
    ("« La Belgique ne pèse que 0,3 % des émissions mondiales, c'est à la Chine d'agir. »", "Rediriger la responsabilité"),
    ("« La technologie va régler le problème, pas besoin de changer nos habitudes. »", "Promouvoir des solutions non transformatrices"),
    ("« Les mesures climatiques vont appauvrir les plus fragiles. »", "Insister sur les inconvénients"),
    ("« De toute façon, c'est trop tard, on ne peut plus rien faire. »", "Capituler"),
]


def ch_concepts():
    ui.md(r"""
**Le développement durable** (rapport Brundtland, 1987) : « un développement qui répond aux besoins du présent sans
compromettre la capacité des générations futures de répondre aux leurs ».

**Les [[limites planétaires]]** : neuf processus qui assurent la stabilité de la Terre. D'après le bilan de 2025,
sept limites sur neuf sont déjà dépassées.
""")
    fig = go.Figure(go.Bar(
        y=[n for n, _ in LIMITES], x=[1] * len(LIMITES), orientation="h",
        marker_color=["#c0392b" if d else "#2e8b57" for _, d in LIMITES],
        text=["dépassée" if d else "dans la zone sûre" for _, d in LIMITES], textposition="inside",
    ))
    fig.update_layout(height=330, margin=dict(l=10, r=10, t=10, b=10), xaxis=dict(visible=False),
                      yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, width="stretch")
    ui.md(r"""
**La [[donut|théorie du Donut]]** (Kate Raworth) : un anneau entre un **plancher social** (personne ne doit manquer
d'eau, de nourriture, de soins, d'éducation…) et un **plafond écologique** (les limites planétaires). L'objectif
est d'être **dans** l'anneau.

**Les [[odd|17 ODD]]** de l'ONU (2015-2030), dont l'ODD 3 : « Bonne santé et bien-être ».

**[[one health|One Health]]** : la santé humaine dépend de celle des animaux et des écosystèmes (zoonoses comme le
COVID-19, résistance aux antibiotiques, pollinisateurs et alimentation).
""")


def ch_sante():
    ui.md(r"""
**Le climat abîme la santé**
- **Chaleur** : coups de chaleur, déshydratation, aggravation des maladies cardiaques et respiratoires, surtout
  chez les personnes âgées et les patients polymédiqués. Les vagues de chaleur font des milliers de morts en Europe.
- **Pollution de l'air** : asthme, BPCO, maladies cardiovasculaires.
- **Allergies** : saisons polliniques plus longues et plus intenses.
- **Maladies infectieuses** : extension des moustiques et des tiques (maladie de Lyme).
- **Santé mentale** : stress après les catastrophes (inondations de 2021 en Wallonie), [[éco-anxiété]].

**Et les soins de santé abîment le climat** : le secteur de la santé représente environ **4 à 5 %** des émissions
mondiales de gaz à effet de serre. La plus grosse part vient du [[scope 3]] : médicaments, matériel, déplacements
des patients et du personnel, alimentation, énergie des bâtiments.
""")
    ui.clinic("En kiné, l'empreinte vient surtout des **déplacements** (patients et kiné à domicile), de l'énergie du "
              "cabinet, du matériel à usage unique et des appareils (électrothérapie, ondes de choc) parfois peu "
              "utiles. Le soin le plus durable est souvent le plus **efficace** : moins de séances inutiles, plus "
              "d'autonomie du patient, exercices à domicile.")


def ch_strategies():
    ui.md(r"""
**Penser en système** : chercher les actions qui ont plusieurs effets positifs à la fois, les
[[co-bénéfice|co-bénéfices]].

| Action | Bénéfice santé | Bénéfice environnemental |
|---|---|---|
| Vélo et marche pour les trajets | activité physique, moins de maladies chroniques | moins de CO₂ et de pollution |
| Alimentation plus végétale | moins de maladies cardiovasculaires | moins d'émissions et d'eau |
| Prévention et activité physique | moins de maladies évitables | moins de soins lourds |
| Téléconsultation quand c'est pertinent | accès facilité | moins de trajets |
| Matériel durable plutôt que jetable | idem | moins de déchets |
""")
    st.markdown("#### À toi : le trajet domicile-travail")
    c1, c2 = st.columns([1, 2])
    with c1:
        km = st.slider("Distance aller (km)", 1, 20, 5, key="dd_km")
        jours = st.slider("Jours par semaine", 1, 5, 4, key="dd_j")
    km_an = km * 2 * jours * 44
    co2 = km_an * 0.2  # ordre de grandeur pour une voiture thermique moyenne (kg CO2/km)
    minutes = km * 2 * jours * 60 / 15  # vélo à 15 km/h
    with c2:
        st.metric("CO₂ évité par an en vélo plutôt qu'en voiture", f"≈ {co2:.0f} kg")
        st.metric("Activité physique gagnée par semaine", f"≈ {minutes:.0f} min",
                  delta="objectif OMS atteint" if minutes >= 150 else f"{150 - minutes:.0f} min de l'objectif OMS")
    st.caption("Ordres de grandeur : environ 0,2 kg de CO₂ par km pour une voiture thermique moyenne, 44 semaines "
               "travaillées, vélo à 15 km/h.")


def ch_transition():
    ui.md(r"""
**Les discours de l'inaction** (Lamb et al., 2020) : des arguments qui ne nient pas le changement climatique mais
**retardent** l'action. Quatre familles :
1. **Rediriger la responsabilité** (« c'est aux autres d'agir d'abord ») ;
2. **Promouvoir des solutions non transformatrices** (« la technologie nous sauvera ») ;
3. **Insister sur les inconvénients** (« ça coûtera trop cher, ce sera injuste ») ;
4. **Capituler** (« c'est trop tard »).

Les reconnaître permet d'y répondre. Par exemple, au « c'est trop tard » : chaque dixième de degré compte, ce
n'est pas tout ou rien.

**Dynamiques de transition** : l'[[éco-anxiété]] est fréquente chez les jeunes ; l'**action** (individuelle et
collective) est l'un des meilleurs moyens d'y faire face. Les changements sociaux ont aussi leurs
[[point de bascule|points de bascule]] : quand une part suffisante d'un groupe adopte une norme (environ 25 % dans
certaines études), elle peut se généraliser vite.

**Perspective éthique** : justice climatique (les plus pauvres polluent le moins et souffrent le plus), justice
entre générations, responsabilité des soignants (« d'abord ne pas nuire » s'étend à l'environnement).
""")


CHAPTERS = [
    ("Concepts clés", ch_concepts),
    ("Climat et santé", ch_sante),
    ("Stratégies pour les soignants", ch_strategies),
    ("Transition, discours et éthique", ch_transition),
]


def _q_discours(rng):
    d, good = rng.choice(DISCOURS)
    return (f"À quelle famille de discours de l'inaction appartient : {d}", good, [g for _, g in DISCOURS], "")


def _q_co2(rng):
    km = rng.choice([3, 5, 8, 10])
    j = rng.choice([3, 4, 5])
    co2 = km * 2 * j * 44 * 0.2
    return dict(prompt=f"Un kiné fait {km} km (aller) en voiture, {j} jours par semaine, 44 semaines par an. À 0,2 kg de "
                       f"CO₂ par km, combien de kg de CO₂ éviterait-il par an en vélo ?",
                answer=co2, unit="kg", tol=0.02, why=f"{km} × 2 × {j} × 44 × 0,2 = {co2:.0f} kg.")


QUESTIONS = [
    qcm(1, "Combien y a-t-il de limites planétaires ?", "9", ["5", "12", "17"]),
    qcm(1, "Combien y a-t-il d'objectifs de développement durable (ONU) ?", "17", ["9", "10", "25"]),
    vf(1, "L'approche One Health relie santé humaine, animale et environnementale.", True),
    qcm(1, "Qui a proposé la théorie du Donut ?", "Kate Raworth", ["Johan Rockström", "Gro Harlem Brundtland", "Greta Thunberg"]),
    gen_qcm(2, _q_discours),
    qcm(2, "Quelle part des émissions mondiales viennent du secteur de la santé ?", "Environ 4 à 5 %",
        ["Moins de 0,1 %", "Environ 25 %", "Environ 50 %"]),
    multi(2, "Quels sont des co-bénéfices santé-environnement ?", ["Aller travailler à vélo", "Manger plus végétal"],
          ["Climatiser davantage", "Utiliser plus de matériel jetable"]),
    qcm(2, "D'où vient la plus grande part de l'empreinte carbone des soins de santé ?",
        "Des émissions indirectes : achats, médicaments, matériel, déplacements (scope 3)",
        ["Uniquement du chauffage des hôpitaux", "Des ambulances seules", "Des ordinateurs"]),
    vf(2, "Dire « c'est trop tard, on ne peut plus rien faire » est un discours de l'inaction.", True, "C'est la capitulation."),
    num(2, _q_co2),
    qcm(3, "Pendant une vague de chaleur, quels patients de kiné sont les plus à risque ?",
        "Les personnes âgées, polymédiquées ou atteintes de maladies cardiaques ou respiratoires",
        ["Les jeunes sportifs", "Personne en particulier", "Uniquement les enfants"]),
    qcm(3, "Pourquoi peut-on dire qu'un soin efficace est aussi un soin durable ?",
        "Il évite des séances, des déplacements et du matériel inutiles", ["Parce qu'il est plus cher",
        "Parce qu'il utilise plus d'appareils", "Ce n'est pas lié"]),
    qcm(3, "Que dit la théorie du Donut sur un pays qui satisfait tous les besoins sociaux mais dépasse les limites "
        "planétaires ?", "Il n'est pas dans l'espace juste et sûr : il dépasse le plafond écologique",
        ["Il est un modèle à suivre", "Il est sous le plancher social", "La théorie ne s'applique pas aux pays"]),
    qcm(3, "Une étudiante dit être paralysée par l'éco-anxiété. Quelle piste est la plus soutenue ?",
        "S'engager dans des actions concrètes, idéalement collectives", ["Ne plus jamais s'informer",
        "Considérer qu'il est trop tard", "Attendre que la technologie règle tout"]),
]

CARDS = [
    ("Rapport Brundtland (1987)", "Répondre aux besoins du présent sans compromettre ceux des générations futures"),
    ("Limites planétaires", "9 seuils (Rockström, 2009) ; 7 dépassées en 2025"),
    ("Théorie du Donut", "Entre plancher social et plafond écologique (Raworth)"),
    ("ODD", "17 objectifs de l'ONU (2015-2030), santé = ODD 3"),
    ("One Health", "Santé humaine, animale et des écosystèmes liées"),
    ("Empreinte du secteur santé", "≈ 4-5 % des émissions mondiales, surtout scope 3"),
    ("4 familles de discours de l'inaction", "Rediriger, solutions non transformatrices, inconvénients, capituler"),
    ("Co-bénéfice", "Bon pour la santé et pour l'environnement"),
]

VIDEOS = [
    ("Les limites planétaires expliquées", "limites planétaires explication"),
    ("La théorie du Donut de Kate Raworth", "théorie du donut Kate Raworth"),
    ("Changement climatique et santé", "changement climatique santé effets"),
    ("Les discours de l'inaction climatique", "discours de l'inaction climatique Lamb"),
]

LINKS = [
    ("Stockholm Resilience Centre : limites planétaires", "https://www.stockholmresilience.org/research/planetary-boundaries.html"),
    ("The Shift Project : décarboner la santé", "https://theshiftproject.org/"),
]
