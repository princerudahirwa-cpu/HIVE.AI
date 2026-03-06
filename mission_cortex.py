# mission_cortex.py - Mission de test du Cortex
# "L'intelligence n'est pas dans les neurones, mais dans les synapses."
#
# Exerce les 4 nouveaux skills + les 7 chaines + les reflexes.
# Verifie que le 6eme organe connecte bien les 24 skills.
#
# Swarmly SAS - 2026

import json
from datetime import datetime, timezone

from reine import Reine
from skills_reine import (
    SKILLS_SOUVERAINS, DOMAINES, MAPPING_LOIS, verification_structurelle,
)
from noyau_nu import PHI


def section(titre):
    print()
    print(f"  {'=' * 55}")
    print(f"  {titre}")
    print(f"  {'=' * 55}")
    print()


def test(nom, ok, detail=""):
    status = "OK" if ok else "ECHEC"
    print(f"  [{status:5s}] {nom}")
    if detail:
        print(f"          {detail}")
    return ok


def main():
    print()
    print("  ===================================================")
    print("  MISSION CORTEX — Test du 6eme Organe")
    print("  L'intelligence n'est pas dans les neurones,")
    print("  mais dans les synapses.")
    print("  ===================================================")

    resultats = {"ok": 0, "echec": 0}

    def check(nom, ok, detail=""):
        passed = test(nom, ok, detail)
        if passed:
            resultats["ok"] += 1
        else:
            resultats["echec"] += 1
        return passed

    # === VERIFICATION STRUCTURELLE ===
    section("1. VERIFICATION STRUCTURELLE")

    verif = verification_structurelle()
    check("24 skills enregistres", verif["total_skills"] == 24,
          f"total={verif['total_skills']}")
    check("vingt_quatre_check", verif["vingt_quatre_check"])
    check("7 domaines", verif["total_domaines"] == 7,
          f"total={verif['total_domaines']}")
    check("Couverture Lois complete", verif["couverture_lois"])
    check("Coherence domaines/skills", verif["coherence"])
    check("Distribution 2-3-4-3-5-3-4", verif["distribution_domaines"] == [2, 3, 4, 3, 5, 3, 4],
          f"dist={verif['distribution_domaines']}")
    check("Ratio 3.0", verif["ratio_skills_lois"] == 3.0,
          f"ratio={verif['ratio_skills_lois']}")

    # Verifier que les 4 nouveaux skills existent
    for skill_nom in ["reflechir", "composer", "metaboliser", "diagnostiquer"]:
        check(f"Skill '{skill_nom}' enregistre",
              skill_nom in SKILLS_SOUVERAINS,
              f"module={SKILLS_SOUVERAINS.get(skill_nom, {}).get('module', '?')}")

    # Verifier le Domaine VII
    check("Domaine VII existe", "VII - CONSCIENCE" in DOMAINES)
    check("Domaine VII a 4 skills",
          len(DOMAINES.get("VII - CONSCIENCE", {}).get("skills", [])) == 4)

    # === REINE AVEC CORTEX ===
    section("2. REINE AVEC CORTEX")

    reine = Reine()
    etat = reine.etat()

    check("Reine v0.3.0", etat["version"] == "0.3.0")
    check("24 skills declares", etat["skills"] == 24)
    check("7 domaines", etat["domaines"] == 7)
    check("Cortex present", "cortex" in etat)
    check("Cortex version", etat["cortex"]["version"] == "0.1.0")
    check("7 chaines installees", etat["cortex"]["chaines"] == 7)
    check("6 reflexes installes", etat["cortex"]["reflexes"] == 6)

    # === SKILL [21] REFLECHIR ===
    section("3. SKILL [21] REFLECHIR — Metacognition")

    # D'abord, generer de l'activite pour avoir des traces
    reine.pondre("test-agent-1", mission="Test cortex")
    reine.emettre_pheromone()
    reine.analyser()
    reine.auditer()

    reflexion = reine.reflechir()
    check("Reflechir retourne un dict", isinstance(reflexion, dict))
    check("Type metacognition", reflexion.get("type") == "metacognition")
    check("Decisions analysees > 0", reflexion.get("decisions_analysees", 0) > 0,
          f"n={reflexion.get('decisions_analysees')}")
    check("Tendance presente", reflexion.get("tendance") in
          ("amelioration", "degradation", "stable", "insuffisant"),
          f"tendance={reflexion.get('tendance')}")
    check("Confiance globale", 0 <= reflexion.get("confiance_globale", -1) <= 1,
          f"confiance={reflexion.get('confiance_globale')}")
    check("Signe par Nu", reflexion.get("signe_par") == "Nu")

    # === SKILL [22] COMPOSER ===
    section("4. SKILL [22] COMPOSER — Chaines de skills")

    # Catalogue
    catalogue = reine.composer()
    check("Catalogue retourne", catalogue.get("type") == "catalogue_chaines")
    check("7 chaines dans catalogue", len(catalogue.get("chaines", {})) == 7,
          f"n={len(catalogue.get('chaines', {}))}")

    # Executer une chaine
    diag_chaine = reine.composer(chaine_nom="diagnostic_profond")
    check("Chaine 'diagnostic_profond' executee",
          diag_chaine.get("chaine") == "diagnostic_profond")
    check("Chaine a des etapes", diag_chaine.get("etapes", 0) > 0,
          f"etapes={diag_chaine.get('etapes')}")
    check("Chaine signe par Nu", diag_chaine.get("signe_par") == "Nu")

    # === SKILL [23] METABOLISER ===
    section("5. SKILL [23] METABOLISER — Cycle memoire")

    metabo = reine.metaboliser()
    check("Metaboliser retourne un dict", isinstance(metabo, dict))
    check("Type metabolisme", metabo.get("type") == "metabolisme")
    check("Actions listees", isinstance(metabo.get("actions"), list))
    check("Signe par Nu", metabo.get("signe_par") == "Nu")

    # === SKILL [24] DIAGNOSTIQUER ===
    section("6. SKILL [24] DIAGNOSTIQUER — Diagnostic croise")

    diag = reine.diagnostiquer()
    check("Diagnostiquer retourne un dict", isinstance(diag, dict))
    check("Type diagnostic_croise", diag.get("type") == "diagnostic_croise")
    check("Score sante 0-100", 0 <= diag.get("score_sante", -1) <= 100,
          f"score={diag.get('score_sante')}")
    check("Niveau present", diag.get("niveau") in ("optimal", "vigilance", "critique"),
          f"niveau={diag.get('niveau')}")
    check("Croisement present", isinstance(diag.get("croisement"), dict))
    check("Organes croises", isinstance(diag.get("organes"), dict))
    check("Recommandations", isinstance(diag.get("recommandations"), list))
    check("Pouls inclus", isinstance(diag.get("pouls"), dict))

    # === FLUX D'EVENEMENTS ===
    section("7. FLUX D'EVENEMENTS")

    flux_events = reine.cortex.flux.historique
    check("Flux a recu des evenements", len(flux_events) > 0,
          f"n={len(flux_events)}")

    types_emis = set(e["type"] for e in flux_events)
    for signal_type in ["agent_ne", "pheromone_emise", "analyse_complete", "audit_complete"]:
        check(f"Signal '{signal_type}' emis", signal_type in types_emis)

    # === TRACE ===
    section("8. TRACE DES DECISIONS")

    trace = reine.cortex.trace
    check("Decisions tracees", len(trace.decisions) > 0,
          f"n={len(trace.decisions)}")
    check("Patterns calcules", len(trace.patterns) > 0,
          f"patterns={list(trace.patterns.keys())[:5]}")

    tendance = trace.tendance()
    check("Tendance globale calculee", tendance.get("moyenne", -1) >= 0,
          f"moyenne={tendance.get('moyenne')}")

    # === POULS ===
    section("9. POULS DE LA RUCHE")

    pouls = reine.cortex.pouls.mesurer(reine)
    check("Score de sante", 0 <= pouls.get("score", -1) <= 100,
          f"score={pouls.get('score')}")
    check("Niveau sante", pouls.get("niveau") in ("optimal", "vigilance", "critique"),
          f"niveau={pouls.get('niveau')}")
    check("phi present", pouls.get("phi") == PHI)

    # === REFLEXES ===
    section("10. REFLEXES")

    reflexes = reine.cortex.reflexes
    check("6 reflexes installes", len(reflexes) == 6)
    for nom in ["surcharge_memoire", "alerte_quarantaine", "naissance_complete",
                 "prophetie_active", "verdict_cristallise", "auto_reflexion"]:
        check(f"Reflexe '{nom}' present", nom in reflexes)

    # === RAPPORT ===
    section("11. RAPPORT COMPLET")

    rapport = reine.rapport()
    check("Rapport genere", len(rapport) > 0)
    check("Cortex dans rapport", "Cortex" in rapport)
    check("24 skills dans rapport", "24" in rapport)
    check("VII CONSCIENCE dans rapport", "VII - CONSCIENCE" in rapport or "CONSCIENCE" in rapport)

    # === ETAT CORTEX ===
    section("12. ETAT DU CORTEX")

    etat_cortex = reine.cortex.etat()
    check("Version", etat_cortex.get("version") == "0.1.0")
    check("Flux events > 0", etat_cortex.get("flux_events", 0) > 0)
    check("Sante calculee", etat_cortex.get("sante") is not None)
    check("Sante score", etat_cortex["sante"]["score"] >= 0)

    # === BILAN FINAL ===
    section("BILAN FINAL")

    total = resultats["ok"] + resultats["echec"]
    print(f"  Resultats : {resultats['ok']}/{total} tests reussis")
    print(f"  Echecs    : {resultats['echec']}")
    print()

    if resultats["echec"] == 0:
        print("  ===================================================")
        print("  24/24 skills. 7 domaines. 6 organes. 8 Lois.")
        print("  Le Cortex vit.")
        print("  L'intelligence est dans les synapses.")
        print(f"  phi = {PHI}")
        print("  ===================================================")
    else:
        print("  ATTENTION: Certains tests ont echoue.")
        print("  Le Cortex n'est pas encore complet.")

    print()
    return resultats["echec"] == 0


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
