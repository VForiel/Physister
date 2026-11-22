"""LFSM1101 Chimie générale et biomolécules."""

import math

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from app import ui
from app.course import Course
from app.quiz import gen_qcm, multi, num, qcm, table_qcm, vf

COURSE = Course(
    code="LFSM1101", title="Chimie générale et biomolécules", short="Chimie",
    bloc=1, quad=1, credits=4, hours="37,5 h", icon=":material/science:",
    intro="Le corps est une immense usine chimique : l'ATP qui fait bouger les muscles, le pH du sang que "
          "la respiration ajuste en permanence, les protéines qui forment tendons et ligaments. Ce cours "
          "donne les bases pour comprendre la physiologie de l'an prochain.",
    acquis=[
        "Maîtriser les notions essentielles de chimie générale et organique.",
        "Connaître la structure et les propriétés des principales biomolécules.",
        "Résoudre des exercices sur ces matières.",
    ],
)

TERMS = {
    "atome": ("Atome", "Plus petite partie d'un élément chimique : un noyau (protons + neutrons) entouré "
              "d'électrons.", "Atome"),
    "numéro atomique": ("Numéro atomique (Z)", "Nombre de protons du noyau. Il définit l'élément : Z = 6, c'est "
                        "toujours du carbone.", "Numéro atomique"),
    "isotope": ("Isotope", "Atomes d'un même élément (même Z) avec un nombre de neutrons différent, donc une masse "
                "différente. Ex. carbone 12 et carbone 14.", "Isotope"),
    "électronégativité": ("Électronégativité", "Tendance d'un atome à attirer vers lui les électrons d'une "
                          "liaison. O, N et F sont très électronégatifs.", "Électronégativité"),
    "liaison covalente": ("Liaison covalente", "Deux atomes partagent une paire d'électrons. Liaison forte, "
                          "typique des molécules organiques.", "Liaison covalente"),
    "liaison ionique": ("Liaison ionique", "Attraction électrique entre un ion positif et un ion négatif, après "
                        "transfert d'électrons (ex. Na⁺Cl⁻).", "Liaison ionique"),
    "liaison hydrogène": ("Liaison hydrogène", "Attraction faible entre un H lié à un atome électronégatif (O, N) "
                          "et un autre atome électronégatif. Elle tient l'eau liquide, la double hélice d'ADN, "
                          "la forme des protéines.", "Liaison hydrogène"),
    "mole": ("Mole", "Quantité de matière contenant 6,022 × 10²³ entités (nombre d'Avogadro).", "Mole (unité)"),
    "ph": ("pH", "Mesure de l'acidité : pH = −log[H₃O⁺]. 7 est neutre à 25 °C, en dessous c'est acide, "
           "au-dessus basique. Le sang est à 7,35–7,45.", "Potentiel hydrogène"),
    "tampon": ("Solution tampon", "Mélange d'un acide faible et de sa base conjuguée qui limite les variations de "
               "pH quand on ajoute un acide ou une base.", "Solution tampon"),
    "acidose": ("Acidose", "pH sanguin inférieur à 7,35.", "Acidose"),
    "alcalose": ("Alcalose", "pH sanguin supérieur à 7,45.", "Alcalose"),
    "acide aminé": ("Acide aminé", "Monomère des protéines : un carbone central portant un groupe amine (−NH₂), "
                    "un groupe carboxyle (−COOH), un H et une chaîne latérale R. Il y en a 20 dans nos protéines.",
                    "Acide aminé"),
    "liaison peptidique": ("Liaison peptidique", "Liaison covalente entre le −COOH d'un acide aminé et le −NH₂ du "
                           "suivant, avec libération d'une molécule d'eau (condensation).", "Liaison peptidique"),
    "triglycéride": ("Triglycéride", "Lipide de réserve : un glycérol estérifié par trois acides gras.",
                     "Triglycéride"),
    "phospholipide": ("Phospholipide", "Lipide à tête polaire (hydrophile) et deux queues d'acides gras "
                      "(hydrophobes). Il forme la bicouche des membranes cellulaires.", "Phospholipide"),
    "nucléotide": ("Nucléotide", "Monomère des acides nucléiques : un sucre (ribose ou désoxyribose), un phosphate "
                   "et une base azotée.", "Nucléotide"),
    "hydrolyse": ("Hydrolyse", "Coupure d'une liaison par ajout d'une molécule d'eau. C'est l'inverse de la "
                  "condensation.", "Hydrolyse"),
    "oxydoréduction": ("Oxydoréduction", "Réaction où des électrons passent d'une espèce (qui s'oxyde) à une "
                       "autre (qui se réduit). Toute la respiration cellulaire repose dessus.", "Oxydoréduction"),
    "enzyme": ("Enzyme", "Protéine qui accélère une réaction chimique (catalyseur) sans être consommée.", "Enzyme"),
}

