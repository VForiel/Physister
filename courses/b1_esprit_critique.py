"""LFSM1103 Esprit critique et posture scientifique."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from app import ui
from app.course import Course
from app.quiz import gen_qcm, multi, qcm, vf

COURSE = Course(
    code="LFSM1103", title="Esprit critique et posture scientifique", short="Esprit critique",
    bloc=1, quad=1, credits=4, hours="37,5 h", icon=":material/fact_check:",
    intro="Ventouses, kinésiotape, « détox », nouvel exercice miracle vu sur Instagram : un kiné est inondé "
          "d'affirmations. Ce cours donne les outils pour trier, et pour savoir pourquoi on croit ce qu'on croit.",
    acquis=[
        "Décoder les biais et les stéréotypes, repérer la manipulation par la mise en scène.",
        "Déterminer la fiabilité d'une information et de sa source.",
        "Décrire la démarche scientifique et les types de raisonnements.",
        "Expliquer la place et les limites de la science.",
        "Interpréter des données scientifiques et leurs représentations graphiques.",
    ],
)

TERMS = {
    "biais cognitif": ("Biais cognitif", "Erreur systématique de raisonnement, due aux raccourcis que prend "
                       "notre cerveau pour décider vite.", "Biais cognitif"),
    "biais de confirmation": ("Biais de confirmation", "Tendance à chercher, retenir et interpréter les "
                              "informations qui confirment ce qu'on pense déjà.", "Biais de confirmation"),
    "sophisme": ("Sophisme", "Raisonnement qui a l'air valide mais qui ne l'est pas.", "Sophisme"),
    "effet placebo": ("Effet placebo", "Amélioration réelle ressentie après un traitement sans principe actif, liée "
                      "aux attentes, au contexte de soin et à l'évolution naturelle.", "Effet placebo"),
    "régression à la moyenne": ("Régression à la moyenne", "Une mesure extrême a tendance à être suivie d'une "
                                "mesure plus proche de la moyenne, sans aucune intervention. Un patient consulte "
                                "au pic de sa douleur : elle va souvent diminuer d'elle-même.",
                                "Régression vers la moyenne"),
    "variable de confusion": ("Variable de confusion", "Troisième facteur qui influence à la fois la cause "
                              "supposée et l'effet, et crée une fausse relation entre eux.", "Facteur de confusion"),
    "réfutabilité": ("Réfutabilité", "Critère de Popper : une théorie est scientifique si on peut imaginer une "
                     "expérience qui la montrerait fausse.", "Réfutabilité"),
    "évaluation par les pairs": ("Évaluation par les pairs", "Relecture critique d'un article par d'autres "
                                 "chercheurs du domaine avant sa publication (peer review).",
                                 "Évaluation par les pairs"),
    "induction": ("Induction", "Raisonnement qui part d'observations particulières pour en tirer une règle "
                  "générale (toujours provisoire).", "Raisonnement inductif"),
    "déduction": ("Déduction", "Raisonnement qui part d'une règle générale pour en tirer une conséquence "
                  "particulière (sûre si les prémisses sont vraies).", "Raisonnement déductif"),
    "hypothèse nulle": ("Hypothèse nulle", "Hypothèse par défaut qu'il n'y a pas d'effet ou pas de différence. "
                        "Un test statistique cherche à la rejeter.", "Hypothèse nulle"),
    "valeur p": ("Valeur p", "Probabilité d'observer un résultat au moins aussi extrême que celui obtenu si "
                 "l'hypothèse nulle était vraie. Ce n'est pas la probabilité que l'hypothèse soit vraie.",
                 "Valeur p"),
}


def ch_pourquoi():
    ui.md(r"""
Notre cerveau n'a pas été fait pour trouver la vérité, mais pour **décider vite** avec peu d'informations.
Ça marche bien la plupart du temps, mais ça crée des erreurs **systématiques** : les [[biais cognitif|biais
cognitifs]]. Les connaître ne nous en protège pas complètement, mais permet de les repérer.

| Biais | Ce que c'est | En kiné |
|---|---|---|
| [[biais de confirmation\|Confirmation]] | on retient ce qui conforte nos idées | on se souvient des patients que la technique a aidés, on oublie les autres |
| Disponibilité | on surestime ce qui vient facilement à l'esprit | après une rupture du tendon d'Achille vue la veille, on en voit partout |
| Ancrage | la première information pèse trop | le diagnostic noté sur la prescription oriente tout l'examen |
| Autorité | on croit plus facilement quelqu'un de prestigieux | « c'est un grand ostéo qui l'a dit » |
| Effet de halo | une qualité visible colore le reste | un formateur charismatique paraît forcément compétent |
| Dunning-Kruger | les débutants surestiment leur compétence | après un week-end de formation, on se croit expert |
| Post hoc | « après, donc à cause de » | « j'ai fait des ventouses et ma douleur est partie » |
""")
    ui.md(r"""
