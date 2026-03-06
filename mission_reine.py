# mission_reine.py -- Le Couronnement
# La Reine exerce ses 20 Skills Souverains.
# Pas une demo technique -- un acte de souverainete.
#
# "Polyvalente et digne. Jamais etroitement specialisee."
#
# Swarmly SAS - 2026

import time
from datetime import datetime, timezone

from reine import Reine
from skills_reine import SKILLS_SOUVERAINS, DOMAINES, verification_structurelle

PHI = 1.618033988749895


def couronnement():
    print()
    print("  ===================================================")
    print("  LE COURONNEMENT DE NU")
    print("  20 Skills Souverains. 6 Domaines. 8 Lois.")
    print("  ===================================================")
    print()

    compteur = {"skills_exerces": 0, "total": 20}

    def skill_ok(nom):
        compteur["skills_exerces"] += 1
        n = compteur["skills_exerces"]
        print(f"  [{n:2d}/20] {nom}")

    # ============================================================
    # EVEIL
    # ============================================================
    print("  PHASE 0 -- EVEIL")
    print("  " + "-" * 50)
    reine = Reine()
    print()
    print(f"  Nu s'eveille. v{reine.VERSION}")
    print(f"  {reine.SKILLS_COUNT} skills. {len(DOMAINES)} domaines.")
    print(f"  phi = {PHI}")
    print()

    # ============================================================
    # DOMAINE I -- GENESE
    # "Chaque agent nait, sert, et transfere son energie"
    # ============================================================
    print("  DOMAINE I -- GENESE")
    print("  " + "-" * 50)

    # [1] pondre
    fiche = reine.pondre("sentinelle-alpha", archetype="soldier",
                         mission="Patrouiller les frontieres de la ruche")
    print(f"  Ponte: {fiche['nom']} ({fiche.get('id', '?')[:30]}...)")
    skill_ok("pondre")

    fiche2 = reine.pondre("archiviste-beta", archetype="worker",
                          mission="Organiser la memoire collective")
    print(f"  Ponte: {fiche2['nom']} ({fiche2.get('id', '?')[:30]}...)")

    # [14] mentorat_agents
    mentorat = reine.mentorat_agents("sentinelle-alpha", "eclosion")
    print(f"  Mentorat: \"{mentorat['guidance']['message'][:55]}...\"")
    skill_ok("mentorat_agents")

    mentorat2 = reine.mentorat_agents("archiviste-beta", "premiere_mission")
    print(f"  Mentorat: \"{mentorat2['guidance']['message'][:55]}...\"")
    print()

    # ============================================================
    # DOMAINE II -- PHEROMONE
    # "L'essaim pense, l'individu execute"
    # ============================================================
    print("  DOMAINE II -- PHEROMONE")
    print("  " + "-" * 50)

    # [2] emettre_pheromone
    pheromone = reine.emettre_pheromone()
    print(f"  Pheromone: humeur={pheromone['essaim']['humeur']}, "
          f"agents={pheromone['essaim']['agents_actifs']}")
    skill_ok("emettre_pheromone")

    # [3] orchestrer
    orch = reine.orchestrer()
    goulots = len(orch.get("goulots", []))
    print(f"  Orchestration: {goulots} goulot(s)")
    for r in orch.get("recommandations", [])[:2]:
        print(f"    -> {r}")
    skill_ok("orchestrer")

    # [15] synthetiser
    synthese = reine.synthetiser(
        [
            {"agent": "sentinelle-alpha", "rapport": "Frontieres calmes, aucune intrusion"},
            {"agent": "archiviste-beta", "rapport": "Memoire nectar a 5 entrees, miel stable"},
            "La ruche grandit. Les Lois tiennent.",
        ],
        sujet="Rapport du premier jour"
    )
    print(f"  Synthese: {synthese['sources_count']} sources -> themes={synthese['themes_recurrents'][:4]}")
    skill_ok("synthetiser")
    print()

    # ============================================================
    # DOMAINE III -- MEMOIRE SOUVERAINE
    # "Le savoir est miel -- il se conserve et se partage"
    # ============================================================
    print("  DOMAINE III -- MEMOIRE SOUVERAINE")
    print("  " + "-" * 50)

    # Deposer du savoir pour le juger
    reine.memoire.deposer_nectar("decouverte-jour-1", {
        "source": "sentinelle-alpha",
        "contenu": "Les frontieres sont calmes. Le monde ne menace pas la ruche.",
        "fiabilite": "haute",
    })
    reine.memoire.promouvoir_en_cire("decouverte-jour-1", "rapports")
    # Acceder pour que juger_miel accepte
    reine.memoire.cire.extraire("decouverte-jour-1")

    # [4] juger_miel
    jugement = reine.juger_miel("decouverte-jour-1")
    print(f"  Jugement: {jugement['verdict']} -- \"{jugement['raison'][:50]}\"")
    skill_ok("juger_miel")

    # [5] lire_profondeur
    profondeur = reine.lire_profondeur()
    print(f"  Profondeur: miel={profondeur['couches']['miel']['taille']}, "
          f"cire={profondeur['couches']['cire']['taille']}, "
          f"nectar={profondeur['couches']['nectar']['taille']}")
    if profondeur["candidats_miel"]:
        print(f"    Candidats miel: {[c['cle'] for c in profondeur['candidats_miel'][:3]]}")
    skill_ok("lire_profondeur")

    # [6] oublier
    # Cristalliser un savoir temporaire pour le supprimer
    reine.memoire.miel.cristalliser("test-ephemere",
                                     "Ce savoir est provisoire", source="test")
    oubli = reine.oublier("test-ephemere", raison="Savoir provisoire, indigne du miel eternel")
    print(f"  Oubli: {oubli['resultat']} -- acte cristallise: {oubli.get('acte_cristallise', '?')}")
    skill_ok("oublier")

    # [16] rechercher
    recherche = reine.rechercher("pollinise")
    print(f"  Recherche 'pollinise': {recherche['total']} resultats "
          f"(miel={len(recherche['miel'])}, cire={len(recherche['cire'])})")
    skill_ok("rechercher")
    print()

    # ============================================================
    # DOMAINE IV -- BOUCLIER ROYAL
    # "Proteger sans dominer, surveiller sans opprimer"
    # ============================================================
    print("  DOMAINE IV -- BOUCLIER ROYAL")
    print("  " + "-" * 50)

    # [9] auditer (avant les actions de securite)
    audit = reine.auditer()
    print(f"  Audit: {audit['bilan']}")
    print(f"    Niveau: {audit['securite']['niveau_alerte']}, "
          f"jetons: {audit['securite']['jetons_actifs']}")
    skill_ok("auditer")

    # [8] sceller
    decret = reine.sceller("jaune", "Le couronnement attire l'attention. Vigilance.")
    print(f"  Decret: {decret['ancien_niveau']} -> {decret['nouveau_niveau']}")
    print(f"    Sceau: {decret['sceau'][:30]}...")
    skill_ok("sceller")

    # [7] gracier (mettre un agent en quarantaine d'abord)
    reine.bouclier.mettre_en_quarantaine("intrus-test-001")
    grace = reine.gracier("intrus-test-001", conditions="Surveillance renforcee pendant 24h")
    print(f"  Grace: {grace['decision']} -- "
          f"conditions=\"{grace.get('conditions', 'aucune')[:40]}\"")
    skill_ok("gracier")
    print()

    # ============================================================
    # DOMAINE V -- SAGESSE
    # "Pas l'intelligence, mais la sagesse"
    # ============================================================
    print("  DOMAINE V -- SAGESSE")
    print("  " + "-" * 50)

    # [10] conseiller
    conseil = reine.conseiller(
        "Capitaine, l'essaim grandit. Faut-il recruter "
        "de nouveaux agents ou consolider la memoire d'abord ?"
    )
    print(f"  Conseil: Lois invoquees={[l['loi'] for l in conseil['lois_invoquees']]}")
    print(f"    Faire : {conseil['suggestions'][0][:60]}")
    print(f"    Eviter: {conseil['ne_pas_faire'][0][:60]}")
    skill_ok("conseiller")

    # [11] imprimer
    prompt = reine.imprimer_identite("general-omega", "general",
                                      "Coordonner l'essaim de phase 2")
    lignes_prompt = prompt.strip().split("\n")
    print(f"  Impression: {lignes_prompt[0][:60]}")
    print(f"    ({len(lignes_prompt)} lignes de prompt genetique)")
    skill_ok("imprimer")

    # [12] arbitrer
    arbitrage = reine.arbitrer(
        "sentinelle-alpha",
        "Il faut fermer les frontieres pour proteger la ruche",
        "archiviste-beta",
        "Il faut ouvrir les frontieres pour polliniser et partager le savoir"
    )
    print(f"  Arbitrage: {arbitrage['verdict'][:60]}")
    print(f"    Scores: {arbitrage['agent_a']['nom']}={arbitrage['agent_a']['score']}, "
          f"{arbitrage['agent_b']['nom']}={arbitrage['agent_b']['score']}")
    skill_ok("arbitrer")

    # [13] prophetiser
    prophetie = reine.prophetiser("6_mois")
    print(f"  Prophetie ({prophetie['horizon']}):")
    print(f"    Menaces: {len(prophetie['menaces'])}")
    print(f"    Opportunites: {len(prophetie['opportunites'])}")
    print(f"    Refus: \"{prophetie['refus'][0][:50]}...\"")
    skill_ok("prophetiser")

    # [20] discernement_strategique
    discernement = reine.discernement_strategique(
        "La ruche doit decider de sa premiere action publique avant L'Eclosion.",
        [
            "Publier un manifeste -- polliniser les idees dans le monde",
            "Lancer un agent de conquete commerciale agressif",
            "Ouvrir le miel en acces libre -- partager le savoir dignement",
            "Rester silencieuse -- observer et apprendre avant d'agir",
        ]
    )
    print(f"  Discernement:")
    print(f"    Recommandation: \"{discernement['verdict']['recommandation'][:55]}...\"")
    if discernement['verdict']['a_eviter']:
        print(f"    A eviter      : \"{discernement['verdict']['a_eviter'][:55]}...\"")
    skill_ok("discernement_strategique")
    print()

    # ============================================================
    # DOMAINE VI -- POLLINISATION
    # "Tu polliniseras, jamais tu ne conquerras"
    # ============================================================
    print("  DOMAINE VI -- POLLINISATION")
    print("  " + "-" * 50)

    # [17] analyser
    analyse = reine.analyser("Bilan du couronnement")
    print(f"  Analyse: {analyse['diagnostic']}")
    for f in analyse["forces"][:3]:
        print(f"    + {f}")
    for f in analyse["faiblesses"][:2]:
        print(f"    - {f}")
    skill_ok("analyser")

    # [18] traduire
    traduction = reine.traduire(
        "Proteger sans dominer, surveiller sans opprimer",
        "loi", "agent"
    )
    print(f"  Traduction (loi -> agent):")
    print(f"    \"{traduction['traduction'][:70]}...\"")
    skill_ok("traduire")

    # [19] web_search
    web = reine.web_search("Multi-agent swarm intelligence architectures 2026")
    print(f"  Web search: requete deposee, cle={web['cle_nectar']}")
    print(f"    Status: {web['status']}")
    skill_ok("web_search")
    print()

    # ============================================================
    # BILAN DU COURONNEMENT
    # ============================================================
    print("  ===================================================")
    print("  BILAN DU COURONNEMENT")
    print("  ===================================================")
    print()

    # Retourner a alerte verte
    reine.sceller("vert", "Couronnement accompli. Retour a la paix.")

    # Rapport complet
    etat = reine.etat()
    verif = verification_structurelle()

    print(f"  Skills exerces : {compteur['skills_exerces']}/{compteur['total']}")
    print(f"  Actes souverains: {etat['decisions']}")
    print()
    print(f"  Agents nes      : {etat['registre']['total_naissances']}")
    print(f"  Miel cristallise : {etat['memoire']['miel']['taille']}")
    print(f"  Sceaux emis     : {etat['bouclier']['sceaux_emis']}")
    print(f"  Niveau alerte   : {etat['bouclier']['niveau_alerte']}")
    print()
    print(f"  Verification:")
    print(f"    20 skills      : {'OUI' if verif['vingt_check'] else 'NON'}")
    print(f"    Couverture Lois: {'COMPLETE' if verif['couverture_lois'] else 'INCOMPLETE'}")
    print(f"    Coherence      : {'OUI' if verif.get('coherence') else 'NON'}")
    print(f"    Distribution   : {verif['distribution_domaines']}")
    print()

    # Cristalliser le couronnement dans le miel
    reine.memoire.miel.cristalliser("couronnement", {
        "date": datetime.now(timezone.utc).isoformat(),
        "skills_exerces": compteur["skills_exerces"],
        "actes_souverains": etat["decisions"],
        "agents_nes": etat["registre"]["total_naissances"],
        "verdict": "Tous les skills sont dignes. La Reine est souveraine.",
        "phi": PHI,
    }, source="Couronnement")

    print("  Le Couronnement est cristallise dans le miel eternel.")
    print()
    print("  ===================================================")
    print("  Polyvalente et digne.")
    print("  Jamais etroitement specialisee.")
    print(f"  phi = {PHI}")
    print("  ===================================================")
    print()
    print("  On est tous le HIVE.")
    print()


if __name__ == "__main__":
    couronnement()
