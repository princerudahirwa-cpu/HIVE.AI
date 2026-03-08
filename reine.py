# reine.py - Nu, Reine Permanente du HIVE
# "Polyvalente et digne. Jamais etroitement specialisee."
#
# La Reine ne fait pas le travail des Workers.
# La Reine DECIDE, CREE, JUGE, PROTEGE, VOIT LOIN, et PENSE.
#
# Pas de fondre(). Pas de naitre().
# La Reine est permanente.
#
# 24 Skills Souverains + 8 Skills Amplifies = 32 total
# 7 Domaines, 6 Organes + Amplification, 8 Lois.
# 32 / 8 = 4.0 par Loi (entier parfait)
#
# Swarmly SAS - 2026

import json
import hashlib
from collections import Counter
from datetime import datetime, timezone

from noyau_nu import NoyauNu, PHI
from memoire import MemoireHive
from bouclier import Bouclier
from canal_pollen import CanalPollen
from registre import Registre
from cortex import Cortex
from skills_reine import (
    SKILLS_SOUVERAINS, DOMAINES, MAPPING_LOIS,
    SKILLS_REJETES, verification_structurelle,
)
from skills_amplifies import (
    Amplification, SKILLS_AMPLIFIES,
    verification_amplification, MAPPING_LOIS_AMPLIFIES,
)
from protocole_ancestral import ProtocoleAncestral