**Pourquoi un traitement inefficace a l'air de marcher ?** Trois raisons, presque toujours présentes ensemble :
1. l'**évolution naturelle** : beaucoup de douleurs (lombalgie, entorse) guérissent seules ;
2. la [[régression à la moyenne]] : on consulte quand c'est au pire, donc ça va mieux ensuite ;
3. l'[[effet placebo]] et les effets contextuels : attention, toucher, confiance, attentes.

C'est pour ça qu'il faut un **groupe contrôle** pour savoir si un traitement fait plus que tout ça.
""")
    ui.clinic("Les effets contextuels ne sont pas « de la triche » : ils font partie de tout soin, et un bon kiné "
              "les utilise (empathie, explications claires, alliance thérapeutique). Le problème est d'attribuer "
              "l'amélioration à une technique qui, elle, ne fait rien de spécifique.")


def ch_discours():
    ui.md(r"""
**Les [[sophisme|sophismes]] les plus courants**

| Sophisme | Exemple |
|---|---|
| Homme de paille | « Les kinés qui critiquent le taping veulent qu'on ne soigne plus personne. » |
| Attaque personnelle (ad hominem) | « Il dit ça parce qu'il n'est pas kiné. » |
| Appel à la nature | « C'est naturel, donc c'est sans danger. » |
| Appel à l'ancienneté | « On fait ça depuis 3000 ans en Chine, ça marche forcément. » |
| Appel à la popularité | « Tous les sportifs pros en mettent. » |
| Faux dilemme | « Soit tu opères, soit tu ne remarcheras jamais. » |
| Pente glissante | « Si on autorise ça, bientôt n'importe qui pourra soigner. » |
| Charge de la preuve inversée | « Prouve-moi que ça ne marche pas ! » |

**La manipulation par la mise en scène** : blouse blanche, jargon scientifique (« quantique », « énergie »,
« neuro- »), témoignages émouvants, avant/après spectaculaires, chiffres sans source, urgence (« offre limitée »).
Aucun de ces éléments n'est une preuve.
""")
    ui.memo("**Ce qui est affirmé sans preuve peut être rejeté sans preuve** (rasoir de Hitchens). "
            "C'est à celui qui affirme d'apporter la preuve, pas à l'autre de prouver que c'est faux.")
    ui.tip("Face à une affirmation, pose trois questions : **Qui le dit ? Comment le sait-il ? Qu'est-ce qui "
           "pourrait montrer que c'est faux ?**")


def ch_sources():
    ui.md(r"""
Toutes les sources ne se valent pas. Du moins au plus fiable, en général :

1. Réseaux sociaux, forums, témoignages.
2. Presse grand public, sites commerciaux.
3. Sites institutionnels (OMS, Sciensano, KCE en Belgique), manuels de référence.
4. **Articles scientifiques** publiés après [[évaluation par les pairs]].
5. **Revues systématiques** et **guides de pratique** (synthèses de nombreux articles).

**Grille rapide pour évaluer une source (CRAAP)**
- **C**urrency (actualité) : la date ? Est-ce encore à jour ?
- **R**elevance (pertinence) : ça répond à ma question, pour mon type de patient ?
- **A**uthority (autorité) : qui est l'auteur, quelles compétences, quel organisme ?
- **A**ccuracy (exactitude) : y a-t-il des sources, des données vérifiables ?
- **P**urpose (but) : informer, vendre, convaincre ? Des conflits d'intérêts ?
""")
    ui.warn("Un article publié n'est pas forcément juste : il existe des revues « prédatrices » qui publient "
            "tout contre paiement, et même les bonnes revues publient des études faibles. Une étude isolée "
            "ne suffit jamais : on regarde l'ensemble des preuves.")


def ch_demarche():
    ui.md(r"""
**La démarche scientifique (hypothético-déductive)**
1. Observer un phénomène et poser une **question**.
2. Formuler une **hypothèse** testable.
3. En **déduire** une prédiction (« si mon hypothèse est vraie, alors on devrait observer… »).
4. **Tester** par une expérience ou une observation contrôlée.
5. **Analyser** et conclure : l'hypothèse est rejetée ou (provisoirement) soutenue.
6. **Publier** pour que d'autres critiquent et **reproduisent**.

