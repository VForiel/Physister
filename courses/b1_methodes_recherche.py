"""LKNR1101 Introduction aux méthodes de recherche."""

import plotly.graph_objects as go
import streamlit as st

from app import ui
from app.course import Course
from app.quiz import gen_qcm, multi, qcm, vf

COURSE = Course(
    code="LKNR1101", title="Introduction aux méthodes de recherche", short="Méthodes de recherche",
    bloc=1, quad=2, credits=3, hours="30 h", icon=":material/travel_explore:",
    intro="Trouver la bonne information scientifique, la lire et la citer correctement : tu en auras besoin pour "
          "tous tes travaux, pour le mémoire, et toute ta carrière pour rester à jour.",
    acquis=[
        "Connaître les principes et les étapes clés de la recherche scientifique.",
        "Situer les champs de recherche ; distinguer approches qualitatives et quantitatives.",
        "Identifier et citer des sources appropriées.",
        "Repérer les limites de la science et les biais.",
        "Identifier les éléments clés de la méthodologie d'un article.",
    ],
)

TERMS = {
    "imrad": ("IMRaD", "Structure standard d'un article scientifique : Introduction, Méthodes, Résultats, "
              "Discussion (and = et).", "IMRaD"),
    "abstract": ("Abstract (résumé)", "Résumé de l'article (250 mots environ), en tête, qui reprend la question, "
                 "les méthodes, les résultats principaux et la conclusion.", None),
    "pubmed": ("PubMed", "Moteur de recherche gratuit de la base MEDLINE (biomédecine), géré par la bibliothèque "
               "nationale de médecine des États-Unis.", "PubMed"),
    "pedro": ("PEDro", "Physiotherapy Evidence Database : base gratuite d'essais, de revues et de guides en "
              "kinésithérapie, avec un score de qualité méthodologique pour chaque essai.", None),
    "cochrane": ("Cochrane", "Organisation internationale qui produit des revues systématiques de référence sur "
                 "l'efficacité des traitements.", "Cochrane (organisation)"),
    "mesh": ("MeSH", "Medical Subject Headings : vocabulaire contrôlé de PubMed. Chaque article est indexé avec des "
             "termes MeSH, ce qui permet de trouver tous les articles sur un sujet quel que soit le mot employé.",
             "Medical Subject Headings"),
    "opérateur booléen": ("Opérateur booléen", "Mot (AND, OR, NOT) qui combine des termes de recherche : AND "
                          "restreint, OR élargit, NOT exclut.", "Algèbre de Boole"),
    "revue systématique": ("Revue systématique", "Synthèse de toutes les études sur une question, avec une méthode "
                           "de recherche et de sélection explicite et reproductible.", "Revue systématique"),
    "méta-analyse": ("Méta-analyse", "Combinaison statistique des résultats de plusieurs études pour obtenir une "
                     "estimation globale de l'effet.", "Méta-analyse"),
    "recherche qualitative": ("Recherche qualitative", "Recherche qui explore le vécu, le sens, les représentations "
                              "(entretiens, observations), sans chercher à mesurer.", "Recherche qualitative"),
    "recherche quantitative": ("Recherche quantitative", "Recherche qui mesure et compte, pour décrire, comparer ou "
                               "tester des hypothèses avec des statistiques.", "Recherche quantitative"),
    "doi": ("DOI", "Digital Object Identifier : identifiant permanent d'un article (ex. 10.1136/bjsports-2019-101253).",
            "Digital Object Identifier"),
    "plagiat": ("Plagiat", "Présenter le travail ou les idées d'autrui comme les siens, sans citer la source.",
                "Plagiat"),
}


def ch_demarche():
    ui.md(r"""
**Littérature scientifique ou vulgarisation ?**

| | Article scientifique | Vulgarisation |
|---|---|---|
| Auteurs | chercheurs, avec affiliation | journaliste, blogueur, parfois chercheur |
| Public | spécialistes | grand public |
| Contrôle | [[évaluation par les pairs]] | rédaction, ou aucun |
| Méthode | détaillée, reproductible | rarement décrite |
| Références | nombreuses, précises | peu ou pas |

**Les étapes d'une recherche** : question → revue de la littérature → hypothèse ou objectif → méthode (population,
mesures, protocole) → récolte des données → analyse → discussion → publication.

**Les grands types de documents**
- **Monographies** (livres, manuels) : bonnes bases, mais vite datées.
- **Articles de revues** : originaux (une étude), revues narratives, [[revue systématique|revues systématiques]]
  et [[méta-analyse|méta-analyses]].
- **Mémoires et thèses** : travaux d'étudiants et de doctorants, de qualité variable.
- **Guides de pratique clinique** : recommandations basées sur les preuves (KCE en Belgique, KNGF aux Pays-Bas…).
""")


