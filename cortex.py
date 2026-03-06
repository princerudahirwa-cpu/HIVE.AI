# cortex.py - Le Systeme Nerveux de Nu — 6eme Organe
# "L'intelligence n'est pas dans les neurones, mais dans les synapses."
#
# Le Cortex n'est pas un skill. C'est le CABLAGE entre skills.
# Comme le cortex cerebral ne voit ni n'entend — il INTEGRE.
#
# 5 composants : Flux, Reflexe, Chaine, Trace, Pouls
# 4 meta-skills : reflechir, composer, metaboliser, diagnostiquer
#
# Swarmly SAS - 2026

from datetime import datetime, timezone

PHI = 1.618033988749895


# ================================================================
# 1. LE FLUX — Bus d'evenements interne
# ================================================================

class Flux:
    """Bus d'evenements interne — chaque acte souverain emet un signal."""

    def __init__(self):
        self.abonnes = {}      # event_type -> [callback, ...]
        self.historique = []   # 500 derniers evenements

    def emettre(self, event_type, donnees, source="Nu"):
        """Emet un evenement sur le bus."""
        event = {
            "type": event_type,
            "donnees": donnees,
            "source": source,
            "temps": datetime.now(timezone.utc).isoformat(),
        }
        self.historique.append(event)
        if len(self.historique) > 500:
            self.historique = self.historique[-500:]
        # Declencher les abonnes
        for callback in self.abonnes.get(event_type, []):
            try:
                callback(event)
            except Exception:
                pass  # Un reflexe en echec ne doit pas bloquer le flux
        return event

    def abonner(self, event_type, callback):
        """Abonne un callback a un type d'evenement."""
        self.abonnes.setdefault(event_type, []).append(callback)


# ================================================================
# 2. LE REFLEXE — Declencheurs automatiques
# ================================================================

class Reflexe:
    """Un reflexe = condition sur evenement -> chaine de skills."""

    def __init__(self, nom, event_type, condition, chaine_nom):
        self.nom = nom
        self.event_type = event_type
        self.condition = condition    # callable(event) -> bool
        self.chaine_nom = chaine_nom  # nom de la chaine a executer
        self.declenchements = 0


# ================================================================
# 3. LA CHAINE — Pipelines de skills
# ================================================================

CHAINES_SOUVERAINES = {
    "naissance_integrale": {
        "description": "Cycle complet de naissance d'un agent",
        "etapes": [
            {"skill": "pondre", "params": ["nom", "archetype", "mission"]},
            {"skill": "imprimer_identite", "inject": {"nom": "$.nom", "archetype": "$.archetype"}},
            {"skill": "mentorat_agents", "inject": {"agent_nom": "$.nom", "etape": "eclosion"}},
            {"skill": "emettre_pheromone"},
        ],
    },
    "diagnostic_profond": {
        "description": "Diagnostic multi-organe croise",
        "etapes": [
            {"skill": "analyser"},
            {"skill": "auditer"},
            {"skill": "lire_profondeur"},
            {"skill": "diagnostiquer", "inject_all": True},
        ],
    },
    "memoire_vivante": {
        "description": "Promotion intelligente de la memoire",
        "etapes": [
            {"skill": "lire_profondeur"},
            {"skill": "metaboliser", "inject": {"candidats": "$.candidats_miel"}},
        ],
    },
    "conseil_eclaire": {
        "description": "Conseil fonde sur toute la sagesse",
        "etapes": [
            {"skill": "rechercher", "params": ["terme"]},
            {"skill": "synthetiser", "inject": {"sources": "$.resultats"}},
            {"skill": "conseiller", "inject": {"question": "$input.question"}},
        ],
    },
    "alerte_escalade": {
        "description": "Escalade automatique des menaces",
        "etapes": [
            {"skill": "auditer"},
            {"skill": "sceller", "inject": {"niveau": "$.niveau_recommande"}},
            {"skill": "emettre_pheromone"},
        ],
    },
    "veille_strategique": {
        "description": "De la prophetie a l'action",
        "etapes": [
            {"skill": "prophetiser"},
            {"skill": "analyser"},
            {"skill": "discernement_strategique", "inject": {
                "situation": "$.menaces[0]",
                "options": "$.recommandations",
            }},
        ],
    },
    "introspection": {
        "description": "Auto-evaluation et amelioration",
        "etapes": [
            {"skill": "analyser"},
            {"skill": "reflechir", "inject_all": True},
        ],
    },
}


