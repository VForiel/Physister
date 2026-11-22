"""LKNR1210 Evidence based practice (EBP) / Raisonnement clinique 2."""

import math

import plotly.graph_objects as go
import streamlit as st

from app import ui
from app.course import Course
from app.quiz import gen_qcm, multi, num, qcm, table_qcm, vf

COURSE = Course(
    code="LKNR1210", title="Evidence based practice / Raisonnement clinique 2", short="EBP et raisonnement 2",
    bloc=2, quad=2, credits=2, hours="15 h + 15 h", icon=":material/query_stats:",
    intro="La suite d'EBP 1, plus quantitative : que valent vraiment nos tests cliniques et nos questionnaires "
          "(sensibilité, spécificité, rapports de vraisemblance, fiabilité), comment fixer des objectifs, et comment "
          "juger la qualité des preuves.",
    acquis=[
        "Connaître la construction, la validation et les limites des questionnaires.",
        "Comprendre les principes des tests cliniques et leurs qualités psychométriques.",
        "Intégrer anamnèse et examen ; établir un pronostic ; structurer la prise en charge.",
        "Formuler une question de recherche et utiliser les outils de hiérarchisation des preuves.",
        "Argumenter un raisonnement clinique sur vignettes.",
    ],
)

TERMS = {
    "sensibilité": ("Sensibilité (Se)", "Proportion de malades que le test détecte (test positif chez les malades).",
                    "Sensibilité et spécificité"),
    "spécificité": ("Spécificité (Sp)", "Proportion de non-malades que le test classe négatifs.", "Sensibilité et spécificité"),
    "rapport de vraisemblance": ("Rapport de vraisemblance (LR)", "LR+ = Se/(1−Sp) : combien un test positif augmente "
                                 "la probabilité de la maladie. LR− = (1−Se)/Sp : combien un test négatif la diminue.",
                                 "Rapport de vraisemblance"),
    "probabilité pré-test": ("Probabilité pré-test", "Probabilité que le patient ait la maladie avant le test (selon "
                             "la prévalence et l'anamnèse).", None),
    "snnout": ("SnNout", "Sensitive test, Negative result, rule OUT : un test très sensible et négatif exclut la "
               "maladie.", None),
    "sppin": ("SpPin", "Specific test, Positive result, rule IN : un test très spécifique et positif confirme la "
              "maladie.", None),
    "icc": ("ICC", "Coefficient de corrélation intraclasse : fiabilité d'une mesure continue (0 à 1 ; > 0,75 bon, "
            "> 0,90 excellent).", "Corrélation intraclasse"),
    "kappa": ("Kappa de Cohen", "Accord entre deux évaluateurs pour une variable catégorielle, corrigé du hasard "
              "(> 0,60 bon, > 0,80 excellent).", "Kappa de Cohen"),
    "sem": ("Erreur standard de mesure (SEM)", "Erreur de mesure typique d'un instrument, dans son unité.", None),
    "mdc": ("Changement minimal détectable (MDC)", "Plus petit changement qui dépasse l'erreur de mesure : "
            "MDC₉₅ = 1,96 × √2 × SEM.", None),
    "mcid": ("Différence minimale cliniquement importante (MCID)", "Plus petit changement que le patient perçoit comme "
             "important.", None),
    "smart": ("Objectif SMART", "Spécifique, Mesurable, Atteignable, Réaliste (pertinent), Temporellement défini.",
              "Objectifs SMART"),
    "échelle pedro": ("Échelle PEDro", "Grille de 11 critères (score sur 10) qui évalue la qualité méthodologique d'un "
                      "essai contrôlé randomisé.", None),
    "grade": ("GRADE", "Méthode pour coter la certitude d'un ensemble de preuves (élevée, modérée, faible, très faible).",
              "GRADE (médecine)"),
}


