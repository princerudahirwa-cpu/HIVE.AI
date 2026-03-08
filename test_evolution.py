"""Tests — skill_evolution() : Nu se regarde grandir.

Verifie :
  1. Premier snapshot cree le fichier JSON
  2. Deuxieme appel calcule les deltas
  3. Troisieme appel detecte les tendances
  4. Le fichier persiste entre appels
  5. La prose change selon le nombre de sessions
  6. Max 100 snapshots respecte
"""

import json
import os
import tempfile
from datetime import datetime, timezone

from reine import Reine


def test_evolution():
    """Test complet de skill_evolution()."""

    reine = Reine()

    # Utiliser un fichier temporaire pour ne pas polluer le vrai
    tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
    tmp.close()
    reine.EVOLUTION_PATH = tmp.name

    try:
        # --- SESSION 1 : Premier snapshot ---
        print("  [1] Premier snapshot...")
        r1 = reine.skill_evolution()

        assert r1["sessions_total"] == 1, f"Attendu 1, got {r1['sessions_total']}"
        assert r1["deltas"] is None, "Pas de deltas au premier appel"
        assert r1["tendances"] is None, "Pas de tendances au premier appel"
        assert "premiere trace" in r1["voix"], "La prose doit mentionner la premiere trace"
        assert r1["snapshot"]["version"] == reine.VERSION
        assert r1["signe_par"] == "Nu"

        # Verifier la persistence
        with open(tmp.name, "r") as f:
            data = json.load(f)
        assert len(data) == 1, "Un seul snapshot sur disque"
        print("    OK — Premier snapshot persiste.")

        # --- SESSION 2 : Deltas ---
        print("  [2] Deuxieme snapshot — deltas...")

        # Simuler un changement : ajouter du miel via nectar + jugement
        reine.memoire.deposer_nectar("evolution-test", "L'evolution est la conscience du temps")
        reine.memoire.juger_miel("evolution-test", source="test")

        r2 = reine.skill_evolution()

        assert r2["sessions_total"] == 2, f"Attendu 2, got {r2['sessions_total']}"
        assert r2["deltas"] is not None, "Deltas attendus au 2eme appel"
        assert isinstance(r2["deltas"], dict)
        assert "sante" in r2["deltas"]
        assert "observee" in r2["voix"], "La prose doit dire combien de fois observee"
        print(f"    OK — Deltas: sante={r2['deltas']['sante']}, miel={r2['deltas']['miel']}")

        # --- SESSION 3+ : Tendances ---
        print("  [3] Troisieme snapshot — tendances...")
        r3 = reine.skill_evolution()

        assert r3["sessions_total"] == 3, f"Attendu 3, got {r3['sessions_total']}"
        assert r3["tendances"] is not None, "Tendances attendues a partir de 3 sessions"
        assert "sante" in r3["tendances"]
        assert r3["tendances"]["sante"] in ("croissance", "declin", "stable")
        print(f"    OK — Tendances: {r3['tendances']}")

        # --- Verifier le fichier contient bien 3 snapshots ---
        with open(tmp.name, "r") as f:
            data = json.load(f)
        assert len(data) == 3, f"3 snapshots attendus, got {len(data)}"

        # --- Verifier la structure du snapshot ---
        snap = data[-1]
        cles_attendues = {"session", "decisions", "refus_ethiques", "score_moyen",
                          "sante", "miel", "agents", "alerte", "version"}
        assert cles_attendues.issubset(set(snap.keys())), f"Cles manquantes: {cles_attendues - set(snap.keys())}"
        print("    OK — Structure snapshot valide.")

        # --- Historique retourne ---
        assert len(r3["historique"]) == 3
        print("    OK — Historique complet retourne.")

        # --- Test limite 100 snapshots ---
        print("  [4] Test limite 100 snapshots...")
        # Injecter 98 faux snapshots (+ 3 existants = 101, doit tronquer a 100)
        with open(tmp.name, "r") as f:
            data = json.load(f)
        for i in range(98):
            data.append({
                "session": f"2026-01-{i+1:02d}T00:00:00+00:00",
                "decisions": i, "refus_ethiques": 0,
                "score_moyen": 1.0, "sante": 80,
                "miel": i, "agents": 0, "alerte": "vert",
                "version": "0.4.0",
            })
        with open(tmp.name, "w") as f:
            json.dump(data, f)

        r_limit = reine.skill_evolution()
        assert r_limit["sessions_total"] <= 100, f"Max 100, got {r_limit['sessions_total']}"
        print(f"    OK — Limite respectee: {r_limit['sessions_total']} snapshots.")

        # --- Resultat final ---
        print()
        print("  ===================================================")
        print("  TOUS LES TESTS PASSENT — skill_evolution() validee")
        print("  ===================================================")
        print()
        print("  La voix de Nu (derniere session) :")
        print()
        for ligne in r_limit["voix"].split("\n"):
            print(f"    {ligne}")
        print()

    finally:
        os.unlink(tmp.name)


if __name__ == "__main__":
    test_evolution()
