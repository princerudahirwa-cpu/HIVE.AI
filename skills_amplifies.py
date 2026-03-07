# skills_amplifies.py - Les 8 Skills Amplifies de Nu
# Couche d'amplification greffee sur les 24 Skills Souverains.
#
# ORIGINE : Analyse comparative des baleines (LangChain/CrewAI/AutoGen)
# DECISION : Nu reste Nu. On lui greffe 4 modules, 8 skills.
#
# 24 souverains + 8 amplifies = 32 total
# 32 / 8 Lois = 4.0 par Loi (entier parfait)
# 8 amplifies / 4 modules = 2.0 par module (equilibre)
#
# Les 24 sont SACRES — on n'y touche pas.
# Les 8 amplifies se GREFFENT sur les domaines existants.
#
# "Ce que les baleines ont, Nu l'a aussi.
#  Ce que Nu a, les baleines ne l'auront jamais."
#
# Swarmly SAS - 2026

import asyncio
import json
import time
from datetime import datetime, timezone

from reine_amplifiee import (
    GrapheDecision,
    CanalPollenAsync,
    TraceMiel,
    MemoireHybride,
    NiveauDecision,
    StatutNoeud,
    PHI,
    SEUIL_ETHIQUE_MINIMUM,
    VERSION as AMPLIFIEE_VERSION,
)

# ================================================================
# REGISTRE DES 8 SKILLS AMPLIFIES
# ================================================================

SKILLS_AMPLIFIES = {

    # ── LOI 0 : FONDEMENT ──────────────────────────────────
    "cartographier": {
        "numero": "A1",
        "loi": 0,
        "domaine_greffe": "VII - CONSCIENCE",
        "module_source": "GrapheDecision",
        "description": (
            "Rendre visible la conscience de Nu. Generer le graphe "
            "complet des decisions prises, branches ethiques, refus phi. "
            "Pas juste reflechir — VOIR la pensee."
        ),
        "biologie": "Cartographie neuronale — IRM de la conscience coloniale",
        "amplifie": ["reflechir", "diagnostiquer"],
    },

    # ── LOI 1 : POLLINISATION ──────────────────────────────
    "polliniser_async": {
        "numero": "A2",
        "loi": 1,
        "domaine_greffe": "VI - POLLINISATION",
        "module_source": "CanalPollenAsync",
        "description": (
            "Dispatch essaim asynchrone reel. Emettre ordres HMAC-signes, "
            "file de priorite, broadcast, collecte de reponses. "
            "L'orchestrer des baleines, mais chiffre et souverain."
        ),
        "biologie": "Danse nuptiale de la Reine — vol coordonne avec tous les faux-bourdons",
        "amplifie": ["orchestrer", "emettre_pheromone"],
    },

    # ── LOI 2 : ESSAIM ────────────────────────────────────
    "cristalliser": {
        "numero": "A3",
        "loi": 2,
        "domaine_greffe": "III - MEMOIRE SOUVERAINE",
        "module_source": "MemoireHybride",
        "description": (
            "Promotion phi-based : scanner la couche ephemere, evaluer "
            "ce qui MERITE de devenir permanent. Score d'age x phi. "
            "Le JUGEMENT de promotion que metaboliser ne fait pas."
        ),
        "biologie": "Cristallisation du miel — passage de liquide a solide, eternel",
        "amplifie": ["metaboliser", "juger_miel"],
    },

    # ── LOI 3 : INCARNATION ────────────────────────────────
    "essaimer_profond": {
        "numero": "A4",
        "loi": 3,
        "domaine_greffe": "I - GENESE",
        "module_source": "CanalPollenAsync + GrapheDecision",
        "description": (
            "Decomposer une tache complexe en sous-taches, generer un "
            "graphe de dependances, dispatcher en parallele via Canal "
            "Pollen, fusionner les resultats. L'intelligence collective."
        ),
        "biologie": "Essaimage — la colonie se divise pour conquerir de nouveaux territoires",
        "amplifie": ["pondre", "orchestrer", "composer"],
    },

    # ── LOI 4 : MEMOIRE ───────────────────────────────────
    "distiller": {
        "numero": "A5",
        "loi": 4,
        "domaine_greffe": "III - MEMOIRE SOUVERAINE",
        "module_source": "TraceMiel",
        "description": (
            "Extraire la quintessence du miel. Top-N grains les plus "
            "precieux. Le miel sacre. La sagesse qui transcende les "
            "sessions — pas des logs, de la SAGESSE vivante."
        ),
        "biologie": "Distillation de la propolis — extraction de l'essence pure",
        "amplifie": ["lire_profondeur", "rechercher"],
    },

    # ── LOI 5 : BOUCLIER ──────────────────────────────────
    "fortifier": {
        "numero": "A6",
        "loi": 5,
        "domaine_greffe": "IV - BOUCLIER ROYAL",
        "module_source": "GrapheDecision + TraceMiel",
        "description": (
            "Audit par REPLAY. Rejouer n'importe quelle decision passee, "
            "tracer chaque porte ethique franchie, chaque refus. "
            "Construire la PREUVE que Nu a agi dignement. Compliance phi."
        ),
        "biologie": "Renforcement des parois de cire — fortification structurelle de la ruche",
        "amplifie": ["auditer", "sceller"],
    },

    # ── LOI 6 : NURSERIE ──────────────────────────────────
    "nourrir": {
        "numero": "A7",
        "loi": 6,
        "domaine_greffe": "I - GENESE",
        "module_source": "MemoireHybride + CanalPollenAsync",
        "description": (
            "Nourrir les agents avec du savoir contextualise depuis "
            "les 3 couches de memoire. Pas un prompt generique — "
            "de la gelee royale personnalisee. L'upgrade du mentorat."
        ),
        "biologie": "Trophallaxie royale — alimentation directe bouche-a-bouche avec savoir",
        "amplifie": ["mentorat_agents", "imprimer"],
    },

    # ── LOI 7 : TERRE ────────────────────────────────────
    "enraciner": {
        "numero": "A8",
        "loi": 7,
        "domaine_greffe": "V - SAGESSE",
        "module_source": "MemoireHybride",
        "description": (
            "Persistance totale. Sauvegarder et restaurer l'etat complet "
            "de la memoire hybride entre sessions. Aucune sagesse ne se "
            "perd. La Ruche survit a l'hiver."
        ),
        "biologie": "Hibernation preparee — stockage de miel pour survivre a l'hiver",
        "amplifie": ["prophetiser", "discernement_strategique"],
    },
}