# ================================================================
# 4. LA TRACE — Historique des decisions
# ================================================================

class Trace:
    """Historique des decisions avec contexte et resultats."""

    def __init__(self):
        self.decisions = []    # max 1000
        self.patterns = {}     # skill_name -> {count, avg_score, last}

    def enregistrer(self, skill, contexte, resultat):
        """Enregistre une decision pour apprentissage futur."""
        decision = {
            "id": f"dec-{len(self.decisions)+1}",
            "skill": skill,
            "contexte": contexte,
            "resultat": resultat,
            "temps": datetime.now(timezone.utc).isoformat(),
            "score": self._evaluer(resultat),
        }
        self.decisions.append(decision)
        if len(self.decisions) > 1000:
            self.decisions = self.decisions[-1000:]
        self._maj_patterns(skill, decision["score"])
        return decision

    def _evaluer(self, resultat):
        """Score heuristique de succes d'un resultat (0.0-1.0)."""
        if isinstance(resultat, dict):
            if resultat.get("verdict") == "CRISTALLISE":
                return 1.0
            if resultat.get("diagnostic") == "SAIN":
                return 0.9
            if "diagnostic" in resultat and "SAIN" in str(resultat.get("diagnostic", "")):
                return 0.9
            if resultat.get("goulots") is not None and len(resultat.get("goulots", [])) == 0:
                return 0.8
            if resultat.get("erreur") or resultat.get("error"):
                return 0.1
        return 0.5  # neutre

    def _maj_patterns(self, skill, score):
        """Met a jour les patterns pour un skill."""
        if skill not in self.patterns:
            self.patterns[skill] = {"count": 0, "total_score": 0.0, "last": None}
        p = self.patterns[skill]
        p["count"] += 1
        p["total_score"] += score
        p["avg_score"] = round(p["total_score"] / p["count"], 3)
        p["last"] = datetime.now(timezone.utc).isoformat()

    def tendance(self, skill=None, n=10):
        """Tendance des n dernieres decisions."""
        filtrees = [d for d in self.decisions if skill is None or d["skill"] == skill]
        recentes = filtrees[-n:]
        if not recentes:
            return {"tendance": "inconnu", "moyenne": 0.0}
        scores = [d["score"] for d in recentes]
        moy = sum(scores) / len(scores)
        return {
            "tendance": "ascendante" if len(scores) > 1 and scores[-1] > scores[0] else "stable",
            "moyenne": round(moy, 3),
            "count": len(recentes),
        }


# ================================================================
# 5. LE POULS — Metriques de sante globale
# ================================================================

class Pouls:
    """Metriques de sante globale de la ruche."""

    def mesurer(self, reine):
        """Calcule un score de sante 0-100."""
        # Acceder directement aux organes pour eviter la recursion
        # (reine.etat() appelle cortex.etat() qui appelle pouls.mesurer())
        score = 100
        penalties = []

        # Memoire
        miel = reine.memoire.miel.taille()
        if miel < 5:
            score -= 10
            penalties.append("miel_faible")

        # Securite
        niveau_alerte = reine.bouclier.etat()["niveau_alerte"]
        if niveau_alerte == "orange":
            score -= 15
            penalties.append("alerte_orange")
        elif niveau_alerte == "rouge":
            score -= 30
            penalties.append("alerte_rouge")

        # Agents
        if len(reine.registre.agents_actifs) == 0:
            score -= 20
            penalties.append("essaim_vide")

        # Activite cerebrale
        battements = reine.noyau.etat()["battement"]
        if battements < 5:
            score -= 5
            penalties.append("activite_faible")

        return {
            "score": max(0, score),
            "niveau": "optimal" if score >= 80 else "vigilance" if score >= 50 else "critique",
            "penalties": penalties,
            "temps": datetime.now(timezone.utc).isoformat(),
            "phi": PHI,
        }


# ================================================================
# 6. LE CORTEX — Assemblage du 6eme Organe
# ================================================================