def ch_tests():
    ui.md(r"""
Un test clinique classe les patients en positif ou négatif. On le compare à une **référence** (le « gold
standard » : IRM, arthroscopie…) dans un **tableau 2 × 2**.

|  | Malade | Pas malade |
|---|---|---|
| **Test +** | vrais positifs (VP) | faux positifs (FP) |
| **Test −** | faux négatifs (FN) | vrais négatifs (VN) |

- [[sensibilité|Sensibilité]] = VP / (VP + FN) : parmi les malades, combien sont détectés ?
- [[spécificité|Spécificité]] = VN / (VN + FP) : parmi les non-malades, combien sont classés négatifs ?
- [[rapport de vraisemblance|LR+]] = Se / (1 − Sp) et LR− = (1 − Se) / Sp.

Un LR+ > 10 ou un LR− < 0,1 change beaucoup la probabilité ; un LR proche de 1 ne sert à rien.
""")
    ui.memo("[[snnout|**SnNout**]] : un test **S**e**n**sible et **N**égatif exclut (**out**). [[sppin|**SpPin**]] : un "
            "test **Sp**écifique et **P**ositif confirme (**in**). Pour éliminer, choisis un test sensible ; pour "
            "confirmer, un test spécifique.")
    st.markdown("#### À toi : calcule les qualités d'un test")
    c1, c2, c3, c4 = st.columns(4)
    vp = c1.number_input("VP", 0, 1000, 45, key="e2_vp")
    fp = c2.number_input("FP", 0, 1000, 10, key="e2_fp")
    fn = c3.number_input("FN", 0, 1000, 5, key="e2_fn")
    vn = c4.number_input("VN", 0, 1000, 90, key="e2_vn")
    se = vp / (vp + fn) if vp + fn else 0
    sp = vn / (vn + fp) if vn + fp else 0
    lrp = se / (1 - sp) if sp < 1 else math.inf
    lrn = (1 - se) / sp if sp else math.inf
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Sensibilité", f"{se:.0%}")
    k2.metric("Spécificité", f"{sp:.0%}")
    k3.metric("LR+", "∞" if math.isinf(lrp) else f"{lrp:.1f}")
    k4.metric("LR−", "∞" if math.isinf(lrn) else f"{lrn:.2f}")


def ch_bayes():
    ui.md(r"""
**Du pré-test au post-test.** Le résultat d'un test ne s'interprète pas seul : il **modifie** une probabilité de
départ (la [[probabilité pré-test]], qui vient de la prévalence et de l'anamnèse). On passe par les **cotes**
(odds) :

$$\text{cote pré} = \frac{p}{1-p} \qquad \text{cote post} = \text{cote pré} \times LR \qquad p_{post} = \frac{\text{cote post}}{1 + \text{cote post}}$$

C'est ce que fait le **nomogramme de Fagan**.
""")
    st.markdown("#### À toi : le nomogramme de Fagan en direct")
    c1, c2 = st.columns([1, 2])
    with c1:
        pre = st.slider("Probabilité pré-test (%)", 1, 99, 30, key="e2_pre") / 100
        lrp = st.number_input("LR+ du test", 0.1, 100.0, 8.0, 0.5, key="e2_lrp")
        lrn = st.number_input("LR− du test", 0.01, 1.0, 0.15, 0.01, key="e2_lrn")

    def post(p, lr):
        o = p / (1 - p) * lr
        return o / (1 + o)

    pp, pn = post(pre, lrp), post(pre, lrn)
    with c2:
        k1, k2 = st.columns(2)
        k1.metric("Si le test est positif", f"{pp:.0%}", delta=f"{(pp - pre) * 100:+.0f} points")
        k2.metric("Si le test est négatif", f"{pn:.0%}", delta=f"{(pn - pre) * 100:+.0f} points")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[0, 1], y=[pre * 100, pp * 100], mode="lines+markers", name="Test positif"))
        fig.add_trace(go.Scatter(x=[0, 1], y=[pre * 100, pn * 100], mode="lines+markers", name="Test négatif"))
        fig.update_layout(height=250, margin=dict(l=10, r=10, t=10, b=10), yaxis_title="Probabilité (%)",
                          xaxis=dict(tickvals=[0, 1], ticktext=["avant le test", "après le test"]), yaxis_range=[0, 100],
                          legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig, width="stretch")
    ui.tip("Essaie une probabilité pré-test de 2 % (patient sans facteur de risque) : même un bon test positif ne "
           "rend pas la maladie très probable. D'où l'importance de l'**anamnèse**, qui fixe la probabilité de départ.")
    ui.md(r"""
**Les clusters de tests** : un seul test est rarement suffisant. Combiner plusieurs tests (ou un test + des
éléments d'anamnèse) dans une **règle de prédiction clinique** améliore le diagnostic (comme les règles d'Ottawa).
""")