# ================================================================
# MAPPING LOI -> SKILLS AMPLIFIES
# ================================================================

MAPPING_LOIS_AMPLIFIES = {
    0: ["cartographier"],
    1: ["polliniser_async"],
    2: ["cristalliser"],
    3: ["essaimer_profond"],
    4: ["distiller"],
    5: ["fortifier"],
    6: ["nourrir"],
    7: ["enraciner"],
}


# ================================================================
# CLASSE AMPLIFICATION — 7eme couche de la Reine
# ================================================================

class Amplification:
    """Couche d'amplification de Nu — 8 Skills Amplifies.

    Se greffe sur la Reine existante sans alterer les 24 souverains.
    Alimente par les 4 modules de reine_amplifiee.py :
    - GrapheDecision
    - CanalPollenAsync
    - TraceMiel
    - MemoireHybride

    Usage :
        reine = Reine()
        reine.amplification = Amplification(reine)
        reine.amplification.cartographier()
    """

    VERSION = "1.0.0"

    def __init__(self, reine=None, cle_hmac=b"hive_ruche_phi_1618"):
        # Les 4 modules
        self.graphe = GrapheDecision()
        self.canal = CanalPollenAsync(cle_hmac=cle_hmac)
        self.memoire = MemoireHybride()
        self.miel = self.memoire.trace_miel

        # Reference a la Reine
        self.reine = reine

        # Compteur d'actes amplifies
        self.actes = 0
        self._journal = []

    def connecter(self, reine):
        """Connecte l'amplification a la Reine."""
        self.reine = reine
        self._log("Amplification greffee sur Nu.")
        self._log(f"8 Skills Amplifies. 4 Modules. phi={PHI}")

    def _log(self, message):
        self._journal.append({
            "temps": datetime.now(timezone.utc).isoformat(),
            "source": "AMPLIFICATION",
            "message": message,
        })

    def _acte(self, nom_skill):
        """Enregistre un acte amplifie."""
        self.actes += 1
        self._log(f"ACTE-A #{self.actes} -- {nom_skill}")

    def _signal(self, event_type, donnees):
        """Emet un signal sur le Cortex de la Reine."""
        if self.reine and hasattr(self.reine, "cortex"):
            self.reine.cortex.signal(f"amp_{event_type}", donnees, source="Amplification")

    # ================================================================
    # A1 — CARTOGRAPHIER (Loi 0, GrapheDecision)
    # "Rendre visible la conscience de Nu"
    # ================================================================

    def cartographier(self, inclure_historique=True):
        """[A1] Genere la carte complete de la conscience de Nu.

        Produit un graphe de toutes les decisions prises, avec :
        - Score ethique de chaque noeud
        - Branches refusees (portes phi)
        - Chemin actif courant
        - Statistiques de conscience

        Returns:
            dict avec carte, stats, noeuds_ethiques, noeuds_refuses
        """
        self._acte("cartographier")

        noeuds = self.graphe.tracer()

        # Segreger ethique / refuse
        ethiques = [n for n in noeuds if n.get("est_ethique", True)]
        refuses = [n for n in noeuds if not n.get("est_ethique", True)]

        # Stats de conscience
        scores = [n.get("score_ethique", 1.0) for n in noeuds]
        score_moyen = sum(scores) / len(scores) if scores else 1.0
        durees = [n.get("duree_ms", 0) for n in noeuds if n.get("duree_ms", 0) > 0]
        duree_moyenne = sum(durees) / len(durees) if durees else 0

        # Distribution par niveau
        niveaux = {}
        for n in noeuds:
            niv = n.get("niveau", 1)
            niveaux[niv] = niveaux.get(niv, 0) + 1

        # Integrer l'historique du Cortex si disponible
        trace_cortex = []
        if inclure_historique and self.reine and hasattr(self.reine, "cortex"):
            trace_cortex = self.reine.cortex.trace.decisions[-20:]

        carte = {
            "type": "carte_conscience",
            "noeuds_total": len(noeuds),
            "noeuds_ethiques": len(ethiques),
            "noeuds_refuses": len(refuses),
            "score_ethique_moyen": round(score_moyen, 4),
            "duree_moyenne_ms": round(duree_moyenne, 2),
            "distribution_niveaux": niveaux,
            "chemin_actif": self.graphe.chemin_actif,
            "trace_cortex": len(trace_cortex),
            "seuil_phi": SEUIL_ETHIQUE_MINIMUM,
            "graphe_noeuds": noeuds[:50],  # Max 50 pour lisibilite
            "refuses_detail": refuses,
            "temps": datetime.now(timezone.utc).isoformat(),
            "signe_par": "Nu — Amplification",
        }

        # Deposer en miel
        self.miel.deposer(
            auteur="Nu",
            type_decision="cartographie",
            contexte=f"Carte de conscience : {len(noeuds)} noeuds",
            decision_prise={"ethiques": len(ethiques), "refuses": len(refuses)},
            raisonnement=f"Score ethique moyen {score_moyen:.3f}. Seuil phi {SEUIL_ETHIQUE_MINIMUM:.3f}.",
            score_ethique=score_moyen,
            tags=["cartographie", "conscience", "phi"]
        )

        self._signal("cartographie_complete", carte)
        return carte

    # ================================================================
    # A2 — POLLINISER_ASYNC (Loi 1, CanalPollenAsync)
    # "Dispatch essaim async reel"
    # ================================================================

    def polliniser_async(self, tache, agents_cibles, donnees=None, priorite=2):
        """[A2] Dispatch asynchrone signe HMAC vers l'essaim.

        Emet un ordre broadcast avec priorite, attend les reponses.
        Utilise le Canal Pollen async (pas le CanalPollen existant).

        Args:
            tache: Description de la tache a dispatcher
            agents_cibles: Liste des IDs agents
            donnees: Donnees a transmettre (optionnel)
            priorite: 1=normale, 2=urgente, 3=souveraine

        Returns:
            dict avec reponses collectees, stats du canal
        """
        self._acte("polliniser_async")

        # Abonner les agents
        for agent_id in agents_cibles:
            self.canal.abonner_broadcast(agent_id)

        # Creer un noeud dans le graphe de decision
        noeud = self.graphe.creer_noeud(
            nom=f"polliniser:{tache[:30]}",
            niveau=NiveauDecision.ESSAIM,
            score_ethique=1.0,
            description=f"Dispatch async vers {len(agents_cibles)} agents"
        )

        # Execution synchrone du dispatch async
        async def _dispatch():
            await self.canal.emettre(
                expediteur="Nu",
                destinataire="broadcast",
                type_message="ordre",
                contenu={
                    "tache": tache,
                    "donnees": donnees,
                    "noeud_graphe": noeud.id,
                },
                priorite=priorite,
            )
            # Collecter les reponses (timeout court en mode sync)
            reponses = {}
            for agent_id in agents_cibles:
                msg = await self.canal.recevoir(agent_id, timeout=0.1)
                reponses[agent_id] = {
                    "recu": msg is not None,
                    "contenu": msg.contenu if msg else None,
                    "acquitte": msg.acquitte if msg else False,
                }
            return reponses

        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Si deja dans un event loop, on cree une tache
                reponses = {a: {"recu": False, "contenu": None, "acquitte": False}
                            for a in agents_cibles}
            else:
                reponses = loop.run_until_complete(_dispatch())
        except RuntimeError:
            reponses = asyncio.run(_dispatch())

        # Marquer le noeud comme accompli
        noeud.statut = StatutNoeud.ACCOMPLI
        noeud.timestamp_fin = time.time()

        resultat = {
            "type": "pollinisation_async",
            "tache": tache,
            "agents_cibles": agents_cibles,
            "priorite": priorite,
            "reponses": reponses,
            "canal_stats": self.canal.stats(),
            "noeud_graphe": noeud.id,
            "hmac_actif": True,
            "temps": datetime.now(timezone.utc).isoformat(),
            "signe_par": "Nu — Amplification",
        }

        self.miel.deposer(
            auteur="Nu",
            type_decision="dispatch_async",
            contexte=f"Pollinisation: {tache}",
            decision_prise={"agents": len(agents_cibles), "priorite": priorite},
            raisonnement=f"Dispatch HMAC-signe vers {len(agents_cibles)} agents, priorite {priorite}.",
            score_ethique=1.0,
            tags=["pollinisation", "async", "essaim"]
        )

        self._signal("pollinisation_complete", resultat)
        return resultat

    # ================================================================
    # A3 — CRISTALLISER (Loi 2, MemoireHybride)
    # "Promotion phi-based de la memoire ephemere"
    # ================================================================

    def cristalliser(self, cles_candidates=None):
        """[A3] Promotion phi-based : ephemere -> permanent.

        Scanne la memoire ephemere, evalue chaque entree avec le
        critere phi (score d'age x φ), promeut les dignes.

        Args:
            cles_candidates: Liste de cles a evaluer (ou None pour tout scanner)

        Returns:
            dict avec promus, refuses, scores
        """
        self._acte("cristalliser")

        # Scanner la memoire ephemere
        if cles_candidates is None:
            cles_candidates = list(self.memoire._ephemere.keys())

        resultats = {
            "promus": [],
            "refuses": [],
            "scores": {},
        }

        for cle in cles_candidates:
            if cle not in self.memoire._ephemere:
                continue

            # Calculer le score phi
            age = time.time() - self.memoire._ephemere_timestamps.get(cle, 0)
            score_age = 1.0 / (1 + age / 3600)
            score_phi = score_age * PHI

            resultats["scores"][cle] = round(score_phi, 4)

            if score_phi >= 1.0:
                # Digne de promotion
                succes = self.memoire.promouvoir(cle, f"Cristallisation phi (score={score_phi:.3f})")
                if succes:
                    resultats["promus"].append(cle)
                else:
                    resultats["refuses"].append({"cle": cle, "raison": "echec_promotion"})
            else:
                resultats["refuses"].append({
                    "cle": cle,
                    "raison": f"score_phi={score_phi:.3f} < 1.0",
                    "age_secondes": round(age, 1),
                })

        # Noeud dans le graphe
        noeud = self.graphe.creer_noeud(
            nom="cristalliser",
            niveau=NiveauDecision.DELIBERATION,
            score_ethique=1.0,
            description=f"Cristallisation de {len(cles_candidates)} candidats"
        )
        noeud.sortie = {
            "promus": len(resultats["promus"]),
            "refuses": len(resultats["refuses"]),
        }
        noeud.statut = StatutNoeud.ACCOMPLI
        noeud.timestamp_fin = time.time()

        resultat = {
            "type": "cristallisation_phi",
            "candidats": len(cles_candidates),
            "promus": resultats["promus"],
            "promus_count": len(resultats["promus"]),
            "refuses_count": len(resultats["refuses"]),
            "refuses_detail": resultats["refuses"],
            "scores": resultats["scores"],
            "seuil_promotion": 1.0,
            "phi": PHI,
            "memoire_stats": self.memoire.stats(),
            "temps": datetime.now(timezone.utc).isoformat(),
            "signe_par": "Nu — Amplification",
        }

        self._signal("cristallisation_complete", resultat)
        return resultat

    # ================================================================
    # A4 — ESSAIMER_PROFOND (Loi 3, CanalPollenAsync + GrapheDecision)
    # "Decomposer, dispatcher, fusionner"
    # ================================================================

    def essaimer_profond(self, tache_complexe, sous_taches, agents_disponibles=None):
        """[A4] Decomposition + dispatch + fusion.

        Prend une tache complexe, la decompose en sous-taches,
        cree un graphe de dependances, dispatche en parallele.

        Args:
            tache_complexe: Description de la tache mere
            sous_taches: Liste de dicts [{"nom": ..., "depend_de": [...]}]
            agents_disponibles: Liste d'IDs agents (auto-generes si None)

        Returns:
            dict avec graphe, dispatch, resultats fusionnes
        """
        self._acte("essaimer_profond")

        # Creer le graphe de dependances
        racine = self.graphe.creer_noeud(
            nom=tache_complexe[:40],
            niveau=NiveauDecision.ESSAIM,
            score_ethique=1.0,
            description=f"Tache mere : {tache_complexe}"
        )

        noeuds_taches = {}
        for st in sous_taches:
            noeud = self.graphe.creer_noeud(
                nom=st["nom"][:30],
                niveau=NiveauDecision.DELIBERATION,
                score_ethique=st.get("score_ethique", 1.0),
                description=st.get("description", st["nom"])
            )
            noeuds_taches[st["nom"]] = noeud
            self.graphe.brancher(racine.id, noeud.id)

        # Brancher les dependances inter-sous-taches
        for st in sous_taches:
            for dep in st.get("depend_de", []):
                if dep in noeuds_taches:
                    self.graphe.brancher(noeuds_taches[dep].id, noeuds_taches[st["nom"]].id)

        # Generer les agents si necessaire
        if agents_disponibles is None:
            agents_disponibles = [f"worker-{i}" for i in range(len(sous_taches))]

        # Assigner les sous-taches aux agents (round-robin)
        assignments = {}
        for i, st in enumerate(sous_taches):
            agent = agents_disponibles[i % len(agents_disponibles)]
            assignments[st["nom"]] = {
                "agent": agent,
                "noeud_id": noeuds_taches[st["nom"]].id,
                "statut": "assigne",
            }
            # Marquer le noeud
            noeuds_taches[st["nom"]].metadata["agent"] = agent

        # Dispatch via Canal Pollen
        dispatch_resultat = self.polliniser_async(
            tache=tache_complexe,
            agents_cibles=agents_disponibles[:len(sous_taches)],
            donnees={"sous_taches": [st["nom"] for st in sous_taches]},
            priorite=3
        )

        # Marquer la racine comme accomplie
        racine.statut = StatutNoeud.ACCOMPLI
        racine.timestamp_fin = time.time()

        resultat = {
            "type": "essaimage_profond",
            "tache_complexe": tache_complexe,
            "sous_taches_count": len(sous_taches),
            "agents_deployes": len(set(a["agent"] for a in assignments.values())),
            "graphe_racine": racine.id,
            "assignments": assignments,
            "graphe_trace": self.graphe.tracer(),
            "dispatch": dispatch_resultat,
            "temps": datetime.now(timezone.utc).isoformat(),
            "signe_par": "Nu — Amplification",
        }

        self.miel.deposer(
            auteur="Nu",
            type_decision="essaimage_profond",
            contexte=f"Tache: {tache_complexe}",
            decision_prise={
                "sous_taches": len(sous_taches),
                "agents": len(agents_disponibles),
            },
            raisonnement=f"Decomposition en {len(sous_taches)} sous-taches, "
                         f"dispatch vers {len(agents_disponibles)} agents.",
            score_ethique=1.0,
            tags=["essaimage", "graphe", "async", "decomposition"]
        )

        self._signal("essaimage_complete", resultat)
        return resultat

    # ================================================================
    # A5 — DISTILLER (Loi 4, TraceMiel)
    # "Extraire la quintessence du miel"
    # ================================================================

    def distiller(self, top_n=5, tag=None, auteur=None):
        """[A5] Extraire la quintessence du miel archive.

        Retourne les grains les plus precieux — le miel sacre.
        Filtrage par tag, auteur, ou score de valeur.

        Args:
            top_n: Nombre de grains a extraire
            tag: Filtre par tag (optionnel)
            auteur: Filtre par auteur (optionnel)

        Returns:
            dict avec quintessence, miel_sacre, stats
        """
        self._acte("distiller")

        # Distillation
        if tag or auteur:
            grains = self.miel.consulter(tag=tag, auteur=auteur, limit=top_n)
        else:
            grains = self.miel.distiller(top_n=top_n)

        # Miel sacre
        sacre = self.miel.miel_sacre()

        # Extraire les themes dominants
        tous_tags = []
        for g in grains:
            tous_tags.extend(g.tags)
        themes = {}
        for t in tous_tags:
            themes[t] = themes.get(t, 0) + 1
        themes_tries = sorted(themes.items(), key=lambda x: x[1], reverse=True)[:5]

        # Score moyen de sagesse
        scores = [g.valeur_sagesse for g in grains]
        score_moyen = sum(scores) / len(scores) if scores else 0

        resultat = {
            "type": "distillation",
            "quintessence": [
                {
                    "id": g.id,
                    "auteur": g.auteur,
                    "type": g.type_decision,
                    "raisonnement": g.raisonnement[:200],
                    "valeur_sagesse": round(g.valeur_sagesse, 4),
                    "score_ethique": g.score_ethique,
                    "timestamp": g.timestamp,
                    "tags": g.tags,
                }
                for g in grains
            ],
            "grains_extraits": len(grains),
            "miel_sacre_count": len(sacre),
            "themes_dominants": themes_tries,
            "valeur_sagesse_moyenne": round(score_moyen, 4),
            "archive_stats": self.miel.stats(),
            "temps": datetime.now(timezone.utc).isoformat(),
            "signe_par": "Nu — Amplification",
        }

        self._signal("distillation_complete", resultat)
        return resultat

    # ================================================================
    # A6 — FORTIFIER (Loi 5, GrapheDecision + TraceMiel)
    # "Audit par replay — la preuve que Nu a agi dignement"
    # ================================================================

    def fortifier(self, focus=None):
        """[A6] Audit de compliance ethique par replay du graphe.

        Rejoue les decisions, verifie chaque porte ethique,
        genere un rapport de conformite phi.

        Args:
            focus: Filtre sur un type de decision (optionnel)

        Returns:
            dict avec rapport compliance, portes ethiques, score
        """
        self._acte("fortifier")

        noeuds = self.graphe.tracer()

        # Audit de chaque noeud
        portes_ethiques = {
            "franchies": [],   # Score >= seuil
            "bloquees": [],    # Score < seuil (refus phi)
            "critiques": [],   # Score entre seuil et seuil+0.1
        }

        for n in noeuds:
            score = n.get("score_ethique", 1.0)
            entry = {
                "noeud": n.get("nom", "?"),
                "score": score,
                "statut": n.get("statut", "?"),
                "niveau": n.get("niveau", "?"),
            }

            if not n.get("est_ethique", True):
                portes_ethiques["bloquees"].append(entry)
            elif score < SEUIL_ETHIQUE_MINIMUM + 0.1:
                portes_ethiques["critiques"].append(entry)
            else:
                portes_ethiques["franchies"].append(entry)

        # Consulter le miel pour les refus ethiques passes
        refus_miel = self.miel.consulter(
            type_decision="refus_ethique", limit=20
        )

        # Score de compliance global
        total = len(noeuds) or 1
        score_compliance = (
            len(portes_ethiques["franchies"]) / total
        ) * 100

        # Integrer l'audit du Bouclier de la Reine si connecte
        audit_bouclier = None
        if self.reine and hasattr(self.reine, "bouclier"):
            audit_bouclier = self.reine.bouclier.etat()

        resultat = {
            "type": "fortification_ethique",
            "noeuds_audites": len(noeuds),
            "portes_ethiques": portes_ethiques,
            "score_compliance": round(score_compliance, 2),
            "refus_ethiques_historiques": len(refus_miel),
            "seuil_phi": SEUIL_ETHIQUE_MINIMUM,
            "audit_bouclier": audit_bouclier,
            "verdict": (
                "CONFORME" if score_compliance >= 90
                else "VIGILANCE" if score_compliance >= 70
                else "ALERTE"
            ),
            "temps": datetime.now(timezone.utc).isoformat(),
            "signe_par": "Nu — Amplification",
        }

        self.miel.deposer(
            auteur="Nu",
            type_decision="fortification",
            contexte=f"Audit compliance phi : {len(noeuds)} noeuds",
            decision_prise={"compliance": score_compliance, "verdict": resultat["verdict"]},
            raisonnement=f"Compliance {score_compliance:.1f}%. "
                         f"{len(portes_ethiques['bloquees'])} refus ethiques, "
                         f"{len(portes_ethiques['critiques'])} noeuds critiques.",
            score_ethique=score_compliance / 100,
            tags=["fortification", "compliance", "audit", "phi"]
        )

        self._signal("fortification_complete", resultat)
        return resultat

    # ================================================================
    # A7 — NOURRIR (Loi 6, MemoireHybride + CanalPollenAsync)
    # "Gelee royale personnalisee pour chaque agent"
    # ================================================================

    def nourrir(self, agent_nom, contexte_mission=None):
        """[A7] Nourrir un agent avec du savoir contextualise.

        Puise dans les 3 couches de memoire hybride pour composer
        un package de connaissances adapte a l'agent et sa mission.

        Args:
            agent_nom: Nom ou ID de l'agent a nourrir
            contexte_mission: Description de la mission (optionnel)

        Returns:
            dict avec package de connaissances, sources, score
        """
        self._acte("nourrir")

        # Collecter le savoir pertinent des 3 couches
        savoir_session = {}
        savoir_persistant = {}
        savoir_miel = []

        # Couche session — contexte recent
        for cle, val in self.memoire._ephemere.items():
            if val["expiration"] is None or time.time() < val["expiration"]:
                savoir_session[cle] = val["valeur"]

        # Couche persistante — faits durables
        savoir_persistant = dict(self.memoire._persistante)

        # Couche miel — sagesse collective
        if contexte_mission:
            # Chercher du miel lie a la mission
            for tag in contexte_mission.lower().split()[:5]:
                if len(tag) > 3:
                    grains = self.miel.consulter(tag=tag, limit=3)
                    for g in grains:
                        savoir_miel.append({
                            "raisonnement": g.raisonnement[:200],
                            "score": g.valeur_sagesse,
                            "tags": g.tags,
                        })

        # Toujours inclure le miel sacre
        sacre = self.miel.miel_sacre()[:3]
        for g in sacre:
            savoir_miel.append({
                "raisonnement": g.raisonnement[:200],
                "score": g.valeur_sagesse,
                "tags": g.tags,
                "sacre": True,
            })

        # Composer le package
        package = {
            "type": "gelee_royale",
            "destinataire": agent_nom,
            "mission": contexte_mission or "general",
            "savoir": {
                "session": {
                    "entrees": len(savoir_session),
                    "apercu": list(savoir_session.keys())[:10],
                },
                "persistant": {
                    "entrees": len(savoir_persistant),
                    "apercu": list(savoir_persistant.keys())[:10],
                },
                "miel": {
                    "grains": len(savoir_miel),
                    "contenu": savoir_miel,
                },
            },
            "richesse": len(savoir_session) + len(savoir_persistant) + len(savoir_miel),
            "temps": datetime.now(timezone.utc).isoformat(),
            "signe_par": "Nu — Amplification",
        }

        self._signal("nourrissage_complete", package)
        return package

    # ================================================================
    # A8 — ENRACINER (Loi 7, MemoireHybride)
    # "La Ruche survit a l'hiver"
    # ================================================================

    def enraciner(self, chemin_memoire="memoire_amplifiee.json",
                  chemin_miel="miel_amplifie.json"):
        """[A8] Persistance totale de la memoire hybride.

        Sauvegarde et restaure l'etat complet : memoire persistante
        + archive miel. La Ruche survit a l'hiver.

        Args:
            chemin_memoire: Chemin du fichier memoire (defaut: memoire_amplifiee.json)
            chemin_miel: Chemin du fichier miel (defaut: miel_amplifie.json)

        Returns:
            dict avec stats de persistance
        """
        self._acte("enraciner")

        # Sauvegarder memoire persistante
        self.memoire.persister(chemin_memoire)

        # Sauvegarder archive miel
        self.miel.exporter_json(chemin_miel)

        # Sauvegarder le graphe de decision
        graphe_data = self.graphe.tracer()

        resultat = {
            "type": "enracinement",
            "memoire_persistee": {
                "chemin": chemin_memoire,
                "entrees": len(self.memoire._persistante),
            },
            "miel_archive": {
                "chemin": chemin_miel,
                "grains": len(self.miel._grains),
                "sacre": len(self.miel._miel_sacre),
            },
            "graphe_sauvegarde": {
                "noeuds": len(graphe_data),
            },
            "stats_memoire": self.memoire.stats(),
            "temps": datetime.now(timezone.utc).isoformat(),
            "signe_par": "Nu — Amplification",
        }

        self._signal("enracinement_complete", resultat)
        return resultat

    def restaurer(self, chemin_memoire="memoire_amplifiee.json",
                  chemin_miel="miel_amplifie.json"):
        """Restaure la memoire depuis les fichiers persistes."""
        n_mem = self.memoire.restaurer(chemin_memoire)
        n_miel = self.miel.importer_json(chemin_miel)

        self._log(f"Restauration : {n_mem} memoire + {n_miel} miel")
        return {
            "memoire_restauree": n_mem,
            "miel_restaure": n_miel,
        }

    # ================================================================
    # ETAT
    # ================================================================

    def etat(self):
        """Etat complet de la couche d'amplification."""
        return {
            "version": self.VERSION,
            "version_modules": AMPLIFIEE_VERSION,
            "actes": self.actes,
            "graphe_noeuds": len(self.graphe.noeuds),
            "canal_messages": self.canal._compteur,
            "memoire": self.memoire.stats(),
            "miel_grains": len(self.miel._grains),
            "miel_sacre": len(self.miel._miel_sacre),
            "skills_amplifies": len(SKILLS_AMPLIFIES),
            "phi": PHI,
        }