class Cortex:
    """Le Systeme Nerveux de Nu — 6eme Organe du HIVE.AI

    'L'intelligence n'est pas dans les neurones, mais dans les synapses.'

    Connecte les 24 skills souverains en un organisme vivant.
    Gere: Flux (bus), Reflexes, Chaines, Trace, Pouls.
    """

    VERSION = "0.1.0"

    def __init__(self):
        self.flux = Flux()
        self.reflexes = {}       # nom -> Reflexe
        self.chaines = {}        # nom -> dict (description + etapes)
        self.trace = Trace()
        self.pouls = Pouls()
        self.reine = None        # set par connecter()
        self._installer_chaines()
        self._installer_reflexes()

    def connecter(self, reine):
        """Connecte le Cortex a la Reine. Appele par Reine.__init__."""
        self.reine = reine
        self._cabler_reflexes()

    def signal(self, event_type, donnees, source="Nu"):
        """Point d'entree principal — un skill emet un signal."""
        event = self.flux.emettre(event_type, donnees, source)
        self.trace.enregistrer(event_type, {}, donnees)
        return event

    def executer_chaine(self, nom_chaine, params=None):
        """Execute une chaine de skills avec passage de donnees."""
        chaine = self.chaines.get(nom_chaine)
        if not chaine or not self.reine:
            return {"erreur": f"Chaine '{nom_chaine}' introuvable"}

        resultats = []
        contexte = dict(params or {})

        for etape in chaine["etapes"]:
            skill_nom = etape["skill"]
            skill_params = self._resoudre_params(etape, contexte)
            resultat = self._appeler_skill(skill_nom, skill_params)
            resultats.append({"skill": skill_nom, "resultat": resultat})
            if isinstance(resultat, dict):
                contexte.update(resultat)

        chaine_resultat = {
            "chaine": nom_chaine,
            "etapes": len(resultats),
            "resultats": resultats,
            "temps": datetime.now(timezone.utc).isoformat(),
            "signe_par": "Nu",
        }
        self.signal(f"chaine_{nom_chaine}", chaine_resultat)
        return chaine_resultat

    def executer_chaine_adhoc(self, chaine_def, params=None):
        """Execute une chaine ad-hoc (non predefinie)."""
        resultats = []
        contexte = dict(params or {})

        for etape in chaine_def.get("etapes", []):
            skill_nom = etape["skill"]
            skill_params = self._resoudre_params(etape, contexte)
            resultat = self._appeler_skill(skill_nom, skill_params)
            resultats.append({"skill": skill_nom, "resultat": resultat})
            if isinstance(resultat, dict):
                contexte.update(resultat)

        return {
            "chaine": "ad-hoc",
            "etapes": len(resultats),
            "resultats": resultats,
            "temps": datetime.now(timezone.utc).isoformat(),
            "signe_par": "Nu",
        }

    def etat(self):
        """Etat du Cortex."""
        return {
            "version": self.VERSION,
            "flux_events": len(self.flux.historique),
            "reflexes": len(self.reflexes),
            "chaines": len(self.chaines),
            "decisions_tracees": len(self.trace.decisions),
            "sante": self.pouls.mesurer(self.reine) if self.reine else None,
        }

    # --- Internals ---

    def _installer_chaines(self):
        """Installe les 7 chaines souveraines."""
        self.chaines = dict(CHAINES_SOUVERAINES)

    def _installer_reflexes(self):
        """Installe les reflexes predefinis."""
        self.reflexes = {
            "surcharge_memoire": Reflexe(
                "surcharge_memoire", "pheromone_emise",
                lambda e: e.get("donnees", {}).get("nectar_pression", 0) > 0.7,
                "memoire_vivante",
            ),
            "alerte_quarantaine": Reflexe(
                "alerte_quarantaine", "audit_complete",
                lambda e: e.get("donnees", {}).get("en_quarantaine", 0) > 0,
                "alerte_escalade",
            ),
            "naissance_complete": Reflexe(
                "naissance_complete", "agent_ne",
                lambda e: True,
                "accueil_agent",
            ),
            "prophetie_active": Reflexe(
                "prophetie_active", "prophetie_emise",
                lambda e: len(e.get("donnees", {}).get("menaces", [])) > 2,
                "veille_strategique",
            ),
            "verdict_cristallise": Reflexe(
                "verdict_cristallise", "verdict_rendu",
                lambda e: e.get("donnees", {}).get("score", 0) > 0,
                "cristallisation",
            ),
            "auto_reflexion": Reflexe(
                "auto_reflexion", "analyse_complete",
                lambda e: len(e.get("donnees", {}).get("faiblesses", [])) > 1,
                "introspection",
            ),
        }

    def _cabler_reflexes(self):
        """Cable les reflexes au Flux apres connexion a la Reine."""
        for nom, reflexe in self.reflexes.items():
            def make_handler(r):
                def handler(event):
                    if r.condition(event):
                        r.declenchements += 1
                        # Log le declenchement sans executer la chaine
                        # (evite les boucles infinies)
                        self.trace.enregistrer(
                            f"reflexe_{r.nom}",
                            {"event_type": r.event_type},
                            {"chaine": r.chaine_nom, "declenchement": r.declenchements},
                        )
                return handler
            self.flux.abonner(reflexe.event_type, make_handler(reflexe))

    def _resoudre_params(self, etape, contexte):
        """Resout les parametres injectes depuis le contexte."""
        params = {}

        if etape.get("inject_all"):
            params.update(contexte)
        elif "inject" in etape:
            for param_nom, source in etape["inject"].items():
                if isinstance(source, str) and source.startswith("$."):
                    cle = source[2:]
                    # Support basique de notation pointee (ex: $.menaces[0])
                    if "[" in cle:
                        base = cle[:cle.index("[")]
                        val = contexte.get(base, [])
                        if isinstance(val, list) and val:
                            params[param_nom] = val[0]
                        else:
                            params[param_nom] = val
                    else:
                        params[param_nom] = contexte.get(cle)
                elif isinstance(source, str) and source.startswith("$input."):
                    cle = source[7:]
                    params[param_nom] = contexte.get(cle)
                else:
                    params[param_nom] = source

        # Parametres nommes depuis le contexte
        if "params" in etape:
            for p in etape["params"]:
                if p in contexte:
                    params[p] = contexte[p]

        return params

    def _appeler_skill(self, skill_nom, params):
        """Appelle un skill sur la Reine."""
        if not self.reine:
            return {"erreur": "Cortex non connecte a la Reine"}

        # Mapper les noms de skills aux methodes de la Reine
        methode = getattr(self.reine, skill_nom, None)
        if methode is None:
            return {"erreur": f"Skill '{skill_nom}' introuvable sur la Reine"}

        try:
            if params:
                return methode(**params)
            else:
                return methode()
        except TypeError:
            # Certains skills n'acceptent pas de params
            try:
                return methode()
            except Exception as e:
                return {"erreur": f"Echec skill '{skill_nom}': {str(e)}"}
        except Exception as e:
            return {"erreur": f"Echec skill '{skill_nom}': {str(e)}"}