ELEMENTS = [  # symbole, nom, Z, masse molaire, électrons de valence
    ("H", "hydrogène", 1, 1.0, 1), ("C", "carbone", 6, 12.0, 4), ("N", "azote", 7, 14.0, 5),
    ("O", "oxygène", 8, 16.0, 6), ("Na", "sodium", 11, 23.0, 1), ("Mg", "magnésium", 12, 24.3, 2),
    ("P", "phosphore", 15, 31.0, 5), ("S", "soufre", 16, 32.1, 6), ("Cl", "chlore", 17, 35.5, 7),
    ("K", "potassium", 19, 39.1, 1), ("Ca", "calcium", 20, 40.1, 2), ("Fe", "fer", 26, 55.8, 2),
]


def ch_atomes():
    ui.md(r"""
Un [[atome]] est fait d'un **noyau** minuscule (protons positifs et neutrons neutres) et d'**électrons**
négatifs qui l'entourent. Deux nombres le décrivent :

- **Z**, le [[numéro atomique]] : le nombre de protons. C'est l'identité de l'élément.
- **A**, le nombre de masse : protons + neutrons. Le nombre de neutrons vaut donc $A - Z$.

Un atome neutre a autant d'électrons que de protons. S'il en perd, il devient un **cation** (positif,
comme Na⁺, K⁺, Ca²⁺) ; s'il en gagne, un **anion** (négatif, comme Cl⁻). Les [[isotope|isotopes]] ont le
même Z mais pas le même A.

Les électrons se rangent en **couches**. Ceux de la dernière couche, les **électrons de valence**, décident
de la chimie de l'atome. Les atomes cherchent à avoir **8 électrons** sur leur couche externe (règle de
l'octet ; 2 pour l'hydrogène). D'où :

| Élément | Électrons de valence | Liaisons habituelles | Ion habituel |
|---|---|---|---|
| H | 1 | 1 | H⁺ |
| C | 4 | 4 | (aucun) |
| N | 5 | 3 | |
| O | 6 | 2 | |
| Na, K | 1 | | Na⁺, K⁺ |
| Ca, Mg | 2 | | Ca²⁺, Mg²⁺ |
| Cl | 7 | 1 | Cl⁻ |
""")
    ui.memo("**HONC 1234** : l'**H**ydrogène fait 1 liaison, l'**O**xygène 2, l'azote (**N**) 3, le "
            "**C**arbone 4. Avec ça tu peux dessiner presque toutes les molécules du vivant.")
    st.markdown("#### À toi : décode un élément")
    el = st.selectbox("Élément", ELEMENTS, format_func=lambda e: f"{e[0]} ({e[1]})", key="ch_el")
    sym, name, z, mm, val = el
    a = round(mm)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Protons (Z)", z)
    c2.metric("Neutrons (≈ A − Z)", a - z)
    c3.metric("Électrons de valence", val)
    c4.metric("Masse molaire", f"{mm:g} g/mol")
    ui.clinic("Na⁺, K⁺, Ca²⁺ et Cl⁻ sont les ions des **électrolytes**. Leur répartition de part et d'autre de la "
              "membrane crée le potentiel électrique des neurones et des muscles (tu le verras en bloc 2). "
              "Une hypokaliémie (K⁺ trop bas) donne crampes, faiblesse, troubles du rythme cardiaque.")


