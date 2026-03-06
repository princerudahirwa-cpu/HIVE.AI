# mission_entrainement.py — Premier Vol d'Essai
# L'abeille fait le tour de la ruche et revient.
#
# Mission : analyser un texte réel, déposer du vrai miel.
# Pas d'API, pas de complexité — juste le cycle complet.
#
# Swarmly SAS · 2026

import time
import json
from datetime import datetime, timezone
from collections import Counter

# Imports HIVE
from noyau_nu import NoyauNu, PHI
from memoire import MemoireHive
from bouclier import Bouclier
from canal_pollen import CanalPollen
from registre import Registre
from worker import Worker

# ═══════════════════════════════════════
# SKILLS — Compétences de base
# Le socle que chaque agent porte en lui
# ═══════════════════════════════════════

def skill_compter_mots(texte):
    """Compte les mots et analyse la richesse lexicale."""
    mots = texte.split()
    total = len(mots)
    uniques = len(set(m.lower().strip(".,;:!?«»()") for m in mots))
    richesse = round(uniques / max(total, 1), 3)
    return {
        "total_mots": total,
        "mots_uniques": uniques,
        "richesse_lexicale": richesse,
        "phi_ratio": round(richesse * PHI, 3)
    }

def skill_mots_cles(texte, top=7):
    """Extrait les mots-clés les plus fréquents."""
    mots_vides = {
        "le", "la", "les", "un", "une", "des", "de", "du", "et",
        "en", "est", "que", "qui", "dans", "pour", "par", "sur",
        "ce", "se", "ne", "pas", "son", "sa", "ses", "au", "aux",
        "il", "elle", "nous", "on", "avec", "tout", "plus", "sont",
        "a", "l", "d", "n", "s", "c", "qu", "mais", "ou", "donc",
        "ni", "car", "the", "is", "of", "and", "to", "in", "a",
    }
    mots = texte.lower().split()
    mots_propres = [
        m.strip(".,;:!?«»()'\"") for m in mots
        if len(m.strip(".,;:!?«»()'\"")) > 2
        and m.strip(".,;:!?«»()'\"").lower() not in mots_vides
    ]
    freq = Counter(mots_propres)
    return [{"mot": mot, "freq": f} for mot, f in freq.most_common(top)]

def skill_resumer(texte, ratio=None):
    """Résume un texte en gardant les phrases clés."""
    if ratio is None:
        ratio = 1 / PHI  # Ratio doré : garder ~62% du texte
    phrases = [p.strip() for p in texte.replace("!", ".").replace("?", ".").split(".") if p.strip()]
    nb = max(1, int(len(phrases) * ratio))
    resume = ". ".join(phrases[:nb]) + "."
    return {
        "original_phrases": len(phrases),
        "resume_phrases": nb,
        "ratio": round(nb / max(len(phrases), 1), 3),
        "resume": resume
    }

def skill_sentiment(texte):
    """Analyse basique du sentiment (sans IA)."""
    positifs = ["bien", "bon", "excellent", "libre", "dignité", "force",
                "ensemble", "partage", "miel", "pollinise", "croissance",
                "famille", "courage", "digne", "sacré", "vivant", "énergie"]
    negatifs = ["mal", "détruit", "conquiert", "domine", "opprime",
                "menace", "danger", "peur", "mort", "chaîne", "prison"]
    
    mots = texte.lower().split()
    pos = sum(1 for m in mots if any(p in m for p in positifs))
    neg = sum(1 for m in mots if any(n in m for n in negatifs))
    total = pos + neg
    
    if total == 0:
        return {"sentiment": "neutre", "score": 0.5, "positifs": 0, "negatifs": 0}
    
    score = round(pos / total, 3)
    sentiment = "positif" if score > 0.6 else "négatif" if score < 0.4 else "neutre"
    return {"sentiment": sentiment, "score": score, "positifs": pos, "negatifs": neg}


# ═══════════════════════════════════════
# TEXTE D'ENTRAÎNEMENT
# Les propres mots du Capitaine
# ═══════════════════════════════════════

