"""LFSM1202 Physiologie des systèmes."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from app import ui
from app.course import Course
from app.quiz import gen_qcm, multi, num, qcm, vf

COURSE = Course(
    code="LFSM1202", title="Physiologie des systèmes", short="Physiologie des systèmes",
    bloc=2, quad=2, credits=3, hours="30 h", icon=":material/cardiology:",
    intro="Comment le cœur, les poumons, les reins, les hormones et le système immunitaire maintiennent "
          "l'équilibre du corps, et comment ils s'adaptent à l'effort. La dernière partie fait le lien avec les "
          "maladies cardio-respiratoires que tu traiteras en kiné.",
    acquis=[
        "Décrire le fonctionnement et le contrôle des grands systèmes (hors système nerveux).",
        "Résoudre des problèmes physiologiques simples.",
        "Mobiliser les grands concepts dans des cas concrets.",
    ],
)

TERMS = {
    "débit cardiaque": ("Débit cardiaque", "Volume de sang éjecté par le ventricule par minute : Q = FC × VES "
                        "(≈ 5 L/min au repos, jusqu'à 20-25 L/min à l'effort).", "Débit cardiaque"),
    "volume d'éjection systolique": ("Volume d'éjection systolique (VES)", "Volume de sang éjecté à chaque "
                                     "battement (≈ 70 mL au repos).", "Volume d'éjection systolique"),
    "frank-starling": ("Loi de Frank-Starling", "Plus le ventricule se remplit (plus il est étiré), plus il éjecte de "
                       "sang : le cœur s'adapte au retour veineux.", "Loi de Frank-Starling"),
    "baroréflexe": ("Baroréflexe", "Réflexe qui stabilise la pression artérielle : des capteurs de la carotide et de "
                    "l'aorte ajustent la FC et le diamètre des vaisseaux.", "Baroréflexe"),
    "ecg": ("ECG", "Électrocardiogramme : enregistrement de l'activité électrique du cœur (onde P, complexe QRS, "
            "onde T).", "Électrocardiographie"),
    "compliance": ("Compliance pulmonaire", "Facilité avec laquelle le poumon se laisse distendre (ΔV/ΔP).",
                   "Compliance pulmonaire"),
    "vems": ("VEMS", "Volume expiratoire maximal en une seconde : le volume soufflé dans la première seconde d'une "
             "expiration forcée.", "Volume expiratoire maximal par seconde"),
    "effet bohr": ("Effet Bohr", "Une baisse du pH (ou une hausse du CO₂ et de la température) diminue l'affinité de "
                   "l'hémoglobine pour l'O₂ : elle le libère plus facilement dans les muscles actifs.", "Effet Bohr"),
    "débit de filtration glomérulaire": ("Débit de filtration glomérulaire", "Volume de plasma filtré par les reins "
                                         "par unité de temps : environ 180 L par jour.", "Débit de filtration glomérulaire"),
    "rétrocontrôle négatif": ("Rétrocontrôle négatif", "Mécanisme où le produit d'une réaction freine sa propre "
                              "production, pour stabiliser une valeur (thermostat).", "Rétroaction"),
    "hémostase": ("Hémostase", "Ensemble des mécanismes qui arrêtent un saignement : vasoconstriction, clou "
                  "plaquettaire, coagulation.", "Hémostase"),
    "bpco": ("BPCO", "Bronchopneumopathie chronique obstructive : obstruction bronchique persistante, surtout due "
             "au tabac.", "Bronchopneumopathie chronique obstructive"),
    "insuffisance cardiaque": ("Insuffisance cardiaque", "Le cœur ne pompe plus assez pour couvrir les besoins de "
                               "l'organisme : essoufflement, fatigue, œdèmes.", "Insuffisance cardiaque"),
}


def ch_homeostasie():
    ui.md(r"""
L'[[homéostasie]] repose sur des boucles de régulation : un **capteur** mesure une variable, un **centre** la
compare à une valeur de consigne, un **effecteur** corrige. La plupart sont des [[rétrocontrôle négatif|rétrocontrôles
négatifs]] (comme un thermostat) : si la variable monte, on la fait redescendre.