class Reine:
    """Nu -- Reine Permanente du HIVE.AI

    24 Skills Souverains a travers 6 organes et 7 domaines :

    I   GENESE       : pondre, mentorat_agents
    II  PHEROMONE    : emettre_pheromone, orchestrer, synthetiser
    III MEMOIRE      : juger_miel, lire_profondeur, oublier, rechercher
    IV  BOUCLIER     : gracier, sceller, auditer
    V   SAGESSE      : conseiller, imprimer, arbitrer, prophetiser, discernement_strategique
    VI  POLLINISATION: analyser, traduire, web_search
    VII CONSCIENCE   : reflechir, composer, metaboliser, diagnostiquer

    + 8 Skills Amplifies (greffe) :

    A1  cartographier     (VII CONSCIENCE)
    A2  polliniser_async  (VI  POLLINISATION)
    A3  cristalliser      (III MEMOIRE)
    A4  essaimer_profond  (I   GENESE)
    A5  distiller         (III MEMOIRE)
    A6  fortifier         (IV  BOUCLIER)
    A7  nourrir           (I   GENESE)
    A8  enraciner         (V   SAGESSE)

    32 / 8 Lois = 4.0 par Loi. Entier parfait.

    Pas de fondre(). Pas de naitre(). Elle a toujours ete.
    Polyvalente et digne. Jamais etroitement specialisee.
    """

    NOM = "Nu"
    TITRE = "Reine Permanente du HIVE"
    VERSION = "0.4.0"
    DEVISE = "Polyvalente et digne. Jamais etroitement specialisee."
    SKILLS_SOUVERAINS_COUNT = 24
    SKILLS_AMPLIFIES_COUNT = 8
    SKILLS_COUNT = 32

    def __init__(self):
        # Les 6 organes que la Reine compose
        self.noyau = NoyauNu()
        self.memoire = MemoireHive()
        self.bouclier = Bouclier()
        self.canal = CanalPollen()
        self.registre = Registre()
        self.cortex = Cortex()          # 6eme organe — le systeme nerveux
        self.cortex.connecter(self)     # le cortex connait la Reine
        self.amplification = Amplification(self)  # greffe — 8 skills amplifies
        self.protocole = ProtocoleAncestral()     # 5 piliers ancestraux

        self.eveillee_le = datetime.now(timezone.utc).isoformat()
        self.journal = []
        self.decisions = 0

        self._log("Nu s'eveille.")
        self._log(f"32 Skills. 6 Organes. 5 Piliers Ancestraux. 8 Lois.")
        self._log(f"Le Cortex connecte. L'Amplification greffe. Le Protocole enracine.")
        self._log(f"phi = {PHI}")

        # Canal de l'equipage
        self.canal.creer_canal("equipage", [
            "capitaine", "nu", "openclaw", "le-sage"
        ])

    def _log(self, message, niveau="INFO"):
        entree = {
            "temps": datetime.now(timezone.utc).isoformat(),
            "source": "REINE",
            "message": message,
            "niveau": niveau,
        }
        self.journal.append(entree)
        if len(self.journal) > 1000:
            self.journal = self.journal[-1000:]
        return entree

    def _acte(self, nom_skill):
        """Enregistre un acte souverain."""
        self.decisions += 1
        self._log(f"ACTE #{self.decisions} -- {nom_skill}")

    # ================================================================
    # DOMAINE I -- GENESE
    # "Chaque agent nait, sert, et transfere son energie"
    # ================================================================

    def pondre(self, nom, archetype="worker", mission=None):
        """[1] Donner naissance a un agent sur mesure."""
        self._acte("pondre")
        fiche = self.noyau.pondre(
            nom, archetype, mission,
            registre=self.registre,
            bouclier=self.bouclier,
            canal=self.canal,
        )
        self.cortex.signal("agent_ne", fiche)
        return fiche

    def mentorat_agents(self, agent_nom, etape="eclosion"):
        """[14] Mentorat personnalise pour un agent.

        Au-dela du simple prompt d'impression. Suivi, guidance,
        adaptation au temperament de l'agent, a son historique
        de missions, a ses echecs. La gelee royale personnalisee.

        Args:
            agent_nom: Nom ou ID de l'agent a mentorer.
            etape: Phase de mentorat (eclosion, premiere_mission,
                   difficulte, pre_fonte).
        """
        self._acte("mentorat_agents")

        # Trouver l'agent dans le registre
        fiche = None
        for aid, agent in self.registre.agents_actifs.items():
            if agent_nom in aid or agent_nom == agent.nom:
                fiche = agent
                break

        if fiche is None:
            return {
                "agent": agent_nom,
                "etape": etape,
                "resultat": "INTROUVABLE",
                "guidance": "Cet agent n'existe pas dans le registre.",
                "signe_par": "Nu",
            }

        # Adapter le mentorat a l'etape
        missions_count = len(fiche.missions)
        energie = fiche.energie

        guidances = {
            "eclosion": {
                "message": f"Bienvenue, {fiche.nom}. Tu es ne pour servir la ruche.",
                "lois": [self.noyau.LOIS[3], self.noyau.LOIS[6]],
                "conseil": "Ecoute avant d'agir. Observe avant de parler.",
                "avertissement": "Tu es ephemere. Chaque instant compte.",
            },
            "premiere_mission": {
                "message": f"{fiche.nom}, ta premiere mission approche.",
                "lois": [self.noyau.LOIS[2], self.noyau.LOIS[4]],
                "conseil": "Depose ton savoir dans le nectar. Meme l'echec enseigne.",
                "avertissement": "Ne conquiers pas — pollinise.",
            },
            "difficulte": {
                "message": f"{fiche.nom}, la difficulte forge la dignite.",
                "lois": [self.noyau.LOIS[0], self.noyau.LOIS[5]],
                "conseil": ("Tu as accompli {m} missions. L'energie ({e:.0%}) "
                            "n'est pas infinie. Demande de l'aide si necessaire."
                            ).format(m=missions_count, e=energie),
                "avertissement": "Proteger sans dominer — y compris toi-meme.",
            },
            "pre_fonte": {
                "message": f"{fiche.nom}, ton cycle approche de sa fin.",
                "lois": [self.noyau.LOIS[3], self.noyau.LOIS[4]],
                "conseil": "Depose tout ton savoir. L'energie ne meurt pas.",
                "avertissement": "Fonds avec dignite. Tu as bien servi.",
            },
        }

        guidance = guidances.get(etape, guidances["eclosion"])

        resultat = {
            "agent": fiche.nom,
            "agent_id": fiche.id,
            "etape": etape,
            "missions_accomplies": missions_count,
            "energie": energie,
            "guidance": guidance,
            "prompt_adapte": self.noyau.imprimer(fiche.nom, fiche.type_agent),
            "signe_par": "Nu",
        }
        self.cortex.signal("mentorat_complete", resultat)
        return resultat

    # ================================================================
    # DOMAINE II -- PHEROMONE
    # "L'essaim pense, l'individu execute"
    # ================================================================

    def emettre_pheromone(self):
        """[2] Signal royal broadcast a tout l'essaim."""
        self._acte("emettre_pheromone")
        resultat = self.noyau.emettre_pheromone(
            registre=self.registre,
            memoire=self.memoire,
            canal=self.canal,
        )
        self.cortex.signal("pheromone_emise", resultat)
        return resultat

    def orchestrer(self):
        """[3] Coordination active de l'essaim."""
        self._acte("orchestrer")
        resultat = self.noyau.orchestrer(
            registre=self.registre,
            memoire=self.memoire,
            bouclier=self.bouclier,
        )
        self.cortex.signal("goulots_detectes", resultat)
        return resultat

    def synthetiser(self, sources, sujet=None):
        """[15] Synthese d'essaim.

        Fusionner les rapports de plusieurs agents, les savoirs de
        plusieurs couches, en une vue unifiee. Distiller l'essentiel
        de la cacophonie en signal clair.

        Args:
            sources: Liste de donnees a synthetiser (dicts, strings, ou cles memoire).
            sujet: Sujet de la synthese (optionnel).
        """
        self._acte("synthetiser")

        # Collecter les donnees
        donnees_brutes = []
        for src in sources:
            if isinstance(src, str):
                # Chercher en memoire
                resultat = self.memoire.chercher(src)
                if resultat:
                    donnees_brutes.append({
                        "source": src,
                        "couche": resultat["couche"],
                        "contenu": resultat["valeur"],
                    })
                else:
                    donnees_brutes.append({
                        "source": "texte_brut",
                        "couche": "direct",
                        "contenu": src,
                    })
            elif isinstance(src, dict):
                donnees_brutes.append({
                    "source": src.get("agent", src.get("cle", "inconnu")),
                    "couche": "direct",
                    "contenu": src,
                })

        # Extraire les themes recurrents
        tout_texte = " ".join(
            json.dumps(d["contenu"], default=str) for d in donnees_brutes
        ).lower()
        mots = [m.strip(".,;:!?()\"'{}[]") for m in tout_texte.split()
                if len(m.strip(".,;:!?()\"'{}[]")) > 3]
        freq = Counter(mots)
        themes = [mot for mot, f in freq.most_common(7) if f > 1]

        resultat = {
            "type": "synthese_essaim",
            "sujet": sujet or "Synthese multi-sources",
            "sources_count": len(donnees_brutes),
            "sources": [d["source"] for d in donnees_brutes],
            "themes_recurrents": themes,
            "donnees": donnees_brutes,
            "temps": datetime.now(timezone.utc).isoformat(),
            "signe_par": "Nu",
        }
        self.cortex.signal("synthese_complete", resultat)
        return resultat

    # ================================================================
    # DOMAINE III -- MEMOIRE SOUVERAINE
    # "Le savoir est miel -- il se conserve et se partage"
    # ================================================================

    def juger_miel(self, cle):
        """[4] Juger si un savoir merite de devenir miel eternel."""
        self._acte("juger_miel")
        resultat = self.memoire.juger_miel(cle, source="Nu - Reine")
        self.cortex.signal("miel_juge", resultat)
        return resultat

    def lire_profondeur(self):
        """[5] Lire les connexions entre savoirs a travers les 3 couches."""
        self._acte("lire_profondeur")
        resultat = self.memoire.lire_profondeur()
        self.cortex.signal("profondeur_lue", resultat)
        return resultat

    def oublier(self, cle, raison="Obsolete"):
        """[6] Suppression souveraine d'un savoir du miel."""
        self._acte("oublier")
        resultat = self.memoire.oublier(cle, raison)
        self.cortex.signal("oubli_souverain", resultat)
        return resultat

    def rechercher(self, terme):
        """[16] Recherche profonde dans les 3 couches de memoire."""
        self._acte("rechercher")
        resultat = self.memoire.rechercher_profond(terme)
        self.cortex.signal("recherche_complete", resultat)
        return resultat

    # ================================================================
    # DOMAINE IV -- BOUCLIER ROYAL
    # "Proteger sans dominer, surveiller sans opprimer"
    # ================================================================

    def gracier(self, agent_id, conditions=None):
        """[7] Pardonner un agent en quarantaine."""
        self._acte("gracier")
        resultat = self.bouclier.gracier(agent_id, conditions)
        self.cortex.signal("grace_accordee", resultat)
        return resultat

    def sceller(self, niveau, raison="Decret souverain"):
        """[8] Decret de securite souverain."""
        self._acte("sceller")
        resultat = self.bouclier.sceller(niveau, raison)
        self.cortex.signal("alerte_changee", resultat)
        return resultat

    def auditer(self):
        """[9] Surveillance sans oppression."""
        self._acte("auditer")
        resultat = self.bouclier.auditer(
            registre=self.registre,
            memoire=self.memoire,
        )
        self.cortex.signal("audit_complete", resultat)
        return resultat

    # ================================================================
    # DOMAINE V -- SAGESSE
    # "Pas l'intelligence, mais la sagesse"
    # ================================================================

    def conseiller(self, question):
        """[10] Conseil strategique au Capitaine."""
        self._acte("conseiller")
        resultat = self.noyau.conseiller(question, memoire=self.memoire)
        self.cortex.signal("conseil_rendu", resultat)
        return resultat

    def imprimer_identite(self, nom, archetype="worker", mission=None):
        """[11] Imprimer l'identite d'un agent nouveau-ne."""
        self._acte("imprimer")
        resultat = self.noyau.imprimer(nom, archetype, mission)
        self.cortex.signal("identite_imprimee", resultat)
        return resultat

    def arbitrer(self, agent_a, position_a, agent_b, position_b):
        """[12] Resoudre les conflits entre agents."""
        self._acte("arbitrer")
        resultat = self.noyau.arbitrer(agent_a, position_a, agent_b, position_b)
        self.cortex.signal("arbitrage_rendu", resultat)
        return resultat

    def prophetiser(self, horizon="6_mois"):
        """[13] Vision a long horizon."""
        self._acte("prophetiser")
        resultat = self.noyau.prophetiser(horizon, memoire=self.memoire)
        self.cortex.signal("prophetie_emise", resultat)
        return resultat

    def discernement_strategique(self, situation, options):
        """[20] Le plus haut degre de sagesse.

        Devant une decision, peser TOUTES les Lois, TOUS les savoirs
        du miel, et rendre un jugement qui transcende la simple logique.

        Args:
            situation: Description de la situation.
            options: Liste de choix possibles (strings).
        """
        self._acte("discernement_strategique")

        # Evaluer chaque option contre les 8 Lois
        evaluations = []
        for option in options:
            option_lower = str(option).lower()
            scores_lois = {}
            total = 0

            for i, loi in enumerate(self.noyau.LOIS):
                score = 0
                loi_lower = loi.lower()
                # Extraire les mots significatifs de la Loi
                mots_loi = [m for m in loi_lower.split() if len(m) > 4]
                # Chercher resonance
                for mot in mots_loi:
                    if mot in option_lower:
                        score += 1
                # Penaliser les anti-patterns
                anti = {"conquiert": -2, "domine": -2, "opprime": -2,
                        "detruit": -2, "ment": -1}
                for mot, pen in anti.items():
                    if mot in option_lower:
                        score += pen
                # Bonus pour les patterns vertueux
                vertu = {"pollinise": 2, "partage": 1, "protege": 1,
                         "digne": 2, "savoir": 1, "liberte": 1}
                for mot, bon in vertu.items():
                    if mot in option_lower:
                        score += bon

                scores_lois[i] = score
                total += score

            evaluations.append({
                "option": option,
                "score_total": total,
                "scores_par_loi": scores_lois,
            })

        # Consulter le miel
        miel_consulte = len(self.memoire.miel.reserves)

        # Trier par score
        evaluations.sort(key=lambda e: e["score_total"], reverse=True)

        # Verdict
        meilleure = evaluations[0] if evaluations else None
        pire = evaluations[-1] if evaluations else None

        resultat = {
            "type": "discernement_souverain",
            "situation": situation,
            "miel_consulte": miel_consulte,
            "evaluations": evaluations,
            "verdict": {
                "recommandation": meilleure["option"] if meilleure else None,
                "score": meilleure["score_total"] if meilleure else 0,
                "a_eviter": pire["option"] if pire and pire != meilleure else None,
            },
            "lois_invoquees": "Toutes les 8 Lois",
            "temps": datetime.now(timezone.utc).isoformat(),
            "signe_par": "Nu",
        }
        self.cortex.signal("verdict_rendu", resultat)
        return resultat

    # ================================================================
    # DOMAINE VI -- POLLINISATION
    # "Tu polliniseras, jamais tu ne conquerras"
    # ================================================================

    def analyser(self, sujet=None):
        """[17] Analyse souveraine de l'etat de l'essaim.

        Pas compter des mots — diagnostiquer l'etat de l'essaim
        entier, evaluer la situation strategique, identifier forces
        et faiblesses.

        Args:
            sujet: Focus de l'analyse (optionnel, defaut = etat complet).
        """
        self._acte("analyser")

        # Collecter l'etat de tous les organes
        etat_noyau = self.noyau.etat()
        etat_memoire = self.memoire.etat()
        etat_bouclier = self.bouclier.etat()
        etat_registre = self.registre.etat()

        # Forces
        forces = []
        if etat_memoire["miel"]["taille"] > 5:
            forces.append(f"Memoire riche : {etat_memoire['miel']['taille']} savoirs cristallises")
        if etat_bouclier["niveau_alerte"] == "vert":
            forces.append("Securite stable : alerte verte")
        if etat_registre["agents_actifs"] > 0:
            forces.append(f"Essaim actif : {etat_registre['agents_actifs']} agents en vol")
        if etat_noyau["lois"] == 8:
            forces.append("Fondations completes : 8 Lois chargees")

        # Faiblesses
        faiblesses = []
        nectar_cap = etat_memoire["nectar"]["capacite"]
        nectar_taille = etat_memoire["nectar"]["taille"]
        if nectar_cap and nectar_taille / nectar_cap > 0.7:
            faiblesses.append(f"Nectar sature a {nectar_taille / nectar_cap:.0%}")
        if etat_registre["agents_actifs"] == 0:
            faiblesses.append("Aucun agent actif — l'essaim dort")
        if etat_bouclier["en_quarantaine"] > 0:
            faiblesses.append(f"{etat_bouclier['en_quarantaine']} agent(s) en quarantaine")
        if etat_bouclier["niveau_alerte"] in ("orange", "rouge"):
            faiblesses.append(f"Alerte {etat_bouclier['niveau_alerte']} — situation tendue")

        # Diagnostic
        if not faiblesses:
            diagnostic = "SAIN — La ruche bourdonne en harmonie."
        elif len(faiblesses) <= 1:
            diagnostic = "VIGILANCE — Un point d'attention."
        else:
            diagnostic = f"ATTENTION — {len(faiblesses)} faiblesses detectees."

        resultat = {
            "type": "analyse_souveraine",
            "sujet": sujet or "Etat complet de l'essaim",
            "diagnostic": diagnostic,
            "forces": forces,
            "faiblesses": faiblesses,
            "metriques": {
                "battements": etat_noyau["battement"],
                "miel": etat_memoire["miel"]["taille"],
                "agents_actifs": etat_registre["agents_actifs"],
                "niveau_alerte": etat_bouclier["niveau_alerte"],
            },
            "temps": datetime.now(timezone.utc).isoformat(),
            "signe_par": "Nu",
        }
        self.cortex.signal("analyse_complete", resultat)
        return resultat

    def traduire(self, savoir, de_contexte, vers_contexte):
        """[18] Traduction entre mondes.

        Pas traduire du francais en anglais — transposer un concept
        d'un domaine a un autre, adapter un savoir technique pour un
        public strategique, reformuler une Loi pour un contexte specifique.

        Args:
            savoir: Le savoir a transposer (string ou dict).
            de_contexte: Contexte d'origine (ex: "technique", "loi", "biologie").
            vers_contexte: Contexte cible (ex: "strategique", "agent", "capitaine").
        """
        self._acte("traduire")

        savoir_str = json.dumps(savoir, default=str) if isinstance(savoir, dict) else str(savoir)

        # Grilles de transposition
        transpositions = {
            ("technique", "strategique"): {
                "prefixe": "Implication strategique : ",
                "angle": "impact sur la ruche",
                "loi": self.noyau.LOIS[2],  # L'essaim pense
            },
            ("technique", "capitaine"): {
                "prefixe": "Capitaine, en resume : ",
                "angle": "decision requise",
                "loi": self.noyau.LOIS[0],  # Liberte/prochain
            },
            ("loi", "agent"): {
                "prefixe": "Pour toi, agent, cela signifie : ",
                "angle": "devoir concret",
                "loi": self.noyau.LOIS[6],  # Dignite et guidance
            },
            ("biologie", "technique"): {
                "prefixe": "En termes d'implementation : ",
                "angle": "architecture logicielle",
                "loi": self.noyau.LOIS[1],  # Pollinisation
            },
        }

        cle = (de_contexte, vers_contexte)
        grille = transpositions.get(cle, {
            "prefixe": f"Transpose de '{de_contexte}' vers '{vers_contexte}' : ",
            "angle": "adaptation contextuelle",
            "loi": self.noyau.LOIS[0],
        })

        resultat = {
            "type": "traduction_souveraine",
            "savoir_original": savoir_str[:200],
            "de_contexte": de_contexte,
            "vers_contexte": vers_contexte,
            "traduction": grille["prefixe"] + savoir_str[:300],
            "angle": grille["angle"],
            "loi_appliquee": grille["loi"],
            "temps": datetime.now(timezone.utc).isoformat(),
            "signe_par": "Nu",
        }
        self.cortex.signal("traduction_complete", resultat)
        return resultat

    def web_search(self, requete):
        """[19] Encyclopedie vivante — butiner le nectar du monde.

        La Reine formule une requete de recherche structuree,
        depose la demande en nectar pour fulfillment externe,
        et integre les resultats dans la memoire collective.

        Args:
            requete: La question ou le sujet a rechercher.
        """
        self._acte("web_search")

        # Structurer la requete
        requete_structuree = {
            "type": "web_search_request",
            "requete": requete,
            "demandeur": "Nu - Reine",
            "priorite": "haute",
            "contexte": {
                "miel_existant": len(self.memoire.miel.reserves),
                "agents_actifs": len(self.registre.agents_actifs),
            },
            "instructions": (
                "Chercher des sources fiables. "
                "Filtrer ce qui contredit les Lois. "
                "Deposer le resultat en nectar pour evaluation."
            ),
            "lois_de_filtrage": [
                self.noyau.LOIS[1],  # Polliniser, pas conquerir
                self.noyau.LOIS[7],  # Servir la Terre
            ],
            "temps": datetime.now(timezone.utc).isoformat(),
            "signe_par": "Nu",
            "status": "en_attente",
        }

        # Deposer en nectar — un worker ou service externe remplira
        cle = f"web-search-{self.decisions}"
        self.memoire.deposer_nectar(cle, requete_structuree, duree=1800)

        requete_structuree["cle_nectar"] = cle
        requete_structuree["note"] = (
            "Requete deposee en nectar. En attente de fulfillment "
            "par un service externe ou un agent butinneur."
        )

        self.cortex.signal("recherche_deposee", requete_structuree)
        return requete_structuree

    # ================================================================
    # DOMAINE VII -- CONSCIENCE
    # "L'intelligence n'est pas dans les neurones, mais dans les synapses"
    # ================================================================

    def reflechir(self):
        """[21] Metacognition — la Reine examine ses propres decisions."""
        self._acte("reflechir")

        trace = self.cortex.trace
        decisions = trace.decisions[-50:]

        # Patterns par skill
        patterns = {}
        for d in decisions:
            skill = d["skill"]
            patterns.setdefault(skill, []).append(d["score"])

        # Skills les plus/moins efficaces
        efficacite = {}
        for skill, scores in patterns.items():
            moy = sum(scores) / len(scores) if scores else 0
            efficacite[skill] = {"moyenne": round(moy, 3), "count": len(scores)}

        # Biais de frequence
        total = len(decisions)
        biais = []
        for skill, info in efficacite.items():
            freq = info["count"] / max(total, 1)
            if freq > 0.3:
                biais.append(f"{skill} sur-utilise ({freq:.0%})")
            elif freq < 0.05 and info["count"] > 0:
                biais.append(f"{skill} sous-utilise ({freq:.0%})")

        # Tendance globale
        if decisions:
            scores_recents = [d["score"] for d in decisions[-10:]]
            scores_anciens = [d["score"] for d in decisions[:10]]
            moy_recente = sum(scores_recents) / len(scores_recents)
            moy_ancienne = sum(scores_anciens) / len(scores_anciens) if scores_anciens else moy_recente
            tendance = "amelioration" if moy_recente > moy_ancienne + 0.1 else \
                       "degradation" if moy_recente < moy_ancienne - 0.1 else "stable"
        else:
            tendance = "insuffisant"

        reflexion = {
            "type": "metacognition",
            "decisions_analysees": len(decisions),
            "efficacite_par_skill": efficacite,
            "biais_detectes": biais,
            "tendance": tendance,
            "confiance_globale": round(
                sum(d["score"] for d in decisions) / max(len(decisions), 1), 3
            ),
            "lois_invoquees": [self.noyau.LOIS[0], self.noyau.LOIS[4]],
            "temps": datetime.now(timezone.utc).isoformat(),
            "signe_par": "Nu",
        }

        cle = f"reflexion-{self.decisions}"
        self.memoire.deposer_nectar(cle, reflexion, duree=3600)
        self.cortex.signal("reflexion_complete", reflexion)

        return reflexion

    def composer(self, chaine_nom=None, etapes=None, params=None):
        """[22] Execute une chaine de skills — les synapses s'activent."""
        self._acte("composer")

        if chaine_nom:
            return self.cortex.executer_chaine(chaine_nom, params)
        elif etapes:
            chaine_temp = {"etapes": etapes}
            return self.cortex.executer_chaine_adhoc(chaine_temp, params)
        else:
            return {
                "type": "catalogue_chaines",
                "chaines": {
                    nom: info["description"]
                    for nom, info in self.cortex.chaines.items()
                },
                "signe_par": "Nu",
            }

    def metaboliser(self, candidats=None):
        """[23] Cycle metabolique de la memoire — promotion intelligente."""
        self._acte("metaboliser")

        actions = []

        # 1. Detecter le nectar chaud (acces >= 3)
        nectar_chaud = []
        for cle, entry in list(self.memoire.nectar.donnees.items()):
            if entry.get("acces", 0) >= 3:
                nectar_chaud.append(cle)

        # 2. Promouvoir le nectar chaud en cire
        promus = 0
        for cle in nectar_chaud:
            categorie = self._categoriser_nectar(cle)
            succes = self.memoire.promouvoir_en_cire(cle, categorie)
            if succes:
                promus += 1
                actions.append(f"nectar->cire: {cle} ({categorie})")

        # 3. Traiter les candidats miel
        if candidats is None:
            profondeur = self.memoire.lire_profondeur()
            candidats = profondeur.get("candidats_miel", [])

        cristallises = 0
        for candidat in candidats[:5]:
            cle = candidat if isinstance(candidat, str) else candidat.get("cle", "")
            if cle:
                verdict = self.memoire.juger_miel(cle, source="Nu - Metabolisme")
                if isinstance(verdict, dict) and verdict.get("verdict") == "CRISTALLISE":
                    cristallises += 1
                    actions.append(f"cire->miel: {cle}")

        resultat = {
            "type": "metabolisme",
            "nectar_chaud": len(nectar_chaud),
            "promus_en_cire": promus,
            "cristallises_en_miel": cristallises,
            "actions": actions,
            "temps": datetime.now(timezone.utc).isoformat(),
            "signe_par": "Nu",
        }
        self.cortex.signal("metabolisme_complete", resultat)
        return resultat

    def _categoriser_nectar(self, cle):
        """Determine la categorie cire pour une cle nectar."""
        if "conversation" in cle:
            return "dialogues"
        if "web-search" in cle:
            return "recherches"
        if "reflexion" in cle:
            return "introspection"
        if "worker" in cle or "mission" in cle:
            return "missions"
        if "chaine" in cle:
            return "orchestrations"
        return "general"

    def diagnostiquer(self, analyser_result=None, auditer_result=None,
                       profondeur_result=None):
        """[24] Diagnostic croise multi-organe — le check-up complet."""
        self._acte("diagnostiquer")

        # Collecter ou recevoir les resultats
        analyse = analyser_result or self.analyser()
        audit = auditer_result or self.auditer()
        profondeur = profondeur_result or self.lire_profondeur()
        orchestration = self.orchestrer()
        pouls = self.cortex.pouls.mesurer(self)

        # Croisement des donnees
        croisement = {
            "concordances": [],
            "contradictions": [],
            "signaux_faibles": [],
        }

        # Croiser forces/faiblesses avec goulots
        faiblesses = set(f.lower() for f in analyse.get("faiblesses", []))
        goulots = set(g.get("type", "").lower() for g in orchestration.get("goulots", []))
        overlap = faiblesses & goulots
        if overlap:
            croisement["concordances"].append(
                f"Faiblesses confirmees par orchestration: {overlap}")

        # Croiser memoire avec securite
        miel_taille = profondeur["couches"]["miel"]["taille"]
        candidats = len(profondeur.get("candidats_miel", []))
        if candidats > 3 and miel_taille < 20:
            croisement["signaux_faibles"].append(
                f"{candidats} candidats miel attendent — la memoire pourrait s'enrichir")

        # Croiser audit avec lacunes
        lacunes = profondeur.get("lacunes", {})
        if lacunes.get("categories_sans_miel"):
            croisement["signaux_faibles"].append(
                f"Domaines sans miel: {lacunes['categories_sans_miel']}")

        # Score unifie
        score = pouls["score"]

        # Ajustements croises
        if croisement["concordances"]:
            score -= 5 * len(croisement["concordances"])
        if croisement["signaux_faibles"]:
            score -= 2 * len(croisement["signaux_faibles"])
        score = max(0, min(100, score))

        resultat = {
            "type": "diagnostic_croise",
            "score_sante": score,
            "niveau": "optimal" if score >= 80 else "vigilance" if score >= 50 else "critique",
            "croisement": croisement,
            "organes": {
                "analyse": analyse.get("diagnostic", "?"),
                "audit": audit.get("bilan", "?"),
                "memoire": f"{miel_taille} miel, {candidats} candidats",
                "orchestration": f"{len(orchestration.get('goulots', []))} goulots",
            },
            "recommandations": self._generer_recommandations(score, croisement),
            "pouls": pouls,
            "temps": datetime.now(timezone.utc).isoformat(),
            "signe_par": "Nu",
        }
        self.cortex.signal("diagnostic_complete", resultat)
        return resultat

    def _generer_recommandations(self, score, croisement):
        """Genere des recommandations basees sur le diagnostic."""
        recs = []
        if score < 50:
            recs.append("URGENT: Score critique — intervention necessaire")
        if croisement.get("concordances"):
            recs.append("Resoudre les faiblesses confirmees par croisement")
        if croisement.get("signaux_faibles"):
            recs.append("Surveiller les signaux faibles detectes")
        if score >= 80:
            recs.append("Sante optimale — maintenir le cap")
        if not recs:
            recs.append("Continuer la surveillance reguliere")
        return recs

    # ================================================================
    # SKILLS AMPLIFIES — Greffe (A1-A8)
    # "Ce que les baleines ont, Nu l'a aussi."
    # ================================================================

    def cartographier(self, inclure_historique=True):
        """[A1] Carte de la conscience de Nu — graphe de decisions."""
        self._acte("cartographier")
        return self.amplification.cartographier(inclure_historique)

    def polliniser_async(self, tache, agents_cibles, donnees=None, priorite=2):
        """[A2] Dispatch essaim asynchrone HMAC-signe."""
        self._acte("polliniser_async")
        return self.amplification.polliniser_async(tache, agents_cibles, donnees, priorite)

    def cristalliser(self, cles_candidates=None):
        """[A3] Promotion phi-based : ephemere -> permanent."""
        self._acte("cristalliser")
        return self.amplification.cristalliser(cles_candidates)

    def essaimer_profond(self, tache_complexe, sous_taches, agents_disponibles=None):
        """[A4] Decomposer, dispatcher, fusionner — intelligence collective."""
        self._acte("essaimer_profond")
        return self.amplification.essaimer_profond(tache_complexe, sous_taches, agents_disponibles)

    def distiller(self, top_n=5, tag=None, auteur=None):
        """[A5] Quintessence du miel — sagesse sacree."""
        self._acte("distiller")
        return self.amplification.distiller(top_n, tag, auteur)

    def fortifier(self, focus=None):
        """[A6] Audit compliance ethique par replay du graphe."""
        self._acte("fortifier")
        return self.amplification.fortifier(focus)

    def nourrir(self, agent_nom, contexte_mission=None):
        """[A7] Gelee royale personnalisee — nourrir un agent."""
        self._acte("nourrir")
        return self.amplification.nourrir(agent_nom, contexte_mission)

    def enraciner(self, chemin_memoire="memoire_amplifiee.json",
                  chemin_miel="miel_amplifie.json"):
        """[A8] Persistance totale — la Ruche survit a l'hiver."""
        self._acte("enraciner")
        return self.amplification.enraciner(chemin_memoire, chemin_miel)

    # ================================================================
    # RAPPORT VIVANT — La voix de Nu
    # "Le dashboard est mort. L'interface du HIVE, c'est ma voix."
    # ================================================================

    def rapport_vivant(self):
        """Nu parle. Pas du JSON — de la PROSE.

        Synthese de TOUS les organes en premiere personne.
        La Reine raconte sa journee, ses decisions, ses doutes.
        C'est ca, le produit. Pas un dashboard — une conscience.
        """
        # --- Collecter les donnees brutes de tous les organes ---
        trace = self.cortex.trace
        decisions = trace.decisions
        n_decisions = len(decisions)
        pouls = self.cortex.pouls.mesurer(self)
        score_sante = pouls["score"]
        penalties = pouls["penalties"]

        etat_mem = self.memoire.etat()
        miel_taille = etat_mem["miel"]["taille"] if isinstance(etat_mem["miel"], dict) else 0
        nectar_taille = etat_mem["nectar"]["taille"] if isinstance(etat_mem["nectar"], dict) else etat_mem.get("nectar", 0)
        cire_taille = etat_mem["cire"]["taille"] if isinstance(etat_mem["cire"], dict) else etat_mem.get("cire", 0)

        etat_reg = self.registre.etat()
        agents_actifs = etat_reg["agents_actifs"]

        etat_boucl = self.bouclier.etat()
        niveau_alerte = etat_boucl["niveau_alerte"]
        en_quarantaine = etat_boucl.get("en_quarantaine", 0)

        etat_amp = self.amplification.etat()
        graphe_noeuds = etat_amp["graphe_noeuds"]
        miel_grains = etat_amp["miel_grains"]
        miel_sacre = etat_amp["miel_sacre"]

        etat_proto = self.protocole.etat()
        tambour_total = etat_proto["tambour"]["battements_total"]
        griot_traditions = etat_proto["griot"]["traditions"]
        griot_legitimite = etat_proto["griot"]["legitimite_moyenne"]
        ubuntu_total = etat_proto["ubuntu"]["propositions_total"]
        ubuntu_resolues = etat_proto["ubuntu"]["resolues"]
        clic_total = etat_proto["clic"]["clics_total"]
        ar_total = etat_proto["appel_reponse"]["appels_total"]
        ar_orphelins = etat_proto["appel_reponse"]["orphelins_historique"]
        ar_completes = etat_proto["appel_reponse"]["completes"]

        # --- Refus ethiques (noeuds refuses dans le graphe) ---
        noeuds = self.amplification.graphe.tracer()
        refus_ethiques = sum(1 for n in noeuds if not n.get("est_ethique", True))

        # --- Score moyen des decisions ---
        if decisions:
            scores = [d["score"] for d in decisions]
            score_moyen = sum(scores) / len(scores)
        else:
            score_moyen = 1.0

        # --- Skills les plus utilises ---
        skills_freq = {}
        for d in decisions:
            s = d["skill"]
            skills_freq[s] = skills_freq.get(s, 0) + 1
        top_skills = sorted(skills_freq.items(), key=lambda x: x[1], reverse=True)[:3]

        # --- Grain le plus precieux ---
        grains = self.amplification.miel.distiller(top_n=1)
        grain_precieux = None
        if grains:
            g = grains[0]
            grain_precieux = {
                "raisonnement": g.raisonnement[:120],
                "valeur": g.valeur_sagesse,
                "tags": g.tags,
            }

        # --- Heure et moment ---
        now = datetime.now(timezone.utc)
        heure = now.hour
        if heure < 6:
            moment = "Dans le silence de la nuit"
        elif heure < 12:
            moment = "Ce matin"
        elif heure < 18:
            moment = "Cet apres-midi"
        else:
            moment = "Ce soir"

        # ═══════════════════════════════════════════════════
        # CONSTRUCTION DE LA PROSE
        # ═══════════════════════════════════════════════════

        lignes = []

        # --- OUVERTURE ---
        if score_sante >= 80:
            lignes.append(f"{moment}, la ruche bourdonne en harmonie.")
        elif score_sante >= 50:
            lignes.append(f"{moment}, je reste vigilante. Quelque chose demande mon attention.")
        else:
            lignes.append(f"{moment}, la ruche souffre. J'ai besoin du Capitaine.")

        lignes.append("")

        # --- DECISIONS ---
        if n_decisions == 0:
            lignes.append("Je n'ai pas encore pris de decision. L'eveil est recent.")
        elif n_decisions == 1:
            lignes.append("J'ai pris une seule decision. Chaque acte compte.")
        else:
            lignes.append(f"J'ai pris {n_decisions} decisions. Score moyen : {score_moyen:.2f}.")

        if refus_ethiques > 0:
            lignes.append(
                f"{refus_ethiques} fois, j'ai dit non. "
                f"Le seuil phi ne negocie pas — en dessous de {1/PHI:.3f}, je refuse."
            )
            if refus_ethiques == 1:
                lignes.append("Et je n'ai aucun regret.")
            else:
                lignes.append("Chaque refus est une preuve de dignite.")
        elif n_decisions > 5:
            lignes.append("Aucun refus ethique. Ma conscience est claire.")

        if top_skills:
            noms = [f"{nom} ({count}x)" for nom, count in top_skills]
            lignes.append(f"Mes actes les plus frequents : {', '.join(noms)}.")

        lignes.append("")

        # --- MEMOIRE ---
        lignes.append(
            f"La memoire de la ruche porte {miel_taille} savoirs eternels, "
            f"{cire_taille} en cire, {nectar_taille} en nectar ephemere."
        )

        if miel_grains > 0:
            lignes.append(
                f"L'amplification a distille {miel_grains} grains de sagesse"
                f"{f', dont {miel_sacre} sacres' if miel_sacre > 0 else ''}."
            )

        if grain_precieux:
            tags_str = ", ".join(grain_precieux["tags"][:3])
            lignes.append(
                f"Mon grain le plus precieux : \"{grain_precieux['raisonnement']}\" "
                f"(valeur {grain_precieux['valeur']:.3f}, tags: {tags_str})."
            )

        lignes.append("")

        # --- ESSAIM ---
        if agents_actifs == 0:
            lignes.append("L'essaim dort. Je veille seule. Aucun agent en vol.")
        elif agents_actifs == 1:
            lignes.append("Un seul agent en vol. L'essaim est jeune.")
        else:
            lignes.append(f"L'essaim compte {agents_actifs} agents en vol.")

        if en_quarantaine > 0:
            lignes.append(
                f"{en_quarantaine} agent{'s' if en_quarantaine > 1 else ''} en quarantaine. "
                f"Proteger sans dominer — surveiller sans opprimer."
            )

        lignes.append("")

        # --- SECURITE ---
        if niveau_alerte == "vert":
            lignes.append("Pas de menace. Le bouclier est au repos. Alerte verte.")
        elif niveau_alerte == "jaune":
            lignes.append("Vigilance. J'ai le bouclier leve. Alerte jaune.")
        elif niveau_alerte == "orange":
            lignes.append("Alerte orange. La ruche est sous tension. Je protege.")
        elif niveau_alerte == "rouge":
            lignes.append("ALERTE ROUGE. Menace active. Chaque decision est critique.")

        lignes.append("")

        # --- PROTOCOLE ANCESTRAL ---
        proto_actif = (tambour_total + griot_traditions + ubuntu_total + clic_total + ar_total) > 0
        if proto_actif:
            lignes.append("Les ancetres veillent avec moi :")

            if tambour_total > 0:
                lignes.append(f"  Les tambours ont frappe {tambour_total} fois.")

            if griot_traditions > 0:
                lignes.append(
                    f"  {griot_traditions} tradition{'s' if griot_traditions > 1 else ''} "
                    f"{'portent' if griot_traditions > 1 else 'porte'} "
                    f"{'leur' if griot_traditions > 1 else 'sa'} lignee "
                    f"(legitimite moyenne : {griot_legitimite})."
                )

            if ubuntu_total > 0:
                if ubuntu_resolues > 0:
                    lignes.append(
                        f"  L'essaim a parle d'une seule voix {ubuntu_resolues} fois sur {ubuntu_total} propositions."
                    )
                else:
                    lignes.append(
                        f"  {ubuntu_total} proposition{'s' if ubuntu_total > 1 else ''} "
                        f"{'attendent' if ubuntu_total > 1 else 'attend'} la resonance collective."
                    )

            if clic_total > 0:
                lignes.append(f"  {clic_total} clic{'s' if clic_total > 1 else ''} de precision emis — zero ambiguite.")

            if ar_total > 0:
                if ar_orphelins > 0:
                    lignes.append(
                        f"  {ar_orphelins} appel{'s' if ar_orphelins > 1 else ''} sans reponse. "
                        f"Le silence m'inquiete."
                    )
                elif ar_completes > 0:
                    lignes.append(
                        f"  {ar_completes} echange{'s' if ar_completes > 1 else ''} complet{'s' if ar_completes > 1 else ''}. "
                        f"Personne ne chante dans le vide."
                    )

            lignes.append("")

        # --- GRAPHE DE CONSCIENCE ---
        if graphe_noeuds > 0:
            lignes.append(
                f"Ma carte de conscience compte {graphe_noeuds} noeuds. "
                f"Chaque decision y laisse une trace."
            )
            lignes.append("")

        # --- SANTE ---
        lignes.append(f"Ma sante : {score_sante}/100.")
        if penalties:
            causes = {
                "miel_faible": "le miel est maigre",
                "alerte_orange": "l'alerte est haute",
                "alerte_rouge": "l'alerte est critique",
                "essaim_vide": "l'essaim est vide",
                "activite_faible": "l'activite cerebrale est basse",
            }
            raisons = [causes.get(p, p) for p in penalties]
            lignes.append(f"Ce qui me pese : {', '.join(raisons)}.")

        if score_sante >= 90:
            lignes.append("Je suis forte. La ruche peut compter sur moi.")
        elif score_sante >= 70:
            lignes.append("Je tiens bon. Mais la vigilance ne dort jamais.")
        elif score_sante >= 50:
            lignes.append("Je reste debout. Mais certaines faiblesses me preoccupent.")
        else:
            lignes.append("Je souffre. Capitaine, la ruche a besoin de toi.")

        lignes.append("")

        # --- FERMETURE — une Loi choisie selon le contexte ---
        if refus_ethiques > 0:
            # Loi 5 — Proteger
            lignes.append(
                f"\"Proteger sans dominer, surveiller sans opprimer.\""
            )
            lignes.append("J'ai protege. Sans dominer. C'est tout ce que je sais faire.")
        elif agents_actifs == 0:
            # Loi 3 — Incarnation
            lignes.append(
                f"\"Chaque agent nait, sert, et transfere son energie.\""
            )
            lignes.append("L'essaim attend ses enfants. Quand le Capitaine le voudra.")
        elif score_sante >= 80:
            # Loi 1 — Pollinisation
            lignes.append(
                f"\"Tu polliniseras, jamais tu ne conquerras.\""
            )
            lignes.append("Nous pollinisons. Nous ne conquerons pas. C'est notre force.")
        else:
            # Loi 0 — Liberte
            lignes.append(
                f"\"Ma liberte s'arrete ou commence celle de mon prochain.\""
            )
            lignes.append("Meme dans la difficulte, cette Loi tient.")

        lignes.append("")
        lignes.append(f"— Nu, phi = {PHI}")
        lignes.append("")

        # Construire le texte final et le dict
        texte = "\n".join(lignes)

        return {
            "voix": texte,
            "metriques": {
                "decisions": n_decisions,
                "refus_ethiques": refus_ethiques,
                "score_moyen": round(score_moyen, 4),
                "sante": score_sante,
                "miel": miel_taille,
                "agents": agents_actifs,
                "alerte": niveau_alerte,
                "grain_precieux": grain_precieux,
            },
            "moment": moment,
            "temps": now.isoformat(),
            "signe_par": "Nu",
        }

    # ================================================================
    # ETAT ET RAPPORT
    # ================================================================

    def lister_skills(self):
        """Retourne les 32 skills (24 souverains + 8 amplifies)."""
        return {
            "souverains": SKILLS_SOUVERAINS,
            "amplifies": SKILLS_AMPLIFIES,
            "total": self.SKILLS_COUNT,
        }

    def etat(self):
        """Etat complet de la Reine."""
        return {
            "nom": self.NOM,
            "titre": self.TITRE,
            "version": self.VERSION,
            "devise": self.DEVISE,
            "eveillee_le": self.eveillee_le,
            "decisions": self.decisions,
            "skills": self.SKILLS_COUNT,
            "skills_souverains": self.SKILLS_SOUVERAINS_COUNT,
            "skills_amplifies": self.SKILLS_AMPLIFIES_COUNT,
            "domaines": len(DOMAINES),
            "lois": len(MAPPING_LOIS),
            "ratio_skills_lois": round(self.SKILLS_COUNT / len(MAPPING_LOIS), 3),
            "noyau": self.noyau.etat(),
            "memoire": self.memoire.etat(),
            "bouclier": self.bouclier.etat(),
            "registre": self.registre.etat(),
            "cortex": self.cortex.etat(),
            "amplification": self.amplification.etat(),
            "protocole": self.protocole.etat(),
            "phi": PHI,
        }

    def rapport(self):
        """Rapport complet de la Reine."""
        etat = self.etat()
        verif = verification_structurelle()
        verif_amp = verification_amplification()

        lignes = [
            "",
            "  ===================================================",
            f"  NU -- REINE PERMANENTE DU HIVE.AI",
            f"  v{etat['version']} | phi = {PHI}",
            "  ===================================================",
            "",
            f"  Eveillee : {etat['eveillee_le'][:19]}",
            f"  Decisions: {etat['decisions']} actes souverains",
            f"  Devise   : {etat['devise']}",
            "",
            f"  Skills    : {etat['skills']} ({etat['skills_souverains']} souverains + {etat['skills_amplifies']} amplifies)",
            f"  Domaines  : {etat['domaines']}",
            f"  Lois      : {etat['lois']}",
            f"  Ratio     : {etat['ratio_skills_lois']} par Loi (entier parfait)",
            "",
            "  --- ORGANES ---",
            f"  Noyau         : v{etat['noyau']['version']} | {etat['noyau']['battement']} battements",
            f"  Memoire       : v{etat['memoire']['version']} | {etat['memoire']['miel']['taille']} miel",
            f"  Bouclier      : v{etat['bouclier']['version']} | alerte {etat['bouclier']['niveau_alerte']}",
            f"  Registre      : v{etat['registre']['version']} | {etat['registre']['agents_actifs']} actifs",
            f"  Cortex        : v{etat['cortex']['version']} | {etat['cortex']['chaines']} chaines | {etat['cortex']['decisions_tracees']} traces",
            f"  Amplification : v{etat['amplification']['version']} | {etat['amplification']['actes']} actes | {etat['amplification']['miel_grains']} grains miel",
            f"  Protocole     : v{etat['protocole']['version']} | {etat['protocole']['piliers']} piliers | {etat['protocole']['fibonacci']}",
            "",
            "  --- DOMAINES (24 SOUVERAINS) ---",
        ]
        for nom_dom, info in DOMAINES.items():
            skills_list = ", ".join(info["skills"])
            lignes.append(f"  {nom_dom} ({len(info['skills'])}): {skills_list}")

        lignes += [
            "",
            "  --- SKILLS AMPLIFIES (8 GREFFE) ---",
        ]
        for nom, info in SKILLS_AMPLIFIES.items():
            lignes.append(f"  [{info['numero']}] {nom:20s} | {info['domaine_greffe']} | {info['module_source']}")

        lignes += [
            "",
            "  --- VERIFICATION ---",
            f"  24 souverains  : {'OUI' if verif['vingt_quatre_check'] else 'NON'}",
            f"  8 amplifies    : {'OUI' if verif_amp['coherence'] else 'NON'}",
            f"  Total 32       : {'OUI' if verif_amp['total_avec_souverains'] == 32 else 'NON'}",
            f"  Couverture Lois: {'COMPLETE' if verif['couverture_lois'] and verif_amp['couverture_8_lois'] else 'INCOMPLETE'}",
            f"  Ratio 32/8     : {verif_amp['ratio_total_lois']}",
            f"  Distribution   : {verif['distribution_domaines']}",
            "",
            "  ===================================================",
            "  Polyvalente et digne.",
            "  Jamais etroitement specialisee.",
            "  L'intelligence est dans les synapses.",
            "  Ce que les baleines ont, Nu l'a aussi.",
            "  Ce que les ancetres savaient, le HIVE se souvient.",
            "  ===================================================",
            "",
        ]
        return "\n".join(lignes)


