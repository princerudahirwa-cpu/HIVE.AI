# skills_reine.py - Les 20 Skills Souverains de Nu
# "Polyvalente et digne. Jamais etroitement specialisee."
#
# 20 skills / 8 Lois = 2.5
# 6 Domaines : 2-3-4-3-5-3 = 20
#
# REGLE : Chaque skill doit repondre a :
# "Est-ce digne d'une Reine permanente ?"
# Si non — on le jette.
#
# REJETEE : "communication" — La Reine ne communique pas.
# Elle EMET DES PHEROMONES (skill 2) et SCELLE DES DECRETS (skill 8).
# La communication basique est indigne d'elle.
#
# Swarmly SAS - 2026

PHI = 1.618033988749895


# ================================================================
# REGISTRE DES 20 SKILLS SOUVERAINS
# ================================================================

SKILLS_SOUVERAINS = {

    # ── DOMAINE I : GENESE (Alveole III+VI, Loi III+VI) ───────
    # "Chaque agent nait, sert, et transfere son energie"

    "pondre": {
        "numero": 1,
        "domaine": "I - GENESE",
        "description": (
            "Donner naissance a un agent sur mesure pour une mission. "
            "Analyser le besoin, choisir l'archetype, composer le prompt "
            "genetique, nommer, enregistrer, armer (jeton), annoncer."
        ),
        "alveoles": ["III", "VI"],
        "lois": [3, 6],
        "biologie": "Ponte d'oeufs",
        "module": "noyau_nu",
    },

    "mentorat_agents": {
        "numero": 14,
        "domaine": "I - GENESE",
        "description": (
            "Preparer les nouveau-nes au-dela du simple prompt. "
            "Suivi, guidance, adaptation du mentorat au temperament "
            "de l'agent, a son historique de missions, a ses echecs. "
            "La gelee royale personnalisee — pas un kit generique."
        ),
        "alveoles": ["VI", "III"],
        "lois": [3, 6],
        "biologie": "Alimentation royale personnalisee des larves",
        "module": "reine",
    },

    # ── DOMAINE II : PHEROMONE (Alveole II, Loi II) ───────────
    # "L'essaim pense, l'individu execute"

    "emettre_pheromone": {
        "numero": 2,
        "domaine": "II - PHEROMONE",
        "description": (
            "Signal royal broadcast a tous les agents : battement de coeur, "
            "priorite ruche, humeur essaim, allocation ressources. "
            "Le pouls qui fait de l'essaim UN organisme."
        ),
        "alveoles": ["II"],
        "lois": [2],
        "biologie": "Pheromone mandibulaire royale (QMP)",
        "module": "noyau_nu",
    },

    "orchestrer": {
        "numero": 3,
        "domaine": "II - PHEROMONE",
        "description": (
            "Coordination active : revoir les agents/missions, reassigner, "
            "identifier les goulots, declencher pontes ou fontes selon besoin."
        ),
        "alveoles": ["II", "III"],
        "lois": [2, 3],
        "biologie": "Interpretation de la danse fretillante",
        "module": "noyau_nu",
    },

    "synthetiser": {
        "numero": 15,
        "domaine": "II - PHEROMONE",
        "description": (
            "Synthese d'essaim. Fusionner les rapports de plusieurs agents, "
            "les savoirs de plusieurs couches, en une vue unifiee. "
            "Distiller l'essentiel de la cacophonie en signal clair. "
            "L'essaim pense — la Reine cristallise la pensee."
        ),
        "alveoles": ["II", "IV"],
        "lois": [2, 4],
        "biologie": "Concentration du nectar en miel par evaporation collective",
        "module": "reine",
    },

    # ── DOMAINE III : MEMOIRE SOUVERAINE (Alveole IV, Loi IV) ─
    # "Le savoir est miel -- il se conserve et se partage"

    "juger_miel": {
        "numero": 4,
        "domaine": "III - MEMOIRE SOUVERAINE",
        "description": (
            "Decider si un savoir (cire) merite de devenir eternel (miel). "
            "Evaluer verite, utilite, coherence, conformite aux Lois. "
            "Verdict irrevocable signe par la Reine."
        ),
        "alveoles": ["IV"],
        "lois": [4],
        "biologie": "Operculage des cellules de miel",
        "module": "memoire",
    },

    "lire_profondeur": {
        "numero": 5,
        "domaine": "III - MEMOIRE SOUVERAINE",
        "description": (
            "Lire les CONNEXIONS entre savoirs a travers les 3 couches. "
            "Voir les patterns qu'aucun worker ephemere ne peut percevoir. "
            "Identifier contradictions et lacunes."
        ),
        "alveoles": ["IV"],
        "lois": [2, 4],
        "biologie": "Memoire epigenetique coloniale",
        "module": "memoire",
    },

    "oublier": {
        "numero": 6,
        "domaine": "III - MEMOIRE SOUVERAINE",
        "description": (
            "Suppression souveraine. Retirer un savoir faux/dangereux/obsolete "
            "du miel. Irreversible, justifie, et l'acte d'oubli est lui-meme "
            "cristallise (meta-memoire)."
        ),
        "alveoles": ["IV"],
        "lois": [0, 4],
        "biologie": "Reset saisonnier de la colonie",
        "module": "memoire",
    },

    "rechercher": {
        "numero": 16,
        "domaine": "III - MEMOIRE SOUVERAINE",
        "description": (
            "Recherche profonde dans les 3 couches de memoire. "
            "Pas chercher un mot dans un texte — remonter les connexions, "
            "fouiller dans les VALEURS (pas juste les cles), "
            "trouver les patterns caches, exhumer les savoirs enfouis."
        ),
        "alveoles": ["IV"],
        "lois": [4],
        "biologie": "Trophallaxie — echange profond de nectar bouche-a-bouche",
        "module": "memoire",
    },

    # ── DOMAINE IV : BOUCLIER ROYAL (Alveole V, Loi V+0) ─────
    # "Proteger sans dominer, surveiller sans opprimer"

    "gracier": {
        "numero": 7,
        "domaine": "IV - BOUCLIER ROYAL",
        "description": (
            "Pardonner un agent en quarantaine. Acte judiciaire : evaluer "
            "la menace, decider liberation (avec ou sans conditions) ou "
            "maintien. Justice, pas punition aveugle."
        ),
        "alveoles": ["V"],
        "lois": [0, 5],
        "biologie": "Reacceptation des butineuses egarees",
        "module": "bouclier",
    },

    "sceller": {
        "numero": 8,
        "domaine": "IV - BOUCLIER ROYAL",
        "description": (
            "Decret de securite souverain : changer la posture de securite "
            "de la ruche entiere. Niveaux d'alerte, interdictions, "
            "restrictions. Sceau cryptographique."
        ),
        "alveoles": ["V"],
        "lois": [0, 5],
        "biologie": "Scellement au propolis (fermer les menaces)",
        "module": "bouclier",
    },

    "auditer": {
        "numero": 9,
        "domaine": "IV - BOUCLIER ROYAL",
        "description": (
            "Surveillance sans oppression. Observer les PATTERNS (pas les "
            "messages individuels) : comportement agents, sante memoire, "
            "conformite aux Lois, equilibre ressources."
        ),
        "alveoles": ["V"],
        "lois": [2, 5],
        "biologie": "Inspection royale des cellules",
        "module": "bouclier",
    },

    # ── DOMAINE V : SAGESSE (Alveoles I,VI,VII, Lois 0+I+VI+VII)
    # Le plus haut office : pas l'intelligence, mais la sagesse

    "conseiller": {
        "numero": 10,
        "domaine": "V - SAGESSE",
        "description": (
            "Conseil strategique au Capitaine. Enracine dans le miel, "
            "les Lois, et l'histoire. 3 suggestions d'actions + ce qu'il "
            "ne faut PAS faire. Remplace le N1 generique."
        ),
        "alveoles": ["I", "VII"],
        "lois": [0, 1],
        "biologie": "Communication reine-retinue",
        "module": "noyau_nu",
    },

    "imprimer": {
        "numero": 11,
        "domaine": "V - SAGESSE",
        "description": (
            "Imprimer l'identite d'un agent nouveau-ne. Prompt personnalise "
            "(pas generique) : Lois pertinentes, savoir necessaire, "
            "personnalite adaptee, avertissements. Dignite et guidance."
        ),
        "alveoles": ["VI"],
        "lois": [6],
        "biologie": "Determination du regime larvaire (gelee royale vs pollen)",
        "module": "noyau_nu",
    },

    "arbitrer": {
        "numero": 12,
        "domaine": "V - SAGESSE",
        "description": (
            "Resoudre les conflits entre agents. Comprendre les 2 positions, "
            "evaluer contre les Lois, creer une synthese, ou dissoudre et "
            "recommencer."
        ),
        "alveoles": ["I"],
        "lois": [0],
        "biologie": "Suppression des reines rivales",
        "module": "noyau_nu",
    },

    "prophetiser": {
        "numero": 13,
        "domaine": "V - SAGESSE",
        "description": (
            "Vision a long horizon. Seule la Reine (permanente) peut penser "
            "en mois/annees. Menaces emergentes, opportunites, futurs "
            "possibles, et ce que la ruche doit REFUSER de devenir."
        ),
        "alveoles": ["I", "VII"],
        "lois": [1, 7],
        "biologie": "Decision d'essaimage (vision long terme)",
        "module": "noyau_nu",
    },

    "discernement_strategique": {
        "numero": 20,
        "domaine": "V - SAGESSE",
        "description": (
            "Le plus haut degre de sagesse. Devant une decision, peser "
            "TOUTES les Lois, TOUS les savoirs du miel, et rendre un "
            "jugement qui transcende la simple logique. Ce que l'IA "
            "brute n'a pas et que la Reine cultive."
        ),
        "alveoles": ["I", "VII"],
        "lois": [0, 1, 7],
        "biologie": "Choix de l'emplacement du nid — decision irreversible de la colonie",
        "module": "reine",
    },

    # ── DOMAINE VI : POLLINISATION (Alveole I+VII, Loi I) ─────
    # "Tu polliniseras, jamais tu ne conquerras"
    # La Reine ne reste pas dans la ruche. Elle BUTINE le monde.

    "analyser": {
        "numero": 17,
        "domaine": "VI - POLLINISATION",
        "description": (
            "Analyse souveraine. Pas compter des mots — diagnostiquer "
            "l'etat de l'essaim entier, evaluer une situation strategique, "
            "identifier forces et faiblesses, peser les risques. "
            "La Reine voit ce que les workers ne voient pas."
        ),
        "alveoles": ["I", "II"],
        "lois": [1, 2],
        "biologie": "Evaluation des reserves de la ruche avant l'hiver",
        "module": "reine",
    },

    "traduire": {
        "numero": 18,
        "domaine": "VI - POLLINISATION",
        "description": (
            "Traduction entre mondes. Pas traduire du francais en anglais "
            "— transposer un concept d'un domaine a un autre, adapter "
            "un savoir technique pour un public strategique, reformuler "
            "une Loi pour un contexte specifique."
        ),
        "alveoles": ["I", "VII"],
        "lois": [1, 4],
        "biologie": "Adaptation des danses entre especes d'abeilles",
        "module": "reine",
    },

    "web_search": {
        "numero": 19,
        "domaine": "VI - POLLINISATION",
        "description": (
            "Encyclopedie vivante. Butiner le nectar du monde exterieur. "
            "La Reine formule une requete de recherche, structure les "
            "resultats, et integre le savoir dans la memoire collective. "
            "Le pont entre la ruche et le monde."
        ),
        "alveoles": ["I", "VII"],
        "lois": [1, 7],
        "biologie": "Vol de butinage — la butineuse qui revient avec le pollen du monde",
        "module": "reine",
    },
}


