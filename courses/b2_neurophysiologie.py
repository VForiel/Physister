"""LFSM1203 Fondements de neurophysiologie."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from app import ui
from app.course import Course
from app.quiz import gen_qcm, multi, num, qcm, table_qcm, vf

COURSE = Course(
    code="LFSM1203", title="Fondements de neurophysiologie", short="Neurophysiologie",
    bloc=2, quad=1, credits=4, hours="45 h", icon=":material/neurology:",
    intro="Comment un nerf transmet un message, comment on sent son corps et le monde, et comment le système "
          "nerveux commande le mouvement, du réflexe le plus simple au geste volontaire. Indispensable pour la "
          "kiné neurologique et pour comprendre l'apprentissage moteur.",
    acquis=[
        "Connaître les méthodes neuroscientifiques d'étude du comportement moteur.",
        "Expliquer l'influx nerveux et le potentiel d'action.",
        "Décrire les traitements sensoriels utiles à la motricité (somesthésie, vision, système vestibulaire).",
        "Expliquer les mécanismes de la motricité, des réflexes aux mouvements volontaires.",
        "Décrire les mémoires et les processus attentionnels.",
    ],
)

TERMS = {
    "potentiel d'action": ("Potentiel d'action", "Inversion brève (≈ 1 ms) et en « tout ou rien » du potentiel de "
                           "membrane, qui se propage le long de l'axone.", "Potentiel d'action"),
    "période réfractaire": ("Période réfractaire", "Moment juste après un potentiel d'action où la membrane ne peut "
                            "pas (absolue) ou difficilement (relative) en produire un nouveau.", "Période réfractaire"),
    "myéline": ("Myéline", "Gaine isolante autour des axones (oligodendrocytes dans le SNC, cellules de Schwann dans "
                "le SNP), interrompue aux nœuds de Ranvier. Elle accélère la conduction.", "Myéline"),
    "conduction saltatoire": ("Conduction saltatoire", "Propagation du potentiel d'action de nœud de Ranvier en "
                              "nœud de Ranvier, beaucoup plus rapide.", "Conduction saltatoire"),
    "synapse": ("Synapse", "Zone de communication entre un neurone et sa cible, le plus souvent chimique "
                "(neurotransmetteur).", "Synapse"),
    "fuseau neuromusculaire": ("Fuseau neuromusculaire", "Récepteur dans le muscle, parallèle aux fibres, qui "
                               "mesure la longueur et la vitesse d'étirement. Point de départ du réflexe myotatique.",
                               "Fuseau neuromusculaire"),
    "organe tendineux de golgi": ("Organe tendineux de Golgi", "Récepteur à la jonction muscle-tendon, en série, qui "
                                  "mesure la tension.", "Organe tendineux de Golgi"),
    "réflexe myotatique": ("Réflexe myotatique", "Contraction d'un muscle en réponse à son étirement rapide "
                           "(réflexe ostéotendineux, comme le rotulien). Monosynaptique.", "Réflexe myotatique"),
    "voie lemniscale": ("Voie lemniscale (cordons dorsaux)", "Voie de la sensibilité fine (tact discriminatif, "
                        "vibrations, proprioception consciente). Croise dans le bulbe.", "Voie lemniscale"),
    "voie spinothalamique": ("Voie spinothalamique", "Voie de la douleur, de la température et du tact grossier. "
                             "Croise dans la moelle, au niveau d'entrée.", "Faisceau spinothalamique"),
    "voie pyramidale": ("Voie pyramidale (corticospinale)", "Voie de la motricité volontaire, du cortex moteur aux "
                        "motoneurones de la moelle. Croise en majorité dans le bulbe (décussation des pyramides).",
                        "Faisceau pyramidal"),
    "noyaux gris centraux": ("Noyaux gris centraux", "Ensemble de noyaux profonds (striatum, pallidum, noyau "
                             "subthalamique, substance noire) qui sélectionnent et facilitent les mouvements. "
                             "Atteints dans la maladie de Parkinson.", "Noyaux gris centraux"),
    "cervelet": ("Cervelet", "Structure qui compare le mouvement prévu et le mouvement réalisé, et corrige : "
                 "coordination, équilibre, apprentissage moteur.", "Cervelet"),
    "générateur central de rythme": ("Générateur central de rythme", "Réseau de neurones de la moelle capable de "
                                     "produire un rythme de marche sans commande du cerveau.", "Générateur central de rythme"),
    "tms": ("Stimulation magnétique transcrânienne", "Technique qui stimule le cortex à travers le crâne par un champ "
            "magnétique bref ; permet de tester la voie corticospinale ou de perturber une zone.",
            "Stimulation magnétique transcrânienne"),
    "homonculus": ("Homonculus", "Représentation du corps sur le cortex moteur ou somesthésique, déformée : la main "
                   "et la bouche y occupent une place énorme.", "Homoncule"),
}


def simulate_hh(i1, i2, delay, ttx=False, tea=False, t_end=40.0, dt=0.01):
    """Modèle de Hodgkin-Huxley (1952), axone géant de calmar, repos à −65 mV."""
    gna, gk, gl = (0.0 if ttx else 120.0), (0.0 if tea else 36.0), 0.3
    ena, ek, el = 50.0, -77.0, -54.387
    n_steps = int(t_end / dt)
    v, m, h, n = -65.0, 0.053, 0.596, 0.318
    vs = np.empty(n_steps)
    for k in range(n_steps):
        t = k * dt
        stim = (i1 if 5 <= t < 6 else 0.0) + (i2 if 5 + delay <= t < 6 + delay else 0.0)
        am = 0.1 * (v + 40) / (1 - np.exp(-(v + 40) / 10)) if abs(v + 40) > 1e-6 else 1.0
        bm = 4 * np.exp(-(v + 65) / 18)
        ah = 0.07 * np.exp(-(v + 65) / 20)
        bh = 1 / (1 + np.exp(-(v + 35) / 10))
        an = 0.01 * (v + 55) / (1 - np.exp(-(v + 55) / 10)) if abs(v + 55) > 1e-6 else 0.1
        bn = 0.125 * np.exp(-(v + 65) / 80)
        m += dt * (am * (1 - m) - bm * m)
        h += dt * (ah * (1 - h) - bh * h)
        n += dt * (an * (1 - n) - bn * n)
        i_ion = gna * m ** 3 * h * (v - ena) + gk * n ** 4 * (v - ek) + gl * (v - el)
        v += dt * (stim - i_ion)
        vs[k] = v
    return np.arange(n_steps) * dt, vs


def ch_methodes():
    ui.md(r"""
