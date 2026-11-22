import streamlit as st
from PIL import Image
import os

st.set_page_config(layout="wide")

st.title("Résolution Examen Méca")

# Helper to load images
def load_image(image_name):
    return Image.open(os.path.join("assets", "exam_meca", image_name))

tab1, tab2 = st.tabs(["Exercice 1: Thomas et ses balles", "Exercice 2: Questions Variées"])

with tab1:
    st.header("Exercice 1: Thomas veut faire rebondir des balles...")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Énoncé")
        st.write("""
        Thomas a deux balles en plastique avec une charge à leur centre.
        Les rayons des balles sont $R_1 = 3R = 0.3$ m et $R_2 = R = 0.1$ m.
        Leurs deux masses sont $3m = 0.03$ kg et $m = 0.01$ kg.
        Leurs deux charges sont $-6q = -6 \\times 10^{-7}$ C et $q = 10^{-7}$ C.
        Thomas pose la petite balle sur la grosse balle.
        
        En $t = 0$, Thomas lâche les deux balles d'une hauteur $h = 3.2$ m.
        Les positions verticales des centres sont notées par $z_1(t)$ et $z_2(t)$.
        
        En $t = t_*$, la grosse balle atteint le sol.
        Les collisions entre les balles et le sol sont **parfaitement élastiques**.
        Ces collisions sont aussi **instantanées et successives**.
        Après les chocs, les balles ont deux vitesses distinctes $v_1^+ < v_2^+$.
        Ensuite, un mouvement périodique par rebonds s'installe.
        La période de ce mouvement est $T$.
        
        Mais, c'était un problème trop simple pour Laurent !
        
        En $t = t_*$, Laurent crée un champ électrique dirigé vers le bas $\\vec{E}$.
        La norme de ce champ spatialement uniforme est $E = 10^6$ V/m.
        La grosse balle peut alors rattraper la petite balle en $t = t_{**}$.
        Le champ électrique est coupé dès que les deux balles sont en contact.
        
        Dans les calculs, on utilisera $g = 10$ m/s$^2$ et $k = 10^{10}$ N m$^2$/C$^2$.
        """)

    with col2:
        with st.expander("Voir l'image de l'énoncé", expanded=True):
            st.image(load_image("1.jpeg"))

       
    st.subheader("Questions")
    st.markdown("""
    1. Montrer que la force d'attraction électrique entre les deux charges est négligeable.
    """)
    with st.expander("Solution Question 1"):
        st.write("""
        **Méthode :**
        Pour montrer qu'une force est négligeable devant une autre, il faut calculer le rapport des deux forces.
        Ici, on compare la force d'attraction électrique $F_e$ (Loi de Coulomb) au poids $P$ de la petite balle (ou de la grosse, l'ordre de grandeur sera le même).
        
        **Calculs :**
        *   **Force électrique :** $F_e = k \\frac{|q_1 q_2|}{d^2}$
            *   Charges : $|q_1| = |-6q| = 6 \\cdot 10^{-7}$ C et $|q_2| = |q| = 10^{-7}$ C.
            *   Distance $d$ : Les balles sont l'une sur l'autre. La distance entre leurs centres est la somme des rayons : $d = R_1 + R_2 = 3R + R = 4R = 0.4$ m.
            *   $k = 10^{10}$ N m$^2$/C$^2$.
            $$F_e = 10^{10} \\frac{(6 \\cdot 10^{-7})(10^{-7})}{(0.4)^2} = 10^{10} \\frac{6 \\cdot 10^{-14}}{0.16} = \\frac{6 \\cdot 10^{-4}}{0.16} = \\frac{6}{1600} \\approx 0.00375 \\text{ N}$$
        
        *   **Poids de la petite balle :** $P = mg$
            *   $m = 0.01$ kg.
            *   $g = 10$ m/s$^2$.
            $$P = 0.01 \\times 10 = 0.1 \\text{ N}$$
        
        **Conclusion :**
        Le rapport $F_e / P = 0.00375 / 0.1 \\approx 0.0375$, soit environ **3.75%**.
        La force électrique est bien plus faible que le poids (un facteur ~25). On peut donc la négliger en première approximation pour l'étude de la chute.
        """)

    st.markdown("""
    2. Calculer le temps $t_*$ correspondant à la chute libre des deux balles.
    """)
    with st.expander("Solution Question 2"):
        st.write("""
        **Méthode :**
        C'est une chute libre sans vitesse initiale. On utilise l'équation horaire de la position selon l'axe vertical (dirigé vers le bas pour simplifier, ou vers le haut, le résultat est le même).
        Appelons $z(t)$ la position. L'accélération est $g$.
        
        **Calculs :**
        *   Loi horaires : $z(t) = \\frac{1}{2} g t^2$ (en prenant l'origine au point de lâcher et l'axe vers le bas).
        *   On cherche $t_*$ tel que la distance parcourue soit $h = 3.2$ m.
        $$h = \\frac{1}{2} g t_*^2 \\implies t_*^2 = \\frac{2h}{g} \\implies t_* = \\sqrt{\\frac{2h}{g}}$$
        *   Application numérique :
            *   $h = 3.2$ m
            *   $g = 10$ m/s$^2$
            $$t_* = \\sqrt{\\frac{2 \\times 3.2}{10}} = \\sqrt{\\frac{6.4}{10}} = \\sqrt{0.64} = 0.8 \\text{ s}$$
        
        **Résultat :**
        La chute dure **0.8 s**.
        """)

    st.markdown("""
    3. Calculer la vitesse $v$ avant la collision, puis les vitesses $v_1^+$ et $v_2^+$.
    """)
    with st.expander("Solution Question 3"):
        st.write("""
        **Méthode :**
        1.  **Vitesse avant choc ($v$)** : Conservation de l'énergie mécanique ou formule de cinématique de chute libre.
        2.  **Vitesse après choc ($v_1^+, v_2^+$)** : Il s'agit d'un problème de collisions successives.
            *   **Choc 1 (Grosse balle - Sol)** : Rebond élastique sur un mur immobile infiniment lourd. La vitesse s'inverse.
            *   **Choc 2 (Grosse balle - Petite balle)** : Choc élastique entre deux masses. On utilise la conservation de la quantité de mouvement et de l'énergie cinétique.
        
        **Calculs :**
        
        **A. Vitesse $v$ juste avant le sol :**
        $$v = gt_* = 10 \\times 0.8 = 8 \\text{ m/s}$$
        Les deux balles descendent à $8$ m/s.
        
        **B. Vitesse après le rebond sol (Grosse balle $3m$) :**
        Juste après le contact avec le sol, la grosse balle repart vers le haut avec la même vitesse (choc élastique).
        Vitesse de la grosse balle ($3m$) : $v_{3m} = +v = 8$ m/s (vers le haut).
        Vitesse de la petite balle ($m$) : $v_{m} = -v = -8$ m/s (vers le bas, elle n'a pas encore touché).
        
        **C. Choc Grosse balle ($3m$) - Petite balle ($m$) :**
        On a un choc élastique 1D.
        *   Masse 1 (grosse) : $M_1 = 3m$, vitesse initiale $u_1 = +v$.
        *   Masse 2 (petite) : $M_2 = m$, vitesse initiale $u_2 = -v$.
        
        Formules du choc élastique pour les vitesses finales $v_1^+$ (grosse) et $v_2^+$ (petite) :
        $$v_1^+ = \\frac{M_1 - M_2}{M_1 + M_2} u_1 + \\frac{2 M_2}{M_1 + M_2} u_2$$
        $$v_2^+ = \\frac{2 M_1}{M_1 + M_2} u_1 + \\frac{M_2 - M_1}{M_1 + M_2} u_2$$
        
        Calcul de $v_1^+$ (grosse balle, notée 1 dans l'énoncé) :
        $$v_1^+ = \\frac{3m - m}{3m + m} (v) + \\frac{2m}{3m + m} (-v)$$
        $$v_1^+ = \\frac{2m}{4m} v - \\frac{2m}{4m} v = \\frac{1}{2} v - \\frac{1}{2} v = 0 \\text{ m/s}$$
        La grosse balle s'arrête net !
        
        Calcul de $v_2^+$ (petite balle, notée 2 dans l'énoncé) :
        $$v_2^+ = \\frac{2(3m)}{4m} (v) + \\frac{m - 3m}{4m} (-v)$$
        $$v_2^+ = \\frac{6}{4} v + \\frac{-2}{4} (-v) = \\frac{3}{2} v + \\frac{1}{2} v = 2v$$
        $$v_2^+ = 2 \\times 8 = 16 \\text{ m/s}$$
        
        **Résultat :**
        *   Vitesse avant choc : **8 m/s**.
        *   Vitesse grosse balle après ($v_1^+$) : **0 m/s**.
        *   Vitesse petite balle après ($v_2^+$) : **16 m/s**.
        """)
    st.markdown("""
    4. Tracer les courbes $z_1(t) - 3R$ et $z_2(t) - 7R$ si le champ électrique $E$ n'est jamais enclenché.
        Quelle est la hauteur maximale atteinte par la petite balle ?
        Quelle est la période $T$ du mouvement par rebonds ?
    """)
    with st.expander("Solution Question 4"):
        st.write("""
        **Méthode :**
        Après le choc en $t_* = 0.8$ s :
        *   La grosse balle (1) a une vitesse nulle ($v_1^+ = 0$). Elle reste au sol (en équilibre, soutenue par le sol). Sa position est $z_1(t) = R_1 = 3R$. Donc $z_1(t) - 3R = 0$.
        *   La petite balle (2) part de $z_2(t_*) = R_1 + R_1 + R_2 = 7R$ avec une vitesse $v_2^+ = 16$ m/s vers le haut. C'est une chute libre avec vitesse initiale.
        
        **Hauteur maximale :**
        L'énergie cinétique initiale est convertie en énergie potentielle.
        Gain de hauteur : $\\Delta h = \\frac{(v_2^+)^2}{2g}$.
        $$\\Delta h = \\frac{16^2}{2 \\times 10} = \\frac{256}{20} = 12.8 \\text{ m}$$
        
        Hauteur totale par rapport au sol (centre de la balle) :
        $$H_{max} = z_2(t_*) + \\Delta h = 7R + 12.8 = 0.7 + 12.8 = 13.5 \\text{ m}$$
        
        (Ou si la question demande la hauteur par rapport à la position de départ $7R$, c'est $12.8$ m).
        
        **Période $T$ :**
        Le mouvement est périodique car la petite balle retombe sur la grosse balle (qui n'a pas bougé).
        La période $T$ correspond à la durée du vol de la petite balle.
        $$T = 2 \\times t_{montée} = 2 \\times \\frac{v_2^+}{g}$$
        $$T = 2 \\times \\frac{16}{10} = 3.2 \\text{ s}$$
        
        Pendant ce temps, $z_1(t) - 3R$ reste à 0.
        $z_2(t) - 7R$ décrit une parabole partant de 0, montant à 12.8m, et revenant à 0 en 3.2s.
        """)
        st.image(load_image("trajectory_q4.png"), caption="Trajectoires sans champ électrique (Q4)")

    st.markdown("""
    5. Calculer le temps $t_{**}$ lorsque la grosse balle rattrape la petite.
        Que deviennent les courbes $z_1(t) - 3R$ et $z_2(t) - 7R$ pour $t \\in [t_*, t_{**}]$ ?
    """)
    with st.expander("Solution Question 5"):
        st.write("""
        **Interprétation de l'énoncé :**
        Le champ électrique est enclenché en $t = t_* = 0.8$ s, juste après le rebond des balles.
        Nous devons calculer le temps $t_{**}$ où la grosse balle rattrape la petite.
        
        **Dynamique avec champ électrique ($t > t_*$) :**
        Définissons $t' = t - t_*$ comme le temps écoulé depuis l'activation du champ.
        
        1.  **Grosse balle ($3m, -6q$) :**
            *   Position initiale en $t_*$: $z_1(t_*) = R_1 = 3R = 0.3$ m (centre de la balle au sol).
            *   Vitesse initiale en $t_*$: $v_1^+ = 0$ m/s.
            *   Forces : Poids $P_1 = 3mg = 0.03 \\times 10 = 0.3$ N (vers le bas).
            *   Force électrique $F_{e1} = q_1 E = (-6 \\times 10^{-7}) (10^6) = -0.6$ N (vers le haut, car $q_1 < 0$ et $\\vec{E}$ vers le bas).
            *   Force nette : $F_{net1} = P_1 + F_{e1} = 0.3 - 0.6 = -0.3$ N (vers le haut).
            *   Accélération : $a_1 = F_{net1} / (3m) = -0.3 / 0.03 = -10$ m/s$^2$. (L'accélération est de $10$ m/s$^2$ vers le haut).
            *   Équation horaire pour $z_1(t')$ (axe $z$ vers le haut, origine au sol) :
                $$z_1(t') = z_1(t_*) + v_1^+ t' + \\frac{1}{2} a_1 t'^2 = 0.3 + 0 \\cdot t' + \\frac{1}{2} (10) t'^2 = 0.3 + 5 t'^2$$
        
        2.  **Petite balle ($m, q$) :**
            *   Position initiale en $t_*$: $z_2(t_*) = R_1 + R_1 + R_2 = 3R + 3R + R = 7R = 0.7$ m (centre de la petite balle posée sur la grosse).
            *   Vitesse initiale en $t_*$: $v_2^+ = 16$ m/s (vers le haut).
            *   Forces : Poids $P_2 = mg = 0.01 \\times 10 = 0.1$ N (vers le bas).
            *   Force électrique $F_{e2} = q E = (10^{-7}) (10^6) = 0.1$ N (vers le bas, car $q > 0$ et $\\vec{E}$ vers le bas).
            *   Force nette : $F_{net2} = P_2 + F_{e2} = 0.1 + 0.1 = 0.2$ N (vers le bas).
            *   Accélération : $a_2 = F_{net2} / m = 0.2 / 0.01 = 20$ m/s$^2$. (L'accélération est de $20$ m/s$^2$ vers le bas).
            *   Équation horaire pour $z_2(t')$ (axe $z$ vers le haut, origine au sol) :
                $$z_2(t') = z_2(t_*) + v_2^+ t' + \\frac{1}{2} a_2 t'^2 = 0.7 + 16 t' - \\frac{1}{2} (20) t'^2 = 0.7 + 16 t' - 10 t'^2$$
        
        **Calcul de $t_{**}$ (Rattrapage) :**
        La grosse balle rattrape la petite lorsque leurs centres sont séparés par la somme de leurs rayons, c'est-à-dire $R_1 + R_2 = 4R = 0.4$ m.
        Puisque la grosse balle est en dessous, on a $z_2(t') - z_1(t') = 0.4$.
        
        $$(0.7 + 16 t' - 10 t'^2) - (0.3 + 5 t'^2) = 0.4$$
        $$0.4 + 16 t' - 15 t'^2 = 0.4$$
        $$16 t' - 15 t'^2 = 0$$
        $$t'(16 - 15 t') = 0$$
        
        Deux solutions pour $t'$ :
        $t'_1 = 0$ s (Contact initial au rebond).
        $t'_2 = 16/15 \\approx 1.067$ s (Rattrapage).
        
        Le temps absolu $t_{**}$ est $t_* + t' = 0.8 + 1.067 = 1.867$ s.
        
        **Résultat :**
        La grosse balle rattrape la petite en $t_{**} \\approx 1.87$ s.
        
        **Courbes pour $t \\in [t_*, t_{**}]$ :**
        *   $z_1(t) - 3R$ : La grosse balle décolle du sol et sa position $z_1(t')$ est une parabole ascendante ($0.3 + 5t'^2$).
        *   $z_2(t) - 7R$ : La petite balle part avec une vitesse initiale vers le haut ($16$ m/s), mais son accélération est fortement dirigée vers le bas ($20$ m/s$^2$). Elle monte, atteint un sommet, puis redescend.
        """)
        st.image(load_image("trajectory_q5.png"), caption="Trajectoires avec champ électrique (Q5)")

    st.markdown("""
    6. Le champ électrique généré par Laurent est-il réaliste d'un point de vue physique ?
    """)
    with st.expander("Solution Question 6"):
        st.write("""
        **Analyse :**
        La valeur du champ est $E = 10^6$ V/m.
        *   **Comparaison avec le claquage de l'air :** La rigidité diélectrique de l'air sec est d'environ $3 \\times 10^6$ V/m (3 kV/mm).
        *   Le champ proposé ($1$ kV/mm) est en dessous de la limite de claquage, donc il ne provoquera pas d'arc électrique spontané immédiat (éclairs).
        *   Cependant, il est proche de la limite (facteur 3). Il est "réaliste" techniquement (on sait faire de tels champs en labo haute tension), mais dangereux et difficile à maintenir sur une grande distance ($h \\sim 13$m implique une différence de potentiel de 13 millions de Volts !).
        
        **Conclusion :**
        Oui, c'est théoriquement réaliste (on ne dépasse pas la limite physique ultime), mais expérimentalement très complexe à réaliser sur un grand volume.
        """)
    st.markdown("""
    7. Mais, c'est encore un problème trop simple pour Vincent !
        Il souhaite introduire une force de trainée $F = -Kv^2$ avec $K = 0.4$ kg/m.
        On suppose aussi maintenant qu'aucun champ électrique n'est présent !
        Quelle est l'équation différentielle gouvernant la chute des deux balles avec cette trainée ?
    """)
    with st.expander("Solution Question 7"):
        st.write("""
        **Modélisation :**
        Les deux balles tombent ensemble (la petite posée sur la grosse).
        On considère le système {Grosse balle + Petite balle} comme un seul objet physique.
        *   Masse totale $M_{tot} = 3m + m = 4m = 4 \\times 0.01 = 0.04$ kg.
        *   Forces appliquées :
            1.  Poids total $P = M_{tot} g$ (vers le bas).
            2.  Trainée $F = -Kv^2$ (vers le haut, opposée à la vitesse).
        
        **Newton (2ème loi) :**
        $$M_{tot} \\cdot a = P - F_{trainée}$$
        (On projette sur un axe vertical descendant, donc $a = \\dot{v}$, $P > 0$, $F_{trainée}$ s'oppose donc $-Kv^2$ si on considère la force en norme, ou alors la force est $-Kv^2$ vecteur et on projette... Bref, l'accélération diminue quand $v$ augmente).
        
        $$M_{tot} \\frac{dv}{dt} = M_{tot} g - K v^2$$
        
        En divisant par $M_{tot}$ :
        $$\\frac{dv}{dt} = g - \\frac{K}{M_{tot}} v^2$$
        """)

    st.markdown("""
    8. Calculer la vitesse critique $v_*$ associée à cette équation.
    """)
    with st.expander("Solution Question 8"):
        st.write("""
        **Définition :**
        La vitesse critique (ou vitesse limite) est atteinte lorsque l'accélération devient nulle (équilibre entre le poids et la trainée).
        La vitesse devient constante.
        
        **Calcul :**
        On pose $\\frac{dv}{dt} = 0$.
        $$0 = g - \\frac{K}{M_{tot}} v_*^2$$
        $$v_*^2 = \\frac{M_{tot} g}{K}$$
        $$v_* = \\sqrt{\\frac{M_{tot} g}{K}}$$
        
        **Application numérique :**
        *   $M_{tot} = 0.04$ kg.
        *   $g = 10$ m/s$^2$.
        *   $K = 0.4$ kg/m.
        
        $$v_* = \\sqrt{\\frac{0.04 \\times 10}{0.4}} = \\sqrt{\\frac{0.4}{0.4}} = \\sqrt{1} = 1 \\text{ m/s}$$
        
        La vitesse limite est de **1 m/s**. (C'est très lent ! Ça frotte beaucoup).
        """)

    st.markdown("""
    9. Résoudre cette équation différentielle.
    """)
    with st.expander("Solution Question 9"):
        st.write("""
        **Méthode : Séparation des variables**
        On repart de l'équation : $\\frac{dv}{dt} = g - \\frac{K}{M_{tot}} v^2$.
        On factorise par $g$ et on utilise $v_*^2 = \\frac{M_{tot} g}{K}$ (donc $\\frac{K}{M_{tot}} = \\frac{g}{v_*^2}$) :
        $$\\frac{dv}{dt} = g \\left( 1 - \\frac{v^2}{v_*^2} \\right)$$
        
        On sépare les variables $v$ et $t$ :
        $$\\frac{dv}{1 - \\left(\\frac{v}{v_*}\\right)^2} = g dt$$
        
        On intègre les deux côtés.
        A gauche, on pose le changement de variable $u = v/v_*$, donc $du = dv/v_*$ ou $dv = v_* du$.
        $$\\int \\frac{v_* du}{1 - u^2} = \\int g dt$$
        $$v_* \\int \\frac{du}{1 - u^2} = g t + C$$
        
        D'après l'indice de l'énoncé : $\\int \\frac{dx}{1-x^2} = \\text{arctanh}(x)$.
        $$v_* \\text{arctanh}(u) = gt + C$$
        $$v_* \\text{arctanh}\\left(\\frac{v}{v_*}\\right) = gt$$
        (La constante $C$ est nulle car à $t=0$, $v=0$).
        
        On isole $v$ :
        $$\\text{arctanh}\\left(\\frac{v}{v_*}\\right) = \\frac{gt}{v_*}$$
        $$\\frac{v}{v_*} = \\tanh\\left(\\frac{gt}{v_*}\\right)$$
        $$v(t) = v_* \\tanh\\left(\\frac{gt}{v_*}\\right)$$
        
        **Résultat final :**
        $$v(t) = 1 \\cdot \\tanh\\left(\\frac{10 t}{1}\\right) = \\tanh(10 t) \\text{ m/s}$$
        """)
    
    st.info("Répondez à chaque sous-question et uniquement à ce qui est demandé. Chaque sous-question peut être résolue de manière symbolique, si les résultats précédents font défaut ! Pensez à encadrer les résultats principaux pour les mettre en évidence.")
    st.latex(r"\int \frac{dx}{1-x^2} = \text{arctanh}(x) = \frac{1}{2} \ln \left[ \frac{1+x}{1-x} \right] \text{ et } \tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}")