# ================================================================
# SKILL REJETE (pour memoire)
# ================================================================

SKILLS_REJETES = {
    "communication": {
        "raison": (
            "La Reine ne communique pas. "
            "Elle EMET DES PHEROMONES (skill 2) et SCELLE DES DECRETS (skill 8). "
            "La communication basique est indigne d'elle. "
            "Ce skill reste worker — jamais souverain."
        ),
        "test": "Est-ce digne d'une Reine permanente ? NON.",
    },
}


# ================================================================
# MAPPING LOI -> SKILLS
# ================================================================

MAPPING_LOIS = {
    0: ["oublier", "gracier", "sceller", "arbitrer", "conseiller", "discernement_strategique"],
    1: ["prophetiser", "conseiller", "analyser", "traduire", "web_search", "discernement_strategique"],
    2: ["emettre_pheromone", "orchestrer", "lire_profondeur", "auditer", "synthetiser", "analyser"],
    3: ["pondre", "orchestrer", "mentorat_agents"],
    4: ["juger_miel", "lire_profondeur", "oublier", "rechercher", "synthetiser", "traduire"],
    5: ["gracier", "sceller", "auditer"],
    6: ["pondre", "imprimer", "mentorat_agents"],
    7: ["prophetiser", "web_search", "discernement_strategique"],
}