**Deux types de raisonnement**
- L'[[induction]] part de cas particuliers vers une règle : « les 50 patients que j'ai traités ont progressé ».
  Utile pour générer des hypothèses, jamais certain.
- La [[déduction]] part d'une règle vers un cas : « tous les muscles ont besoin d'ATP, le biceps est un muscle,
  donc il a besoin d'ATP ». Sûre si les prémisses sont vraies.

Pour Karl Popper, une théorie scientifique doit être [[réfutabilité|réfutable]] : on doit pouvoir imaginer ce
qui la contredirait. « Cette énergie invisible agit mais ne se mesure pas » n'est pas réfutable, donc pas
scientifique.
""")
    ui.md("**Les grands champs de recherche en sciences de la motricité** : neurosciences du mouvement "
          "(contrôle moteur, apprentissage), physiologie de l'exercice, biomécanique, réadaptation clinique "
          "(efficacité des traitements), psychologie et sociologie du sport et de la santé.")


def ch_donnees():
    ui.md(r"""
**Corrélation n'est pas causalité.** Deux variables peuvent varier ensemble sans que l'une cause l'autre :
- une [[variable de confusion]] les influence toutes les deux ;
- la causalité peut être **inversée** (les gens qui ont mal bougent moins, ou ceux qui bougent moins ont mal ?) ;
- c'est le **hasard** (avec assez de variables, on trouve toujours des corrélations).
""")
    st.markdown("#### À toi : la corrélation trompeuse")
    st.caption("On mesure, jour par jour, les ventes de glaces et le nombre de noyades. Bouge l'influence de la "
               "température : elle seule fait varier les deux.")
    c1, c2 = st.columns([1, 2])
    with c1:
        k = st.slider("Influence de la température", 0.0, 1.0, 0.8, 0.05, key="ec_k")
        n = st.slider("Nombre de jours", 20, 365, 120, key="ec_n")
        show = st.toggle("Colorer par la température", value=False, key="ec_col")
    rng = np.random.default_rng(1)
    temp = rng.uniform(5, 32, n)
    z = (temp - temp.mean()) / temp.std()
    glaces = 200 + 60 * (k * z + (1 - k) * rng.normal(size=n))
    noyades = 3 + 1.5 * (k * z + (1 - k) * rng.normal(size=n))
    r = np.corrcoef(glaces, noyades)[0, 1]
    with c2:
        fig = go.Figure(go.Scatter(x=glaces, y=noyades, mode="markers",
                                   marker=dict(color=temp if show else None, colorscale="RdBu_r", showscale=show,
                                               colorbar=dict(title="°C"))))
        fig.update_layout(height=320, margin=dict(l=10, r=10, t=30, b=10), title=f"Corrélation r = {r:.2f}",
                          xaxis_title="Glaces vendues", yaxis_title="Noyades")
        st.plotly_chart(fig, width="stretch")
    st.caption("Les glaces ne causent pas les noyades : quand il fait chaud, on mange des glaces **et** on se baigne.")

    st.markdown("#### À toi : le graphique qui ment")
    c1, c2 = st.columns([1, 2])
    with c1:
        tronque = st.toggle("Tronquer l'axe vertical", value=True, key="ec_trunc")
    with c2:
        fig = go.Figure(go.Bar(x=["Traitement A", "Traitement B"], y=[62, 65], text=["62 %", "65 %"]))
        fig.update_layout(height=260, margin=dict(l=10, r=10, t=10, b=10), yaxis_title="Patients améliorés (%)",
                          yaxis_range=[60, 66] if tronque else [0, 100])
        st.plotly_chart(fig, width="stretch")
    st.caption("Même données. Avec l'axe tronqué, B a l'air deux fois meilleur ; avec l'axe complet, la différence "
               "est minime. Regarde **toujours** l'échelle des axes.")
    ui.md(r"""
**Quelques réflexes de lecture**
- Regarder la **taille de l'échantillon** : 10 patients, c'est très peu, le hasard pèse lourd.
- Distinguer **risque relatif** et **risque absolu** : « le risque est divisé par 2 » peut vouloir dire de 2 sur
  10 000 à 1 sur 10 000.
- Une différence **statistiquement significative** ([[valeur p]] < 0,05) n'est pas forcément **cliniquement
  importante** : 1 mm de plus sur une échelle de douleur de 100 mm ne change la vie de personne.
""")


def ch_limites():
    ui.md(r"""
La science ne donne pas des vérités définitives, mais **les meilleures explications disponibles**, révisables.
C'est sa force (elle se corrige), pas une faiblesse.

