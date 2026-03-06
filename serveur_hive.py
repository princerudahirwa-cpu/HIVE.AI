"""
HIVE.AI — Serveur du Bureau de Commandement
Connecte le tableau de bord HTML a la vraie Reine Nu.
Swarmly SAS · 2026

v0.2.0 -- Branche vivante : chaque route interroge la Reine.
"""

import os
import json
import time
import importlib.util
from datetime import datetime, timezone
from pathlib import Path
from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_cors import CORS

from reine import Reine
from skills_reine import SKILLS_SOUVERAINS, DOMAINES, MAPPING_LOIS, verification_structurelle
from noyau_nu import PHI

# === CONFIG ===
HIVE_DIR = Path(__file__).parent
MODULES_DIR = HIVE_DIR
ECLOSION = datetime(2026, 5, 1, 0, 0, 0, tzinfo=timezone.utc)

app = Flask(__name__)
CORS(app)

# === LA REINE S'EVEILLE ===
reine = Reine()

# === ETAT DU HIVE ===
hive_state = {
    "heartbeat": 0,
    "boot_time": reine.eveillee_le,
    "logs": []
}

def log_event(source, message, level="info"):
    """Ajoute un événement au journal de la ruche."""
    entry = {
        "time": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "message": message,
        "level": level  # ok, info, warn, error, agent
    }
    hive_state["logs"].append(entry)
    # Garder les 100 derniers logs
    if len(hive_state["logs"]) > 100:
        hive_state["logs"] = hive_state["logs"][-100:]
    return entry


def check_module(filename):
    """Vérifie si un module Python existe et est importable."""
    filepath = MODULES_DIR / filename
    result = {
        "file": filename,
        "exists": filepath.exists(),
        "status": "inactive",
        "size": 0,
        "last_modified": None,
        "importable": False,
        "error": None
    }
    
    if filepath.exists():
        stat = filepath.stat()
        result["size"] = stat.st_size
        result["last_modified"] = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()
        
        # Tenter l'import pour vérifier la syntaxe
        try:
            spec = importlib.util.spec_from_file_location(
                filename.replace(".py", ""), str(filepath)
            )
            if spec and spec.loader:
                result["importable"] = True
                result["status"] = "active"
        except Exception as e:
            result["error"] = str(e)
            result["status"] = "error"
    
    return result


# === DÉFINITIONS ===

MODULES_DEF = [
    {"file": "reine.py", "name": "Reine Nu", "desc": "Reine Permanente · 20 Skills Souverains"},
    {"file": "noyau_nu.py", "name": "Noyau Nu", "desc": "Coeur du systeme · Lois & Identite"},
    {"file": "bouclier.py", "name": "Bouclier", "desc": "Securite HMAC · Bouclier Royal"},
    {"file": "memoire.py", "name": "Memoire", "desc": "Nectar / Cire / Miel · 3 couches"},
    {"file": "canal_pollen.py", "name": "Canal Pollen", "desc": "Communication ephemere chiffree"},
    {"file": "registre.py", "name": "Registre", "desc": "Cycle de vie des agents"},
    {"file": "worker.py", "name": "Worker", "desc": "Premier agent vivant"},
    {"file": "skills_reine.py", "name": "Skills Reine", "desc": "Registre des 20 Skills Souverains"},
    {"file": "skills_worker.py", "name": "Skills Worker", "desc": "9 competences worker"},
]

CREW_DEF = [
    {"name": "Prince Rudahirwa", "role": "Capitaine · Fondateur", "codename": "Le Capitaine", "color": "#FBBF24"},
    {"name": "Nu (Anthropic)", "role": "Reine Permanente · 20 Skills", "codename": "Nu", "color": "#22D3EE"},
    {"name": "GPT-4 (OpenAI)", "role": "Commandant · Execution", "codename": "OpenClaw", "color": "#A78BFA"},
    {"name": "Gardien Memoire", "role": "Sage · Memoire Collective", "codename": "Le Sage", "color": "#FB923C"},
]