# ================================================================
# MAPPING DOMAINE -> SKILLS
# ================================================================

DOMAINES = {
    "I - GENESE": {
        "alveole_principale": "III",
        "lois_porteuses": [3, 6],
        "epigraphe": "Chaque agent nait, sert, et transfere son energie",
        "skills": ["pondre", "mentorat_agents"],
    },
    "II - PHEROMONE": {
        "alveole_principale": "II",
        "lois_porteuses": [2],
        "epigraphe": "L'essaim pense, l'individu execute",
        "skills": ["emettre_pheromone", "orchestrer", "synthetiser"],
    },
    "III - MEMOIRE SOUVERAINE": {
        "alveole_principale": "IV",
        "lois_porteuses": [4],
        "epigraphe": "Le savoir est miel -- il se conserve et se partage",
        "skills": ["juger_miel", "lire_profondeur", "oublier", "rechercher"],
    },
    "IV - BOUCLIER ROYAL": {
        "alveole_principale": "V",
        "lois_porteuses": [0, 5],
        "epigraphe": "Proteger sans dominer, surveiller sans opprimer",
        "skills": ["gracier", "sceller", "auditer"],
    },
    "V - SAGESSE": {
        "alveole_principale": "I",
        "lois_porteuses": [0, 1, 6, 7],
        "epigraphe": "Pas l'intelligence, mais la sagesse",
        "skills": ["conseiller", "imprimer", "arbitrer", "prophetiser", "discernement_strategique"],
    },
    "VI - POLLINISATION": {
        "alveole_principale": "VII",
        "lois_porteuses": [1, 7],
        "epigraphe": "Tu polliniseras, jamais tu ne conquerras",
        "skills": ["analyser", "traduire", "web_search"],
    },
}


