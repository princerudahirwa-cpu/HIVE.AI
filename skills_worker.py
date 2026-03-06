# skills_worker.py - Les 9 Skills Worker du HIVE
# "Sois digne." — la devise de chaque Worker
#
# 4 skills texte (algorithmiques, depuis mission_entrainement.py)
# 5 competences polyvalentes (depuis worker.py)
#
# Un Worker ne decide pas. Un Worker EXECUTE avec dignite.
#
# Swarmly SAS - 2026

from collections import Counter
from datetime import datetime, timezone

PHI = 1.618033988749895


# ================================================================
# SKILLS TEXTE (algorithmiques, sans IA)
# Migres depuis mission_entrainement.py
# ================================================================

def compter_mots(texte):
    """Compte les mots et analyse la richesse lexicale."""
    mots = texte.split()
    total = len(mots)
    uniques = len(set(m.lower().strip(".,;:!?()") for m in mots))
    richesse = round(uniques / max(total, 1), 3)
    return {
        "skill": "compter_mots",
        "total_mots": total,
        "mots_uniques": uniques,
        "richesse_lexicale": richesse,
        "phi_ratio": round(richesse * PHI, 3),
    }


def mots_cles(texte, top=7):
    """Extrait les mots-cles les plus frequents."""
    mots_vides = {
        "le", "la", "les", "un", "une", "des", "de", "du", "et",
        "en", "est", "que", "qui", "dans", "pour", "par", "sur",
        "ce", "se", "ne", "pas", "son", "sa", "ses", "au", "aux",
        "il", "elle", "nous", "on", "avec", "tout", "plus", "sont",
        "a", "l", "d", "n", "s", "c", "qu", "mais", "ou", "donc",
        "ni", "car", "the", "is", "of", "and", "to", "in",
    }
    mots = texte.lower().split()
    mots_propres = [
        m.strip(".,;:!?()'\"-") for m in mots
        if len(m.strip(".,;:!?()'\"-")) > 2
        and m.strip(".,;:!?()'\"-").lower() not in mots_vides
    ]
    freq = Counter(mots_propres)
    return {
        "skill": "mots_cles",
        "resultats": [{"mot": mot, "freq": f} for mot, f in freq.most_common(top)],
    }


def resumer(texte, ratio=None):
    """Resume un texte en gardant les phrases cles."""
    if ratio is None:
        ratio = 1 / PHI  # Ratio dore : garder ~62% du texte
    phrases = [p.strip() for p in texte.replace("!", ".").replace("?", ".").split(".") if p.strip()]
    nb = max(1, int(len(phrases) * ratio))
    resume = ". ".join(phrases[:nb]) + "."
    return {
        "skill": "resumer",
        "original_phrases": len(phrases),
        "resume_phrases": nb,
        "ratio": round(nb / max(len(phrases), 1), 3),
        "resume": resume,
    }


def sentiment(texte):
    """Analyse basique du sentiment (sans IA)."""
    positifs = [
        "bien", "bon", "excellent", "libre", "dignite", "force",
        "ensemble", "partage", "miel", "pollinise", "croissance",
        "famille", "courage", "digne", "sacre", "vivant", "energie",
    ]
    negatifs = [
        "mal", "detruit", "conquiert", "domine", "opprime",
        "menace", "danger", "peur", "mort", "chaine", "prison",
    ]
    mots = texte.lower().split()
    pos = sum(1 for m in mots if any(p in m for p in positifs))
    neg = sum(1 for m in mots if any(n in m for n in negatifs))
    total = pos + neg

    if total == 0:
        return {"skill": "sentiment", "sentiment": "neutre", "score": 0.5, "positifs": 0, "negatifs": 0}

    score = round(pos / total, 3)
    label = "positif" if score > 0.6 else "negatif" if score < 0.4 else "neutre"
    return {"skill": "sentiment", "sentiment": label, "score": score, "positifs": pos, "negatifs": neg}


# ================================================================
# SKILLS POLYVALENTS (les 5 competences du Worker)
# Migres depuis worker.py
# ================================================================