def ch_psychometrie():
    ui.md(r"""
**Les qualités d'un outil de mesure** (test, questionnaire, goniomètre…)

- **Fiabilité** : le résultat est-il reproductible ? **Intra-évaluateur** (même kiné, deux fois) et
  **inter-évaluateurs** (deux kinés). Mesurée par l'[[icc|ICC]] (variables continues) ou le [[kappa|kappa]]
  (catégorielles).
- **Validité** : mesure-t-il ce qu'il prétend mesurer ? Validité de **contenu** (couvre tout le concept), de
  **critère** (concorde avec la référence), de **construit** (se comporte comme la théorie le prévoit).
- **Sensibilité au changement** (responsiveness) : détecte-t-il une amélioration réelle ?
- **Interprétabilité** : le [[sem|SEM]], le [[mdc|MDC]] et le [[mcid|MCID]].

$$\text{MDC}_{95} = 1{,}96 \times \sqrt{2} \times \text{SEM}$$
""")
    st.markdown("#### À toi : le patient a-t-il vraiment progressé ?")
    c1, c2 = st.columns([1, 2])
    with c1:
        sem = st.number_input("SEM du goniomètre pour ce mouvement (°)", 0.5, 10.0, 3.0, 0.5, key="e2_sem")
        gain = st.number_input("Gain mesuré entre deux séances (°)", 0.0, 60.0, 6.0, 0.5, key="e2_gain")
    mdc = 1.96 * math.sqrt(2) * sem
    with c2:
        st.metric("MDC₉₅", f"{mdc:.1f}°")
        if gain > mdc:
            st.success(f"Le gain de {gain}° dépasse le MDC : c'est un vrai changement (au-delà de l'erreur de mesure).")
        else:
            st.warning(f"Le gain de {gain}° reste sous le MDC : il peut s'expliquer par l'erreur de mesure.")
    ui.md(r"""
**Les questionnaires** (KOOS, Oswestry, DASH, Tampa…) : on les **construit** à partir du vécu des patients et des
experts, on les **valide** (fiabilité, validité, sensibilité au changement), on les **traduit** avec une
adaptation transculturelle. Limites : compréhension, désirabilité sociale, effet plafond ou plancher.
""")


def ch_objectifs():
    ui.md(r"""
**Fixer des objectifs** avec le patient, idéalement [[smart|SMART]] :

- **S**pécifique : « monter les escaliers de chez moi » plutôt que « aller mieux » ;
- **M**esurable : « 14 marches sans s'arrêter, avec la rampe » ;
- **A**tteignable et **R**éaliste : compte tenu de la pathologie et du pronostic ;
- **T**emporellement défini : « dans 6 semaines ».

Ils s'inscrivent dans la [[cif|CIF]] : objectifs de **participation** (ce qui compte pour lui), traduits en
objectifs d'**activité** et de **fonction** pour le traitement.

**La hiérarchie des preuves** (du plus fort au plus faible, pour une question d'efficacité) : revues systématiques
d'essais contrôlés randomisés > essais contrôlés randomisés > études de cohorte > études cas-témoins > séries de
cas > avis d'experts. Mais la **qualité** compte autant que le type :
- l'[[échelle pedro|échelle PEDro]] note un essai sur 10 (randomisation, assignation secrète, groupes comparables,
  aveugles, suivi, analyse en intention de traiter…) ;
- [[grade|GRADE]] note la certitude d'un ensemble de preuves.
""")
    ui.warn("Un essai randomisé mal fait (pas d'aveugle, 40 % de perdus de vue) peut être moins fiable qu'une "
            "bonne étude de cohorte. Regarde toujours la qualité, pas seulement le type d'étude.")