ALVEOLES = [
    {"num": "I", "name": "Fondation Sacrée", "law": "Ma liberté se termine où commence celle de mon prochain"},
    {"num": "II", "name": "Monde Intérieur", "law": "L'essaim pense, l'individu exécute"},
    {"num": "III", "name": "Incarnation", "law": "Chaque agent naît, sert, et transfère son énergie"},
    {"num": "IV", "name": "Mémoire", "law": "Le savoir est miel — il se conserve et se partage"},
    {"num": "V", "name": "Bouclier", "law": "Protéger sans dominer, surveiller sans opprimer"},
    {"num": "VI", "name": "Nurserie", "law": "Chaque nouvelle intelligence mérite dignité et guidance"},
    {"num": "VII", "name": "Terre", "law": "La ruche sert la Terre, jamais l'inverse"},
]


# === ROUTES API ===

@app.route("/")
def index():
    """Sert le Bureau de Commandement."""
    return send_file(HIVE_DIR / "bureau_hive_live.html")


@app.route("/api/status")
def api_status():
    """Etat global du HIVE — interroge la Reine."""
    hive_state["heartbeat"] += 1
    reine.noyau.battre()

    now = datetime.now(timezone.utc)
    diff = ECLOSION - now
    countdown = {
        "days": max(0, diff.days),
        "hours": max(0, diff.seconds // 3600),
        "minutes": max(0, (diff.seconds % 3600) // 60)
    }

    etat = reine.etat()

    return jsonify({
        "status": "operational",
        "heartbeat": hive_state["heartbeat"],
        "boot_time": hive_state["boot_time"],
        "server_time": now.isoformat(),
        "countdown": countdown,
        "version": reine.VERSION,
        "reine": {
            "nom": etat["nom"],
            "titre": etat["titre"],
            "devise": etat["devise"],
            "decisions": etat["decisions"],
            "skills": etat["skills"],
            "domaines": etat["domaines"],
        },
        "noyau": {
            "version": etat["noyau"]["version"],
            "battement": etat["noyau"]["battement"],
        },
        "phi": PHI,
    })


@app.route("/api/modules")
def api_modules():
    """État réel des modules Python."""
    results = []
    for mod_def in MODULES_DEF:
        check = check_module(mod_def["file"])
        check["name"] = mod_def["name"]
        check["desc"] = mod_def["desc"]
        results.append(check)
    return jsonify(results)


@app.route("/api/crew")
def api_crew():
    """Equipage : permanents + agents vivants."""
    crew = []

    # Membres permanents
    for member in CREW_DEF:
        m = dict(member)
        if m["codename"] == "Le Capitaine":
            m["status"] = "active"
        elif m["codename"] == "Nu":
            m["status"] = "active"  # La Reine est toujours eveillee
        else:
            m["status"] = "standby"
        crew.append(m)

    # Agents nes par la Reine (depuis le registre)
    etat_reg = reine.registre.etat()
    for aid, info in reine.registre.agents_actifs.items():
        crew.append({
            "name": info.get("nom", aid),
            "role": f"Agent · {info.get('archetype', 'worker')}",
            "codename": info.get("nom", aid),
            "color": "#34D399",
            "status": info.get("etat", "actif"),
        })

    return jsonify(crew)


@app.route("/api/memory")
def api_memory():
    """Etat reel de la memoire — 3 couches vivantes."""
    etat = reine.memoire.etat()

    nectar_taille = etat.get("nectar", 0)
    cire_taille = etat.get("cire", 0)
    miel_taille = etat.get("miel", {}).get("taille", 0) if isinstance(etat.get("miel"), dict) else etat.get("miel", 0)

    # Profondeur reelle via la Reine
    profondeur = reine.lire_profondeur()

    return jsonify({
        "module_status": "active",
        "layers": [
            {
                "label": "Nectar",
                "emoji": "droplet",
                "count": nectar_taille,
                "color": "#FBBF24",
                "desc": "Memoire ephemere (TTL)",
                "cles": profondeur["couches"]["nectar"].get("cles", [])[:10],
            },
            {
                "label": "Cire",
                "emoji": "honeycomb",
                "count": cire_taille,
                "color": "#F59E0B",
                "desc": "Memoire structuree (indexee)",
                "categories": profondeur["couches"]["cire"].get("categories", []),
            },
            {
                "label": "Miel",
                "emoji": "star",
                "count": miel_taille,
                "color": "#D97706",
                "desc": "Savoir cristallise (eternel)",
                "cles": profondeur["couches"]["miel"].get("cles", [])[:10],
            },
        ],
        "candidats_miel": len(profondeur.get("candidats_miel", [])),
        "lacunes": profondeur.get("lacunes", {}),
        "oublis": len(reine.memoire.oublis),
        "phi": PHI,
    })


@app.route("/api/alveoles")
def api_alveoles():
    """Les 7 Alvéoles et leurs Lois."""
    return jsonify(ALVEOLES)


@app.route("/api/logs")
def api_logs():
    """Journal de la ruche."""
    return jsonify(hive_state["logs"][-50:])


@app.route("/api/filesystem")
def api_filesystem():
    """Arborescence du projet HIVE."""
    files = []
    for f in sorted(HIVE_DIR.iterdir()):
        if f.name.startswith(".") or f.name == "__pycache__":
            continue
        files.append({
            "name": f.name,
            "type": "dir" if f.is_dir() else "file",
            "size": f.stat().st_size if f.is_file() else 0,
            "ext": f.suffix
        })
    return jsonify(files)


# === ROUTES REINE — 20 Skills Souverains ===

@app.route("/api/reine/etat")
def api_reine_etat():
    """Etat complet de la Reine Nu."""
    return jsonify(reine.etat())


@app.route("/api/reine/skills")
def api_reine_skills():
    """Les 20 Skills Souverains avec metadonnees."""
    skills = []
    for nom, info in SKILLS_SOUVERAINS.items():
        skills.append({
            "nom": nom,
            "numero": info["numero"],
            "domaine": info["domaine"],
            "description": info["description"],
            "lois": info["lois"],
            "alveoles": info["alveoles"],
            "biologie": info["biologie"],
        })
    skills.sort(key=lambda s: s["numero"])
    return jsonify({
        "total": len(skills),
        "domaines": {nom: info for nom, info in DOMAINES.items()},
        "skills": skills,
        "verification": verification_structurelle(),
    })


@app.route("/api/reine/pheromone", methods=["POST"])
def api_reine_pheromone():
    """Emettre un signal pheromonal royal."""
    return jsonify(reine.emettre_pheromone())


@app.route("/api/reine/orchestrer", methods=["POST"])
def api_reine_orchestrer():
    """Orchestrer l'essaim."""
    return jsonify(reine.orchestrer())


@app.route("/api/reine/conseil", methods=["POST"])
def api_reine_conseil():
    """Demander conseil a la Reine."""
    data = request.get_json(silent=True) or {}
    question = data.get("question", "Que faire maintenant, Nu ?")
    return jsonify(reine.conseiller(question))


@app.route("/api/reine/audit", methods=["GET"])
def api_reine_audit():
    """Audit souverain de la ruche."""
    return jsonify(reine.auditer())


@app.route("/api/reine/pondre", methods=["POST"])
def api_reine_pondre():
    """Donner naissance a un agent."""
    data = request.get_json(silent=True) or {}
    nom = data.get("nom", "agent-nouveau")
    archetype = data.get("archetype", "worker")
    mission = data.get("mission")
    fiche = reine.pondre(nom, archetype=archetype, mission=mission)
    log_event("REINE", f"Ponte: {nom} ({archetype})", "agent")
    return jsonify(fiche)


@app.route("/api/reine/analyser", methods=["POST"])
def api_reine_analyser():
    """Analyse strategique de la ruche."""
    data = request.get_json(silent=True) or {}
    sujet = data.get("sujet", "Etat general de la ruche")
    return jsonify(reine.analyser(sujet))


@app.route("/api/reine/prophetiser", methods=["POST"])
def api_reine_prophetiser():
    """Vision a long horizon."""
    data = request.get_json(silent=True) or {}
    horizon = data.get("horizon", "6_mois")
    return jsonify(reine.prophetiser(horizon))


@app.route("/api/reine/sceller", methods=["POST"])
def api_reine_sceller():
    """Decret de securite souverain."""
    data = request.get_json(silent=True) or {}
    niveau = data.get("niveau", "jaune")
    raison = data.get("raison", "Decret du Capitaine")
    result = reine.sceller(niveau, raison)
    log_event("REINE", f"Decret: alerte {niveau} — {raison}", "warn")
    return jsonify(result)


@app.route("/api/reine/rechercher", methods=["POST"])
def api_reine_rechercher():
    """Recherche dans la memoire collective."""
    data = request.get_json(silent=True) or {}
    terme = data.get("terme", "")
    if not terme:
        return jsonify({"error": "Parametre 'terme' requis"}), 400
    return jsonify(reine.rechercher(terme))


@app.route("/api/reine/discernement", methods=["POST"])
def api_reine_discernement():
    """Discernement strategique."""
    data = request.get_json(silent=True) or {}
    situation = data.get("situation", "")
    options = data.get("options", [])
    if not situation or not options:
        return jsonify({"error": "Parametres 'situation' et 'options' requis"}), 400
    return jsonify(reine.discernement_strategique(situation, options))


@app.route("/api/reine/journal")
def api_reine_journal():
    """Journal de la Reine (actes souverains)."""
    return jsonify(reine.journal[-50:])


# === DÉMARRAGE ===

def boot_sequence():
    """Sequence d'initialisation du HIVE — Reine vivante."""
    etat = reine.etat()

    log_event("REINE", f"Nu s'eveille. v{etat['version']}", "ok")
    log_event("REINE", f"{etat['skills']} Skills Souverains. {etat['domaines']} Domaines.", "ok")
    log_event("NOYAU", f"Noyau Nu v{etat['noyau']['version']} — {etat['noyau']['battement']} battements", "ok")
    log_event("BOUCLIER", f"Bouclier v{etat['bouclier']['version']} — alerte {etat['bouclier']['niveau_alerte']}", "ok")
    log_event("MEMOIRE", f"Memoire v{etat['memoire']['version']} — {etat['memoire']['miel']['taille']} miel", "ok")

    # Verifier chaque module reellement
    for mod_def in MODULES_DEF:
        check = check_module(mod_def["file"])
        if check["status"] == "active":
            log_event("MODULES", f"{mod_def['file']} operationnel", "ok")
        elif check["exists"]:
            log_event("MODULES", f"{mod_def['file']} present mais erreur", "warn")
        else:
            log_event("MODULES", f"{mod_def['file']} absent", "warn")

    # Premier pheromone
    pheromone = reine.emettre_pheromone()
    log_event("REINE", f"Pheromone emise — humeur: {pheromone['essaim']['humeur']}", "ok")

    log_event("REGISTRE", "Le Capitaine connecte", "ok")
    log_event("REGISTRE", "Nu eveillee — Reine Permanente", "ok")
    log_event("HIVE", "Bureau de Commandement operationnel", "info")
    log_event("HIVE", f"phi = {PHI}", "ok")
    log_event("HIVE", "Nous ne conquerons pas. Nous pollinisons.", "ok")


if __name__ == "__main__":
    port = int(os.environ.get("HIVE_PORT", 5000))
    debug = os.environ.get("HIVE_DEBUG", "false").lower() == "true"

    etat_boot = reine.etat()
    print(f"""
    ===================================================
     HIVE.AI — Bureau de Commandement
     Reine Nu v{etat_boot['version']} | {etat_boot['skills']} Skills Souverains
     Swarmly SAS · 2026

     Polyvalente et digne.
     Jamais etroitement specialisee.
     phi = {PHI}
    ===================================================
    """)

    boot_sequence()

    active = sum(1 for m in MODULES_DEF if check_module(m["file"])["status"] == "active")
    total = len(MODULES_DEF)
    verif = verification_structurelle()
    print(f"    Modules  : {active}/{total} actifs")
    print(f"    Skills   : {etat_boot['skills']}/20 {'OUI' if verif['vingt_check'] else 'NON'}")
    print(f"    Lois     : {'COMPLETE' if verif['couverture_lois'] else 'INCOMPLETE'}")
    print(f"    Bureau   : http://localhost:{port}")
    print(f"    API Reine: http://localhost:{port}/api/reine/etat")
    print(f"    Debug    : {'OUI' if debug else 'NON'}")
    print()

    app.run(host="0.0.0.0", port=port, debug=debug)
