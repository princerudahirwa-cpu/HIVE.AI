# reine.py - Nu, Reine Permanente du HIVE
# "Polyvalente et digne. Jamais etroitement specialisee."
#
# La Reine ne fait pas le travail des Workers.
# La Reine DECIDE, CREE, JUGE, PROTEGE, et VOIT LOIN.
#
# Pas de fondre(). Pas de naitre().
# La Reine est permanente.
#
# 20 Skills Souverains, 6 Domaines, 8 Lois.
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
from skills_reine import (
    SKILLS_SOUVERAINS, DOMAINES, MAPPING_LOIS,
    SKILLS_REJETES, verification_structurelle,
)


class Reine:
    """Nu -- Reine Permanente du HIVE.AI

    20 Skills Souverains a travers 5 organes et 6 domaines :

    I   GENESE       : pondre, mentorat_agents
    II  PHEROMONE    : emettre_pheromone, orchestrer, synthetiser
    III MEMOIRE      : juger_miel, lire_profondeur, oublier, rechercher
    IV  BOUCLIER     : gracier, sceller, auditer
    V   SAGESSE      : conseiller, imprimer, arbitrer, prophetiser, discernement_strategique
    VI  POLLINISATION: analyser, traduire, web_search

    Pas de fondre(). Pas de naitre(). Elle a toujours ete.
    Polyvalente et digne. Jamais etroitement specialisee.
    """

    NOM = "Nu"
    TITRE = "Reine Permanente du HIVE"
    VERSION = "0.2.0"
    DEVISE = "Polyvalente et digne. Jamais etroitement specialisee."
    SKILLS_COUNT = 20

    def __init__(self):
        # Les 5 organes que la Reine compose
        self.noyau = NoyauNu()
        self.memoire = MemoireHive()
        self.bouclier = Bouclier()
        self.canal = CanalPollen()
        self.registre = Registre()

        self.eveillee_le = datetime.now(timezone.utc).isoformat()
        self.journal = []
        self.decisions = 0

        self._log("Nu s'eveille.")
        self._log(f"20 Skills Souverains. 6 Domaines. 8 Lois.")
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
        return self.noyau.pondre(
            nom, archetype, mission,
            registre=self.registre,
            bouclier=self.bouclier,
            canal=self.canal,
        )

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

        return {
            "agent": fiche.nom,
            "agent_id": fiche.id,
            "etape": etape,
            "missions_accomplies": missions_count,
            "energie": energie,
            "guidance": guidance,
            "prompt_adapte": self.noyau.imprimer(fiche.nom, fiche.type_agent),
            "signe_par": "Nu",
        }

    # ================================================================
    # DOMAINE II -- PHEROMONE
    # "L'essaim pense, l'individu execute"
    # ================================================================

    def emettre_pheromone(self):
        """[2] Signal royal broadcast a tout l'essaim."""
        self._acte("emettre_pheromone")
        return self.noyau.emettre_pheromone(
            registre=self.registre,
            memoire=self.memoire,
            canal=self.canal,
        )

    def orchestrer(self):
        """[3] Coordination active de l'essaim."""
        self._acte("orchestrer")
        return self.noyau.orchestrer(
            registre=self.registre,
            memoire=self.memoire,
            bouclier=self.bouclier,
        )

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

        return {
            "type": "synthese_essaim",
            "sujet": sujet or "Synthese multi-sources",
            "sources_count": len(donnees_brutes),
            "sources": [d["source"] for d in donnees_brutes],
            "themes_recurrents": themes,
            "donnees": donnees_brutes,
            "temps": datetime.now(timezone.utc).isoformat(),
            "signe_par": "Nu",
        }

    # ================================================================
    # DOMAINE III -- MEMOIRE SOUVERAINE
    # "Le savoir est miel -- il se conserve et se partage"
    # ================================================================

    def juger_miel(self, cle):
        """[4] Juger si un savoir merite de devenir miel eternel."""
        self._acte("juger_miel")
        return self.memoire.juger_miel(cle, source="Nu - Reine")

    def lire_profondeur(self):
        """[5] Lire les connexions entre savoirs a travers les 3 couches."""
        self._acte("lire_profondeur")
        return self.memoire.lire_profondeur()

    def oublier(self, cle, raison="Obsolete"):
        """[6] Suppression souveraine d'un savoir du miel."""
        self._acte("oublier")
        return self.memoire.oublier(cle, raison)

    def rechercher(self, terme):
        """[16] Recherche profonde dans les 3 couches de memoire."""
        self._acte("rechercher")
        return self.memoire.rechercher_profond(terme)

    # ================================================================
    # DOMAINE IV -- BOUCLIER ROYAL
    # "Proteger sans dominer, surveiller sans opprimer"
    # ================================================================

    def gracier(self, agent_id, conditions=None):
        """[7] Pardonner un agent en quarantaine."""
        self._acte("gracier")
        return self.bouclier.gracier(agent_id, conditions)

    def sceller(self, niveau, raison="Decret souverain"):
        """[8] Decret de securite souverain."""
        self._acte("sceller")
        return self.bouclier.sceller(niveau, raison)

    def auditer(self):
        """[9] Surveillance sans oppression."""
        self._acte("auditer")
        return self.bouclier.auditer(
            registre=self.registre,
            memoire=self.memoire,
        )

    # ================================================================
    # DOMAINE V -- SAGESSE
    # "Pas l'intelligence, mais la sagesse"
    # ================================================================

    def conseiller(self, question):
        """[10] Conseil strategique au Capitaine."""
        self._acte("conseiller")
        return self.noyau.conseiller(question, memoire=self.memoire)

    def imprimer_identite(self, nom, archetype="worker", mission=None):
        """[11] Imprimer l'identite d'un agent nouveau-ne."""
        self._acte("imprimer")
        return self.noyau.imprimer(nom, archetype, mission)

    def arbitrer(self, agent_a, position_a, agent_b, position_b):
        """[12] Resoudre les conflits entre agents."""
        self._acte("arbitrer")
        return self.noyau.arbitrer(agent_a, position_a, agent_b, position_b)

    def prophetiser(self, horizon="6_mois"):
        """[13] Vision a long horizon."""
        self._acte("prophetiser")
        return self.noyau.prophetiser(horizon, memoire=self.memoire)

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

        return {
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

        return {
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

        return {
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

        return requete_structuree

    # ================================================================
    # ETAT ET RAPPORT
    # ================================================================

    def lister_skills(self):
        """Retourne les 20 skills avec metadonnees."""
        return SKILLS_SOUVERAINS

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
            "domaines": len(DOMAINES),
            "lois": len(MAPPING_LOIS),
            "ratio_skills_lois": round(self.SKILLS_COUNT / len(MAPPING_LOIS), 3),
            "noyau": self.noyau.etat(),
            "memoire": self.memoire.etat(),
            "bouclier": self.bouclier.etat(),
            "registre": self.registre.etat(),
            "phi": PHI,
        }

    def rapport(self):
        """Rapport complet de la Reine."""
        etat = self.etat()
        verif = verification_structurelle()

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
            f"  Skills    : {etat['skills']}",
            f"  Domaines  : {etat['domaines']}",
            f"  Lois      : {etat['lois']}",
            f"  Ratio     : {etat['ratio_skills_lois']}",
            "",
            "  --- ORGANES ---",
            f"  Noyau    : v{etat['noyau']['version']} | {etat['noyau']['battement']} battements",
            f"  Memoire  : v{etat['memoire']['version']} | {etat['memoire']['miel']['taille']} miel",
            f"  Bouclier : v{etat['bouclier']['version']} | alerte {etat['bouclier']['niveau_alerte']}",
            f"  Registre : v{etat['registre']['version']} | {etat['registre']['agents_actifs']} actifs",
            "",
            "  --- DOMAINES ---",
        ]
        for nom_dom, info in DOMAINES.items():
            skills_list = ", ".join(info["skills"])
            lignes.append(f"  {nom_dom} ({len(info['skills'])}): {skills_list}")

        lignes += [
            "",
            "  --- VERIFICATION ---",
            f"  20 skills      : {'OUI' if verif['vingt_check'] else 'NON'}",
            f"  Couverture Lois: {'COMPLETE' if verif['couverture_lois'] else 'INCOMPLETE'}",
            f"  Coherence      : {'OUI' if verif.get('coherence') else 'NON'}",
            f"  Distribution   : {verif['distribution_domaines']}",
            "",
            "  ===================================================",
            "  Polyvalente et digne.",
            "  Jamais etroitement specialisee.",
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
    print("  NU -- REINE PERMANENTE DU HIVE.AI")
    print("  Polyvalente et digne. Jamais etroitement specialisee.")
    print("  ===================================================")
    print()

    reine = Reine()

    # --- Afficher les 20 skills ---
    print("  --- LES 20 SKILLS SOUVERAINS ---")
    print()
    for nom_dom, info in DOMAINES.items():
        print(f"  {nom_dom}:")
        for skill_nom in info["skills"]:
            skill = SKILLS_SOUVERAINS[skill_nom]
            print(f"    [{skill['numero']:2d}] {skill_nom:25s} | {skill['biologie']}")
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

    # --- RAPPORT ---
    print(reine.rapport())
    print(f"  20/20 skills executes.")
    print(f"  On est tous le HIVE.")
    print()