def ch_liaisons():
    ui.md(r"""
Les atomes se lient pour compléter leur couche externe.

- **[[liaison covalente|Covalente]]** : partage d'électrons. Si les deux atomes ont la même
  [[électronégativité]] (C–C, C–H), le partage est équitable : liaison **apolaire**. Si l'un attire plus
  (O–H, N–H), il porte une charge partielle négative δ⁻ : liaison **polaire**.
- **[[liaison ionique|Ionique]]** : un atome arrache carrément l'électron de l'autre (Na⁺ Cl⁻).
- **[[liaison hydrogène|Hydrogène]]** : attraction faible entre un H polarisé δ⁺ et un O ou N δ⁻ voisin.
  Faible une à une, mais très nombreuses : elles donnent leur forme aux protéines et à l'ADN.
- **Interactions hydrophobes** : les parties apolaires se regroupent pour fuir l'eau. C'est ce qui forme
  les membranes.

**L'eau, molécule de la vie.** L'oxygène est très électronégatif et la molécule est coudée (104,5°) : l'eau
est **polaire**. Conséquences : elle dissout les ions et les molécules polaires (**hydrophiles**), mais pas
les graisses (**hydrophobes**) ; elle a une grande capacité thermique (elle amortit les variations de
température, et la sueur refroidit en s'évaporant).
""")
    ui.memo("**« Qui se ressemble s'assemble »** : polaire dissout polaire, apolaire dissout apolaire. "
            "Le sel dans l'eau oui, l'huile dans l'eau non.")
    ui.md(r"""
**Les réactions.** Une équation chimique doit être **équilibrée** : autant d'atomes de chaque élément à gauche
et à droite (rien ne se perd, rien ne se crée). Exemple : la combustion complète du glucose, bilan de la
respiration cellulaire :

$$\mathrm{C_6H_{12}O_6 + 6\,O_2 \longrightarrow 6\,CO_2 + 6\,H_2O} \quad (+\ \text{énergie})$$

**La [[mole]]** compte les molécules par paquets de $6{,}022\times10^{23}$. La **masse molaire** *M* (g/mol) est
la masse d'une mole : $n = \dfrac{m}{M}$. La **concentration molaire** est $C = \dfrac{n}{V}$ (mol/L).
""")
    st.markdown("#### À toi : calcul de quantités")
    c1, c2 = st.columns(2)
    with c1:
        mol = st.selectbox("Molécule", ["glucose C₆H₁₂O₆ (180 g/mol)", "NaCl (58,5 g/mol)", "eau H₂O (18 g/mol)",
                                        "CO₂ (44 g/mol)"], key="ch_mol")
        M = {"glucose": 180, "NaCl": 58.5, "eau": 18, "CO₂": 44}[mol.split()[0]]
        m = st.number_input("Masse (g)", 0.1, 1000.0, 9.0, key="ch_masse")
        v = st.number_input("Volume de solution (L)", 0.01, 10.0, 1.0, key="ch_vol")
    with c2:
        n = m / M
        st.metric("Quantité de matière n = m/M", f"{n:.4g} mol")
        st.metric("Concentration C = n/V", f"{n / v:.4g} mol/L")
        st.metric("Nombre de molécules", f"{n * 6.022e23:.3g}")
    ui.tip("Le sérum physiologique contient 9 g de NaCl par litre : environ 0,154 mol/L. "
           "Essaie avec les curseurs !")