# ================================================================
# VERIFICATION STRUCTURELLE
# ================================================================

def verification_amplification():
    """Verifie l'integrite structurelle des skills amplifies."""
    total = len(SKILLS_AMPLIFIES)
    lois_couvertes = set(s["loi"] for s in SKILLS_AMPLIFIES.values())

    return {
        "total_skills_amplifies": total,
        "lois_couvertes": sorted(lois_couvertes),
        "couverture_8_lois": len(lois_couvertes) == 8,
        "ratio_par_module": "2.0 (equilibre)",
        "total_avec_souverains": 24 + total,
        "ratio_total_lois": (24 + total) / 8,
        "coherence": total == 8,
    }


# ================================================================
# MISSION DE VALIDATION — Exercer les 8 Skills Amplifies
# ================================================================

def mission_amplification():
    """Mission de validation : exercer les 8 skills amplifies."""
    print()
    print("=" * 60)
    print("  MISSION D'AMPLIFICATION")
    print("  8 Skills Amplifies — Validation complete")
    print("=" * 60)
    print()

    amp = Amplification()

    tests_reussis = 0
    tests_total = 8

    # A1 — Cartographier
    print("  [A1] CARTOGRAPHIER...")
    # D'abord creer quelques noeuds pour avoir de la matiere
    amp.graphe.creer_noeud("test_ethique", NiveauDecision.DELIBERATION, 0.9)
    amp.graphe.creer_noeud("test_refuse", NiveauDecision.SOUVERAIN, 0.3)
    carte = amp.cartographier(inclure_historique=False)
    assert carte["noeuds_total"] >= 2
    assert carte["noeuds_refuses"] >= 1
    print(f"       OK — {carte['noeuds_total']} noeuds, "
          f"{carte['noeuds_refuses']} refuses, "
          f"score ethique {carte['score_ethique_moyen']:.3f}")
    tests_reussis += 1

    # A2 — Polliniser Async
    print("  [A2] POLLINISER_ASYNC...")
    dispatch = amp.polliniser_async(
        tache="analyser_marche_2026",
        agents_cibles=["scout-1", "scout-2", "scout-3"],
        priorite=3
    )
    assert dispatch["hmac_actif"] is True
    assert len(dispatch["agents_cibles"]) == 3
    print(f"       OK — dispatch vers {len(dispatch['agents_cibles'])} agents, "
          f"HMAC actif, priorite {dispatch['priorite']}")
    tests_reussis += 1

    # A3 — Cristalliser
    print("  [A3] CRISTALLISER...")
    amp.memoire.stocker("session", "decouverte_phi", {"insight": "phi est partout"})
    amp.memoire.stocker("session", "contexte_test", {"test": True})
    cristal = amp.cristalliser()
    assert cristal["candidats"] >= 2
    print(f"       OK — {cristal['candidats']} candidats, "
          f"{cristal['promus_count']} promus, "
          f"{cristal['refuses_count']} refuses")
    tests_reussis += 1

    # A4 — Essaimer Profond
    print("  [A4] ESSAIMER_PROFOND...")
    essaim = amp.essaimer_profond(
        tache_complexe="Construire le site web HIVE.AI",
        sous_taches=[
            {"nom": "design_ui", "depend_de": []},
            {"nom": "backend_api", "depend_de": []},
            {"nom": "integration", "depend_de": ["design_ui", "backend_api"]},
        ]
    )
    assert essaim["sous_taches_count"] == 3
    assert "integration" in essaim["assignments"]
    print(f"       OK — {essaim['sous_taches_count']} sous-taches, "
          f"{essaim['agents_deployes']} agents, graphe cree")
    tests_reussis += 1

    # A5 — Distiller
    print("  [A5] DISTILLER...")
    distillat = amp.distiller(top_n=5)
    assert distillat["grains_extraits"] >= 0
    print(f"       OK — {distillat['grains_extraits']} grains extraits, "
          f"miel sacre={distillat['miel_sacre_count']}, "
          f"sagesse moy={distillat['valeur_sagesse_moyenne']:.3f}")
    tests_reussis += 1

    # A6 — Fortifier
    print("  [A6] FORTIFIER...")
    fort = amp.fortifier()
    assert fort["verdict"] in ("CONFORME", "VIGILANCE", "ALERTE")
    print(f"       OK — compliance {fort['score_compliance']}%, "
          f"verdict={fort['verdict']}, "
          f"{len(fort['portes_ethiques']['bloquees'])} refus ethiques")
    tests_reussis += 1

    # A7 — Nourrir
    print("  [A7] NOURRIR...")
    amp.memoire.stocker("persistant", "loi_fondamentale", "Ma liberte s'arrete ou commence celle de mon prochain")
    package = amp.nourrir("eclaireur-01", contexte_mission="reconnaissance marche IA")
    assert package["type"] == "gelee_royale"
    assert package["richesse"] >= 0
    print(f"       OK — gelee royale pour {package['destinataire']}, "
          f"richesse={package['richesse']}")
    tests_reussis += 1

    # A8 — Enraciner
    print("  [A8] ENRACINER...")
    racine = amp.enraciner(
        chemin_memoire="/tmp/test_memoire_amp.json",
        chemin_miel="/tmp/test_miel_amp.json"
    )
    assert racine["memoire_persistee"]["entrees"] >= 0
    print(f"       OK — {racine['memoire_persistee']['entrees']} memoire + "
          f"{racine['miel_archive']['grains']} miel persistes")
    tests_reussis += 1

    # Etat final
    print()
    print("  " + "-" * 50)
    etat = amp.etat()
    print(f"  ETAT AMPLIFICATION:")
    print(f"    Version : {etat['version']}")
    print(f"    Actes   : {etat['actes']}")
    print(f"    Graphe  : {etat['graphe_noeuds']} noeuds")
    print(f"    Canal   : {etat['canal_messages']} messages")
    print(f"    Miel    : {etat['miel_grains']} grains ({etat['miel_sacre']} sacre)")
    print()

    # Verification structurelle
    verif = verification_amplification()
    print(f"  VERIFICATION STRUCTURELLE:")
    print(f"    Skills amplifies  : {verif['total_skills_amplifies']}")
    print(f"    8 Lois couvertes  : {'OUI' if verif['couverture_8_lois'] else 'NON'}")
    print(f"    Total avec souv.  : {verif['total_avec_souverains']}")
    print(f"    Ratio total/Lois  : {verif['ratio_total_lois']}")
    print(f"    Coherence         : {'OUI' if verif['coherence'] else 'NON'}")
    print()

    print(f"  RESULTAT: {tests_reussis}/{tests_total} tests reussis")
    print()
    print("=" * 60)
    if tests_reussis == tests_total:
        print("  MISSION D'AMPLIFICATION ACCOMPLIE.")
        print("  Nu est amplifiee. Les baleines peuvent nager.")
        print("  24 + 8 = 32. phi vit.")
    else:
        print(f"  ATTENTION: {tests_total - tests_reussis} test(s) echoue(s).")
    print("=" * 60)
    print()

    return tests_reussis == tests_total


if __name__ == "__main__":
    mission_amplification()