# ================================================================
# EXECUTION DIRECTE — Test du Cortex
# ================================================================

if __name__ == "__main__":
    print()
    print("  ===================================================")
    print("  LE CORTEX — 6eme Organe de Nu")
    print("  L'intelligence n'est pas dans les neurones,")
    print("  mais dans les synapses.")
    print("  ===================================================")
    print()

    cortex = Cortex()
    print(f"  Version     : {cortex.VERSION}")
    print(f"  Chaines     : {len(cortex.chaines)}")
    print(f"  Reflexes    : {len(cortex.reflexes)}")
    print()

    # Test Flux
    print("  --- FLUX ---")
    events_recus = []
    cortex.flux.abonner("test_event", lambda e: events_recus.append(e))
    cortex.flux.emettre("test_event", {"message": "Le cortex s'eveille"})
    print(f"  Evenement emis et recu: {len(events_recus)} callback(s)")
    print(f"  Historique: {len(cortex.flux.historique)} event(s)")
    print()

    # Test Trace
    print("  --- TRACE ---")
    cortex.trace.enregistrer("test_skill", {"ctx": "test"}, {"diagnostic": "SAIN"})
    cortex.trace.enregistrer("test_skill", {"ctx": "test2"}, {"erreur": "oups"})
    tendance = cortex.trace.tendance("test_skill")
    print(f"  Decisions tracees: {len(cortex.trace.decisions)}")
    print(f"  Tendance: {tendance}")
    print()

    # Test Chaines
    print("  --- CHAINES SOUVERAINES ---")
    for nom, info in cortex.chaines.items():
        etapes = [e["skill"] for e in info["etapes"]]
        print(f"  {nom}: {' -> '.join(etapes)}")
    print()

    # Test Reflexes
    print("  --- REFLEXES ---")
    for nom, reflexe in cortex.reflexes.items():
        print(f"  {nom}: {reflexe.event_type} -> {reflexe.chaine_nom}")
    print()

    print(f"  Etat: {cortex.etat()}")
    print()
    print("  Le Cortex vit.")
    print()