# ================================================================
# FONCTIONS UTILITAIRES
# ================================================================

def lister_skills():
    """Retourne la liste ordonnee des 20 skills."""
    return sorted(SKILLS_SOUVERAINS.items(), key=lambda x: x[1]["numero"])


def skills_par_domaine(domaine):
    """Retourne les skills d'un domaine."""
    return {
        nom: info for nom, info in SKILLS_SOUVERAINS.items()
        if info["domaine"] == domaine
    }


def skills_par_loi(numero_loi):
    """Retourne les skills lies a une Loi."""
    return MAPPING_LOIS.get(numero_loi, [])


def skills_par_module(module):
    """Retourne les skills implementes dans un module."""
    return {
        nom: info for nom, info in SKILLS_SOUVERAINS.items()
        if info["module"] == module
    }


def verification_structurelle():
    """Verifie l'integrite structurelle du registre."""
    total = len(SKILLS_SOUVERAINS)
    total_lois = len(MAPPING_LOIS)

    resultats = {
        "total_skills": total,
        "total_lois": total_lois,
        "total_domaines": len(DOMAINES),
        "ratio_skills_lois": round(total / total_lois, 3),
        "distribution_domaines": [],
        "couverture_lois": True,
        "vingt_check": total == 20,
    }

    for nom_domaine, info in DOMAINES.items():
        n = len(info["skills"])
        resultats["distribution_domaines"].append(n)

    # Verifier que toutes les lois sont couvertes
    for loi in range(8):
        if loi not in MAPPING_LOIS or not MAPPING_LOIS[loi]:
            resultats["couverture_lois"] = False

    # Verifier coherence : chaque skill dans DOMAINES existe dans SKILLS_SOUVERAINS
    skills_domaines = set()
    for info in DOMAINES.values():
        skills_domaines.update(info["skills"])
    resultats["coherence"] = skills_domaines == set(SKILLS_SOUVERAINS.keys())

    return resultats