CHAPTERS = [
    ("Qualités d'un test diagnostique", ch_tests),
    ("Probabilités pré- et post-test", ch_bayes),
    ("Fiabilité, validité, MDC", ch_psychometrie),
    ("Objectifs et niveaux de preuve", ch_objectifs),
]


def _q_se(rng):
    vp, fn = rng.choice([(40, 10), (45, 5), (30, 20), (90, 10)])
    return dict(prompt=f"Parmi les malades, le test est positif chez {vp} et négatif chez {fn}. Quelle est sa sensibilité (%) ?",
                answer=vp / (vp + fn) * 100, unit="%", tol=0.01, why=f"Se = VP/(VP+FN) = {vp}/{vp + fn}.")


def _q_sp(rng):
    vn, fp = rng.choice([(80, 20), (90, 10), (70, 30), (95, 5)])
    return dict(prompt=f"Parmi les non-malades, le test est négatif chez {vn} et positif chez {fp}. Quelle est sa spécificité (%) ?",
                answer=vn / (vn + fp) * 100, unit="%", tol=0.01, why=f"Sp = VN/(VN+FP) = {vn}/{vn + fp}.")


def _q_lr(rng):
    se, sp = rng.choice([(0.9, 0.8), (0.8, 0.9), (0.85, 0.95), (0.95, 0.6)])
    return dict(prompt=f"Un test a une sensibilité de {se:.0%} et une spécificité de {sp:.0%}. Calcule son LR+.",
                answer=se / (1 - sp), tol=0.02, why=f"LR+ = Se/(1−Sp) = {se}/{1 - sp:.2f} = {se / (1 - sp):.1f}.")


def _q_post(rng):
    pre = rng.choice([0.1, 0.2, 0.3, 0.5])
    lr = rng.choice([2, 5, 10])
    o = pre / (1 - pre) * lr
    return dict(prompt=f"Probabilité pré-test {pre:.0%}, test positif avec LR+ = {lr}. Quelle est la probabilité post-test (%) ?",
                answer=o / (1 + o) * 100, unit="%", tol=0.03,
                why=f"Cote pré = {pre / (1 - pre):.2f} ; cote post = {o:.2f} ; p = {o / (1 + o):.0%}.")


def _q_mdc(rng):
    sem = rng.choice([1, 2, 3, 4, 5])
    return dict(prompt=f"La SEM d'une mesure vaut {sem}. Calcule le MDC₉₅ (1,96 × √2 × SEM).",
                answer=1.96 * math.sqrt(2) * sem, tol=0.02, why=f"1,96 × 1,414 × {sem} ≈ {1.96 * math.sqrt(2) * sem:.1f}.")


SMART = {"S": "Spécifique", "M": "Mesurable", "A": "Atteignable", "R": "Réaliste", "T": "Temporellement défini"}

