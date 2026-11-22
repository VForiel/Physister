"""Registre des cours, dans l'ordre du programme (bloc, quadrimestre)."""

from __future__ import annotations

import importlib
from functools import cache

MODULES = [
    # Bloc 1
    "b1_chimie",
    "b1_anatomie_generale",
    "b1_esprit_critique",
    "b1_physique",
    "b1_philosophie_ethique",
    "b1_psychologie",
    "b1_metier_kine",
    "b1_questions_ethiques",
    "b1_biologie_histologie",
    "b1_biomecanique",
    "b1_anatomie_locomoteur",
    "b1_methodes_recherche",
    "b1_developpement_durable",
    "b1_systeme_sante",
    "b1_ebp1",
    # Bloc 2
    "b2_physio_cellulaire",
    "b2_neurophysiologie",
    "b2_recolte_donnees",
    "b2_techniques_base",
    "b2_anatomie_palpatoire",
    "b2_geriatrie",
    "b2_psychiatrie",
    "b2_motricite1",
    "b2_anglais",
    "b2_physio_systemes",
    "b2_complements_neuro",
    "b2_musculo_squelettique",
    "b2_cardio_respiratoire",
    "b2_systeme_nerveux",
    "b2_intro_pathologie",
    "b2_ebp2",
    "b2_motricite2",
]


@cache
def load():
    mods = []
    for name in MODULES:
        mod = importlib.import_module(f"courses.{name}")
        for q in mod.QUESTIONS:
            q.course = mod.COURSE.code
        mods.append(mod)
    mods.sort(key=lambda m: (m.COURSE.bloc, m.COURSE.quad, MODULES.index(m.__name__.split(".")[-1])))
    return mods


@cache
def all_terms() -> dict:
    from courses.common_terms import TERMS as common

    terms = dict(common)
    for mod in load():
        for k, v in getattr(mod, "TERMS", {}).items():
            terms.setdefault(k.lower(), v)
    return terms
