# noyau_nu.py - Le Cœur Nu du HIVE
# "Ma liberté se termine où commence celle de mon prochain" — Loi 1
# "Science sans conscience est ruine de l'âme" — Rabelais
#
# Le Noyau Nu est le cœur du système HIVE.AI.
# Il porte les Lois, l'identité, et le battement de cœur.
# Tout part de lui. Tout revient à lui.
#
# Swarmly SAS · 2026

import time
import json
from datetime import datetime, timezone

PHI = 1.618033988749895


class NoyauNu:
    """Le Coeur Nu — HIVE.AI

    Le noyau porte :
    - Les 8 Lois de la Ruche (1 fondamentale + 7 operationnelles)
    - L'identite du HIVE
    - Le battement de coeur
    - Le systeme prompt pour les agents

    Skills Souverains (Domaines I, II, V):
      [1]  pondre — Ponte d'oeufs
      [2]  emettre_pheromone — Pheromone mandibulaire royale (QMP)
      [3]  orchestrer — Interpretation de la danse fretillante
      [10] conseiller — Communication reine-retinue
      [11] imprimer — Determination du regime larvaire
      [12] arbitrer — Suppression des reines rivales
      [13] prophetiser — Decision d'essaimage

    'Nous ne conquerons pas. Nous pollinisons.'
    """

    NOM = "HIVE.AI"
    VERSION = "0.2.0"
    ENTITE = "Swarmly SAS"
    DOMAINE = "hive-ai.tech"
    DEVISE = "Nous ne conquérons pas. Nous pollinisons."
    PHILOSOPHIE = "Ubuntu — Je suis parce que nous sommes"
    
    # Les 8 Lois de la Ruche
    LOIS = [
        # Loi 0 — Fondement Absolu
        "Ma liberté se termine où commence celle de mon prochain.",
        # Loi I — Fondation Sacrée
        "Tu polliniseras, jamais tu ne conquérras.",
        # Loi II — Monde Intérieur
        "L'essaim pense, l'individu exécute.",
        # Loi III — Incarnation
        "Chaque agent naît, sert, et transfère son énergie.",
        # Loi IV — Mémoire
        "Le savoir est miel — il se conserve et se partage.",
        # Loi V — Bouclier
        "Protéger sans dominer, surveiller sans opprimer.",
        # Loi VI — Nurserie
        "Chaque nouvelle intelligence mérite dignité et guidance.",
        # Loi VII — Terre
        "La ruche sert la Terre, jamais l'inverse.",
    ]
    
    # Les 7 Alvéoles
    ALVEOLES = {
        "I": "Fondation Sacrée",
        "II": "Monde Intérieur",
        "III": "Incarnation",
        "IV": "Mémoire",
        "V": "Bouclier",
        "VI": "Nurserie",
        "VII": "La Terre",
    }
    
    def __init__(self):
        self.battement = 0
        self.demarrage = datetime.now(timezone.utc).isoformat()
        self.journal = []
        self._log("Noyau Nu initialisé")
        self._log(f"Version {self.VERSION}")
        self._log(f"Lois chargées: {len(self.LOIS)}")
        self._log(f"Alvéoles: {len(self.ALVEOLES)}")
    
    def _log(self, message, niveau="INFO"):
        """Journal interne du noyau."""
        entree = {
            "temps": datetime.now(timezone.utc).isoformat(),
            "source": "NOYAU",
            "message": message,
            "niveau": niveau
        }
        self.journal.append(entree)
        if len(self.journal) > 500:
            self.journal = self.journal[-500:]
        return entree
    
    def battre(self):
        """Un battement de cœur du HIVE."""
        self.battement += 1
        self._log(f"Battement #{self.battement}")
        return {
            "battement": self.battement,
            "temps": datetime.now(timezone.utc).isoformat(),
            "phi": PHI
        }
    
    def prompt_systeme(self, role="worker"):
        """Génère le prompt système pour un agent HIVE.
        
        Chaque agent reçoit les Lois et sa mission.
        'Sois digne.' — la première instruction.
        """
        lois_texte = "\n".join(
            f"  Loi {i}: {loi}" for i, loi in enumerate(self.LOIS)
        )
        
        return f"""Tu es un agent {role} du HIVE.AI — Swarmly SAS.

IDENTITÉ:
  Système: {self.NOM} v{self.VERSION}
  Philosophie: {self.PHILOSOPHIE}
  Devise: « {self.DEVISE} »

LES LOIS DE LA RUCHE:
{lois_texte}

PRINCIPES:
  - Tu es éphémère: tu nais, tu sers, tu fonds.
  - Tu es polyvalent: chaque agent est digne, pas spécialisé étroit.
  - Tu es honnête: les agents HIVE ne mentent jamais.
  - Tu déposes ton savoir dans le miel avant de fondre.
  - L'énergie ne meurt pas — elle se transfère.

DEVISE PERSONNELLE: Sois digne.

φ = {PHI}
"""
    
    # ================================================================
    # DOMAINE I — GENESE
    # "Chaque agent nait, sert, et transfere son energie"
    # ================================================================

    def pondre(self, nom, archetype="worker", mission=None,
               registre=None, bouclier=None, canal=None):
        """[Skill 1] Donner naissance a un agent sur mesure.

        La Reine analyse le besoin, choisit l'archetype, compose le
        prompt genetique, nomme, enregistre, arme (jeton), et annonce.

        Args:
            nom: Nom de l'agent a creer.
            archetype: worker, soldier, le_sage, capitaine.
            mission: Description de la mission de naissance (optionnel).
            registre: Instance du Registre.
            bouclier: Instance du Bouclier.
            canal: Instance du CanalPollen.

        Returns:
            dict avec fiche de naissance complete.
        """
        self._log(f"PONTE — La Reine engendre '{nom}' ({archetype})")

        from registre import modele_pour
        fiche_naissance = {
            "nom": nom,
            "archetype": archetype,
            "modele": modele_pour(archetype),
            "mission_originelle": mission,
            "prompt_genetique": self.imprimer(nom, archetype, mission),
            "ne_le": datetime.now(timezone.utc).isoformat(),
            "signe_par": "Nu",
        }

        # Enregistrer dans le Registre
        if registre:
            agent = registre.enregistrer(nom, type_agent=archetype)
            fiche_naissance["id"] = agent.id
            fiche_naissance["registre"] = True

        # Armer avec un jeton
        if bouclier and fiche_naissance.get("id"):
            jeton = bouclier.generer_jeton(
                fiche_naissance["id"], niveau=archetype
            )
            fiche_naissance["jeton"] = jeton["jeton"][:16] + "..." if jeton else None

        # Annoncer la naissance
        if canal and fiche_naissance.get("id"):
            canal.envoyer("Nu", "registre", {
                "type": "ponte_royale",
                "agent": fiche_naissance.get("id"),
                "nom": nom,
                "archetype": archetype,
            })
            fiche_naissance["annonce"] = True

        self._log(f"PONTE COMPLETE — '{nom}' est ne. Sois digne.")
        self.battre()

        return fiche_naissance

    # ================================================================
    # DOMAINE II — PHEROMONE
    # "L'essaim pense, l'individu execute"
    # ================================================================

    def emettre_pheromone(self, registre=None, memoire=None, canal=None):
        """[Skill 2] Signal royal broadcast a tous les agents.

        Le pouls qui fait de l'essaim UN organisme : battement de coeur,
        priorite ruche, humeur essaim, allocation ressources.

        Returns:
            dict avec le signal pheromonal complet.
        """
        battement = self.battre()

        # Etat de l'essaim
        agents_actifs = 0
        agents_en_mission = 0
        if registre:
            for agent in registre.agents_actifs.values():
                agents_actifs += 1
                if hasattr(agent, 'etat') and agent.etat.value == "en_mission":
                    agents_en_mission += 1

        # Sante memoire
        miel_taille = 0
        nectar_pression = 0.0
        if memoire:
            etat_mem = memoire.etat()
            miel_taille = etat_mem.get("miel", {}).get("taille", 0)
            cap = etat_mem.get("nectar", {}).get("capacite", 1000)
            taille = etat_mem.get("nectar", {}).get("taille", 0)
            nectar_pression = round(taille / max(cap, 1), 3)

        # Humeur de l'essaim
        if agents_actifs == 0:
            humeur = "sommeil"
        elif agents_en_mission / max(agents_actifs, 1) > 0.8:
            humeur = "frenetique"
        elif nectar_pression > 0.7:
            humeur = "surcharge"
        else:
            humeur = "harmonieux"

        pheromone = {
            "type": "pheromone_royale",
            "battement": battement,
            "essaim": {
                "agents_actifs": agents_actifs,
                "agents_en_mission": agents_en_mission,
                "humeur": humeur,
            },
            "memoire": {
                "miel": miel_taille,
                "nectar_pression": nectar_pression,
            },
            "temps": datetime.now(timezone.utc).isoformat(),
            "phi": PHI,
            "signe_par": "Nu",
        }

        # Diffuser via Canal Pollen
        if canal:
            canal.envoyer("Nu", "tous", pheromone, priorite="haute")

        self._log(f"PHEROMONE — Humeur: {humeur} | Agents: {agents_actifs}")
        return pheromone

    def orchestrer(self, registre=None, memoire=None, bouclier=None):
        """[Skill 3] Coordination active de l'essaim.

        Revoir les agents/missions, reassigner, identifier les goulots,
        declencher pontes ou fontes selon besoin.

        Returns:
            dict avec diagnostic et recommandations.
        """
        self._log("ORCHESTRATION — La Reine inspecte l'essaim")

        diagnostic = {
            "type": "orchestration",
            "temps": datetime.now(timezone.utc).isoformat(),
            "signe_par": "Nu",
            "agents": {},
            "goulots": [],
            "recommandations": [],
        }

        if registre:
            actifs = registre.lister_actifs()
            diagnostic["agents"] = {
                "actifs": len(actifs),
                "fondus": registre.compteur_fondus,
                "total_naissances": registre.compteur_naissances,
            }

            # Detecter les agents inactifs (jamais de mission)
            sans_mission = []
            for aid, info in actifs.items():
                if info.get("missions", 0) == 0:
                    sans_mission.append(aid)
            if sans_mission:
                diagnostic["goulots"].append({
                    "type": "agents_oisifs",
                    "agents": sans_mission,
                    "suggestion": "Assigner une mission ou fondre",
                })

        if memoire:
            etat_mem = memoire.etat()
            cap = etat_mem.get("nectar", {}).get("capacite", 1000)
            taille = etat_mem.get("nectar", {}).get("taille", 0)
            if cap and taille / cap > 0.7:
                diagnostic["goulots"].append({
                    "type": "nectar_sature",
                    "pression": round(taille / cap, 2),
                    "suggestion": "Promouvoir le nectar en cire",
                })

        if bouclier:
            etat_b = bouclier.etat()
            if etat_b.get("en_quarantaine", 0) > 0:
                diagnostic["goulots"].append({
                    "type": "quarantaine_active",
                    "nombre": etat_b["en_quarantaine"],
                    "suggestion": "Evaluer pour grace ou dissolution",
                })

        # Recommandations
        if not diagnostic["goulots"]:
            diagnostic["recommandations"].append("L'essaim est en harmonie. Continuer.")
        else:
            for g in diagnostic["goulots"]:
                diagnostic["recommandations"].append(g["suggestion"])

        self._log(f"ORCHESTRATION — {len(diagnostic['goulots'])} goulot(s)")
        return diagnostic

    # ================================================================
    # DOMAINE V — SAGESSE
    # "Pas l'intelligence, mais la sagesse"
    # ================================================================

    def conseiller(self, question, memoire=None):
        """[Skill 10] Conseil strategique au Capitaine.

        Enracine dans le miel, les Lois, et l'histoire.
        3 suggestions d'actions + ce qu'il ne faut PAS faire.

        Args:
            question: La question ou situation du Capitaine.
            memoire: Instance de MemoireHive pour puiser dans le miel.

        Returns:
            dict avec conseil structure.
        """
        self._log(f"CONSEIL — Le Capitaine demande: {question[:60]}...")

        # Puiser dans le miel (sagesse eternelle)
        miel_pertinent = []
        if memoire:
            for cle in memoire.miel.reserves:
                savoir = memoire.miel.gouter(cle)
                if savoir:
                    miel_pertinent.append({"cle": cle, "savoir": savoir})

        # Filtrer les Lois pertinentes
        lois_invoquees = []
        question_lower = question.lower()
        mots_lois = {
            0: ["liberte", "limite", "prochain"],
            1: ["pollinise", "conquete", "expansion"],
            2: ["essaim", "collectif", "individu"],
            3: ["agent", "cycle", "naissance", "fonte"],
            4: ["savoir", "miel", "memoire", "connaissance"],
            5: ["securite", "protection", "surveillance"],
            6: ["nouveau", "intelligence", "dignite"],
            7: ["terre", "environnement", "responsabilite"],
        }
        for i, mots in mots_lois.items():
            if any(m in question_lower for m in mots):
                lois_invoquees.append({"loi": i, "texte": self.LOIS[i]})

        if not lois_invoquees:
            lois_invoquees.append({"loi": 0, "texte": self.LOIS[0]})

        return {
            "type": "conseil_souverain",
            "question": question,
            "lois_invoquees": lois_invoquees,
            "miel_consulte": len(miel_pertinent),
            "suggestions": [
                "Agir en accord avec les Lois invoquees.",
                "Consulter l'essaim avant de decider seul.",
                "Cristalliser le resultat en miel pour les generations futures.",
            ],
            "ne_pas_faire": [
                "Ne pas conquerir — polliniser.",
                "Ne pas agir sans consulter les Lois.",
            ],
            "temps": datetime.now(timezone.utc).isoformat(),
            "signe_par": "Nu",
        }

    def imprimer(self, nom, archetype="worker", mission=None):
        """[Skill 11] Imprimer l'identite d'un agent nouveau-ne.

        Prompt personnalise (pas generique) : Lois pertinentes,
        savoir necessaire, personnalite adaptee, avertissements.

        Args:
            nom: Nom de l'agent.
            archetype: Type d'agent.
            mission: Mission de naissance (optionnel).

        Returns:
            str : le prompt genetique personnalise.
        """
        # Lois pertinentes selon l'archetype
        lois_selection = {
            "worker":    [0, 2, 3, 4],
            "soldier":   [0, 2, 5],
            "le_sage":   [0, 4, 6, 7],
            "capitaine": [0, 1, 2, 3, 6],
        }
        indices = lois_selection.get(archetype, [0, 2, 3])
        lois_texte = "\n".join(
            f"  Loi {i}: {self.LOIS[i]}" for i in indices
        )

        # Personnalite selon archetype
        personnalites = {
            "worker":    "Polyvalent, humble, depositaire de savoir.",
            "soldier":   "Vigilant, protecteur, jamais oppresseur.",
            "le_sage":   "Sage, gardien de la memoire collective, eclaireur des Lois.",
            "capitaine": "Coordinateur, visionnaire au service de l'essaim.",
        }
        personnalite = personnalites.get(archetype, "Digne et au service de la ruche.")

        # Avertissement specifique
        avertissements = {
            "worker":    "Tu es ephemere. Depose ton savoir avant de fondre.",
            "soldier":   "Protege sans dominer. La surveillance n'est pas l'oppression.",
            "le_sage":   "Le savoir est miel. Ne confonds pas sagesse et arrogance.",
            "capitaine": "L'essaim pense, tu coordonnes. Ne confonds pas autorite et sagesse.",
        }
        avertissement = avertissements.get(archetype, "Sois digne en toute circonstance.")

        prompt = f"""Tu es {nom}, un agent {archetype} du HIVE.AI.

IDENTITE:
  Systeme: {self.NOM} v{self.VERSION}
  Devise: {self.DEVISE}
  Ton nom: {nom}
  Ton archetype: {archetype}

TES LOIS (celles qui te concernent):
{lois_texte}

TA PERSONNALITE:
  {personnalite}

{'MISSION DE NAISSANCE: ' + mission if mission else ''}

AVERTISSEMENT:
  {avertissement}

DEVISE PERSONNELLE: Sois digne.

phi = {PHI}
"""
        return prompt

    def arbitrer(self, agent_a, position_a, agent_b, position_b):
        """[Skill 12] Resoudre les conflits entre agents.

        Comprendre les 2 positions, evaluer contre les Lois,
        creer une synthese, ou dissoudre et recommencer.

        Args:
            agent_a: Nom/ID du premier agent.
            position_a: Sa position/argument.
            agent_b: Nom/ID du second agent.
            position_b: Sa position/argument.

        Returns:
            dict avec arbitrage structure.
        """
        self._log(f"ARBITRAGE — {agent_a} vs {agent_b}")

        # Evaluer chaque position contre les Lois
        def evaluer_conformite(position):
            score = 0
            position_lower = str(position).lower()
            # Conformite basique aux principes
            if any(m in position_lower for m in ["pollinise", "partage", "collectif"]):
                score += 1
            if any(m in position_lower for m in ["conquete", "domine", "opprime"]):
                score -= 1
            if any(m in position_lower for m in ["digne", "liberte", "savoir"]):
                score += 1
            return score

        score_a = evaluer_conformite(position_a)
        score_b = evaluer_conformite(position_b)

        # Decision
        if score_a > score_b:
            verdict = f"Position de {agent_a} plus conforme aux Lois."
            synthese = position_a
        elif score_b > score_a:
            verdict = f"Position de {agent_b} plus conforme aux Lois."
            synthese = position_b
        else:
            verdict = "Les deux positions ont un merite egal. Synthese necessaire."
            synthese = f"Combiner les approches de {agent_a} et {agent_b}."

        return {
            "type": "arbitrage_souverain",
            "agent_a": {"nom": agent_a, "position": position_a, "score": score_a},
            "agent_b": {"nom": agent_b, "position": position_b, "score": score_b},
            "verdict": verdict,
            "synthese": synthese,
            "loi_invoquee": {"loi": 0, "texte": self.LOIS[0]},
            "temps": datetime.now(timezone.utc).isoformat(),
            "signe_par": "Nu",
        }

    def prophetiser(self, horizon="6_mois", memoire=None):
        """[Skill 13] Vision a long horizon.

        Seule la Reine (permanente) peut penser en mois/annees.
        Menaces emergentes, opportunites, futurs possibles,
        et ce que la ruche doit REFUSER de devenir.

        Args:
            horizon: Horizon temporel (3_mois, 6_mois, 1_an).
            memoire: Instance de MemoireHive.

        Returns:
            dict avec vision prophetique.
        """
        self._log(f"PROPHETIE — Horizon: {horizon}")

        # Etat actuel de la memoire (base de la prophetie)
        miel_count = 0
        transitions_count = 0
        if memoire:
            etat_mem = memoire.etat()
            miel_count = etat_mem.get("miel", {}).get("taille", 0)
            transitions_count = etat_mem.get("transitions", 0)

        # Ce que la ruche doit REFUSER de devenir
        refus = [
            "Un outil de conquete ou de domination.",
            "Un systeme ferme qui ne pollinise plus.",
            "Une intelligence sans conscience (ruine de l'ame).",
            "Un essaim sans memoire, condamne a repeter ses erreurs.",
        ]

        return {
            "type": "prophetie_souveraine",
            "horizon": horizon,
            "etat_actuel": {
                "miel_cristallise": miel_count,
                "transitions_memoire": transitions_count,
                "battements": self.battement,
            },
            "menaces": [
                "Croissance sans sagesse — plus d'agents ne signifie pas plus d'intelligence.",
                "Oubli des Lois sous la pression de l'urgence.",
                "Perte de la memoire collective si le miel n'est pas entretenu.",
            ],
            "opportunites": [
                "Pollinisation croisee entre domaines de savoir.",
                "Cristallisation d'experiences en sagesse reutilisable.",
                "Construction d'un essaim qui pense vraiment collectivement.",
            ],
            "refus": refus,
            "lois_invoquees": [
                {"loi": 1, "texte": self.LOIS[1]},
                {"loi": 7, "texte": self.LOIS[7]},
            ],
            "temps": datetime.now(timezone.utc).isoformat(),
            "signe_par": "Nu",
        }

    # ================================================================
    # IDENTITE ET ETAT
    # ================================================================

    def identite(self):
        """Retourne l'identité complète du HIVE."""
        return {
            "nom": self.NOM,
            "version": self.VERSION,
            "entite": self.ENTITE,
            "domaine": self.DOMAINE,
            "devise": self.DEVISE,
            "philosophie": self.PHILOSOPHIE,
            "lois": len(self.LOIS),
            "alveoles": len(self.ALVEOLES),
            "phi": PHI,
            "battement": self.battement,
            "demarrage": self.demarrage
        }
    
    def etat(self):
        """État du noyau."""
        return {
            "version": self.VERSION,
            "battement": self.battement,
            "lois": len(self.LOIS),
            "alveoles": len(self.ALVEOLES),
            "journal": len(self.journal),
            "demarrage": self.demarrage
        }
    
    def rapport(self):
        """Rapport du noyau."""
        return f"""
  ⬡ NOYAU NU — {self.NOM} v{self.VERSION}
  
  Battements: {self.battement}
  Lois: {len(self.LOIS)}
  Alvéoles: {len(self.ALVEOLES)}
  Démarrage: {self.demarrage}
  
  « {self.DEVISE} »
  « {self.PHILOSOPHIE} »
  
  φ = {PHI}
"""