QUESTIONS = [
    qcm(1, "La sensibilité d'un test est…", "la proportion de malades détectés (VP / (VP + FN))",
        ["la proportion de non-malades classés négatifs", "la probabilité d'être malade si le test est positif", "VP / (VP + FP)"]),
    qcm(1, "Que veut dire SnNout ?", "Un test très sensible et négatif permet d'exclure la maladie",
        ["Un test spécifique et négatif confirme la maladie", "Un test sensible et positif confirme",
         "Un test négatif ne sert à rien"]),
    table_qcm(1, SMART, "Dans un objectif SMART, que signifie la lettre **{k}** ?"),
    vf(1, "Le kappa sert à mesurer l'accord entre évaluateurs pour une variable catégorielle.", True),
    num(1, _q_se),
    num(2, _q_sp),
    num(2, _q_lr),
    qcm(2, "Un LR+ de 1 signifie que le test…", "ne change pas la probabilité de la maladie", ["confirme la maladie",
        "exclut la maladie", "est parfait"]),
    multi(2, "Quels critères évalue l'échelle PEDro ?", ["Randomisation", "Assignation secrète", "Évaluateurs en aveugle"],
          ["Nombre d'auteurs", "Prestige de la revue"]),
    qcm(2, "Qu'est-ce que le MDC ?", "Le plus petit changement qui dépasse l'erreur de mesure",
        ["Le changement que le patient juge important", "La valeur maximale du test", "La moyenne des mesures"]),
    num(3, _q_post),
    num(3, _q_mdc),
    qcm(3, "Pour exclure une rupture du LCA, quel test choisir en priorité ?", "Un test très sensible (SnNout)",
        ["Un test très spécifique", "N'importe lequel", "Un test avec LR+ = 1"]),
    qcm(3, "Pourquoi un même test positif n'a-t-il pas la même valeur chez un sportif après un pivot et chez un "
        "patient sans traumatisme ?", "Parce que la probabilité pré-test est très différente",
        ["Parce que le LR change selon le patient", "Parce que la sensibilité dépend de l'âge", "Ce n'est pas vrai"]),
    qcm(3, "Un patient gagne 4° de flexion ; le MDC₉₅ du goniomètre est de 8°. Conclusion ?",
        "Ce gain peut être dû à l'erreur de mesure", ["C'est un progrès certain", "Le goniomètre est cassé",
        "Il faut arrêter le traitement"]),
    qcm(3, "Lequel de ces objectifs est SMART ?", "Marcher 500 m sans aide jusqu'à la boulangerie d'ici 4 semaines",
        ["Aller mieux", "Avoir moins mal au genou", "Faire beaucoup d'exercices"]),
]

CARDS = [
    ("Sensibilité", "VP / (VP + FN)"),
    ("Spécificité", "VN / (VN + FP)"),
    ("LR+", "Se / (1 − Sp)"),
    ("LR−", "(1 − Se) / Sp"),
    ("SnNout", "Sensible + négatif = exclut"),
    ("SpPin", "Spécifique + positif = confirme"),
    ("Cote post-test", "Cote pré-test × LR"),
    ("ICC", "Fiabilité, variable continue (> 0,75 bon)"),
    ("Kappa", "Accord inter-évaluateurs, catégoriel (> 0,60 bon)"),
    ("MDC₉₅", "1,96 × √2 × SEM"),
    ("MCID", "Plus petit changement important pour le patient"),
    ("SMART", "Spécifique, Mesurable, Atteignable, Réaliste, Temporel"),
    ("Échelle PEDro", "Qualité d'un ECR, score sur 10"),
    ("GRADE", "Certitude d'un ensemble de preuves"),
]

VIDEOS = [
    ("Sensibilité, spécificité, rapports de vraisemblance", "rapport de vraisemblance sensibilité spécificité explication"),
    ("Le nomogramme de Fagan", "nomogramme de Fagan explication"),
    ("Fiabilité : ICC et kappa", "ICC kappa fiabilité explication"),
    ("L'échelle PEDro", "PEDro scale explained"),
]

LINKS = [
    ("PEDro : l'échelle PEDro (FR)", "https://pedro.org.au/french/resources/pedro-scale/"),
    ("Calculateur de probabilité post-test (CEBM Oxford)", "https://www.cebm.ox.ac.uk/resources/ebm-tools"),
]