def ch_types():
    ui.md(r"""
| | [[recherche quantitative\|Quantitative]] | [[recherche qualitative\|Qualitative]] |
|---|---|---|
| Question | « Combien ? Est-ce efficace ? » | « Comment ? Pourquoi ? Comment est-ce vécu ? » |
| Données | nombres (mesures, scores) | mots, récits, observations |
| Échantillon | grand, représentatif | petit, choisi pour sa richesse |
| Analyse | statistiques | thèmes, codage du discours |
| Exemple | « Le renforcement réduit-il la douleur du genou arthrosique ? » | « Comment les patients vivent-ils l'arthrose au quotidien ? » |

Les deux sont **complémentaires** : la qualitative explique pourquoi un traitement efficace en moyenne n'est pas
suivi par les patients. On parle de **méthodes mixtes** quand on combine les deux.

**Champs de recherche en sciences de la motricité** : contrôle et apprentissage moteur, physiologie de l'exercice,
biomécanique, réadaptation (efficacité des traitements), santé publique (activité physique et santé),
sciences humaines du sport.
""")


def ch_chercher():
    ui.md(r"""
**Les bases de données utiles en kiné**
- [[pubmed|PubMed]] (MEDLINE) : la référence en biomédecine, gratuite.
- [[pedro|PEDro]] : spécialisée kiné, avec la qualité de chaque essai (score PEDro sur 10).
- [[cochrane|Cochrane Library]] : revues systématiques.
- Le **catalogue des bibliothèques UCLouvain** pour les livres et l'accès aux articles payants (connexion via
  l'université).
- Google Scholar : pratique pour retrouver un article, mais sans filtre de qualité.

**Construire une recherche**
1. Découper ta question en **concepts** (ex. : *lombalgie*, *exercice*, *personnes âgées*).
2. Pour chaque concept, lister les **synonymes** et les termes anglais (la plupart des articles sont en anglais),
   et le terme [[mesh|MeSH]] s'il existe.
3. Combiner avec les [[opérateur booléen|opérateurs booléens]] : **OR** entre synonymes, **AND** entre concepts.
4. Utiliser les **guillemets** pour une expression exacte et la **troncature** (`rehabilit*` trouve rehabilitation,
   rehabilitative…).
5. Ajouter des **filtres** (date, type d'étude, langue).
""")
    st.markdown("#### À toi : AND, OR, NOT")
    st.caption("Base fictive : 400 articles sur la lombalgie, 300 sur l'exercice, 120 parlent des deux.")
    op = st.radio("Requête", ["low back pain", "exercise", "low back pain AND exercise", "low back pain OR exercise",
                              "low back pain NOT exercise"], key="mr_bool", horizontal=True)
    a, b, ab = 400, 300, 120
    n = {"low back pain": a, "exercise": b, "low back pain AND exercise": ab, "low back pain OR exercise": a + b - ab,
         "low back pain NOT exercise": a - ab}[op]
    import numpy as np

    xs, ys = np.meshgrid(np.linspace(-0.05, 3.25, 90), np.linspace(-0.05, 2.05, 58))
    xs, ys = xs.ravel(), ys.ravel()
    in_a = (xs - 1) ** 2 + (ys - 1) ** 2 <= 1
    in_b = (xs - 2.2) ** 2 + (ys - 1) ** 2 <= 1
    sel = {"low back pain": in_a, "exercise": in_b, "low back pain AND exercise": in_a & in_b,
           "low back pain OR exercise": in_a | in_b, "low back pain NOT exercise": in_a & ~in_b}[op]
    other = (in_a | in_b) & ~sel
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs[other], y=ys[other], mode="markers", marker=dict(size=4, color="rgba(128,128,128,0.25)"),
                             hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=xs[sel], y=ys[sel], mode="markers", marker=dict(size=4, color="#4d5f92"), hoverinfo="skip"))
    fig.add_annotation(x=0.5, y=1, text="lombalgie", showarrow=False)
    fig.add_annotation(x=2.7, y=1, text="exercice", showarrow=False)
    fig.update_layout(height=260, margin=dict(l=10, r=10, t=10, b=10), xaxis=dict(visible=False, range=[-0.2, 3.4]),
                      yaxis=dict(visible=False, scaleanchor="x", range=[-0.1, 2.1]), showlegend=False)
    c1, c2 = st.columns([2, 1])
    c1.plotly_chart(fig, width="stretch")
    c2.metric("Articles trouvés", n)
    ui.memo("**AND** = « et aussi » : moins de résultats. **OR** = « ou bien » : plus de résultats. "
            "**NOT** = « sauf » : à utiliser avec prudence, on exclut vite des articles utiles.")