Deux systèmes transmettent l'information : le **système nerveux** (rapide, ciblé) et le **système endocrinien**
(hormones dans le sang : plus lent, plus diffus, plus durable).

**Le système endocrinien** : l'**hypothalamus** commande l'**hypophyse**, qui commande d'autres glandes
(thyroïde, surrénales, gonades) : ce sont les **axes**. Exemples d'hormones utiles au kiné : **insuline** et
**glucagon** (glycémie), **cortisol** (stress, anti-inflammatoire, catabolisant), **adrénaline** (effort),
**hormones thyroïdiennes** (métabolisme), **hormone de croissance** et **testostérone** (anabolisme),
**œstrogènes** (protègent l'os : d'où l'ostéoporose après la ménopause).
""")


def ch_cardio():
    ui.md(r"""
**Le cycle cardiaque** : la **systole** (contraction, éjection) et la **diastole** (relâchement, remplissage).
L'activité électrique naît dans le **nœud sinusal** (le pacemaker naturel), passe aux atria, au **nœud
atrio-ventriculaire** (qui ralentit un peu), puis au faisceau de His et aux ventricules. L'[[ecg|ECG]] la
montre : onde **P** (atria), complexe **QRS** (ventricules), onde **T** (repolarisation des ventricules).

**Les équations clés**

$$Q = \text{FC} \times \text{VES} \qquad \text{PAM} = Q \times R$$

Le [[débit cardiaque]] dépend de la fréquence et du [[volume d'éjection systolique]]. La pression artérielle
moyenne (PAM) dépend du débit et des résistances des vaisseaux. La loi de [[frank-starling|Frank-Starling]] dit que
le cœur éjecte ce qu'il reçoit.

**La régulation** : le [[baroréflexe]] corrige en quelques secondes ; le système rénine-angiotensine-aldostérone
et les reins règlent le volume sanguin sur le long terme.
""")
    st.markdown("#### À toi : le débit cardiaque")
    c1, c2 = st.columns([1, 2])
    with c1:
        fc = st.slider("Fréquence cardiaque (bpm)", 40, 200, 70, key="ps_fc")
        ves = st.slider("Volume d'éjection systolique (mL)", 40, 200, 70, key="ps_ves")
        r = st.slider("Résistances périphériques (unités relatives)", 0.3, 2.0, 1.0, 0.05, key="ps_r",
                      help="À l'effort, la vasodilatation musculaire les fait chuter.")
    q = fc * ves / 1000
    pam = 93 * q / 4.9 * r
    with c2:
        k1, k2 = st.columns(2)
        k1.metric("Débit cardiaque", f"{q:.1f} L/min")
        k2.metric("Pression artérielle moyenne", f"{pam:.0f} mmHg", help="Normalisée : 93 mmHg pour 4,9 L/min et R = 1.")
        st.caption("Essaie l'effort intense d'un sportif : FC 190, VES 130 mL, résistances 0,4. Le débit est multiplié "
                   "par 5, mais la pression monte beaucoup moins grâce à la vasodilatation.")
    ui.clinic("Un patient sous **bêtabloquants** ne peut pas monter sa FC normalement : son débit à l'effort augmente "
              "moins. Et la PA d'un patient **hypertendu** doit être vérifiée avant une séance d'effort (on ne commence "
              "pas un effort intense au-delà d'environ 180/110 mmHg au repos).")


def ch_respi():
    ui.md(r"""
**La ventilation** : à l'inspiration, le **diaphragme** descend et les intercostaux externes soulèvent les côtes ;
le volume du thorax augmente, la pression dans les alvéoles baisse, l'air entre. L'expiration de repos est
**passive** (élasticité du poumon) ; l'expiration forcée utilise les abdominaux.

**Les volumes** : volume courant (≈ 0,5 L), capacité vitale (≈ 4 à 5 L), volume résiduel (≈ 1,2 L, ce qui reste
toujours). La [[compliance]] mesure la facilité à distendre le poumon (diminuée dans la fibrose). Le [[vems|VEMS]]
mesure la vitesse de vidange (diminué dans l'asthme et la BPCO).

**Les échanges** se font par diffusion à travers la membrane alvéolo-capillaire (loi de Fick). L'O₂ est transporté
à 98 % par l'**hémoglobine**, dont l'affinité dépend des conditions locales.
""")
    st.markdown("#### À toi : la courbe de dissociation de l'hémoglobine")
    c1, c2 = st.columns([1, 2])
    with c1:
        ph = st.slider("pH", 7.0, 7.7, 7.4, 0.01, key="ps_ph")
        temp = st.slider("Température (°C)", 35.0, 41.0, 37.0, 0.1, key="ps_temp")
        po2 = st.slider("PO₂ du sang (mmHg)", 10, 110, 40, key="ps_po2", help="Artériel ≈ 95 ; veineux au repos ≈ 40 ; muscle à l'effort ≈ 20.")
    p50 = 26.8 * 10 ** (0.48 * (7.4 - ph)) * 10 ** (0.024 * (temp - 37))
    x = np.linspace(0, 120, 300)

    def sat(p, p50_):
        return 100 * p ** 2.7 / (p ** 2.7 + p50_ ** 2.7)

    with c2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=sat(x, 26.8), name="Normal (pH 7,4 ; 37 °C)", line=dict(dash="dot")))
        fig.add_trace(go.Scatter(x=x, y=sat(x, p50), name="Tes conditions"))
        fig.add_trace(go.Scatter(x=[po2], y=[sat(po2, p50)], mode="markers", marker=dict(size=12), showlegend=False))
        fig.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="PO₂ (mmHg)",
                          yaxis_title="Saturation de l'Hb (%)", legend=dict(orientation="h", y=-0.25),
                          xaxis_range=[0, 120], yaxis_range=[0, 105])
        ui.chart(fig, "physio_systemes_0")
        st.caption(f"P50 = {p50:.1f} mmHg ; saturation à {po2} mmHg : {sat(po2, p50):.0f} %.")
    ui.md(r"""
C'est l'[[effet bohr|effet Bohr]] : dans un muscle qui travaille (plus acide, plus chaud, plus de CO₂), la courbe se
déplace **vers la droite**, et l'hémoglobine **lâche plus d'O₂** exactement là où on en a besoin. La forme en « S »
protège aussi : même si la PO₂ artérielle baisse de 95 à 70 mmHg, la saturation reste au-dessus de 90 %.
""")
    ui.memo("Vers la **droite** = l'hémoglobine **donne** (« **D**roite, **D**onne ») : acidose, chaleur, CO₂, 2,3-DPG, "
            "effort.")


def ch_autres():
    ui.md(r"""
**Le rein** : il filtre environ **180 L** de plasma par jour ([[débit de filtration glomérulaire]]) et en réabsorbe
plus de 99 %, pour ne former que 1 à 2 L d'urine. Il règle l'eau, le sodium, le potassium, le pH (bicarbonates),
la pression artérielle (rénine), et fabrique l'**EPO** (globules rouges) et la vitamine D active.

**Le système digestif** : digestion mécanique et chimique, absorption surtout dans l'intestin grêle ; le foie
stocke le glycogène et transforme les nutriments.

**Le sang et l'[[hémostase]]** : plasma, globules rouges (transport de l'O₂), globules blancs (défense), plaquettes.
L'hémostase : vasoconstriction, **clou plaquettaire**, puis **coagulation** (fibrine). Un caillot qui se forme dans
une veine profonde est une **thrombose veineuse profonde** ; s'il migre au poumon, c'est une **embolie pulmonaire**.

**L'immunité** : **innée** (barrières, inflammation, phagocytes : rapide, non spécifique) et **adaptative**
(lymphocytes B → anticorps, lymphocytes T : spécifique, avec mémoire, c'est le principe des vaccins).

**La reproduction** : axes hypothalamo-hypophyso-gonadiques, cycle menstruel (dont les variations hormonales
peuvent influencer la laxité ligamentaire et la performance).
""")
    ui.clinic("Le kiné doit repérer la **thrombose veineuse profonde** : mollet gonflé, chaud, douloureux, surtout "
              "après une chirurgie ou une immobilisation. On n'en masse pas le mollet, et on oriente vers le médecin "
              "en urgence.")


def ch_effort():
    ui.md(r"""
**Adaptations aiguës à l'effort** : la FC et le VES augmentent (débit ×4 à ×5), le sang est redistribué vers les
muscles (vasodilatation locale, vasoconstriction digestive et rénale), la ventilation augmente (jusqu'à plus de
100 L/min), la PA systolique monte tandis que la diastolique varie peu, la température monte et on transpire.

**Adaptations chroniques à l'entraînement en endurance** : cœur plus gros et plus efficace (VES plus grand, FC de
repos plus basse), plus de capillaires et de mitochondries dans les muscles, VO₂max plus élevée, meilleure
utilisation des graisses.
""")
    st.markdown("#### Bases physiopathologiques")
    ui.table([
        ["Cardiopathie ischémique", "rétrécissement des coronaires (athérome) : le muscle cardiaque manque d'O₂", "angor à l'effort, infarctus"],
        ["[[insuffisance cardiaque|Insuffisance cardiaque]]", "le cœur pompe mal (muscle abîmé, surcharge)", "dyspnée, fatigue, œdèmes"],
        ["Arythmies", "troubles du rythme (fibrillation atriale…)", "palpitations, malaises, risque d'AVC"],
        ["Insuffisance respiratoire", "échanges gazeux insuffisants", "hypoxémie, parfois hypercapnie"],
        ["[[bpco|BPCO]]", "obstruction bronchique persistante, destruction des alvéoles (tabac)", "dyspnée d'effort, toux, VEMS bas"],
        ["Asthme", "obstruction bronchique **réversible** (inflammation, bronchospasme)", "crises de sifflements, toux, oppression"],
    ], headers=["Pathologie", "Mécanisme", "Signes"])
    ui.tip("Ces pathologies sont reprises en détail avec la kiné dans le cours « Pathologies et kinésithérapie du "
           "système cardio-respiratoire » (LKNR1205), au même quadrimestre.")


CHAPTERS = [
    ("Homéostasie et hormones", ch_homeostasie),
    ("Système cardiovasculaire", ch_cardio),
    ("Système respiratoire", ch_respi),
    ("Rein, sang, immunité", ch_autres),
    ("Effort et physiopathologie", ch_effort),
]


def _q_debit(rng):
    fc = rng.choice([60, 70, 80, 120, 150, 180])
    ves = rng.choice([60, 70, 90, 110, 130])
    return dict(prompt=f"FC = {fc} bpm et VES = {ves} mL. Quel est le débit cardiaque (L/min) ?", answer=fc * ves / 1000,
                unit="L/min", why=f"Q = FC × VES = {fc} × {ves} mL = {fc * ves / 1000:.2f} L/min.")


def _q_ves(rng):
    q = rng.choice([5, 6, 15, 20])
    fc = rng.choice([70, 100, 150, 180])
    return dict(prompt=f"Le débit cardiaque est de {q} L/min avec une FC de {fc} bpm. Quel est le VES (mL) ?",
                answer=q * 1000 / fc, unit="mL", tol=0.02, why=f"VES = Q/FC = {q * 1000}/{fc} ≈ {q * 1000 / fc:.0f} mL.")


def _q_filtration(rng):
    jours = rng.choice([1, 2, 7])
    return dict(prompt=f"Les reins filtrent environ 180 L de plasma par jour. Combien de litres en {jours} jour(s) ?",
                answer=180 * jours, unit="L", tol=0.0)


QUESTIONS = [
    qcm(1, "Quelle est la formule du débit cardiaque ?", "FC × VES", ["FC / VES", "PA × R", "VES − FC"]),
    qcm(1, "Le pacemaker naturel du cœur est…", "le nœud sinusal", ["le nœud atrio-ventriculaire", "le faisceau de His",
        "le ventricule gauche"]),
    qcm(1, "Que représente le complexe QRS de l'ECG ?", "La dépolarisation des ventricules",
        ["La dépolarisation des atria", "La repolarisation des ventricules", "La fermeture des valves"]),
    vf(1, "L'expiration de repos est un phénomène passif.", True, "Elle repose sur l'élasticité du poumon."),
    qcm(1, "Combien de plasma les reins filtrent-ils environ par jour ?", "180 L", ["1,5 L", "18 L", "1800 L"]),
    num(1, _q_debit),
    qcm(2, "Que fait l'effet Bohr ?", "Il pousse l'hémoglobine à libérer plus d'O₂ dans un milieu acide et chaud",
        ["Il augmente l'affinité de l'Hb pour l'O₂ dans les muscles", "Il bloque la respiration",
         "Il augmente la production de globules rouges"]),
    multi(2, "Quelles sont des adaptations chroniques à l'entraînement en endurance ?", ["FC de repos plus basse",
          "VES plus grand", "Plus de mitochondries"], ["VO₂max plus basse", "Moins de capillaires"]),
    qcm(2, "Quelle différence majeure entre asthme et BPCO ?", "L'obstruction de l'asthme est réversible, celle de la BPCO persistante",
        ["La BPCO touche surtout les enfants", "L'asthme est dû au tabac", "Il n'y en a pas"]),
    num(2, _q_ves),
    qcm(2, "Le système immunitaire adaptatif se distingue de l'inné par…", "sa spécificité et sa mémoire",
        ["sa rapidité", "l'absence de cellules", "le fait qu'il ne fonctionne qu'à la naissance"]),
    qcm(3, "À l'effort, le débit est multiplié par 5 mais la PAM augmente peu. Pourquoi ?",
        "Les résistances périphériques chutent grâce à la vasodilatation musculaire", ["Le cœur ralentit",
        "Le volume sanguin diminue", "Les reins éliminent l'eau"], "PAM = Q × R."),
    qcm(3, "Un patient opéré de la hanche a le mollet gonflé, chaud et douloureux. Que faire ?",
        "Suspecter une thrombose veineuse profonde, ne pas masser, orienter en urgence", ["Masser pour drainer",
        "Faire marcher plus vite", "Appliquer de la glace et continuer"]),
    qcm(3, "Pourquoi une saturation reste-t-elle supérieure à 90 % quand la PO₂ artérielle baisse de 95 à 70 mmHg ?",
        "La courbe de dissociation est plate dans cette zone (forme en S)", ["L'Hb fabrique de l'O₂",
        "Le CO₂ compense", "La saturation ne dépend pas de la PO₂"]),
    num(3, _q_filtration),
    qcm(3, "Après la ménopause, quel changement hormonal explique la perte osseuse ?", "La baisse des œstrogènes",
        ["La hausse de l'insuline", "La baisse du cortisol", "La hausse de la testostérone"]),
]

CARDS = [
    ("Débit cardiaque", "Q = FC × VES (≈ 5 L/min au repos)"),
    ("Pression artérielle moyenne", "PAM = Q × R"),
    ("Frank-Starling", "Plus le ventricule se remplit, plus il éjecte"),
    ("Onde P / QRS / T", "Atria / ventricules / repolarisation ventriculaire"),
    ("Baroréflexe", "Stabilise la PA en quelques secondes"),
    ("Volume courant", "≈ 0,5 L"),
    ("VEMS", "Volume soufflé en 1 s d'expiration forcée"),
    ("Effet Bohr", "Acidose, chaleur, CO₂ : courbe vers la droite, l'Hb libère l'O₂"),
    ("P50 de l'hémoglobine", "≈ 27 mmHg"),
    ("Filtration rénale", "≈ 180 L/jour, 1-2 L d'urine"),
    ("Hémostase", "Vasoconstriction, clou plaquettaire, coagulation"),
    ("Immunité adaptative", "Spécifique avec mémoire (lymphocytes B et T)"),
    ("Asthme vs BPCO", "Obstruction réversible vs persistante"),
]

VIDEOS = [
    ("Le cycle cardiaque et l'ECG", "cycle cardiaque ECG explication animation"),
    ("Courbe de dissociation de l'hémoglobine", "courbe dissociation hémoglobine effet Bohr"),
    ("Physiologie rénale simplifiée", "physiologie du rein néphron filtration explication"),
    ("Adaptations cardiovasculaires à l'effort", "adaptations cardiovasculaires exercice physiologie"),
]

LINKS = [("Physiopedia : Cardiovascular system", "https://www.physio-pedia.com/index.php?search=cardiovascular+physiology")]