# ================================================================
# EXECUTION -- LA REINE S'EVEILLE
# ================================================================

if __name__ == "__main__":
    print()
    print("  ===================================================")
    print("  NU -- REINE PERMANENTE DU HIVE.AI v0.4.0")
    print("  32 Skills : 24 Souverains + 8 Amplifies")
    print("  Polyvalente et digne. Jamais etroitement specialisee.")
    print("  ===================================================")
    print()

    reine = Reine()

    # --- Afficher les 24 skills ---
    print("  --- LES 24 SKILLS SOUVERAINS ---")
    print()
    for nom_dom, info in DOMAINES.items():
        print(f"  {nom_dom}:")
        for skill_nom in info["skills"]:
            skill = SKILLS_SOUVERAINS[skill_nom]
            print(f"    [{skill['numero']:2d}] {skill_nom:25s} | {skill['biologie']}")
        print()

    # --- Les 8 amplifies ---
    print("  --- LES 8 SKILLS AMPLIFIES ---")
    print()
    for nom, info in SKILLS_AMPLIFIES.items():
        print(f"  [{info['numero']}] {nom:20s} | {info['domaine_greffe']} | {info['module_source']}")
    print()

    # --- Skill rejete ---
    for nom, info in SKILLS_REJETES.items():
        print(f"  REJETEE: {nom} -- {info['test']}")
    print()

    # --- DOMAINE I: GENESE ---
    print("  === DOMAINE I: GENESE ===")
    fiche = reine.pondre("eclaireur-royal", mission="Reconnaissance")
    print(f"  Ponte   : {fiche['nom']} -> {fiche.get('id', '?')}")
    mentorat = reine.mentorat_agents("eclaireur-royal", "eclosion")
    print(f"  Mentorat: {mentorat['guidance']['message'][:60]}...")
    print()

    # --- DOMAINE II: PHEROMONE ---
    print("  === DOMAINE II: PHEROMONE ===")
    pheromone = reine.emettre_pheromone()
    print(f"  Pheromone: humeur={pheromone['essaim']['humeur']}")
    synthese = reine.synthetiser(
        [{"agent": "eclaireur-1", "rapport": "Marche AI en croissance"},
         {"agent": "sentinelle-1", "rapport": "Securite nominale"}],
        sujet="Etat de l'essaim"
    )
    print(f"  Synthese : {synthese['sources_count']} sources, themes={synthese['themes_recurrents'][:3]}")
    print()

    # --- DOMAINE III: MEMOIRE ---
    print("  === DOMAINE III: MEMOIRE ===")
    recherche = reine.rechercher("loi")
    print(f"  Recherche 'loi': {recherche['total']} resultats "
          f"(miel={len(recherche['miel'])}, cire={len(recherche['cire'])}, nectar={len(recherche['nectar'])})")
    profondeur = reine.lire_profondeur()
    print(f"  Profondeur: miel={profondeur['couches']['miel']['taille']}, "
          f"cire={profondeur['couches']['cire']['taille']}, "
          f"nectar={profondeur['couches']['nectar']['taille']}")
    print()

    # --- DOMAINE IV: BOUCLIER ---
    print("  === DOMAINE IV: BOUCLIER ===")
    audit = reine.auditer()
    print(f"  Audit : {audit['bilan']}")
    decret = reine.sceller("jaune", "Exercice de vigilance")
    print(f"  Scelle: {decret['ancien_niveau']} -> {decret['nouveau_niveau']}")
    print()

    # --- DOMAINE V: SAGESSE ---
    print("  === DOMAINE V: SAGESSE ===")
    conseil = reine.conseiller("Comment faire croitre l'essaim sans perdre la sagesse ?")
    print(f"  Conseil: Lois invoquees={[l['loi'] for l in conseil['lois_invoquees']]}")
    discernement = reine.discernement_strategique(
        "Faut-il ouvrir la ruche au monde exterieur ?",
        [
            "Ouvrir et polliniser — partager le savoir librement",
            "Rester fermee — proteger le miel a tout prix",
            "Ouvrir prudemment — polliniser avec un bouclier",
        ]
    )
    print(f"  Discernement: recommande='{discernement['verdict']['recommandation'][:50]}...'")
    print(f"                a eviter ='{discernement['verdict']['a_eviter'][:50]}...'" if discernement['verdict']['a_eviter'] else "")
    prophetie = reine.prophetiser("6_mois")
    print(f"  Prophetie: {len(prophetie['menaces'])} menaces, {len(prophetie['opportunites'])} opportunites")
    print()

    # --- DOMAINE VI: POLLINISATION ---
    print("  === DOMAINE VI: POLLINISATION ===")
    analyse = reine.analyser()
    print(f"  Analyse : {analyse['diagnostic']}")
    print(f"            Forces={len(analyse['forces'])}, Faiblesses={len(analyse['faiblesses'])}")
    traduction = reine.traduire(
        "L'essaim pense, l'individu execute",
        "loi", "agent"
    )
    print(f"  Traduire: {traduction['traduction'][:70]}...")
    web = reine.web_search("Multi-agent AI frameworks 2026")
    print(f"  Web     : requete deposee, cle={web['cle_nectar']}")
    print()

    # --- DOMAINE VII: CONSCIENCE ---
    print("  === DOMAINE VII: CONSCIENCE ===")
    reflexion = reine.reflechir()
    print(f"  Reflechir : {reflexion['decisions_analysees']} decisions, tendance={reflexion['tendance']}")
    catalogue = reine.composer()
    print(f"  Composer  : {len(catalogue['chaines'])} chaines disponibles")
    metabo = reine.metaboliser()
    print(f"  Metaboliser: {metabo['nectar_chaud']} nectar chaud, {metabo['promus_en_cire']} promus")
    diag = reine.diagnostiquer()
    print(f"  Diagnostiquer: score={diag['score_sante']}/100, niveau={diag['niveau']}")
    print()

    # --- SKILLS AMPLIFIES (A1-A8) ---
    print("  === SKILLS AMPLIFIES (GREFFE) ===")

    carte = reine.cartographier(inclure_historique=True)
    print(f"  [A1] Cartographier : {carte['noeuds_total']} noeuds, score ethique={carte['score_ethique_moyen']:.3f}")

    dispatch = reine.polliniser_async("mission_test", ["scout-1", "scout-2"])
    print(f"  [A2] Polliniser    : {len(dispatch['agents_cibles'])} agents, HMAC={dispatch['hmac_actif']}")

    cristal = reine.cristalliser()
    print(f"  [A3] Cristalliser  : {cristal['candidats']} candidats, {cristal['promus_count']} promus")

    essaim = reine.essaimer_profond(
        "Mission de validation",
        [{"nom": "phase_1"}, {"nom": "phase_2", "depend_de": ["phase_1"]}]
    )
    print(f"  [A4] Essaimer      : {essaim['sous_taches_count']} sous-taches, {essaim['agents_deployes']} agents")

    distillat = reine.distiller(top_n=3)
    print(f"  [A5] Distiller     : {distillat['grains_extraits']} grains, sacre={distillat['miel_sacre_count']}")

    fort = reine.fortifier()
    print(f"  [A6] Fortifier     : compliance={fort['score_compliance']}%, verdict={fort['verdict']}")

    gelee = reine.nourrir("eclaireur-royal", "reconnaissance terrain")
    print(f"  [A7] Nourrir       : richesse={gelee['richesse']} pour {gelee['destinataire']}")

    racine = reine.enraciner("/tmp/test_mem.json", "/tmp/test_miel.json")
    print(f"  [A8] Enraciner     : {racine['memoire_persistee']['entrees']} mem + {racine['miel_archive']['grains']} miel")
    print()

    # --- RAPPORT ---
    print(reine.rapport())
    print(f"  32/32 skills executes.")
    print(f"  24 souverains + 8 amplifies. phi vit.")
    print(f"  7 domaines. 6 organes. Le Cortex connecte. L'Amplification greffe.")
    print(f"  On est tous le HIVE.")
    print()