def ch_ph():
    ui.md(r"""
Un **acide** libère des ions H⁺ (ou plutôt H₃O⁺ dans l'eau), une **base** les capte. Le [[ph|pH]] mesure
leur concentration sur une échelle logarithmique :

$$\mathrm{pH} = -\log_{10}[\mathrm{H_3O^+}]$$

Une unité de pH en moins, c'est **10 fois** plus d'ions H₃O⁺. Le sang est à **7,40 ± 0,05** : c'est
très serré, et l'organisme y tient absolument. En dessous de 7,35 on parle d'[[acidose]], au-dessus de 7,45
d'[[alcalose]].

**Acide fort ou faible ?** Un acide fort (HCl) se dissocie complètement. Un acide faible (acide carbonique,
acide lactique) se dissocie partiellement, selon sa constante $K_a$ ; on utilise $\mathrm{p}K_a = -\log K_a$.

**Les [[tampon|tampons]]** mélangent un acide faible et sa base conjuguée. Si on ajoute de l'acide, la base
le capte ; si on ajoute une base, l'acide la neutralise. Le pH bouge peu. Leur pH suit l'équation
d'**Henderson-Hasselbalch** :

$$\mathrm{pH} = \mathrm{p}K_a + \log\frac{[\text{base}]}{[\text{acide}]}$$

Le tampon principal du sang est le couple **bicarbonate / acide carbonique** :

$$\mathrm{CO_2 + H_2O \rightleftharpoons H_2CO_3 \rightleftharpoons H^+ + HCO_3^-}$$

Son grand avantage : les **poumons** règlent le CO₂ (en quelques minutes) et les **reins** règlent le HCO₃⁻
(en quelques jours).
""")
    st.markdown("#### À toi : le pH du sang")
    st.caption("pH = 6,1 + log( [HCO₃⁻] / (0,03 × PaCO₂) ). Valeurs normales : HCO₃⁻ = 24 mmol/L, PaCO₂ = 40 mmHg.")
    c1, c2 = st.columns([1, 2])
    with c1:
        hco3 = st.slider("Bicarbonates [HCO₃⁻] (mmol/L)", 10.0, 40.0, 24.0, 0.5, key="ch_hco3")
        paco2 = st.slider("PaCO₂ (mmHg)", 20.0, 80.0, 40.0, 1.0, key="ch_paco2")
    ph = 6.1 + math.log10(hco3 / (0.03 * paco2))
    with c2:
        st.metric("pH sanguin", f"{ph:.2f}")
        if ph < 7.35:
            cause = "respiratoire (trop de CO₂)" if paco2 > 45 else "métabolique (pas assez de bicarbonates)"
            st.error(f"Acidose {cause}.")
        elif ph > 7.45:
            cause = "respiratoire (trop peu de CO₂)" if paco2 < 35 else "métabolique (trop de bicarbonates)"
            st.warning(f"Alcalose {cause}.")
        else:
            st.success("pH normal.")
        xs = np.linspace(20, 80, 100)
        fig = go.Figure(go.Scatter(x=xs, y=6.1 + np.log10(hco3 / (0.03 * xs)), name="pH"))
        fig.add_hrect(y0=7.35, y1=7.45, fillcolor="green", opacity=0.12, line_width=0)
        fig.add_trace(go.Scatter(x=[paco2], y=[ph], mode="markers", marker=dict(size=12), name="Ton patient"))
        fig.update_layout(height=280, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="PaCO₂ (mmHg)",
                          yaxis_title="pH", showlegend=False)
        st.plotly_chart(fig, width="stretch")
    ui.clinic("Un patient BPCO qui ventile mal garde son CO₂ : **acidose respiratoire**. Ses reins compensent "
              "lentement en retenant des bicarbonates. À l'inverse, une crise d'angoisse avec hyperventilation "
              "fait chuter le CO₂ : **alcalose respiratoire** (fourmillements autour de la bouche, vertiges).")
    ui.warn("Le pH est un logarithme : passer de 7,4 à 7,1 n'est pas « un petit peu » plus acide. "
            "C'est deux fois plus d'ions H⁺ (10^0,3 ≈ 2).")


def ch_organique():
    ui.md(r"""
La chimie **organique** est la chimie du **carbone**. Avec ses 4 liaisons, il forme des chaînes, des
ramifications, des cycles : un squelette sur lequel se greffent des **groupements fonctionnels** qui donnent
ses propriétés à la molécule.

| Groupement | Formule | Nom de la fonction | Où on le trouve |
|---|---|---|---|
| Hydroxyle | −OH | alcool | sucres, glycérol |
| Carbonyle | C=O | aldéhyde (en bout) ou cétone (au milieu) | glucose (aldéhyde), fructose (cétone) |
| Carboxyle | −COOH | acide carboxylique | acides gras, acides aminés, acide lactique |
| Amine | −NH₂ | amine | acides aminés |
| Phosphate | −OPO₃²⁻ | ester phosphorique | [[atp|ATP]], ADN, phospholipides |
| Ester | −COO− | ester | triglycérides |
""")
    ui.md(r"""
Deux réactions reviennent partout dans le vivant :

- **Condensation** (ou déshydratation) : on relie deux petites molécules en retirant une molécule d'eau. C'est
  ainsi qu'on construit les macromolécules.
- **[[hydrolyse|Hydrolyse]]** : on casse la liaison en ajoutant une molécule d'eau. C'est la digestion, ou
  l'utilisation de l'ATP : $\mathrm{ATP + H_2O \rightarrow ADP + P_i}$ + énergie.

Et une troisième, essentielle pour l'énergie : l'**[[oxydoréduction]]**. Quand on « brûle » le glucose, ses
électrons passent de molécule en molécule jusqu'à l'oxygène, et l'énergie libérée sert à fabriquer de l'ATP.
""")
    ui.memo("**OIL RIG** (en anglais) : **O**xidation **I**s **L**oss, **R**eduction **I**s **G**ain (d'électrons). "
            "En français : celui qui s'**o**xyde **o**ffre ses électrons.")