with tab2:
    st.header("Exercice 2: Questions Variées")
    
    # Q 2.1
    st.subheader("Q 2.1: Circuit et Puissance")
    col21_txt, col21_img = st.columns([1, 1])
    with col21_txt:
        st.write("""
        Deux piles modélisées par leurs forces électromotrices $V_1$ et $V_2$ avec leurs résistances internes $R_1$ et $R_2$ sont montées en opposition.
        La borne positive d'une pile est reliée à la borne négative de l'autre pile.
        Ensuite ces deux piles sont connectées à une résistance externe $R_3$.
        
        *   $R_1 = 0.9$ $\\Omega$, $V_1 = 9.0$ V
        *   $R_2 = 1.8$ $\\Omega$, $V_2 = 9.0$ V
        *   $R_3 = 2.4$ $\\Omega$
        
        **Quelle la puissance $P$ dissipée dans la résistance externe ?**
        """)
    
    with col21_img:
         with st.expander("Image Q 2.1, Q 2.2 & Q 2.4"):
            st.image(load_image("2.1 & 2.2 & 2.3.jpeg"))

    with st.expander("Solution Q 2.1"):
        st.write("""
        **Analyse du schéma :**
        Le terme "montées en opposition" avec "borne positive reliée à la borne négative" peut porter à confusion s'il s'agissait d'une seule maille (ce serait une série additive).
        Cependant, le schéma (et les annotations d'étudiant visible) montre clairement une structure à **deux mailles** (deux piles en parallèle alimentant la résistance centrale).
        
        On a donc :
        *   Branche 1 : Générateur de Thévenin ($V_1, R_1$).
        *   Branche 2 : Générateur de Thévenin ($V_2, R_2$).
        *   Branche 3 (centrale) : Résistance $R_3$.
        
        Les deux générateurs sont orientés pour débiter dans la branche centrale (mémé sens).
        
        **Méthode des noeuds (Millman) :**
        Calculons la tension $U_{AB}$ aux bornes de $R_3$.
        $$U_{AB} = \\frac{\\frac{V_1}{R_1} + \\frac{V_2}{R_2} + \\frac{0}{R_3}}{\\frac{1}{R_1} + \\frac{1}{R_2} + \\frac{1}{R_3}}$$
        
        *   $V_1/R_1 = 9.0 / 0.9 = 10$ A.
        *   $V_2/R_2 = 9.0 / 1.8 = 5$ A.
        *   Somme numérateur = $15$ A.
        
        *   $1/R_1 = 1/0.9 \\approx 1.11$ S.
        *   $1/R_2 = 1/1.8 \\approx 0.55$ S.
        *   $1/R_3 = 1/2.4 \\approx 0.416$ S.
        *   Pour être précis, utilisons des fractions :
            $$1/0.9 = 10/9$$
            $$1/1.8 = 5/9$$
            $$1/2.4 = 5/12$$
            Somme = $15/9 + 5/12 = 5/3 + 5/12 = 20/12 + 5/12 = 25/12$ S.
        
        $$U_{AB} = \\frac{15}{25/12} = 15 \\times \\frac{12}{25} = 3 \\times \\frac{12}{5} = \\frac{36}{5} = 7.2 \\text{ V}$$
        
        **Puissance :**
        $$P = \\frac{U_{AB}^2}{R_3}$$
        $$P = \\frac{(7.2)^2}{2.4} = \\frac{51.84}{2.4} = 21.6 \\text{ W}$$
        
        (Autre calcul rapide : $7.2 / 2.4 = 3$ A. $P = 3 \\times 7.2 = 21.6$ W).
        """)

    st.divider()

    # Q 2.2
    st.subheader("Q 2.2: Charge RC")
    col22_txt, col22_img = st.columns([1, 1])
    with col22_txt:
        st.write("""
        A l'instant $t=0$, on commence à charger un condensateur de capacité inconnue $C$ avec une source de tension constante $V$ connectée en série avec une résistance $R=1$ k$\\Omega$.
        Ensuite, on mesure la charge à deux instants $t_1$ et $t_2 = t_1 + 20$ ms :
        
        $$Q(t_1) = (1 - 1/e) Q_{max}$$
        $$Q(t_2) = (1 - 1/e^2) Q_{max}$$
        
        **Quelle est la valeur de $C$ ?**
        """)
        
    with col22_img:
         # Same image as 2.1
        pass

    with st.expander("Solution Q 2.2"):
        st.write("""
        **Loi de charge :**
        $$Q(t) = Q_{max} \\left( 1 - e^{-t/\\tau} \\right)$$ avec $\\tau = RC$.
        
        **Système d'équations :**
        1.  $Q(t_1) = Q_{max} (1 - e^{-1})$. Ceci implique que le terme exponentiel vaut $e^{-1}$.
            $$e^{-t_1/\\tau} = e^{-1} \\implies t_1/\\tau = 1 \\implies t_1 = \\tau$$
        
        2.  $Q(t_2) = Q_{max} (1 - e^{-2})$. De même :
            $$e^{-t_2/\\tau} = e^{-2} \\implies t_2/\\tau = 2 \\implies t_2 = 2\\tau$$
        
        **Donnée temporelle :**
        On sait que $t_2 = t_1 + 20$ ms.
        En remplaçant :
        $$2\\tau = \\tau + 20 \\text{ ms}$$
        $$\\tau = 20 \\text{ ms}$$
        
        **Calcul de C :**
        $\\tau = RC \\implies C = \\tau / R$.
        *   $\\tau = 20 \\times 10^{-3}$ s.
        *   $R = 1 \\text{ k}\\Omega = 10^3 \\Omega$.
        
        $$C = \\frac{20 \\times 10^{-3}}{10^3} = 20 \\times 10^{-6} \\text{ F} = 20 \\mu\\text{F}$$
        """)

    st.divider()

    # Q 2.3
    st.subheader("Q 2.3: Condensateur et Diélectrique")
    col23_txt, col23_img = st.columns([1, 1])
    with col23_txt:
        st.write("""
        Un condensateur a deux plaques distantes de $d=1$ mm.
        La surface des plaques est $S=100$ cm$^2$.
        On charge le condensateur avec une source de tension constante $V=100$ V.
        Ensuite, la source est déconnectée : le condensateur est isolé.
        Finalement, on insère une lame diélectrique de permittivité relative $\\epsilon_r = 5$.
        Dans les calculs, on approximera $\\epsilon_0 \\approx 10^{-11}$ F/m.
        Tous les effets de bord sont négligés.
        
        **Quelle est l'énergie $U$ dans le condensateur isolé avec le diélectrique ?**
        """)
    
    with st.expander("Solution Q 2.3"):
        st.write("""
        **Étape 1 : Avant insertion (dans le vide/air)**
        *   Capacité $C_0 = \\frac{\\epsilon_0 S}{d}$.
            *   $\\epsilon_0 = 10^{-11}$ F/m.
            *   $S = 100 \\text{ cm}^2 = 100 \\times 10^{-4} \\text{ m}^2 = 10^{-2} \\text{ m}^2$.
            *   $d = 1 \\text{ mm} = 10^{-3} \\text{ m}$.
            $$C_0 = \\frac{10^{-11} \\times 10^{-2}}{10^{-3}} = 10^{-10} \\text{ F}$$
        *   Charge $Q_0$ acquise sous $V=100$ V :
            $$Q_0 = C_0 V = 10^{-10} \\times 100 = 10^{-8} \\text{ C}$$
        *   Énergie initiale $U_0 = \\frac{1}{2} C_0 V^2 = \\frac{1}{2} Q_0 V = 0.5 \\times 10^{-6}$ J.
        
        **Étape 2 : Condensateur isolé**
        La source est déconnectée $\\rightarrow$ La **charge $Q$ reste constante**.
        $$Q = Q_0 = 10^{-8} \\text{ C}$$
        
        **Étape 3 : Avec diélectrique**
        La capacité change : $C' = \\epsilon_r C_0$.
        $$C' = 5 \\times C_0 = 5 \\cdot 10^{-10} \\text{ F}$$
        
        **Calcul de l'énergie finale :**
        On utilise la formule avec $Q$ (car $Q$ est constant, $V$ change) :
        $$U = \\frac{1}{2} \\frac{Q^2}{C'}$$
        $$U = \\frac{1}{2} \\frac{(10^{-8})^2}{5 \\cdot 10^{-10}} = \\frac{1}{2} \\frac{10^{-16}}{5 \\cdot 10^{-10}}$$
        $$U = \\frac{1}{10} 10^{-6} = 10^{-7} \\text{ J}$$
        
        **Note :** L'énergie a diminué (divisée par $\\epsilon_r$). Le travail fourni pour insérer le diélectrique est négatif (le diélectrique est aspiré).
        """)

    st.divider()

    # Q 2.4
    st.subheader("Q 2.4: Bloc et Ressort")
    col24_txt, col24_img = st.columns([1, 1])
    with col24_txt:
        st.write("""
        Un bloc de masse $m$ est coincé entre un ressort de raideur $k$ et le sol.
        Le ressort, de longueur initiale $h_0$, est comprimé à une longueur $h < h_0$.
        Le coefficient de frottement statique entre le bloc et le sol est noté $\\mu_s$.
        
        **Quelle est l'expression de la force minimale $F$ requise pour mettre le bloc en mouvement ?**
        """)
        
    with col24_img:
        with st.expander("Image Q 2.4 & Q 2.5"):
            st.image(load_image("2.4 & 2.5.jpeg"))

    with st.expander("Solution Q 2.4"):
        st.write("""
        **Bilan des forces :**
        Nous cherchons la condition limite de glissement (Loi de Coulomb : $F_{frot} = \\mu_s N$).
        
        1.  **Axe Vertical (y) :**
            *   Poids $P = mg$ (vers le bas).
            *   Force du ressort $F_k$. Le ressort est comprimé (longueur $h < h_0$). Il pousse donc vers le bas sur le bloc.
                *   Compression $\\Delta x = h_0 - h$.
                *   $F_k = k(h_0 - h)$.
            *   Réaction normale du sol $N$ (vers le haut).
            
            Équilibre vertical : $N = P + F_k = mg + k(h_0 - h)$.
        
        2.  **Axe Horizontal (x) :**
            *   Force de poussée $F$.
            *   Frottement statique $f$ (opposé au mouvement).
            
            Pour bouger, il faut vaincre le frottement maximal : $F > f_{max} = \\mu_s N$.
        
        **Résultat :**
        $$F_{min} = \\mu_s (mg + k(h_0 - h))$$
        """)

    st.divider()

    # Q 2.5
    st.subheader("Q 2.5: Catapulte")
    col25_txt, col25_img = st.columns([1, 1])
    with col25_txt:
        st.write("""
        Une catapulte est composée d'un ressort, d'un tube et de deux blocs de masse $m$.
        Le premier bloc est posé sur le ressort de raideur $k$ comprimé d'une longueur $h$.
        Le second bloc est posé sur la sortie du tube à une hauteur $h_0$ au dessus du premier.
        On libère le ressort, le bloc du bas est propulsé et atteint le second bloc.
        La collision est parfaitement inélastique : les deux blocs restent collés.
        Ensuite, l'ensemble des deux blocs continue à monter jusqu'à une hauteur maximale $h_{max}$.
        Tous les frottements sont négligés.
        
        Note: Le schéma montre $h$ comme la compression (ou hauteur initiale?) et $h_0$ la distance de separation. La question demande $h$ maximale ($h_{max}$ pour éviter confusion).
        
        **Quelle est l'expression de la hauteur maximale atteinte par les deux blocs ?**
        """)
    
    with col25_img:
        pass

    with st.expander("Solution Q 2.5"):
        st.write("""
        Le problème se décompose en 3 phases.
        
        **Phase 1 : Propulsion (Conservation de l'énergie)**
        *   Etat initial : Ressort comprimé de $h$ (énergie $1/2 k h^2$), vitesse nulle.
        *   Etat intermédiaire (juste avant choc) : Le bloc 1 monte de $h_0$. Vitesse $v_1$.
        $$E_{init} = E_{avant\\_choc} \\implies \\frac{1}{2} k h^2 = m g h_0 + \\frac{1}{2} m v_1^2$$
        $$v_1^2 = \\frac{2}{m} (\\frac{1}{2} k h^2 - m g h_0) = \\frac{k h^2}{m} - 2 g h_0$$
        
        **Phase 2 : Collision Inélastique (Conservation de la quantité de mouvement)**
        *   Juste avant : Bloc 1 ($m$, $v_1$), Bloc 2 ($m$, $0$).
        *   Juste après : Ensemble ($2m$, $v'$).
        $$m v_1 = (m + m) v' \\implies v' = \\frac{v_1}{2}$$
        
        **Phase 3 : Ascension finale (Conservation de l'énergie)**
        *   L'ensemble de masse $2m$ part de la hauteur $h_0$ avec vitesse $v'$ et monte de $\\Delta H$.
        *   Energie cinétique après choc : $E_c' = \\frac{1}{2} (2m) v'^2 = m (\\frac{v_1}{2})^2 = \\frac{1}{4} m v_1^2$.
        *   Cette énergie est convertie en potentiel : $E_c' = (2m) g \\Delta H$.
        
        $$\\Delta H = \\frac{E_c'}{2mg} = \\frac{\\frac{1}{4} m v_1^2}{2mg} = \\frac{v_1^2}{8g}$$
        
        En remplaçant $v_1^2$ :
        $$\\Delta H = \\frac{1}{8g} (\\frac{k h^2}{m} - 2 g h_0) = \\frac{k h^2}{8mg} - \\frac{h_0}{4}$$
        
        **Hauteur Maximale Totale (depuis le point de départ du bloc 2, soit $h_0$ à partir du bas) :**
        Nous mesurons par rapport au sol (bas du tube) ? Le bloc 2 était à $h_0$.
        $$H_{max} = h_0 + \\Delta H = h_0 + \\frac{k h^2}{8mg} - \\frac{h_0}{4}$$
        $$H_{max} = \\frac{3}{4} h_0 + \\frac{k h^2}{8mg}$$
        """)

    st.divider()

    # Q 2.6
    st.subheader("Q 2.6: Roue et Amortisseur")
    col26_txt, col26_img = st.columns([1, 1])
    with col26_txt:
        st.write("""
        Un cylindre plein de rayon $R$ et de masse $m$ roule sans glisser à vitesse constante $v = R\\omega$.
        La roue descend sur un plan incliné qui a un angle $\\phi$ avec l'horizontale.
        La roue est équipée d'un amortisseur visqueux rotatif composé d'un rotor et d'un stator.
        Un fluide visqueux est cisaillé entre ces deux éléments de l'amortisseur.
        Cet amortisseur exerce uniquement un moment $\\tau = K\\omega$ qui s'oppose à la rotation.
        Tous les frottements avec l'air sont négligés.
        
        **Quelle est l'expression de la vitesse de rotation $\\omega$ de la roue ?**
        """)
        
    with col26_img:
         with st.expander("Image Q 2.6 & Q 2.7"):
            st.image(load_image("2.6 & 2.7.jpeg"))

    with st.expander("Solution Q 2.6"):
        st.write(r"""
        **Méthode des Puissances (le plus simple) :**
        La vitesse est constante, donc l'énergie cinétique est constante.
        La puissance fournie par les forces motrices compense exactement la puissance dissipée.
        
        1.  **Puissance motrice (Poids) :**
            Le poids fait avancer la roue. La composante active est $F_{g, //}$.
            $P_{g} = \vec{P} \cdot \vec{v} = (mg \sin \phi) v$.
            Comme $v = R\omega$, $P_g = mg R \sin \phi \cdot \omega$.
        
        2.  **Puissance résistante (Amortisseur) :**
            Le couple résistant est $\tau = K\omega$.
            $P_{diss} = \tau \omega = K \omega^2$.
        
        (Note : La force de frottement au point de contact ne travaille pas car la vitesse du point de contact est nulle en roulement sans glissement).
        
        **Bilan :**
        $$P_g = P_{diss}$$
        $$mg R \sin \phi \cdot \omega = K \omega^2$$
        
        En simplifiant par $\omega$ (non nul) :
        $$\omega = \frac{mg R \sin \phi}{K}$$
        """)

    st.divider()

    # Q 2.7
    st.subheader("Q 2.7: Bille sur barre")
    col27_txt, col27_img = st.columns([1, 1])
    with col27_txt:
        st.write("""
        Une bille de masse $m$ est fixée à l'extrémité d'une barre rigide.
        La tige, de longueur $L$ et de masse négligeable, peut tourner librement autour d'un axe fixe.
        Initialement, la bille est située presque à la verticale au-dessus de l'axe ($\\theta = \\epsilon$) et est immobile. Toutefois, cette position est instable !
        Sous l'effet de la gravité, la bille et la tige se mettent progressivement en mouvement.
        La bille descend alors et puis remonte vers sa hauteur initiale ($\\theta = 2\\pi - \\epsilon$).
        Tous les frottements sont négligés.
        
        **Quelle est l'expression de la vitesse angulaire $\\omega(\\theta)$ ?**
        """)
        
    with st.expander("Solution Q 2.7"):
        st.write(r"""
        **Méthode : Conservation de l'Énergie Mécanique**
        Le sytème est conservatif (pas de frottements).
        L'énergie totale est : $E = E_{cinétique} + E_{potentielle}$.
        
        1.  **État Initial ($\theta \approx 0$, disons position haute) :**
            *   Vitesse nulle $\implies E_k = 0$.
            *   Hauteur $z = L$ (si on place l'origine au pivot). Ou $z=2L$ si sol en bas.
            *   Prenons l'origine des potentiels au pivot ($z=0$ au centre).
            *   La bille est en haut : $z_{init} = +L$.
            *   $E_{init} = m g L$.
        
        2.  **État Quelconque (angle $\theta$) :**
            *   La hauteur de la bille est $z(\theta) = L \cos \theta$ (Attention à la convention d'angle, ici $\theta=0$ en haut est cohérent avec l'énoncé qui dit "descend puis remonte à $2\pi$").
            *   Vitesse linéaire : $v = L \omega$.
            *   $E_{cin} = \frac{1}{2} m v^2 = \frac{1}{2} m L^2 \omega^2$.
            *   $E_{pot} = m g z = m g L \cos \theta$.
            *   $E_{tot} = \frac{1}{2} m L^2 \omega^2 + m g L \cos \theta$.
        
        **Conservation :**
        $$E_{init} = E_{tot}$$
        $$m g L = \frac{1}{2} m L^2 \omega^2 + m g L \cos \theta$$
        
        On simplifie par $m$ et $L$ (non nuls) :
        $$g = \frac{1}{2} L \omega^2 + g \cos \theta$$
        $$\frac{1}{2} L \omega^2 = g - g \cos \theta = g (1 - \cos \theta)$$
        $$\omega^2 = \frac{2g}{L} (1 - \cos \theta)$$
        
        $$\omega(\theta) = \sqrt{\frac{2g}{L} (1 - \cos(\theta))}$$
        """)

    st.divider()

    # Q 2.8
    st.subheader("Q 2.8: Sphère chargée")
    col28_txt, col28_img = st.columns([1, 1])
    with col28_txt:
        st.write("""
        Une sphère de rayon $a$ a une densité de charge volumique $\\rho$.
        Cette sphère est dans une coquille de rayon $b$ avec une charge surfacique $\\sigma$.
        Il n'y a aucune autre charge présente dans l'univers de la question !
        
        **Quelle doit être le rapport entre les densités de charge $\\rho$ et $\\sigma$ afin que le champ électrique soit nul à l'extérieur de la coquille sphérique ?**
        """)
        
    with col28_img:
        with st.expander("Image Q 2.8"):
            st.image(load_image("2.8.jpeg"))

    with st.expander("Solution Q 2.8"):
        st.write(r"""
        **Théorème de Gauss :**
        Pour une symétrie sphérique, le champ électrique à l'extérieur d'une distribution de charge ne dépend que de la **charge totale** contenue à l'intérieur.
        $$E_{ext} \propto Q_{totale}$$
        Pour que le champ soit nul à l'extérieur ($r > b$), il faut que la charge totale apparente soit nulle.
        
        **Calcul des charges :**
        1.  **Sphère interne (Pleine) :**
            *   Rayon $a$, densité volumique $\rho$.
            *   Charge $Q_{sphere} = \text{Volume} \times \rho = \frac{4}{3} \pi a^3 \rho$.
        
        2.  **Coquille externe (Surface) :**
            *   Rayon $b$, densité surfacique $\sigma$.
            *   Charge $Q_{coquille} = \text{Surface} \times \sigma = 4 \pi b^2 \sigma$.
        
        **Condition d'annulation :**
        $$Q_{totale} = Q_{sphere} + Q_{coquille} = 0$$
        $$\frac{4}{3} \pi a^3 \rho + 4 \pi b^2 \sigma = 0$$
        
        On simplifie par $4\pi$ :
        $$\frac{1}{3} a^3 \rho + b^2 \sigma = 0$$
        $$b^2 \sigma = - \frac{1}{3} a^3 \rho$$
        
        **Rapport demandé ($\rho$ et $\sigma$) :**
        Exprimons le ratio $\rho / \sigma$ :
        $$\frac{\rho}{\sigma} = - \frac{3 b^2}{a^3}$$
        
        (Cela signifie que les charges doivent être de signes opposés pour se compenser).
        """)