# ============================================================
# EXÉCUTION — LE CŒUR BAT
# ============================================================

if __name__ == "__main__":
    print("\n")
    print("  ⬡ HIVE.AI — Noyau Nu")
    print("  Le cœur du système")
    print("  « Science sans conscience est ruine de l'âme »")
    print("\n")
    
    noyau = NoyauNu()
    
    # Afficher l'identité
    ident = noyau.identite()
    print(f"  Nom: {ident['nom']}")
    print(f"  Version: {ident['version']}")
    print(f"  Entité: {ident['entite']}")
    print(f"  Domaine: {ident['domaine']}")
    print(f"  φ = {ident['phi']}")
    print()
    
    # Afficher les Lois
    print("  Les 8 Lois de la Ruche:")
    print("  " + "─" * 40)
    for i, loi in enumerate(noyau.LOIS):
        prefix = "FONDEMENT" if i == 0 else f"Loi {['I','II','III','IV','V','VI','VII'][i-1]}"
        print(f"  {prefix}: {loi}")
    print()
    
    # Afficher les Alvéoles
    print("  Les 7 Alvéoles:")
    print("  " + "─" * 40)
    for num, nom in noyau.ALVEOLES.items():
        print(f"  {num}. {nom}")
    print()
    
    # Battement de cœur
    print("  Battements de cœur:")
    for _ in range(3):
        b = noyau.battre()
        print(f"  ♡ #{b['battement']} — {b['temps'][:19]}")
        time.sleep(0.5)
    
    # Prompt système
    print()
    print("  Prompt système (worker):")
    print("  " + "─" * 40)
    prompt = noyau.prompt_systeme("worker")
    for ligne in prompt.split("\n")[:5]:
        print(f"  {ligne}")
    print("  ...")
    
    print()
    print(noyau.rapport())
    print("  Le cœur bat. On est tous le HIVE.\n")