def ch_biomolecules():
    ui.md(r"""
Quatre grandes familles de macromolécules, chacune construite à partir de petites briques (**monomères**) :

| Famille | Monomère | Liaison | Rôles |
|---|---|---|---|
| **Glucides** | oses (glucose, fructose…) | glycosidique | énergie rapide (glucose), réserve (glycogène dans le foie et les muscles), structure (cellulose chez les plantes) |
| **Lipides** | acides gras + glycérol (pas de vrai polymère) | ester | réserve d'énergie ([[triglycéride|triglycérides]]), membranes ([[phospholipide|phospholipides]], cholestérol), hormones stéroïdes |
| **Protéines** | [[acide aminé|acides aminés]] (20) | [[liaison peptidique|peptidique]] | structure (collagène, kératine), mouvement (actine, myosine), [[enzyme|enzymes]], transport (hémoglobine), défense (anticorps) |
| **Acides nucléiques** | [[nucléotide|nucléotides]] | phosphodiester | information génétique (ADN), expression des gènes (ARN), énergie (ATP est un nucléotide) |
""")
    st.markdown("#### Les quatre niveaux de structure d'une protéine")
    ui.md(r"""
1. **Primaire** : la séquence des acides aminés (liaisons peptidiques).
2. **Secondaire** : repliements locaux, hélices α et feuillets β, tenus par des [[liaison hydrogène|liaisons hydrogène]].
3. **Tertiaire** : la forme 3D complète d'une chaîne (ponts disulfure, interactions hydrophobes…).
4. **Quaternaire** : l'assemblage de plusieurs chaînes (l'hémoglobine en a 4, le collagène est une triple hélice).

La **forme fait la fonction**. Une protéine chauffée ou mise dans un pH extrême se **dénature** : elle perd sa
forme 3D (pas sa séquence) et ne fonctionne plus. C'est l'œuf qui cuit.
""")
    ui.md(r"""
**Saturé ou insaturé ?** Un acide gras **saturé** n'a que des liaisons simples : chaîne droite, les molécules
s'empilent bien, solide à température ambiante (beurre). Un acide gras **insaturé** a une ou plusieurs doubles
liaisons qui font des coudes : liquide (huile d'olive). Les phospholipides insaturés rendent la membrane plus fluide.
""")
    ui.clinic("Le **collagène** (type I dans les tendons, ligaments, os ; type II dans le cartilage) est la "
              "protéine la plus abondante du corps. Sa triple hélice résiste énormément à la traction mais se "
              "renouvelle lentement : c'est pour ça qu'un tendon met des mois à cicatriser.")
    ui.memo("**ADN** : A–T et C–G (« **A**lice **T**ravaille, **C**harlotte **G**lande »). Dans l'**ARN**, le T est "
            "remplacé par U (uracile).")


CHAPTERS = [
    ("Atomes et éléments", ch_atomes),
    ("Liaisons, eau et réactions", ch_liaisons),
    ("Acides, bases et pH", ch_ph),
    ("Chimie du carbone", ch_organique),
    ("Biomolécules", ch_biomolecules),
]


def _q_ph(rng):
    exp = rng.choice([2, 3, 4, 5, 6, 8, 9])
    mant = rng.choice([1, 2, 5])
    c = mant * 10 ** -exp
    ph = -math.log10(c)
    return dict(prompt=f"Une solution a une concentration [H₃O⁺] = {mant} × 10⁻{exp} mol/L. Quel est son pH ?",
                answer=ph, tol=0.01, why=f"pH = −log({mant} × 10⁻{exp}) = {exp} − log {mant} ≈ {ph:.2f}.")