**Ses limites**
- Elle répond à des questions **empiriques** (comment ça marche ?), pas aux questions de **valeurs** (que faut-il
  faire ?). Ce qui est faisable n'est pas forcément souhaitable : c'est le rôle de l'éthique.
- Elle travaille sur des **moyennes** : un traitement efficace en moyenne peut ne pas marcher chez ton patient.
- Elle dépend de **moyens**, de financements, d'intérêts : certaines questions sont peu étudiées.
- La **crise de la reproductibilité** : beaucoup de résultats publiés ne se retrouvent pas quand on refait l'étude
  (petits échantillons, biais de publication des résultats positifs).

**Le scientisme** (la science répond à tout) et le **relativisme** (tout se vaut, « chacun sa vérité ») sont deux
excès. La posture scientifique, c'est le doute **méthodique** : douter, puis vérifier, puis accepter de changer d'avis.
""")
    ui.key_points([
        "Un témoignage ou une expérience personnelle ne prouve pas qu'un traitement marche.",
        "Toujours chercher le groupe contrôle et la taille de l'échantillon.",
        "Corrélation n'est pas causalité.",
        "Significatif ne veut pas dire important.",
        "La science se corrige : changer d'avis devant des preuves est une qualité.",
    ])


CHAPTERS = [
    ("Pourquoi l'esprit critique ?", ch_pourquoi),
    ("Décoder un discours", ch_discours),
    ("Évaluer les sources", ch_sources),
    ("La démarche scientifique", ch_demarche),
    ("Lire les données", ch_donnees),
    ("Les limites de la science", ch_limites),
]

SOPHISMES = [
    ("« C'est à base de plantes, donc il n'y a aucun risque. »", "Appel à la nature"),
    ("« Il ne peut pas parler de kiné, il est seulement médecin du sport. »", "Attaque personnelle (ad hominem)"),
    ("« Prouve-moi que les cristaux ne soignent pas ! »", "Inversion de la charge de la preuve"),
    ("« La moitié de l'équipe nationale utilise ce bracelet. »", "Appel à la popularité"),
    ("« Soit tu fais mon programme, soit tu finiras en fauteuil. »", "Faux dilemme"),
    ("« On masse comme ça depuis des siècles, ça a fait ses preuves. »", "Appel à l'ancienneté"),
    ("« J'ai porté la genouillère et le lendemain je n'avais plus mal : c'est elle qui m'a guéri. »",
     "Post hoc (après, donc à cause de)"),
]
BIAIS = [
    ("Un kiné ne se souvient que des patients que sa technique a soulagés.", "Biais de confirmation"),
    ("Après avoir vu une embolie pulmonaire la semaine dernière, une étudiante en suspecte chez tous ses patients essoufflés.",
     "Biais de disponibilité"),
    ("Le diagnostic « tendinite » inscrit sur la prescription empêche d'envisager autre chose.", "Ancrage"),
    ("Après une formation de deux jours, un étudiant se sent prêt à traiter n'importe quel patient.", "Effet Dunning-Kruger"),
]


def _q_sophisme(rng):
    ex, good = rng.choice(SOPHISMES)
    return (f"Quel sophisme reconnais-tu ? {ex}", good, [s for _, s in SOPHISMES] + ["Homme de paille"], "")


def _q_biais(rng):
    ex, good = rng.choice(BIAIS)
    return (f"Quel biais est en jeu ? {ex}", good, [b for _, b in BIAIS] + ["Effet de halo"], "")


QUESTIONS = [
    gen_qcm(1, _q_sophisme),
    gen_qcm(1, _q_biais),
    vf(1, "Une corrélation entre deux variables prouve que l'une cause l'autre.", False,
       "Il peut y avoir une variable de confusion, une causalité inversée ou du hasard."),
    vf(1, "Un article scientifique passe normalement par une évaluation par les pairs avant publication.", True),
    qcm(1, "Que signifie le premier A de la grille CRAAP ?", "Authority (qui est l'auteur ?)",
        ["Accuracy", "Availability", "Abstract"], "Currency, Relevance, Authority, Accuracy, Purpose."),
    qcm(1, "Quel raisonnement part d'observations particulières pour en tirer une règle générale ?", "L'induction",
        ["La déduction", "L'abduction", "Le syllogisme"]),
    multi(2, "Pourquoi un traitement sans effet propre peut-il sembler efficace ?",
          ["Évolution naturelle de la maladie", "Régression à la moyenne", "Effet placebo et effets contextuels"],
          ["Il agit forcément un peu", "La significativité statistique"],
          "C'est pour ça qu'on compare toujours à un groupe contrôle."),
    qcm(2, "Selon Popper, une théorie est scientifique si…", "on peut imaginer une observation qui la réfuterait",
        ["elle est acceptée par la majorité des scientifiques", "elle a été prouvée vraie définitivement",
         "elle est publiée dans une revue"]),
    qcm(2, "Une étude trouve un lien entre la consommation de café et les infarctus, mais les buveurs de café fument "
        "plus. Le tabac est ici…", "une variable de confusion", ["un biais de publication", "un placebo", "une cause inversée"]),
    vf(2, "Un résultat statistiquement significatif est forcément important pour le patient.", False,
       "Avec un grand échantillon, une différence minuscule peut être significative sans intérêt clinique."),
    qcm(2, "Sur un graphique en barres, l'axe vertical commence à 60 au lieu de 0. Quel est le risque ?",
        "Exagérer visuellement une petite différence", ["Masquer une grande différence", "Aucun",
        "Inverser le sens des résultats"]),
    qcm(3, "« Ce traitement réduit le risque de récidive de 50 % ». Le risque passe de 2 à 1 pour 1000. Quelle "
        "est la réduction du risque absolu ?", "0,1 point de pourcentage (1 pour 1000)",
        ["50 %", "2 %", "1 %"], "Risque relatif divisé par 2, mais le gain absolu est minime."),
    qcm(3, "Un patient lombalgique consulte au pic de sa douleur ; après 3 séances de n'importe quoi, il va mieux. "
        "Quel phénomène explique en partie cette amélioration, indépendamment du traitement ?",
        "La régression à la moyenne", ["L'effet nocebo", "Le biais d'ancrage", "L'effet Hawthorne"]),
    qcm(3, "La valeur p d'une étude vaut 0,03. Que peut-on dire ?",
        "Si le traitement n'avait aucun effet, un tel résultat aurait 3 % de chances d'arriver",
        ["Il y a 97 % de chances que le traitement marche", "Il y a 3 % de chances que l'hypothèse nulle soit vraie",
         "L'effet du traitement est grand"], "La valeur p ne dit rien de la taille de l'effet ni de la probabilité de l'hypothèse."),
    qcm(3, "Pourquoi une seule étude positive ne suffit-elle pas à recommander un traitement ?",
        "Elle peut être due au hasard ou à des biais ; il faut des réplications et des synthèses",
        ["Parce que les études sont toujours fausses", "Parce qu'il faut l'accord du ministère",
         "Parce que seules les études négatives comptent"]),
    multi(3, "Quels éléments sont des signaux d'alerte dans une publicité pour un soin ?",
          ["Jargon « quantique » ou « énergétique »", "Témoignages avant/après sans groupe contrôle",
           "Offre limitée dans le temps"], ["Lien vers une revue systématique indépendante"],
          "Aucun de ces éléments n'est une preuve d'efficacité."),
]

CARDS = [
    ("Biais de confirmation", "Retenir ce qui confirme nos idées, ignorer le reste"),
    ("Régression à la moyenne", "Après une valeur extrême, la suivante est souvent plus proche de la moyenne"),
    ("Variable de confusion", "Facteur qui influence la cause et l'effet supposés"),
    ("Post hoc ergo propter hoc", "« Après, donc à cause de »"),
    ("Grille CRAAP", "Currency, Relevance, Authority, Accuracy, Purpose"),
    ("Réfutabilité (Popper)", "Une théorie scientifique doit pouvoir être montrée fausse"),
    ("Induction", "Du particulier au général"),
    ("Déduction", "Du général au particulier"),
    ("Valeur p", "Probabilité d'un résultat au moins aussi extrême si l'hypothèse nulle est vraie"),
    ("Risque relatif vs absolu", "« Divisé par 2 » peut vouloir dire 2 → 1 pour 1000"),
    ("Rasoir de Hitchens", "Ce qui est affirmé sans preuve peut être rejeté sans preuve"),
    ("Trois raisons pour lesquelles un faux traitement « marche »", "Évolution naturelle, régression à la moyenne, placebo"),
]

VIDEOS = [
    ("Hygiène Mentale (chaîne sur l'esprit critique)", "Hygiène Mentale esprit critique"),
    ("La Tronche en Biais : biais cognitifs", "La Tronche en Biais biais cognitifs"),
    ("Corrélation et causalité", "corrélation causalité explication esprit critique"),
    ("La régression à la moyenne", "régression à la moyenne explication"),
]

LINKS = [
    ("Cortecs : ressources pour l'esprit critique", "https://cortecs.org/"),
    ("Liste de biais cognitifs (Wikipédia)", "https://fr.wikipedia.org/wiki/Biais_cognitif"),
]