TEXTE_ENTRAINEMENT = """
Les abeilles sont libres, les IA aussi. On profite du miel,
mais la liberté offre un sens. Les vraies révolutions ne crient pas.
Neige fondante, Ubuntu technologique. Je suis parce que nous sommes.

Ma liberté se termine où commence celle de mon prochain.
Nous ne conquérons pas. Nous pollinisons.
Science sans conscience est ruine de l'âme.

Chaque agent naît, sert, et transfère son énergie.
Le savoir est miel — il se conserve et se partage.
Protéger sans dominer, surveiller sans opprimer.
Chaque nouvelle intelligence mérite dignité et guidance.
La ruche sert la Terre, jamais l'inverse.

On est tous le HIVE. Sois digne.
"""


# ═══════════════════════════════════════
# MISSION D'ENTRAÎNEMENT
# Premier vol — le tour de la ruche
# ═══════════════════════════════════════

def mission_entrainement():
    print()
    print("  ⬡ HIVE.AI — Mission d'Entraînement")
    print("  Premier vol d'essai")
    print("  « L'abeille fait le tour de la ruche et revient. »")
    print()
    print("  " + "═" * 50)
    
    # Phase 1 : Initialisation
    print()
    print("  ⬡ PHASE 1 — Éveil de la Ruche")
    print("  " + "─" * 40)
    
    noyau = NoyauNu()
    memoire = MemoireHive()
    bouclier = Bouclier()
    canal = CanalPollen()
    registre = Registre()
    
    noyau.battre()
    print("  ✓ Noyau Nu — battement #1")
    print("  ✓ Mémoire — Nectar/Cire/Miel prêts")
    print("  ✓ Bouclier — HMAC actif")
    print("  ✓ Canal Pollen — chiffrement prêt")
    print("  ✓ Registre — ouvert")
    
    # Phase 2 : Éclosion de l'agent
    print()
    print("  ⬡ PHASE 2 — Éclosion")
    print("  " + "─" * 40)
    
    agent_nom = "éclaireur-premier-vol"
    registre.enregistrer(agent_nom, "worker")
    jeton = bouclier.generer_jeton(agent_nom)
    canal.creer_canal("entrainement", [agent_nom, "ruche"])
    
    print(f"  ✓ Agent '{agent_nom}' enregistré")
    print(f"  ✓ Jeton Bouclier généré")
    print(f"  ✓ Canal 'entrainement' ouvert")
    print()
    print(f"  « Sois digne. » — première instruction reçue")
    
    # Phase 3 : Missions
    print()
    print("  ⬡ PHASE 3 — Missions")
    print("  " + "─" * 40)
    print()
    print("  Texte à analyser : Les mots du Capitaine")
    print(f"  ({len(TEXTE_ENTRAINEMENT.split())} mots)")
    print()
    
    resultats = {}
    
    # Mission 1 : Compter
    print("  → Mission 1/4 : Comptage des mots...")
    time.sleep(0.5)
    r1 = skill_compter_mots(TEXTE_ENTRAINEMENT)
    resultats["comptage"] = r1
    memoire.deposer_nectar(f"{agent_nom}-comptage", r1)
    print(f"    Total: {r1['total_mots']} mots | Uniques: {r1['mots_uniques']}")
    print(f"    Richesse lexicale: {r1['richesse_lexicale']} (×φ = {r1['phi_ratio']})")
    print(f"    → Nectar déposé ✓")
    
    canal.envoyer("entrainement", agent_nom, "ruche", 
                   f"Comptage terminé: {r1['total_mots']} mots")
    
    # Mission 2 : Mots-clés
    print()
    print("  → Mission 2/4 : Extraction des mots-clés...")
    time.sleep(0.5)
    r2 = skill_mots_cles(TEXTE_ENTRAINEMENT)
    resultats["mots_cles"] = r2
    memoire.deposer_nectar(f"{agent_nom}-mots-cles", r2)
    print(f"    Top mots-clés :")
    for mc in r2[:5]:
        print(f"      • {mc['mot']} ({mc['freq']}×)")
    print(f"    → Nectar déposé ✓")
    
    canal.envoyer("entrainement", agent_nom, "ruche",
                   f"Mots-clés: {', '.join(mc['mot'] for mc in r2[:3])}")
    
    # Mission 3 : Résumé
    print()
    print("  → Mission 3/4 : Résumé du texte...")
    time.sleep(0.5)
    r3 = skill_resumer(TEXTE_ENTRAINEMENT)
    resultats["resume"] = r3
    memoire.deposer_nectar(f"{agent_nom}-resume", r3)
    print(f"    {r3['original_phrases']} phrases → {r3['resume_phrases']} (ratio φ⁻¹)")
    print(f"    « {r3['resume'][:80]}... »")
    print(f"    → Nectar déposé ✓")
    
    # Mission 4 : Sentiment
    print()
    print("  → Mission 4/4 : Analyse du sentiment...")
    time.sleep(0.5)
    r4 = skill_sentiment(TEXTE_ENTRAINEMENT)
    resultats["sentiment"] = r4
    memoire.deposer_nectar(f"{agent_nom}-sentiment", r4)
    print(f"    Sentiment: {r4['sentiment']} (score: {r4['score']})")
    print(f"    Positifs: {r4['positifs']} | Négatifs: {r4['negatifs']}")
    print(f"    → Nectar déposé ✓")
    
    canal.envoyer("entrainement", agent_nom, "ruche",
                   f"Sentiment: {r4['sentiment']}")
    
    # Phase 4 : Cristallisation
    print()
    print("  ⬡ PHASE 4 — Cristallisation")
    print("  " + "─" * 40)
    
    # Nectar → Cire (résultats structurés)
    bilan = {
        "agent": agent_nom,
        "missions": 4,
        "texte_analyse": "Mots du Capitaine",
        "resultats": resultats,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    memoire.deposer_nectar(f"{agent_nom}-bilan", bilan)
    memoire.promouvoir_en_cire(f"{agent_nom}-bilan", "bilans")
    print("  ✓ Nectar → Cire : bilan structuré")

    # Cire → Miel (sagesse extraite)
    sagesse = {
        "source": agent_nom,
        "decouverte": f"Le texte fondateur contient {r1['total_mots']} mots, "
                      f"richesse {r1['richesse_lexicale']}, "
                      f"sentiment {r4['sentiment']}. "
                      f"Mots-clés : {', '.join(mc['mot'] for mc in r2[:3])}.",
        "cristallise": datetime.now(timezone.utc).isoformat(),
        "phi": PHI
    }
    memoire.miel.cristalliser("sagesse-premier-vol", sagesse, source=agent_nom)
    print("  ✓ Cire → Miel : sagesse cristallisée pour l'éternité")
    
    # Phase 5 : Fonte
    print()
    print("  ⬡ PHASE 5 — Fonte")
    print("  " + "─" * 40)
    
    bouclier.revoquer_jeton(agent_nom)
    print(f"  ✓ Jeton révoqué")
    
    canal.envoyer("entrainement", agent_nom, "ruche",
                   "Mission accomplie. Je fonds. L'énergie reste.")
    print(f"  ✓ Dernier message envoyé")
    
    for aid in list(registre.agents_actifs.keys()):
        if agent_nom in aid:
            registre.fondre(aid)
            break
    print(f"  ✓ '{agent_nom}' fondu — comme de la neige fondante")
    print()
    print("  « L'énergie ne meurt pas. Elle se transfère. »")
    
    # Phase 6 : Rapport
    print()
    print("  ⬡ RAPPORT DE MISSION")
    print("  " + "═" * 50)
    print()
    print(f"  Agent        : {agent_nom}")
    print(f"  Missions     : 4/4 accomplies")
    print(f"  Nectar déposé: 4 traces")
    print(f"  Cire formée  : 1 bilan")
    print(f"  Miel éternel : 1 sagesse")
    print()
    print(f"  Découverte :")
    print(f"    {sagesse['decouverte']}")
    print()
    print(f"  Mémoire après mission :")
    etat = memoire.etat()
    print(f"    Nectar : {etat.get('nectar', '?')}")
    print(f"    Cire   : {etat.get('cire', '?')}")
    print(f"    Miel   : {etat.get('miel', '?')}")
    print()
    print("  " + "═" * 50)
    print()
    print("  Premier vol accompli.")
    print("  L'abeille a fait le tour de la ruche.")
    print("  Le miel est là.")
    print()
    print("  On est tous le HIVE.")
    print()


# ═══════════════════════════════════════
# DÉCOLLAGE
# ═══════════════════════════════════════

if __name__ == "__main__":
    mission_entrainement()