def ch_lire():
    ui.md(r"""
**Un article suit presque toujours la structure [[imrad|IMRaD]]**, précédée d'un [[abstract]] :
- **Introduction** : ce qu'on sait, ce qu'on ne sait pas, la **question** ou l'objectif.
- **Méthodes** : qui (participants, critères d'inclusion et d'exclusion), quoi (intervention, mesures), comment
  (protocole, analyse statistique). C'est la partie qui dit si on peut faire confiance aux résultats.
- **Résultats** : les chiffres, sans interprétation.
- **Discussion** : interprétation, comparaison avec la littérature, **limites**, conclusion.

**Lecture efficace** : titre et abstract d'abord (est-ce pertinent ?), puis les figures et tableaux, puis la
méthode, puis la discussion (surtout les limites). On lit rarement un article d'une traite du début à la fin.
""")
    ui.tip("Commence chaque lecture par trois questions : **Quelle est la question exacte ? Sur qui ? Avec quelle "
           "méthode ?** Si tu peux y répondre en une phrase chacune, tu as compris l'essentiel.")


def ch_citer():
    ui.md(r"""
**Pourquoi citer ?** Pour reconnaître le travail des autres, permettre au lecteur de vérifier, et éviter le
[[plagiat]] (sanctionné à l'université, même involontaire). Paraphraser sans citer est aussi du plagiat.

**Le style APA (7e édition)**, très utilisé en sciences de la santé :
- dans le texte : (Auteur, année), par exemple (Dubois & Esculier, 2020) ; à partir de trois auteurs :
  (Hayden et al., 2021) ;
- en bibliographie, par ordre alphabétique :
  *Auteur, A. A., & Auteur, B. B. (Année). Titre de l'article. Nom de la Revue, volume(numéro), pages.*
  suivi du [[doi|DOI]].
""")
    st.markdown("#### À toi : construis une référence APA")
    c1, c2 = st.columns(2)
    auteurs = c1.text_input("Auteurs (Nom, Initiales ; séparés par ;)", "Dubois, B. ; Esculier, J.-F.", key="mr_aut")
    annee = c2.text_input("Année", "2020", key="mr_an")
    titre = st.text_input("Titre de l'article", "Soft-tissue injuries simply need PEACE and LOVE", key="mr_titre")
    c1, c2, c3, c4 = st.columns(4)
    revue = c1.text_input("Revue", "British Journal of Sports Medicine", key="mr_revue")
    vol = c2.text_input("Volume", "54", key="mr_vol")
    num_ = c3.text_input("Numéro", "2", key="mr_num")
    pages = c4.text_input("Pages", "72-73", key="mr_pages")
    doi = st.text_input("DOI", "10.1136/bjsports-2019-101253", key="mr_doi")
    names = [a.strip() for a in auteurs.split(";") if a.strip()]
    if len(names) == 1:
        a_txt = names[0]
    elif len(names) > 1:
        a_txt = ", ".join(names[:-1]) + ", & " + names[-1]
    else:
        a_txt = ""
    ref = f"{a_txt} ({annee}). {titre}. *{revue}*, *{vol}*({num_}), {pages}. https://doi.org/{doi}"
    st.markdown("**Référence** :")
    st.markdown(ref)
    first = names[0].split(",")[0] if names else ""
    cite = f"({first}, {annee})" if len(names) == 1 else (
        f"({first} & {names[1].split(',')[0]}, {annee})" if len(names) == 2 else f"({first} et al., {annee})")
    st.markdown(f"**Dans le texte** : {cite}")
    ui.tip("Un gestionnaire de références comme **Zotero** (gratuit) fait tout ça automatiquement : installe-le dès "
           "maintenant, tu gagneras des heures pour le mémoire.")


CHAPTERS = [
    ("Démarche et types de documents", ch_demarche),
    ("Quantitatif et qualitatif", ch_types),
    ("Chercher dans les bases", ch_chercher),
    ("Lire un article", ch_lire),
    ("Citer ses sources", ch_citer),
]

QUESTIONS_TYPE = [
    ("Comment les patients amputés vivent-ils leur première année avec une prothèse ?", "Qualitative"),
    ("Le renforcement musculaire réduit-il les chutes chez les plus de 70 ans ?", "Quantitative"),
    ("Quelle est la prévalence de la lombalgie chez les étudiants en kiné ?", "Quantitative"),
    ("Quelles sont les représentations des soignants sur la douleur chronique ?", "Qualitative"),
]