def _q_mol(rng):
    name, M = rng.choice([("glucose (180 g/mol)", 180), ("NaCl (58,5 g/mol)", 58.5), ("eau (18 g/mol)", 18)])
    m = rng.choice([9, 18, 36, 90, 117])
    return dict(prompt=f"Combien de moles y a-t-il dans {m} g de {name} ?", answer=m / M, unit="mol",
                why=f"n = m / M = {m} / {M} ≈ {m / M:.3g} mol.")


def _q_conc(rng):
    m = rng.choice([4.5, 9, 18])
    v = rng.choice([0.5, 1, 2])
    c = m / 58.5 / v
    return dict(prompt=f"On dissout {m} g de NaCl (58,5 g/mol) dans {v} L. Quelle est la concentration (mmol/L) ?",
                answer=c * 1000, unit="mmol/L", why=f"n = {m}/58,5 = {m / 58.5:.4f} mol ; C = n/V ≈ {c * 1000:.0f} mmol/L.")


def _q_hh(rng):
    hco3 = rng.choice([18, 20, 24, 28, 30])
    pco2 = rng.choice([30, 40, 50, 60])
    ph = 6.1 + math.log10(hco3 / (0.03 * pco2))
    return dict(prompt=f"[HCO₃⁻] = {hco3} mmol/L et PaCO₂ = {pco2} mmHg. Calcule le pH avec "
                       f"pH = 6,1 + log([HCO₃⁻] / (0,03 × PaCO₂)).",
                answer=ph, tol=0.005, why=f"pH = 6,1 + log({hco3} / {0.03 * pco2:.2f}) ≈ {ph:.2f}.")


def _q_neutrons(rng):
    sym, name, z, mm, val = rng.choice(ELEMENTS)
    a = round(mm)
    return dict(prompt=f"Combien de neutrons a l'isotope principal du {name} ({sym}, Z = {z}, A = {a}) ?",
                answer=a - z, tol=0.0, why=f"Neutrons = A − Z = {a} − {z} = {a - z}.")


MONOMERES = {"protéines": "acides aminés", "acides nucléiques": "nucléotides", "glycogène": "glucose",
             "amidon": "glucose", "triglycérides": "glycérol + 3 acides gras"}