Comment étudie-t-on le système nerveux qui commande le mouvement ?

| Méthode | Ce qu'elle mesure ou fait | Résolution |
|---|---|---|
| Électrophysiologie (enregistrement unitaire, EEG, EMG) | activité électrique des neurones ou des muscles | temporelle excellente (ms) |
| Lésion (patients, lésions réversibles par refroidissement ou médicament) | ce qui manque quand une zone ne marche pas | montre la **nécessité** d'une zone |
| [[tms\|Stimulation magnétique transcrânienne]] (TMS) | active ou perturbe une zone corticale | causalité, chez l'humain sain |
| Imagerie fonctionnelle (IRMf, TEP) | zones actives pendant une tâche (débit sanguin) | spatiale bonne (mm), temporelle lente (s) |
""")
    ui.tip("Corrélation ou causalité ? L'IRMf montre qu'une zone **s'active** pendant une tâche (corrélation). La "
           "lésion ou la TMS montrent qu'elle est **nécessaire** (causalité). Les deux se complètent.")


def ch_influx():
    ui.md(r"""
Le **[[potentiel d'action]]** (PA) naît quand la membrane atteint le **seuil** (≈ −55 mV) :
1. **Dépolarisation** : les canaux Na⁺ voltage-dépendants s'ouvrent, le Na⁺ entre, le potentiel monte vers +40 mV.
2. **Repolarisation** : les canaux Na⁺ s'inactivent, les canaux K⁺ s'ouvrent, le K⁺ sort.
3. **Hyperpolarisation** : les canaux K⁺ se ferment lentement, le potentiel passe un moment sous le repos.

Il obéit à la loi du **tout ou rien** : sous le seuil, rien ; au-dessus, toujours le même PA. L'**intensité** d'un
stimulus est codée par la **fréquence** des PA, pas par leur taille.
""")
    st.markdown("#### À toi : le modèle de Hodgkin et Huxley")
    st.caption("Le vrai modèle de 1952 (prix Nobel), calculé en direct. Stimulations de 1 ms.")
    c1, c2 = st.columns([1, 2])
    with c1:
        i1 = st.slider("Intensité du 1er stimulus (µA/cm²)", 0.0, 30.0, 10.0, 0.5, key="np_i1")
        i2 = st.slider("Intensité du 2e stimulus", 0.0, 60.0, 0.0, 1.0, key="np_i2")
        delay = st.slider("Délai entre les deux (ms)", 2.0, 25.0, 10.0, 0.5, key="np_delay")
        ttx = st.toggle("Bloquer les canaux Na⁺ (tétrodotoxine)", key="np_ttx")
        tea = st.toggle("Bloquer les canaux K⁺ (TEA)", key="np_tea")
    t, v = simulate_hh(i1, i2, delay, ttx, tea)
    with c2:
        fig = go.Figure(go.Scatter(x=t, y=v, mode="lines"))
        fig.add_hline(y=-65, line_dash="dot", annotation_text="repos")
        fig.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="Temps (ms)",
                          yaxis_title="Potentiel (mV)", yaxis_range=[-90, 60])
        st.plotly_chart(fig, width="stretch")
    st.markdown("""
**Expériences à faire**
- Baisse le 1er stimulus jusqu'à trouver le **seuil** (vers 7 µA/cm²) : en dessous, une petite bosse ; au-dessus, un PA complet, toujours de la même taille.
- Ajoute un 2e stimulus de 10 µA/cm² à 5 ms : il ne déclenche rien, c'est la [[période réfractaire]]. Vers 9 à 13 ms, il faut un stimulus bien plus fort (40 à 60) : c'est la période réfractaire **relative**. Vers 15 ms, 10 µA/cm² suffit de nouveau.
- Bloque les canaux Na⁺ : plus aucun PA. C'est l'effet de la tétrodotoxine du poisson-globe, et des anesthésiques locaux.
""".replace("[[période réfractaire]]", ui.terms("[[période réfractaire]]")), unsafe_allow_html=True)
    ui.md(r"""
**La conduction** : le PA se propage parce qu'il dépolarise la zone voisine. Sa vitesse augmente avec le
**diamètre** de l'axone et surtout avec la [[myéline]] : le PA saute de nœud de Ranvier en nœud de Ranvier
([[conduction saltatoire]]). Les grosses fibres myélinisées (Aα, motoneurones et fuseaux) conduisent à 70-120 m/s,
les petites fibres C (douleur lente) à environ 1 m/s.

**La [[synapse]] chimique** : le PA arrive à la terminaison, le Ca²⁺ entre, les vésicules libèrent le
neurotransmetteur, qui se fixe sur les récepteurs du neurone suivant et crée un potentiel **excitateur** (PPSE,
glutamate, acétylcholine) ou **inhibiteur** (PPSI, GABA, glycine). Le neurone **somme** ces potentiels (dans
l'espace et dans le temps) et décide de décharger ou non.
""")
    ui.clinic("Dans la **sclérose en plaques**, la myéline du SNC est détruite : la conduction ralentit ou se bloque, "
              "d'où des troubles moteurs, sensitifs et visuels. La chaleur aggrave temporairement ces blocs "
              "(phénomène d'Uhthoff) : attention aux séances en salle chaude ou en balnéothérapie trop chaude.")


def ch_sens():
    ui.md(r"""
**Récepteurs et transduction** : chaque récepteur transforme un stimulus (pression, étirement, lumière,
température, molécule) en potentiel de récepteur, puis en PA. Certains s'**adaptent** vite (ils signalent le
changement : corpuscules de Pacini, vibrations) ; d'autres lentement (ils signalent le maintien : récepteurs de
Merkel, pression continue).

**Les deux grandes voies de la somesthésie**

| | [[voie lemniscale\|Voie lemniscale]] (cordons dorsaux) | [[voie spinothalamique\|Voie spinothalamique]] |
|---|---|---|
| Informations | tact fin, vibrations, proprioception consciente | douleur, température, tact grossier |
| Croisement | dans le **bulbe** | dans la **moelle**, au niveau d'entrée |
| Relais | bulbe → thalamus → cortex | moelle → thalamus → cortex |
""")
    ui.clinic("Une hémisection de moelle (syndrome de **Brown-Séquard**) donne, sous la lésion : du **même côté**, une "
              "paralysie et une perte du tact fin et de la proprioception (voie lemniscale, pas encore croisée) ; "
              "du côté **opposé**, une perte de la douleur et de la température (spinothalamique, déjà croisée).")
    ui.md(r"""
**La proprioception** (le sens de la position et du mouvement) vient surtout des [[fuseau neuromusculaire|fuseaux
neuromusculaires]] (longueur et vitesse), des [[organe tendineux de golgi|organes tendineux de Golgi]] (tension)
et des récepteurs articulaires et cutanés.

**Le système vestibulaire** (oreille interne) : les **canaux semi-circulaires** détectent les accélérations
**angulaires** (rotations de la tête), les **otolithes** (utricule et saccule) les accélérations **linéaires** et
la gravité. Il stabilise le regard (réflexe vestibulo-oculaire) et la posture.

**La vision** apporte l'essentiel des informations sur l'environnement, et participe beaucoup à l'équilibre :
fermer les yeux fait osciller (test de Romberg).

**Le cortex somesthésique** (gyrus post-central) a une carte du corps, l'[[homonculus]], où la main et la bouche
occupent une surface énorme : c'est là que la sensibilité est la plus fine.
""")


def ch_reflexes():
    ui.md(r"""
**Le [[motoneurone]] alpha** de la corne antérieure est la **voie finale commune** : tout mouvement, réflexe ou
volontaire, passe par lui. Une **unité motrice** = un motoneurone + toutes les fibres qu'il innerve (quelques-unes
pour les muscles de l'œil, des centaines ou milliers pour le quadriceps). La force augmente par le **recrutement**
de plus d'unités (des plus petites aux plus grandes : principe de **Henneman**) et l'augmentation de leur
**fréquence** de décharge.

**Les réflexes spinaux**

| Réflexe | Récepteur | Circuit | Effet |
|---|---|---|---|
| [[réflexe myotatique\|Myotatique]] (rotulien) | fuseau neuromusculaire | **monosynaptique** | le muscle étiré se contracte ; l'antagoniste est inhibé (inhibition réciproque) |
| Myotatique inverse | organe tendineux de Golgi | disynaptique | une forte tension inhibe le muscle (protection, relâchement) |
| De flexion (retrait) | nocicepteurs | polysynaptique | retrait du membre agressé |
| Extension croisée | nocicepteurs | polysynaptique | l'autre jambe s'étend pour porter le poids |

Le **tonus musculaire** est la légère tension permanente d'un muscle au repos, entretenue par les fuseaux et réglée
par les centres supérieurs (via les motoneurones gamma qui règlent la sensibilité des fuseaux).
""")
    ui.clinic("Quand les voies descendantes sont lésées (AVC, lésion médullaire), les réflexes ne sont plus freinés : "
              "**hyperréflexie** et **spasticité** (résistance qui augmente avec la vitesse d'étirement). Une lésion "
              "du nerf périphérique ou de la racine donne au contraire une **hyporéflexie** ou une aréflexie.")
    ui.memo("Les réflexes ostéotendineux et leurs racines : « **1, 2** (S1-S2 : achilléen), **3, 4** (L3-L4 : "
            "rotulien), **5, 6** (C5-C6 : bicipital), **7, 8** (C7-C8 : tricipital) ».")


def ch_moteur():
    ui.md(r"""
**L'organisation hiérarchique du mouvement**
- **Moelle** : réflexes et [[générateur central de rythme|générateurs de rythme]] (la marche).
- **Tronc cérébral** : posture, équilibre, tonus (voies réticulo-spinales et vestibulo-spinales).
- **Cortex moteur** : le cortex moteur primaire (gyrus pré-central, avec son homonculus) envoie la
  [[voie pyramidale]] ; les aires prémotrices et motrice supplémentaire **planifient** et préparent.
- **Deux boucles de régulation**, qui ne commandent pas directement les muscles mais modulent le cortex :
  - les [[noyaux gris centraux]] **sélectionnent** le bon programme et inhibent les autres, et ils initient le
    mouvement ;
  - le [[cervelet]] **compare** le mouvement voulu au mouvement réel et **corrige** ; il coordonne et participe à
    l'apprentissage.

**La locomotion** : la moelle produit le rythme, le tronc cérébral l'initie, le cortex l'adapte (obstacles,
précision), le cervelet la coordonne.
""")
    ui.table([
        ["Voie pyramidale (cortex, capsule interne, moelle)", "Paralysie, spasticité, hyperréflexie, signe de Babinski", "AVC"],
        ["Noyaux gris centraux", "Lenteur (akinésie, bradykinésie), rigidité, tremblement de repos", "Maladie de Parkinson"],
        ["Cervelet", "Ataxie, dysmétrie, tremblement d'action, troubles de l'équilibre", "Lésion cérébelleuse, alcool"],
    ], headers=["Lésion", "Signes", "Exemple"])
    ui.memo("Le cervelet est le **correcteur** (il compare et ajuste), les noyaux gris centraux sont le **sélecteur** "
            "(ils choisissent et lancent). Atteinte du correcteur : mouvements imprécis. Atteinte du sélecteur : "
            "mouvements rares et lents.")


def ch_memoire():
    ui.md(r"""
**Les mémoires**
- **Déclarative** (explicite) : épisodique et sémantique ; dépend de l'**hippocampe** et du lobe temporal médian.
- **Non déclarative** (implicite) : **procédurale** (habiletés motrices : cervelet, noyaux gris centraux, cortex
  moteur), conditionnement, amorçage.

Le patient **H.M.**, opéré des deux hippocampes en 1953, ne pouvait plus former de nouveaux souvenirs, mais
progressait jour après jour sur une tâche de dessin en miroir… sans se souvenir de l'avoir pratiquée. Preuve que
les deux mémoires sont distinctes.

**L'attention** sélectionne une partie de l'information et a des ressources limitées. L'apprentissage moteur et la
plasticité sont approfondis dans le cours de compléments de neurophysiologie (LKNR1200).
""")
    ui.clinic("Un patient amnésique (Alzheimer débutant, traumatisme crânien) peut encore apprendre un geste par la "
              "pratique répétée, même s'il ne se souvient pas des séances : la mémoire procédurale est souvent "
              "préservée. On en tient compte en rééducation.")


CHAPTERS = [
    ("Méthodes d'investigation", ch_methodes),
    ("Influx nerveux et synapse", ch_influx),
    ("Sensibilité et sens", ch_sens),
    ("Moelle, unités motrices et réflexes", ch_reflexes),
    ("Contrôle moteur", ch_moteur),
    ("Mémoire et attention", ch_memoire),
]

REFLEXES = {"achilléen": "S1-S2", "rotulien": "L3-L4", "bicipital": "C5-C6", "tricipital": "C7-C8"}
LESIONS = {"Cervelet": "dysmétrie et tremblement d'action", "Noyaux gris centraux": "rigidité et tremblement de repos",
           "Voie pyramidale": "spasticité et signe de Babinski"}


def _q_vitesse(rng):
    d = rng.choice([0.5, 0.8, 1.0])
    v = rng.choice([50, 60, 80, 100])
    return dict(prompt=f"Un influx parcourt {d} m le long d'un axone myélinisé à {v} m/s. Combien de temps met-il (ms) ?",
                answer=d / v * 1000, unit="ms", why=f"t = d/v = {d}/{v} s = {d / v * 1000:.3g} ms.")


QUESTIONS = [
    qcm(1, "Quel ion entre dans la cellule pendant la dépolarisation du potentiel d'action ?", "Na⁺", ["K⁺", "Cl⁻", "Mg²⁺"]),
    qcm(1, "Le réflexe myotatique part de quel récepteur ?", "Le fuseau neuromusculaire",
        ["L'organe tendineux de Golgi", "Le corpuscule de Pacini", "Le nocicepteur"]),
    vf(1, "Le potentiel d'action obéit à la loi du tout ou rien.", True),
    qcm(1, "Les canaux semi-circulaires détectent…", "les accélérations angulaires de la tête",
        ["la gravité", "les sons", "la position des articulations"]),
    table_qcm(1, REFLEXES, "Quelles racines teste le réflexe **{k}** ?", "Quel réflexe teste les racines **{v}** ?"),
    qcm(2, "Où croise la voie spinothalamique ?", "Dans la moelle, au niveau d'entrée", ["Dans le bulbe",
        "Dans le thalamus", "Elle ne croise pas"]),
    qcm(2, "Qu'est-ce qui augmente le plus la vitesse de conduction ?", "La myéline", ["Un axone plus long",
        "Un stimulus plus fort", "La température basse"]),
    table_qcm(2, LESIONS, "Quels signes évoquent une atteinte : **{k}** ?", "Quelle structure est atteinte si on observe : {v} ?"),
    multi(2, "Quelles méthodes permettent de montrer qu'une zone cérébrale est nécessaire à une tâche ?",
          ["Étude de lésions", "Stimulation magnétique transcrânienne"], ["IRM fonctionnelle seule", "EEG seul"]),
    qcm(2, "Comment l'intensité d'un stimulus est-elle codée ?", "Par la fréquence des potentiels d'action",
        ["Par leur amplitude", "Par leur durée", "Par le type d'ion"]),
    num(2, _q_vitesse),
    qcm(3, "Une hémisection droite de la moelle en T10. Que trouve-t-on sous la lésion ?",
        "À droite : paralysie et perte du tact fin ; à gauche : perte de la douleur et de la température",
        ["Tout à gauche", "Tout à droite", "Perte de tout des deux côtés"], "Syndrome de Brown-Séquard."),
    qcm(3, "Pourquoi un 2e stimulus de même intensité, 3 ms après un PA, ne déclenche-t-il rien ?",
        "Les canaux Na⁺ sont encore inactivés (période réfractaire absolue)", ["Le Na⁺ est épuisé",
        "La pompe Na⁺/K⁺ est arrêtée", "Le seuil a diminué"]),
    qcm(3, "Selon le principe de Henneman, quelles unités motrices sont recrutées en premier ?",
        "Les plus petites (motoneurones de petite taille, fibres lentes)", ["Les plus grandes",
        "Au hasard", "Les plus proches du tendon"]),
    qcm(3, "Un patient amnésique progresse à une tâche motrice sans se souvenir des séances. Qu'est-ce que cela montre ?",
        "La mémoire procédurale est indépendante de la mémoire déclarative", ["Il simule",
        "L'hippocampe gère les gestes", "La mémoire de travail suffit"]),
    qcm(3, "La spasticité se distingue de la rigidité parce qu'elle…", "augmente avec la vitesse de l'étirement",
        ["est identique quelle que soit la vitesse", "touche uniquement les fléchisseurs", "disparaît au repos"]),
]

CARDS = [
    ("Seuil du potentiel d'action", "≈ −55 mV"),
    ("Dépolarisation", "Entrée de Na⁺"),
    ("Repolarisation", "Sortie de K⁺ (et inactivation Na⁺)"),
    ("Codage de l'intensité", "Fréquence des potentiels d'action"),
    ("Conduction saltatoire", "De nœud de Ranvier en nœud de Ranvier (myéline)"),
    ("Voie lemniscale", "Tact fin, vibrations, proprioception ; croise dans le bulbe"),
    ("Voie spinothalamique", "Douleur, température ; croise dans la moelle"),
    ("Fuseau neuromusculaire", "Longueur et vitesse d'étirement"),
    ("Organe tendineux de Golgi", "Tension"),
    ("Réflexe myotatique", "Monosynaptique, avec inhibition réciproque de l'antagoniste"),
    ("Réflexes et racines", "Achilléen S1-S2, rotulien L3-L4, bicipital C5-C6, tricipital C7-C8"),
    ("Cervelet", "Compare et corrige : coordination"),
    ("Noyaux gris centraux", "Sélectionnent et initient : Parkinson"),
    ("Principe de Henneman", "Petites unités motrices recrutées d'abord"),
    ("Brown-Séquard", "Motricité + tact fin homolatéraux, douleur et température controlatérales"),
]

VIDEOS = [
    ("Le potentiel d'action animé", "potentiel d'action animation canaux sodium potassium"),
    ("La synapse chimique", "synapse chimique neurotransmetteur animation"),
    ("Les voies de la sensibilité", "voie lemniscale spinothalamique explication"),
    ("Le réflexe myotatique", "réflexe myotatique fuseau neuromusculaire explication"),
    ("Cervelet et noyaux gris centraux", "rôle cervelet noyaux gris centraux mouvement"),
]

LINKS = [("Le cerveau à tous les niveaux (Université McGill)", "https://lecerveau.mcgill.ca/")]