def _q_type(rng):
    q, good = rng.choice(QUESTIONS_TYPE)
    return (f"Quelle approche est la plus adaptée à cette question : « {q} »", good, ["Qualitative", "Quantitative"], "")


QUESTIONS = [
    qcm(1, "Que signifie IMRaD ?", "Introduction, Méthodes, Résultats, Discussion",
        ["Introduction, Matériel, Revue, Débat", "Idée, Mesure, Résumé, Données", "Index, Méthode, Recherche, Discussion"]),
    qcm(1, "Quelle base de données est spécialisée en kinésithérapie ?", "PEDro", ["Cochrane", "Google Scholar", "Wikipédia"]),
    qcm(1, "L'opérateur AND entre deux termes…", "réduit le nombre de résultats", ["l'augmente",
        "exclut le second terme", "ne change rien"]),
    vf(1, "Paraphraser un texte sans citer sa source est du plagiat.", True),
    gen_qcm(1, _q_type),
    qcm(2, "Dans une recherche, on combine les synonymes d'un même concept avec…", "OR", ["AND", "NOT", "des guillemets"]),
    qcm(2, "À quoi sert la troncature (rehabilit*) ?", "À trouver toutes les terminaisons d'un mot",
        ["À exclure un mot", "À chercher l'expression exacte", "À limiter aux articles récents"]),
    qcm(2, "Dans quelle partie d'un article trouve-t-on les critères d'inclusion des participants ?", "Méthodes",
        ["Introduction", "Résultats", "Discussion"]),
    multi(2, "Quelles caractéristiques sont typiques d'un article scientifique ?",
          ["Évaluation par les pairs", "Méthode détaillée", "Références précises"], ["Témoignages", "Publicité"]),
    qcm(2, "Comment cite-t-on en APA un article de trois auteurs ou plus dans le texte ?", "(Premier auteur et al., année)",
        ["(Tous les auteurs, année)", "[1]", "(Titre, année)"]),
    qcm(3, "Base fictive : 500 articles « knee osteoarthritis », 800 « exercise », 200 les deux. Combien pour "
        "« knee osteoarthritis OR exercise » ?", "1100", ["1300", "200", "300"], "500 + 800 − 200 (on ne compte pas deux fois l'intersection)."),
    qcm(3, "Pourquoi le MeSH est-il utile sur PubMed ?",
        "Il trouve les articles indexés sur un concept, quel que soit le mot utilisé par les auteurs",
        ["Il traduit automatiquement en français", "Il trie par qualité", "Il donne accès aux articles payants"]),
    qcm(3, "Quelle partie d'un article lire en priorité pour juger de la confiance à accorder aux résultats ?",
        "Les méthodes", ["L'introduction", "Les remerciements", "Le titre"]),
    qcm(3, "Pourquoi l'opérateur NOT est-il à utiliser avec prudence ?",
        "Il peut exclure des articles pertinents qui mentionnent aussi le terme exclu",
        ["Il ralentit la recherche", "Il n'existe pas sur PubMed", "Il double le nombre de résultats"]),
]

CARDS = [
    ("IMRaD", "Introduction, Méthodes, Résultats, Discussion"),
    ("AND", "Restreint (intersection)"),
    ("OR", "Élargit (union), entre synonymes"),
    ("NOT", "Exclut, avec prudence"),
    ("Troncature", "rehabilit* : toutes les terminaisons"),
    ("PEDro", "Base kiné avec score de qualité /10"),
    ("MeSH", "Vocabulaire contrôlé de PubMed"),
    ("Citation APA, 2 auteurs", "(Dubois & Esculier, 2020)"),
    ("Citation APA, 3 auteurs et plus", "(Hayden et al., 2021)"),
    ("Recherche qualitative", "Explore le vécu, le sens (entretiens)"),
    ("Méta-analyse", "Combinaison statistique de plusieurs études"),
    ("DOI", "Identifiant permanent d'un article"),
]

VIDEOS = [
    ("Faire une recherche sur PubMed", "tutoriel recherche PubMed MeSH débutant"),
    ("Utiliser la base PEDro", "PEDro database tutorial physiotherapy"),
    ("Citer en APA 7e édition", "normes APA 7 citation bibliographie tutoriel"),
    ("Prise en main de Zotero", "Zotero tutoriel débutant"),
]

LINKS = [
    ("PubMed", "https://pubmed.ncbi.nlm.nih.gov/"),
    ("PEDro (en français)", "https://pedro.org.au/french/"),
    ("Cochrane Library", "https://www.cochranelibrary.com/"),
    ("Zotero", "https://www.zotero.org/"),
]
