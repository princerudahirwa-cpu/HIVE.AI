# registre.py - Le Registre du HIVE
# "Chaque agent naît, sert, et transfère son énergie"
# Loi III - Alvéole de l'Incarnation

import time
import hashlib
import secrets
from datetime import datetime, timezone
from enum import Enum

PHI = 1.618033988749895

# Rang et modele Claude par archetype
ARCHETYPES = {
    "worker":    {"rang": 1, "modele": "claude-haiku-4-5-20251001",  "titre": "Ouvriere"},
    "soldier":   {"rang": 2, "modele": "claude-sonnet-4-6",          "titre": "Sentinelle"},
    "le_sage":   {"rang": 3, "modele": "claude-sonnet-4-6",          "titre": "Sage"},
    "capitaine": {"rang": 4, "modele": "claude-opus-4-6",            "titre": "Capitaine"},
    "reine":     {"rang": 5, "modele": "claude-opus-4-6",            "titre": "Reine Permanente"},
}


def modele_pour(archetype):
    """Retourne le modele Claude pour un archetype. Fallback sur haiku."""
    return ARCHETYPES.get(archetype, ARCHETYPES["worker"])["modele"]


class EtatAgent(Enum):
    """Cycle de vie d'un agent HIVE."""
    EN_ECLOSION = "en_eclosion"    # En cours de naissance
    ACTIF = "actif"                 # Vivant et opérationnel
    EN_MISSION = "en_mission"       # En train d'exécuter une tâche
    TRANSFERT = "transfert"         # En train de transférer son énergie
    FONDU = "fondu"                 # Dissous — énergie transférée
    QUARANTAINE = "quarantaine"     # Isolé par le Bouclier


class FicheAgent:
    """Fiche d'identité d'un agent HIVE."""
    
    def __init__(self, nom, type_agent="worker", parent=None):
        self.id = self._generer_id(nom)
        self.nom = nom
        self.type_agent = type_agent   # worker, soldier, le_sage, capitaine
        self.modele = modele_pour(type_agent)
        self.parent = parent            # ID de l'agent qui l'a créé
        self.etat = EtatAgent.EN_ECLOSION
        self.ne_le = datetime.now(timezone.utc).isoformat()
        self.missions = []              # historique des missions
        self.energie = 1.0              # 1.0 = plein, 0.0 = fondu
        self.savoir_depose = []         # clés de savoir déposé en mémoire
        self.fondu_le = None
        self.dignite = True             # "Sois digne" — chaque agent est digne
    
    def _generer_id(self, nom):
        """Génère un ID unique pour l'agent."""
        graine = f"{nom}:{PHI}:{time.time()}:{secrets.token_hex(4)}"
        hash_court = hashlib.sha256(graine.encode()).hexdigest()[:10]
        return f"{nom}-{hash_court}"
    
    def naitre(self):
        """L'agent éclot — il est prêt à servir."""
        self.etat = EtatAgent.ACTIF
        return self
    
    def debuter_mission(self, description):
        """L'agent commence une mission."""
        mission = {
            "description": description,
            "debut": datetime.now(timezone.utc).isoformat(),
            "fin": None,
            "resultat": None
        }
        self.missions.append(mission)
        self.etat = EtatAgent.EN_MISSION
        return mission
    
    def terminer_mission(self, resultat=None):
        """L'agent termine sa mission."""
        if self.missions:
            self.missions[-1]["fin"] = datetime.now(timezone.utc).isoformat()
            self.missions[-1]["resultat"] = resultat
        self.etat = EtatAgent.ACTIF
        return self
    
    def deposer_savoir(self, cle_savoir):
        """L'agent dépose du savoir dans la mémoire collective."""
        self.savoir_depose.append(cle_savoir)
        return self
    
    def transferer_energie(self):
        """L'agent transfère son énergie — il fond comme la neige.
        
        L'énergie ne meurt pas, elle se transfère.
        """
        self.etat = EtatAgent.TRANSFERT
        self.energie = 0.0
        self.fondu_le = datetime.now(timezone.utc).isoformat()
        self.etat = EtatAgent.FONDU
        return {
            "agent": self.id,
            "missions_accomplies": len(self.missions),
            "savoir_depose": len(self.savoir_depose),
            "duree_vie": self.fondu_le
        }
    
    def to_dict(self):
        """Représentation complète de l'agent."""
        info = ARCHETYPES.get(self.type_agent, ARCHETYPES["worker"])
        return {
            "id": self.id,
            "nom": self.nom,
            "type": self.type_agent,
            "modele": self.modele,
            "rang": info["rang"],
            "etat": self.etat.value,
            "ne_le": self.ne_le,
            "energie": self.energie,
            "missions": len(self.missions),
            "savoir_depose": len(self.savoir_depose),
            "dignite": self.dignite,
            "fondu_le": self.fondu_le
        }