QUESTIONS = [
    qcm(1, "Le numéro atomique Z correspond au nombre de…", "protons", ["neutrons", "électrons de valence",
        "protons + neutrons"], "Z = nombre de protons, il définit l'élément."),
    qcm(1, "Combien de liaisons covalentes forme habituellement le carbone ?", "4", ["2", "3", "6"], "HONC 1234."),
    qcm(1, "Le pH normal du sang artériel est…", "7,35 à 7,45", ["6,8 à 7,0", "7,0 exactement", "7,8 à 8,0"],
        "Une plage très étroite, défendue par les tampons, les poumons et les reins."),
    table_qcm(1, MONOMERES, "Quel est le monomère (la brique de base) des **{k}** ?"),
    vf(1, "L'eau est une molécule apolaire.", False, "Elle est polaire : O est très électronégatif et la molécule est coudée."),
    vf(1, "Une solution à pH 4 est 10 fois plus acide qu'une solution à pH 5.", True,
       "Échelle logarithmique : 1 unité = facteur 10 en [H₃O⁺]."),
    qcm(1, "Quelle liaison relie deux acides aminés ?", "peptidique", ["glycosidique", "phosphodiester", "hydrogène"]),
    num(1, _q_neutrons),
    qcm(2, "Pourquoi l'huile ne se mélange-t-elle pas à l'eau ?", "Ses molécules sont apolaires (hydrophobes)",
        ["Elle est plus dense que l'eau", "Elle est ionique", "Elle forme des liaisons hydrogène avec l'eau"],
        "Polaire dissout polaire, apolaire dissout apolaire."),
    qcm(2, "Une protéine dénaturée par la chaleur a perdu…", "sa structure 3D (secondaire, tertiaire), pas sa séquence",
        ["sa séquence d'acides aminés", "ses liaisons peptidiques", "ses atomes de carbone"],
        "La dénaturation casse les liaisons faibles, pas les liaisons peptidiques."),
    multi(2, "Quelles molécules sont des lipides ?", ["Triglycérides", "Phospholipides", "Cholestérol"],
          ["Glycogène", "Collagène", "ATP"], "Le glycogène est un glucide, le collagène une protéine, l'ATP un nucléotide."),
    qcm(2, "L'hydrolyse de l'ATP…", "libère de l'énergie en coupant une liaison phosphate grâce à une molécule d'eau",
        ["consomme de l'énergie et produit de l'eau", "fabrique du glucose", "est une réaction de condensation"]),
    num(2, _q_ph),
    num(2, _q_mol),
    qcm(2, "Le tampon principal du sang est le couple…", "bicarbonate / acide carbonique",
        ["phosphate / acide phosphorique", "lactate / acide lactique", "ammonium / ammoniac"]),
    qcm(3, "Un patient a pH 7,30, PaCO₂ 60 mmHg, HCO₃⁻ 28 mmol/L. Il s'agit d'une…",
        "acidose respiratoire (partiellement compensée par les reins)",
        ["acidose métabolique", "alcalose respiratoire", "alcalose métabolique"],
        "pH bas + CO₂ élevé = cause respiratoire. Les bicarbonates un peu hauts montrent que les reins compensent."),
    qcm(3, "Un patient hyperventile pendant une crise d'angoisse. Que devient son pH ?",
        "Il augmente (alcalose respiratoire), car il élimine trop de CO₂",
        ["Il diminue, car il produit de l'acide lactique", "Il ne change pas, les tampons compensent tout",
         "Il diminue, car le CO₂ s'accumule"], "Moins de CO₂ → moins d'acide carbonique → pH plus élevé."),
    num(3, _q_hh),
    num(3, _q_conc),
    qcm(3, "Dans la respiration cellulaire, le glucose est…", "oxydé (il perd des électrons) et l'oxygène est réduit",
        ["réduit et l'oxygène oxydé", "hydrolysé en eau uniquement", "ni oxydé ni réduit"],
        "Les électrons du glucose finissent sur l'O₂, qui devient H₂O."),
]

CARDS = [
    ("Définition du pH", "$\\mathrm{pH} = -\\log[\\mathrm{H_3O^+}]$"),
    ("pH normal du sang", "7,35 à 7,45"),
    ("Henderson-Hasselbalch", "$\\mathrm{pH} = \\mathrm{p}K_a + \\log([\\text{base}]/[\\text{acide}])$"),
    ("Quantité de matière", "$n = m / M$ (mol)"),
    ("Concentration molaire", "$C = n / V$ (mol/L)"),
    ("Nombre d'Avogadro", "$6{,}022 \\times 10^{23}$ par mole"),
    ("HONC 1234", "H fait 1 liaison, O 2, N 3, C 4"),
    ("Monomère des protéines", "Acides aminés (20), reliés par des liaisons peptidiques"),
    ("Structure secondaire d'une protéine", "Hélices α et feuillets β (liaisons hydrogène)"),
    ("Hydrolyse", "Coupure d'une liaison par ajout d'eau"),
    ("Acide gras saturé", "Que des liaisons simples, chaîne droite, solide (beurre)"),
    ("Appariement des bases de l'ADN", "A–T et C–G (A–U dans l'ARN)"),
    ("Acidose respiratoire", "CO₂ retenu (hypoventilation, BPCO) → pH bas"),
    ("Isotope", "Même Z, nombre de neutrons différent"),
]

VIDEOS = [
    ("Le pH et les solutions tampons expliqués", "pH solution tampon explication cours"),
    ("Les liaisons chimiques (covalente, ionique, hydrogène)", "liaisons chimiques covalente ionique hydrogène cours"),
    ("Les biomolécules : glucides, lipides, protéines, acides nucléiques", "biomolécules glucides lipides protéines acides nucléiques"),
    ("Structure des protéines (4 niveaux)", "structure primaire secondaire tertiaire quaternaire protéine"),
]

LINKS = [("Khan Academy (FR) : chimie", "https://fr.khanacademy.org/science/chemistry")]