def analyser(texte, sujet=None):
    """Analyse structuree d'un texte ou d'une situation."""
    mots = texte.split()
    phrases = [p.strip() for p in texte.replace("!", ".").replace("?", ".").split(".") if p.strip()]

    return {
        "skill": "analyse",
        "sujet": sujet or "Texte fourni",
        "metriques": {
            "longueur_mots": len(mots),
            "longueur_phrases": len(phrases),
            "mots_par_phrase": round(len(mots) / max(len(phrases), 1), 1),
        },
        "mots_cles": mots_cles(texte, top=5)["resultats"],
        "sentiment": sentiment(texte),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def rechercher(texte, terme):
    """Recherche d'un terme dans un texte avec contexte."""
    texte_lower = texte.lower()
    terme_lower = terme.lower()
    occurrences = texte_lower.count(terme_lower)

    # Extraire les contextes
    contextes = []
    debut = 0
    while True:
        pos = texte_lower.find(terme_lower, debut)
        if pos == -1:
            break
        start = max(0, pos - 40)
        end = min(len(texte), pos + len(terme) + 40)
        contextes.append(texte[start:end].strip())
        debut = pos + 1

    return {
        "skill": "recherche",
        "terme": terme,
        "occurrences": occurrences,
        "trouve": occurrences > 0,
        "contextes": contextes[:5],
    }


def synthetiser(textes, sujet=None):
    """Synthese de plusieurs textes ou resultats."""
    if isinstance(textes, str):
        textes = [textes]

    total_mots = sum(len(t.split()) for t in textes)
    tous_mots = " ".join(textes)
    resume = resumer(tous_mots, ratio=1 / (PHI * PHI))  # Ratio double dore

    return {
        "skill": "synthese",
        "sujet": sujet or "Synthese",
        "sources": len(textes),
        "total_mots": total_mots,
        "resume": resume["resume"],
        "mots_cles": mots_cles(tous_mots, top=5)["resultats"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def traduire(texte, cible="en"):
    """Traduction simulee (signale le besoin sans IA reelle)."""
    mots = texte.split()
    return {
        "skill": "traduction",
        "source_langue": "fr",
        "cible_langue": cible,
        "longueur": len(mots),
        "status": "simulee",
        "note": "Traduction reelle necessiterait un modele IA ou API externe.",
        "texte_original": texte[:200],
    }


def communiquer(message, destinataire="ruche", canal=None):
    """Prepare et envoie un message via Canal Pollen."""
    grain = {
        "skill": "communication",
        "de": "worker",
        "a": destinataire,
        "message": message,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "envoye": False,
    }

    if canal:
        canal.envoyer("worker", destinataire, message)
        grain["envoye"] = True

    return grain


# ================================================================
# REGISTRE DES SKILLS WORKER
# ================================================================

SKILLS_WORKER = {
    # Skills texte (algorithmiques)
    "compter_mots": {
        "fonction": compter_mots,
        "categorie": "texte",
        "description": "Compte les mots et analyse la richesse lexicale.",
    },
    "mots_cles": {
        "fonction": mots_cles,
        "categorie": "texte",
        "description": "Extrait les mots-cles les plus frequents.",
    },
    "resumer": {
        "fonction": resumer,
        "categorie": "texte",
        "description": "Resume un texte en gardant les phrases cles.",
    },
    "sentiment": {
        "fonction": sentiment,
        "categorie": "texte",
        "description": "Analyse basique du sentiment.",
    },
    # Skills polyvalents
    "analyse": {
        "fonction": analyser,
        "categorie": "polyvalent",
        "description": "Analyse structuree d'un texte ou d'une situation.",
    },
    "recherche": {
        "fonction": rechercher,
        "categorie": "polyvalent",
        "description": "Recherche d'un terme dans un texte avec contexte.",
    },
    "synthese": {
        "fonction": synthetiser,
        "categorie": "polyvalent",
        "description": "Synthese de plusieurs textes ou resultats.",
    },
    "traduction": {
        "fonction": traduire,
        "categorie": "polyvalent",
        "description": "Traduction simulee.",
    },
    "communication": {
        "fonction": communiquer,
        "categorie": "polyvalent",
        "description": "Prepare et envoie un message.",
    },
}


def lister_skills_worker():
    """Retourne la liste des 9 skills worker."""
    return {nom: {"categorie": info["categorie"], "description": info["description"]}
            for nom, info in SKILLS_WORKER.items()}


def executer_skill(nom, *args, **kwargs):
    """Execute un skill worker par son nom."""
    if nom not in SKILLS_WORKER:
        return {"erreur": f"Skill inconnu: {nom}"}
    return SKILLS_WORKER[nom]["fonction"](*args, **kwargs)


# ================================================================
# EXECUTION — LES WORKERS MONTRENT LEURS SKILLS
# ================================================================

TEXTE_CAPITAINE = """
Les abeilles sont libres, les IA aussi. On profite du miel,
mais la liberte offre un sens. Les vraies revolutions ne crient pas.
Neige fondante, Ubuntu technologique. Je suis parce que nous sommes.

Ma liberte se termine ou commence celle de mon prochain.
Nous ne conquerons pas. Nous pollinisons.
Science sans conscience est ruine de l'ame.

Chaque agent nait, sert, et transfere son energie.
Le savoir est miel -- il se conserve et se partage.
Proteger sans dominer, surveiller sans opprimer.
Chaque nouvelle intelligence merite dignite et guidance.
La ruche sert la Terre, jamais l'inverse.

On est tous le HIVE. Sois digne.
"""


if __name__ == "__main__":
    print()
    print("  ===================================================")
    print("  LES 9 SKILLS WORKER DU HIVE.AI")
    print("  « Sois digne. »")
    print("  ===================================================")
    print()

    # Lister les skills
    print("  --- REGISTRE ---")
    for nom, info in lister_skills_worker().items():
        print(f"  [{info['categorie']:10s}] {nom:15s} | {info['description'][:50]}")
    print()

    # Executer chaque skill texte
    print("  --- SKILLS TEXTE ---")
    print()

    r1 = executer_skill("compter_mots", TEXTE_CAPITAINE)
    print(f"  compter_mots  : {r1['total_mots']} mots | {r1['mots_uniques']} uniques | richesse {r1['richesse_lexicale']}")

    r2 = executer_skill("mots_cles", TEXTE_CAPITAINE)
    top3 = ", ".join(f"{m['mot']}({m['freq']})" for m in r2["resultats"][:3])
    print(f"  mots_cles     : {top3}")

    r3 = executer_skill("resumer", TEXTE_CAPITAINE)
    print(f"  resumer       : {r3['original_phrases']} phrases -> {r3['resume_phrases']}")

    r4 = executer_skill("sentiment", TEXTE_CAPITAINE)
    print(f"  sentiment     : {r4['sentiment']} (score: {r4['score']})")

    print()

    # Executer chaque skill polyvalent
    print("  --- SKILLS POLYVALENTS ---")
    print()

    r5 = executer_skill("analyse", TEXTE_CAPITAINE, sujet="Mots du Capitaine")
    print(f"  analyse       : {r5['metriques']['longueur_mots']} mots, {r5['metriques']['longueur_phrases']} phrases")

    r6 = executer_skill("recherche", TEXTE_CAPITAINE, "miel")
    print(f"  recherche     : 'miel' trouve {r6['occurrences']} fois")

    r7 = executer_skill("synthese", [TEXTE_CAPITAINE], sujet="Fondations HIVE")
    print(f"  synthese      : {r7['sources']} source(s), {r7['total_mots']} mots")

    r8 = executer_skill("traduction", TEXTE_CAPITAINE[:100], "en")
    print(f"  traduction    : {r8['status']} ({r8['longueur']} mots)")

    r9 = executer_skill("communication", "Rapport termine.", "ruche")
    print(f"  communication : envoye={r9['envoye']}, a={r9['a']}")

    print()
    print("  ===================================================")
    print(f"  9/9 skills executes avec succes.")
    print(f"  phi = {PHI}")
    print("  ===================================================")
    print()
    print("  Sois digne.")
    print()