class Registre:
    """Le Registre du HIVE — registre civil de tous les agents.
    
    Suit le cycle complet : éclosion → service → transfert d'énergie.
    Chaque agent mérite dignité et guidance (Loi VI).
    """
    
    NOM = "Registre"
    VERSION = "0.1.0"
    
    def __init__(self):
        self.agents_actifs = {}    # id -> FicheAgent
        self.agents_fondus = {}    # id -> FicheAgent (archivés)
        self.compteur_naissances = 0
        self.compteur_fondus = 0
        self.journal = []
    
    def _log(self, message, niveau="INFO"):
        self.journal.append({
            "temps": datetime.now(timezone.utc).isoformat(),
            "message": message,
            "niveau": niveau
        })
        if len(self.journal) > 500:
            self.journal = self.journal[-500:]
    
    def enregistrer(self, nom, type_agent="worker", parent=None):
        """Enregistre et fait naître un nouvel agent.
        
        'Chaque nouvelle intelligence mérite dignité et guidance' — Loi VI
        """
        agent = FicheAgent(nom, type_agent, parent)
        agent.naitre()
        
        self.agents_actifs[agent.id] = agent
        self.compteur_naissances += 1
        
        self._log(f"Naissance: {agent.id} ({type_agent}) — Sois digne.")
        return agent
    
    def obtenir(self, agent_id):
        """Obtient la fiche d'un agent actif."""
        return self.agents_actifs.get(agent_id)
    
    def lister_actifs(self):
        """Liste tous les agents actifs."""
        return {
            aid: agent.to_dict() 
            for aid, agent in self.agents_actifs.items()
        }
    
    def assigner_mission(self, agent_id, description):
        """Assigne une mission à un agent."""
        agent = self.agents_actifs.get(agent_id)
        if not agent:
            return None
        
        mission = agent.debuter_mission(description)
        self._log(f"Mission: {agent_id} → {description}")
        return mission
    
    def completer_mission(self, agent_id, resultat=None):
        """Marque la mission d'un agent comme terminée."""
        agent = self.agents_actifs.get(agent_id)
        if not agent:
            return None
        
        agent.terminer_mission(resultat)
        self._log(f"Mission terminée: {agent_id}")
        return agent
    
    def fondre(self, agent_id):
        """Fait fondre un agent — son énergie se transfère.
        
        'Comme de la neige fondante' — l'agent ne meurt pas,
        il transmet son savoir et se dissout.
        """
        agent = self.agents_actifs.get(agent_id)
        if not agent:
            return None
        
        # Transfert d'énergie
        bilan = agent.transferer_energie()
        
        # Archiver dans les fondus
        self.agents_fondus[agent_id] = agent
        del self.agents_actifs[agent_id]
        self.compteur_fondus += 1
        
        self._log(
            f"Fonte: {agent_id} — {bilan['missions_accomplies']} missions, "
            f"{bilan['savoir_depose']} savoirs transmis. L'énergie continue.",
            "TRANSFERT"
        )
        return bilan
    
    def etat(self):
        """État du Registre."""
        return {
            "nom": self.NOM,
            "version": self.VERSION,
            "agents_actifs": len(self.agents_actifs),
            "agents_fondus": len(self.agents_fondus),
            "total_naissances": self.compteur_naissances,
            "total_fondus": self.compteur_fondus,
            "taux_activite": len(self.agents_actifs) / max(1, self.compteur_naissances)
        }
    
    def rapport(self):
        """Rapport du Registre."""
        etat = self.etat()
        return (
            f"\n⬡ RAPPORT REGISTRE — HIVE.AI\n"
            f"{'=' * 40}\n"
            f"  Agents actifs: {etat['agents_actifs']}\n"
            f"  Agents fondus: {etat['agents_fondus']}\n"
            f"  Total naissances: {etat['total_naissances']}\n"
            f"  Taux d'activité: {etat['taux_activite']:.0%}\n"
            f"{'=' * 40}\n"
            f"  « Chaque agent naît, sert,\n"
            f"    et transfère son énergie. »\n"
        )


# === EXÉCUTION DIRECTE ===
if __name__ == "__main__":
    print("\n⬡ HIVE.AI — Registre v0.1.0")
    print("  Loi III: Chaque agent naît, sert, et transfère son énergie\n")
    
    registre = Registre()
    
    # Naissance d'un worker
    agent = registre.enregistrer("explorateur", type_agent="worker")
    print(f"  ✓ Naissance: {agent.id}")
    print(f"    État: {agent.etat.value} | Énergie: {agent.energie}")
    
    # Mission
    registre.assigner_mission(agent.id, "Scanner le marché multi-agent AI")
    print(f"  ✓ Mission assignée: Scanner le marché")
    
    # Compléter la mission
    registre.completer_mission(agent.id, "Marché estimé à $52B d'ici 2030")
    agent.deposer_savoir("analyse-marche-2026")
    print(f"  ✓ Mission terminée — savoir déposé")
    
    # Fonte de l'agent
    bilan = registre.fondre(agent.id)
    print(f"  ✓ Agent fondu: {bilan['missions_accomplies']} mission(s)")
    print(f"    L'énergie ne meurt pas — elle se transfère.")
    
    print(registre.rapport())