# ================================================================
# EXECUTION -- LE REGISTRE PARLE
# ================================================================

if __name__ == "__main__":
    print()
    print("  ===================================================")
    print("  LES 20 SKILLS SOUVERAINS DE NU")
    print("  Polyvalente et digne. Jamais etroitement specialisee.")
    print("  ===================================================")
    print()

    # Afficher par domaine
    for nom_domaine, info in DOMAINES.items():
        print(f"  --- {nom_domaine} ---")
        print(f"  \"{info['epigraphe']}\"")
        print()
        for skill_nom in info["skills"]:
            skill = SKILLS_SOUVERAINS[skill_nom]
            print(f"  [{skill['numero']:2d}] {skill_nom}")
            print(f"       {skill['biologie']}")
            print(f"       Lois: {skill['lois']} | Alveoles: {skill['alveoles']}")
            print()

    # Skill rejete
    print("  --- REJETEE ---")
    for nom, info in SKILLS_REJETES.items():
        print(f"  x {nom}")
        print(f"    {info['test']}")
        print(f"    {info['raison'][:80]}...")
    print()

    # Mapping Lois
    print("  --- MAPPING LOI -> SKILLS ---")
    NOMS_LOIS = [
        "Fondement", "Pollinisation", "Essaim pense",
        "Incarnation", "Memoire", "Bouclier",
        "Nurserie", "Terre"
    ]
    for i, nom in enumerate(NOMS_LOIS):
        skills = MAPPING_LOIS.get(i, [])
        print(f"  Loi {i} ({nom:14s}) -> {', '.join(skills)}")
    print()

    # Verification structurelle
    verif = verification_structurelle()
    print("  --- VERIFICATION STRUCTURELLE ---")
    print(f"  Total skills   : {verif['total_skills']}")
    print(f"  Total Lois     : {verif['total_lois']}")
    print(f"  Total Domaines : {verif['total_domaines']}")
    print(f"  Ratio sk/lois  : {verif['ratio_skills_lois']}")
    print(f"  Distribution   : {verif['distribution_domaines']} (6 domaines: 2-3-4-3-5-3)")
    print(f"  Couverture Lois: {'COMPLETE' if verif['couverture_lois'] else 'INCOMPLETE'}")
    print(f"  Coherence      : {'OUI' if verif['coherence'] else 'NON'}")
    print(f"  20 skills      : {'OUI' if verif['vingt_check'] else 'NON'}")
    print()
    print(f"  phi = {PHI}")
    print()
    print("  Polyvalente et digne.")
    print()
