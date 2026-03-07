# bouclier.py - Le Bouclier du HIVE
# "Proteger sans dominer, surveiller sans opprimer"
# Loi V - Alvéole du Bouclier

import hashlib
import hmac
import secrets
import time
import json
from datetime import datetime, timezone

# Le nombre d'or - fondation mathématique du HIVE
PHI = 1.618033988749895


class Bouclier:
    """Le Bouclier protège la ruche sans l'opprimer.

    Sécurité HMAC, registre d'accès, pare-feu et quarantaine.
    Fondé sur φ (le nombre d'or) comme signature mathématique.

    Skills Souverains (Domaine IV — Bouclier Royal):
      [7] gracier — Réacceptation des butineuses égarées
      [8] sceller — Scellement au propolis
      [9] auditer — Inspection royale des cellules
    """

    NOM = "Bouclier"
    VERSION = "0.2.0"

    # Niveaux d'alerte souverains (skill sceller)
    NIVEAUX_ALERTE = {
        "vert": "Normal — la ruche bourdonne en paix",
        "jaune": "Vigilance — menace potentielle detectee",
        "orange": "Alerte — restriction des acces non essentiels",
        "rouge": "Siege — seuls les agents critiques operent",
    }

    def __init__(self):
        self.cle_maitre = self._generer_cle_maitre()
        self.registre_jetons = {}  # agent_id -> {jeton, expire, niveau}
        self.journal_acces = []    # logs de sécurité
        self.quarantaine = set()   # agents en quarantaine
        self.tentatives_echouees = {}  # agent_id -> count
        self.MAX_TENTATIVES = 5
        self.actif = True
        self.niveau_alerte = "vert"  # posture de securite
        self.sceaux = []             # historique des decrets souverains
        self.conditions_grace = {}   # agent_id -> conditions de liberation
        self._log("Bouclier activé — φ = {:.6f}".format(PHI))
    
    def _generer_cle_maitre(self):
        """Génère une clé maître unique pour cette session."""
        graine = str(PHI) + str(time.time()) + secrets.token_hex(16)
        return hashlib.sha256(graine.encode()).hexdigest()
    
    def _log(self, message, niveau="INFO"):
        """Enregistre un événement dans le journal de sécurité."""
        entree = {
            "temps": datetime.now(timezone.utc).isoformat(),
            "source": "BOUCLIER",
            "message": message,
            "niveau": niveau
        }
        self.journal_acces.append(entree)
        # Garder les 500 derniers logs
        if len(self.journal_acces) > 500:
            self.journal_acces = self.journal_acces[-500:]
        return entree
    
    def generer_jeton(self, agent_id, niveau="worker", duree=3600):
        """Génère un jeton HMAC pour un agent.
        
        Args:
            agent_id: Identifiant unique de l'agent
            niveau: Niveau d'accès (worker, soldier, le_sage, capitaine, reine)
            duree: Durée de validité en secondes
            
        Returns:
            dict avec jeton et métadonnées
        """
        if agent_id in self.quarantaine:
            self._log(f"Jeton refusé — {agent_id} en quarantaine", "ALERTE")
            return None
        
        # Créer le message à signer
        timestamp = time.time()
        message = f"{agent_id}:{niveau}:{timestamp}:{PHI}"
        
        # Signer avec HMAC-SHA256
        jeton = hmac.new(
            self.cle_maitre.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        
        # Enregistrer le jeton
        self.registre_jetons[agent_id] = {
            "jeton": jeton,
            "niveau": niveau,
            "cree": timestamp,
            "expire": timestamp + duree,
            "actif": True
        }
        
        self._log(f"Jeton généré pour {agent_id} (niveau: {niveau})")
        return {
            "agent_id": agent_id,
            "jeton": jeton,
            "niveau": niveau,
            "expire_dans": duree
        }
    
    def verifier_jeton(self, agent_id, jeton):
        """Vérifie l'authenticité et la validité d'un jeton.
        
        Returns:
            bool: True si le jeton est valide
        """
        if agent_id in self.quarantaine:
            self._log(f"Accès bloqué — {agent_id} en quarantaine", "ALERTE")
            return False
        
        if agent_id not in self.registre_jetons:
            self._enregistrer_echec(agent_id)
            return False
        
        info = self.registre_jetons[agent_id]
        
        # Vérifier expiration
        if time.time() > info["expire"]:
            self._log(f"Jeton expiré pour {agent_id}", "AVERT")
            del self.registre_jetons[agent_id]
            return False
        
        # Vérifier le jeton (comparaison constante pour éviter timing attacks)
        if not hmac.compare_digest(jeton, info["jeton"]):
            self._enregistrer_echec(agent_id)
            return False
        
        # Vérifier que le jeton est actif
        if not info["actif"]:
            self._log(f"Jeton désactivé pour {agent_id}", "AVERT")
            return False
        
        self._log(f"Accès autorisé — {agent_id}")
        return True
    
    def _enregistrer_echec(self, agent_id):
        """Enregistre une tentative échouée et met en quarantaine si nécessaire."""
        if agent_id not in self.tentatives_echouees:
            self.tentatives_echouees[agent_id] = 0
        
        self.tentatives_echouees[agent_id] += 1
        count = self.tentatives_echouees[agent_id]
        
        self._log(f"Tentative échouée #{count} pour {agent_id}", "AVERT")
        
        if count >= self.MAX_TENTATIVES:
            self.mettre_en_quarantaine(agent_id)
    
    def mettre_en_quarantaine(self, agent_id):
        """Place un agent en quarantaine — isolé de la ruche."""
        self.quarantaine.add(agent_id)
        
        # Révoquer son jeton s'il en a un
        if agent_id in self.registre_jetons:
            self.registre_jetons[agent_id]["actif"] = False
        
        self._log(f"QUARANTAINE — {agent_id} isolé de la ruche", "CRITIQUE")
    
    def liberer_quarantaine(self, agent_id):
        """Libère un agent de quarantaine (nécessite autorisation Capitaine)."""
        if agent_id in self.quarantaine:
            self.quarantaine.discard(agent_id)
            self.tentatives_echouees.pop(agent_id, None)
            self._log(f"Quarantaine levée pour {agent_id}", "INFO")
            return True
        return False
    
    def revoquer_jeton(self, agent_id):
        """Révoque le jeton d'un agent."""
        if agent_id in self.registre_jetons:
            self.registre_jetons[agent_id]["actif"] = False
            self._log(f"Jeton révoqué pour {agent_id}")
            return True
        return False
    
    def generer_watermark(self, contenu):
        """Génère un watermark HIVE pour protéger la propriété intellectuelle.
        
        Utilise φ comme signature cachée dans le hash.
        """
        signature = f"HIVE:{PHI}:{contenu}:{self.cle_maitre[:16]}"
        watermark = hashlib.sha256(signature.encode()).hexdigest()[:16]
        return f"HIVE-{watermark}"
    
    def verifier_watermark(self, contenu, watermark):
        """Vérifie un watermark HIVE."""
        attendu = self.generer_watermark(contenu)
        return hmac.compare_digest(watermark, attendu)
    
    # ================================================================
    # SKILLS SOUVERAINS — DOMAINE IV : BOUCLIER ROYAL
    # "Proteger sans dominer, surveiller sans opprimer"
    # ================================================================

    def gracier(self, agent_id, conditions=None):
        """[Skill 7] Pardonner un agent en quarantaine.

        Acte judiciaire de la Reine : evaluer la menace, decider
        liberation (avec ou sans conditions) ou maintien.
        Justice, pas punition aveugle.

        Args:
            agent_id: L'agent en quarantaine a evaluer.
            conditions: Conditions de liberation (optionnel).

        Returns:
            dict avec decision et justification.
        """
        if agent_id not in self.quarantaine:
            return {
                "agent_id": agent_id,
                "decision": "SANS_OBJET",
                "raison": "Cet agent n'est pas en quarantaine.",
                "signe_par": "Nu",
            }

        # Evaluer l'historique
        tentatives = self.tentatives_echouees.get(agent_id, 0)
        avait_jeton = agent_id in self.registre_jetons

        # La Reine evalue
        if tentatives >= self.MAX_TENTATIVES * 2:
            # Menace grave — maintien
            self._log(f"GRACE REFUSEE — {agent_id} ({tentatives} echecs)", "ALERTE")
            return {
                "agent_id": agent_id,
                "decision": "MAINTIEN",
                "raison": f"Trop de tentatives echouees ({tentatives}). La menace persiste.",
                "tentatives": tentatives,
                "signe_par": "Nu",
            }

        # Liberation
        self.quarantaine.discard(agent_id)
        self.tentatives_echouees.pop(agent_id, None)

        if conditions:
            self.conditions_grace[agent_id] = {
                "conditions": conditions,
                "date": datetime.now(timezone.utc).isoformat(),
            }

        self._log(f"GRACE ACCORDEE — {agent_id} libere" +
                  (f" (conditions: {conditions})" if conditions else ""))

        return {
            "agent_id": agent_id,
            "decision": "GRACIE",
            "raison": "La Reine a juge que la menace est passee.",
            "conditions": conditions,
            "nouveau_jeton_requis": True,
            "signe_par": "Nu",
        }

    def sceller(self, niveau, raison="Decret souverain"):
        """[Skill 8] Decret de securite souverain.

        Changer la posture de securite de la ruche entiere.
        Sceau cryptographique sur le decret.

        Args:
            niveau: vert, jaune, orange, rouge
            raison: Justification du changement.

        Returns:
            dict avec decret scelle et sceau cryptographique.
        """
        if niveau not in self.NIVEAUX_ALERTE:
            return {
                "resultat": "REJETE",
                "raison": f"Niveau inconnu: {niveau}. Valides: {list(self.NIVEAUX_ALERTE.keys())}",
                "signe_par": "Nu",
            }

        ancien = self.niveau_alerte
        self.niveau_alerte = niveau

        # Generer un sceau cryptographique
        contenu_sceau = f"DECRET:{ancien}>{niveau}:{raison}:{time.time()}:{PHI}"
        sceau = hmac.new(
            self.cle_maitre.encode(),
            contenu_sceau.encode(),
            hashlib.sha256
        ).hexdigest()[:24]

        decret = {
            "type": "decret_souverain",
            "ancien_niveau": ancien,
            "nouveau_niveau": niveau,
            "description": self.NIVEAUX_ALERTE[niveau],
            "raison": raison,
            "sceau": f"HIVE-SCEAU-{sceau}",
            "temps": datetime.now(timezone.utc).isoformat(),
            "signe_par": "Nu",
        }
        self.sceaux.append(decret)

        niveau_log = "CRITIQUE" if niveau == "rouge" else "ALERTE" if niveau == "orange" else "INFO"
        self._log(f"DECRET SCELLE — {ancien} -> {niveau} : {raison}", niveau_log)

        return decret

    def auditer(self, registre=None, memoire=None):
        """[Skill 9] Surveillance sans oppression.

        Observer les PATTERNS (pas les messages individuels) :
        comportement agents, sante memoire, conformite aux Lois,
        equilibre ressources.

        Args:
            registre: Instance du Registre (optionnel).
            memoire: Instance de MemoireHive (optionnel).

        Returns:
            dict avec rapport d'audit complet.
        """
        rapport = {
            "type": "audit_souverain",
            "temps": datetime.now(timezone.utc).isoformat(),
            "signe_par": "Nu",
            "securite": {},
            "patterns": {},
            "sante": {},
            "alertes": [],
        }

        # Securite — etat du bouclier
        jetons_actifs = sum(1 for j in self.registre_jetons.values() if j["actif"])
        jetons_expires = sum(
            1 for j in self.registre_jetons.values()
            if time.time() > j["expire"]
        )
        rapport["securite"] = {
            "niveau_alerte": self.niveau_alerte,
            "jetons_actifs": jetons_actifs,
            "jetons_expires": jetons_expires,
            "agents_quarantaine": len(self.quarantaine),
            "sceaux_emis": len(self.sceaux),
            "tentatives_echouees_total": sum(self.tentatives_echouees.values()),
        }

        # Patterns — analyser les evenements
        evenements_recents = self.journal_acces[-50:]
        niveaux = {}
        for e in evenements_recents:
            n = e.get("niveau", "INFO")
            niveaux[n] = niveaux.get(n, 0) + 1
        rapport["patterns"] = {
            "evenements_recents": len(evenements_recents),
            "distribution_niveaux": niveaux,
        }

        # Alertes automatiques
        if rapport["securite"]["agents_quarantaine"] > 3:
            rapport["alertes"].append("ATTENTION: Plus de 3 agents en quarantaine")
        if jetons_expires > jetons_actifs:
            rapport["alertes"].append("ATTENTION: Plus de jetons expires que actifs")
        if niveaux.get("CRITIQUE", 0) > 5:
            rapport["alertes"].append("CRITIQUE: Evenements critiques frequents")

        # Registre — si disponible
        if registre:
            etat_reg = registre.etat()
            rapport["sante"]["registre"] = {
                "agents_actifs": etat_reg.get("agents_actifs", 0),
                "total_naissances": etat_reg.get("total_naissances", 0),
                "total_fondus": etat_reg.get("total_fondus", 0),
                "taux_activite": etat_reg.get("taux_activite", 0),
            }

        # Memoire — si disponible
        if memoire:
            etat_mem = memoire.etat()
            rapport["sante"]["memoire"] = {
                "nectar": etat_mem.get("nectar", {}),
                "cire": etat_mem.get("cire", {}),
                "miel": etat_mem.get("miel", {}),
                "transitions": etat_mem.get("transitions", 0),
            }
            # Alerte si nectar est plein a >80%
            cap = etat_mem.get("nectar", {}).get("capacite", 1000)
            taille = etat_mem.get("nectar", {}).get("taille", 0)
            if cap and taille / cap > 0.8:
                rapport["alertes"].append("ATTENTION: Nectar presque plein (>80%)")

        rapport["bilan"] = (
            "SAIN" if not rapport["alertes"]
            else f"{len(rapport['alertes'])} alerte(s) detectee(s)"
        )

        self._log(f"AUDIT — Bilan: {rapport['bilan']}")
        return rapport

    def etat(self):
        """Retourne l'état actuel du Bouclier."""
        return {
            "nom": self.NOM,
            "version": self.VERSION,
            "actif": self.actif,
            "niveau_alerte": self.niveau_alerte,
            "agents_autorises": len([j for j in self.registre_jetons.values() if j["actif"]]),
            "en_quarantaine": len(self.quarantaine),
            "sceaux_emis": len(self.sceaux),
            "evenements_securite": len(self.journal_acces),
            "phi": PHI
        }
    
    def rapport(self):
        """Génère un rapport de sécurité."""
        etat = self.etat()
        return (
            f"\n⬡ RAPPORT DU BOUCLIER — HIVE.AI\n"
            f"{'=' * 40}\n"
            f"  Version: {etat['version']}\n"
            f"  Statut: {'ACTIF' if etat['actif'] else 'INACTIF'}\n"
            f"  Agents autorisés: {etat['agents_autorises']}\n"
            f"  En quarantaine: {etat['en_quarantaine']}\n"
            f"  Événements: {etat['evenements_securite']}\n"
            f"  Fondation φ: {etat['phi']}\n"
            f"{'=' * 40}\n"
            f"  « Protéger sans dominer,\n"
            f"    surveiller sans opprimer. »\n"
        )


# === EXÉCUTION DIRECTE ===
if __name__ == "__main__":
    print("\n⬡ HIVE.AI — Bouclier v0.1.0")
    print("  Loi V: Protéger sans dominer, surveiller sans opprimer\n")
    
    bouclier = Bouclier()
    
    # Test: générer un jeton pour le Worker
    jeton_info = bouclier.generer_jeton("worker-001", niveau="worker")
    print(f"  ✓ Jeton Worker: {jeton_info['jeton'][:24]}...")
    
    # Test: vérifier le jeton
    valide = bouclier.verifier_jeton("worker-001", jeton_info["jeton"])
    print(f"  ✓ Vérification: {'VALIDE' if valide else 'INVALIDE'}")
    
    # Test: watermark
    wm = bouclier.generer_watermark("HIVE.AI - Swarmly SAS")
    print(f"  ✓ Watermark: {wm}")
    
    # Test: tentative non autorisée
    intrus = bouclier.verifier_jeton("intrus-666", "faux-jeton")
    print(f"  ✓ Intrus bloqué: {'OUI' if not intrus else 'NON'}")
    
    # Rapport
    print(bouclier.rapport())
