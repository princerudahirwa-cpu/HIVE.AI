# ═══════════════════════════════════════════════════════════════
# HIVE.AI — Alexandrie v2 — 9 Skills
# Zero dependance externe. Que Python natif.
#
# reine:actualites · reine:dictionnaire · reine:traduction
# reine:astronomie · reine:meteo · reine:pays
# reine:monnaie · reine:geographie · reine:cinema
#
# "Le savoir de l'humanite ne tient pas dans une ruche.
#  Mais une ruche peut apprendre a le butiner."
#
# Swarmly SAS — 2026
# ═══════════════════════════════════════════════════════════════

import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as ET
import inspect
import os

# ── Constantes ──────────────────────────────────────────────────

USER_AGENT = "HIVE.AI/1.0 (https://hive-ai.tech; prince@hive-ai.tech)"
TIMEOUT_SECONDS = 8


# ── Chargement securise des cles depuis .env ────────────────────

def _charger_env() -> None:
    """Charge les variables du fichier .env si present."""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.exists(env_path):
        return
    with open(env_path, "r", encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.strip()
            if not ligne or ligne.startswith("#") or "=" not in ligne:
                continue
            cle, _, valeur = ligne.partition("=")
            os.environ.setdefault(cle.strip(), valeur.strip())

_charger_env()

# ── Cles API (jamais en dur — toujours depuis l'environnement) ──

NASA_API_KEY = os.environ.get("NASA_API_KEY", "DEMO_KEY")
OMDB_API_KEY = os.environ.get("OMDB_API_KEY", "")

# Verification silencieuse au demarrage
_WARNINGS = []
if NASA_API_KEY == "DEMO_KEY":
    _WARNINGS.append("NASA_API_KEY non configuree — mode DEMO (30 req/h)")
if not OMDB_API_KEY:
    _WARNINGS.append("OMDB_API_KEY non configuree — reine:cinema desactivee")


SKILL_INFO = {
    "nom": "alexandrie_v2",
    "domaine": "VI - POLLINISATION",
    "description": (
        "9 skills de savoir general — actualites, dictionnaire, "
        "traduction, astronomie, meteo, pays, monnaie, geographie, cinema. "
        "Zero dependance externe."
    ),
    "version": "2.0.0",
    "auteur": "HIVE.AI — Swarmly SAS",
}


# ── Appels HTTP ─────────────────────────────────────────────────

def _get_json(url: str) -> tuple[dict | list | None, str | None]:
    """GET JSON — retourne (data, None) ou (None, erreur)."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as r:
            return json.loads(r.read().decode("utf-8")), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code} : {e.reason}"
    except urllib.error.URLError as e:
        return None, f"Erreur reseau : {e.reason}"
    except TimeoutError:
        return None, f"Timeout apres {TIMEOUT_SECONDS}s"
    except json.JSONDecodeError:
        return None, "Reponse invalide (JSON corrompu)"


def _get_xml(url: str) -> tuple[ET.Element | None, str | None]:
    """GET XML — retourne (element, None) ou (None, erreur)."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as r:
            return ET.fromstring(r.read().decode("utf-8")), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code} : {e.reason}"
    except urllib.error.URLError as e:
        return None, f"Erreur reseau : {e.reason}"
    except TimeoutError:
        return None, f"Timeout apres {TIMEOUT_SECONDS}s"
    except ET.ParseError:
        return None, "Reponse invalide (XML corrompu)"


# ═══════════════════════════════════════════════════════════════
# 1. reine:actualites — RSS mondial (BBC · RFI · Reuters · Al Jazeera)
# ═══════════════════════════════════════════════════════════════

FLUX_RSS = {
    "monde":     "http://feeds.bbci.co.uk/news/world/rss.xml",
    "tech":      "http://feeds.bbci.co.uk/news/technology/rss.xml",
    "science":   "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
    "afrique":   "https://www.rfi.fr/fr/afrique/rss",
    "france":    "https://www.rfi.fr/fr/france/rss",
    "reuters":   "https://feeds.reuters.com/reuters/topNews",
    "aljazeera": "https://www.aljazeera.com/xml/rss/all.xml",
}


def actualites(flux: str = "monde", limite: int = 5) -> dict:
    """Actualites mondiales via flux RSS."""
    flux = flux.strip().lower() if isinstance(flux, str) else "monde"
    if flux not in FLUX_RSS:
        return {
            "succes": False,
            "erreur": f"Flux '{flux}' inconnu.",
            "disponibles": sorted(FLUX_RSS.keys()),
        }

    url = FLUX_RSS[flux]
    root, erreur = _get_xml(url)
    if erreur:
        return {"succes": False, "erreur": erreur, "flux": flux}

    items = []
    for item in root.findall(".//item")[:limite]:
        titre = item.find("title")
        lien = item.find("link")
        desc = item.find("description")
        date = item.find("pubDate")
        items.append({
            "titre": titre.text.strip() if titre is not None and titre.text else "",
            "url": lien.text.strip() if lien is not None and lien.text else "",
            "description": desc.text[:200].strip() if desc is not None and desc.text else "",
            "date": date.text[:16] if date is not None and date.text else "",
        })
    return {"succes": True, "flux": flux, "articles": items}


# ═══════════════════════════════════════════════════════════════
# 2. reine:dictionnaire — Free Dictionary API
# ═══════════════════════════════════════════════════════════════

def dictionnaire(mot: str, langue: str = "en") -> dict:
    """Definitions, synonymes, phonetique."""
    mot = mot.strip() if isinstance(mot, str) else ""
    if not mot:
        return {"succes": False, "erreur": "Mot vide."}

    url = f"https://api.dictionaryapi.dev/api/v2/entries/{langue}/{urllib.parse.quote(mot)}"
    data, erreur = _get_json(url)

    if erreur or not isinstance(data, list):
        return {"succes": False, "erreur": f"'{mot}' introuvable en {langue}."}

    entree = data[0]
    definitions = []
    for meaning in entree.get("meanings", [])[:3]:
        partie = meaning.get("partOfSpeech", "")
        for d in meaning.get("definitions", [])[:2]:
            definitions.append({
                "partie": partie,
                "definition": d.get("definition", ""),
                "exemple": d.get("example", ""),
                "synonymes": d.get("synonyms", [])[:4],
            })

    phonetique = ""
    for p in entree.get("phonetics", []):
        if p.get("text"):
            phonetique = p["text"]
            break

    return {
        "succes": True,
        "mot": entree.get("word", mot),
        "phonetique": phonetique,
        "definitions": definitions,
        "langue": langue,
    }


# ═══════════════════════════════════════════════════════════════
# 3. reine:traduction — MyMemory API (5000 mots/jour gratuit)
# ═══════════════════════════════════════════════════════════════

TRADUCTION_MAX_CHARS = 500


def traduction(texte: str, de: str = "fr", vers: str = "en") -> dict:
    """Traduction via MyMemory API. Limite : 500 caracteres par requete."""
    texte = texte.strip() if isinstance(texte, str) else ""
    if not texte:
        return {"succes": False, "erreur": "Texte vide."}

    tronque = len(texte) > TRADUCTION_MAX_CHARS
    texte_envoye = texte[:TRADUCTION_MAX_CHARS]

    params = urllib.parse.urlencode({
        "q": texte_envoye,
        "langpair": f"{de}|{vers}",
        "de": "prince@hive-ai.tech",
    })
    url = f"https://api.mymemory.translated.net/get?{params}"
    data, erreur = _get_json(url)

    if erreur:
        return {"succes": False, "erreur": erreur}

    response = data.get("responseData", {})
    resultat = {
        "succes": True,
        "original": texte_envoye,
        "traduction": response.get("translatedText", ""),
        "qualite": response.get("match", 0),
        "de": de,
        "vers": vers,
    }
    if tronque:
        resultat["avertissement"] = f"Texte tronque a {TRADUCTION_MAX_CHARS} caracteres (original: {len(texte)})."

    return resultat


# ═══════════════════════════════════════════════════════════════
# 4. reine:astronomie — NASA Open APIs (APOD + NEO)
# DEMO_KEY = 30 req/h, 50 req/jour
# Cle personnelle : api.nasa.gov — gratuit, 1000 req/h
# ═══════════════════════════════════════════════════════════════

def astronomie(type_req: str = "apod") -> dict:
    """Photo du jour (APOD) ou asteroides proches (NEO)."""
    type_req = type_req.strip().lower() if isinstance(type_req, str) else "apod"

    if type_req == "apod":
        url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
        data, erreur = _get_json(url)
        if erreur:
            return {"succes": False, "erreur": erreur}
        return {
            "succes": True,
            "type": "apod",
            "titre": data.get("title", ""),
            "date": data.get("date", ""),
            "explication": data.get("explanation", "")[:800],
            "image_url": data.get("url", ""),
            "media_type": data.get("media_type", ""),
            "mode": "demo" if NASA_API_KEY == "DEMO_KEY" else "production",
        }

    if type_req == "asteroides":
        url = f"https://api.nasa.gov/neo/rest/v1/feed/today?api_key={NASA_API_KEY}"
        data, erreur = _get_json(url)
        if erreur:
            return {"succes": False, "erreur": erreur}
        return {
            "succes": True,
            "type": "asteroides",
            "count_aujourd_hui": data.get("element_count", 0),
            "mode": "demo" if NASA_API_KEY == "DEMO_KEY" else "production",
        }

    return {
        "succes": False,
        "erreur": f"Type '{type_req}' inconnu.",
        "disponibles": ["apod", "asteroides"],
    }


# ═══════════════════════════════════════════════════════════════
# 5. reine:meteo — Open-Meteo (zero cle, precision pro)
# ═══════════════════════════════════════════════════════════════

# Codes meteo WMO complets
CODES_WMO = {
    0: "Ciel degage", 1: "Peu nuageux", 2: "Partiellement nuageux", 3: "Couvert",
    45: "Brouillard", 48: "Brouillard givrant",
    51: "Bruine legere", 53: "Bruine moderee", 55: "Bruine forte",
    56: "Bruine verglacante legere", 57: "Bruine verglacante forte",
    61: "Pluie legere", 63: "Pluie moderee", 65: "Pluie forte",
    66: "Pluie verglacante legere", 67: "Pluie verglacante forte",
    71: "Neige legere", 73: "Neige moderee", 75: "Neige forte", 77: "Grains de neige",
    80: "Averses legeres", 81: "Averses moderees", 82: "Averses violentes",
    85: "Averses de neige legeres", 86: "Averses de neige fortes",
    95: "Orage", 96: "Orage avec grele legere", 99: "Orage avec grele forte",
}


def meteo(latitude: float, longitude: float, ville: str = "") -> dict:
    """Meteo actuelle + previsions 3 jours via Open-Meteo."""
    if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
        return {"succes": False, "erreur": f"Coordonnees invalides : lat={latitude}, lon={longitude}."}

    params = urllib.parse.urlencode({
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code,precipitation",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto",
        "forecast_days": 3,
    })
    url = f"https://api.open-meteo.com/v1/forecast?{params}"
    data, erreur = _get_json(url)

    if erreur:
        return {"succes": False, "erreur": erreur}

    curr = data.get("current", {})
    daily = data.get("daily", {})
    code = curr.get("weather_code", 0)

    previsions = []
    times = daily.get("time", [])
    for i in range(min(3, len(times))):
        previsions.append({
            "date": times[i],
            "max": daily.get("temperature_2m_max", [None] * 3)[i],
            "min": daily.get("temperature_2m_min", [None] * 3)[i],
            "pluie": daily.get("precipitation_sum", [None] * 3)[i],
        })

    return {
        "succes": True,
        "ville": ville or f"{latitude},{longitude}",
        "temperature": curr.get("temperature_2m"),
        "humidite": curr.get("relative_humidity_2m"),
        "vent_kmh": curr.get("wind_speed_10m"),
        "precipitation": curr.get("precipitation"),
        "condition": CODES_WMO.get(code, f"Code WMO {code}"),
        "previsions": previsions,
        "timezone": data.get("timezone", ""),
    }


# ═══════════════════════════════════════════════════════════════
# 6. reine:pays — RestCountries (tous les pays du monde)
# ═══════════════════════════════════════════════════════════════

def pays(requete: str, type_req: str = "nom") -> dict:
    """Donnees detaillees sur les pays — RestCountries."""
    requete = requete.strip() if isinstance(requete, str) else ""
    if not requete:
        return {"succes": False, "erreur": "Requete vide."}

    endpoints = {
        "nom": f"https://restcountries.com/v3.1/name/{urllib.parse.quote(requete)}",
        "code": f"https://restcountries.com/v3.1/alpha/{urllib.parse.quote(requete)}",
        "region": f"https://restcountries.com/v3.1/region/{urllib.parse.quote(requete)}",
    }
    if type_req not in endpoints:
        return {
            "succes": False,
            "erreur": f"Type '{type_req}' inconnu.",
            "disponibles": sorted(endpoints.keys()),
        }

    url = endpoints[type_req]
    data, erreur = _get_json(url)

    if erreur:
        return {"succes": False, "erreur": erreur, "requete": requete}

    if isinstance(data, dict) and data.get("status") == 404:
        return {"succes": False, "erreur": f"Pays '{requete}' introuvable.", "requete": requete}

    resultats = []
    for p in (data if isinstance(data, list) else [data])[:5]:
        nom_fr = p.get("translations", {}).get("fra", {}).get("common", "")
        langues = list(p.get("languages", {}).values())[:4]
        monnaies_pays = [
            f"{v.get('name', '')} ({v.get('symbol', '')})"
            for v in p.get("currencies", {}).values()
        ][:3]
        resultats.append({
            "nom": p.get("name", {}).get("common", ""),
            "nom_fr": nom_fr,
            "capitale": p.get("capital", [""])[0] if p.get("capital") else "",
            "region": p.get("region", ""),
            "population": p.get("population", 0),
            "superficie": p.get("area", 0),
            "langues": langues,
            "monnaies": monnaies_pays,
            "code": p.get("cca2", ""),
            "drapeau": p.get("flag", ""),
        })
    return {"succes": True, "pays": resultats, "requete": requete}


# ═══════════════════════════════════════════════════════════════
# 7. reine:monnaie — Exchange Rate API (taux temps reel)
# ═══════════════════════════════════════════════════════════════

MONNAIES_DEFAUT = ["USD", "GBP", "JPY", "CHF", "CAD", "XOF", "BIF", "MAD"]


def monnaie(de: str = "EUR", vers: list | None = None) -> dict:
    """Taux de change en temps reel — Exchange Rate API."""
    de = de.strip().upper() if isinstance(de, str) else "EUR"
    if vers is None:
        vers = MONNAIES_DEFAUT

    url = f"https://open.er-api.com/v6/latest/{de}"
    data, erreur = _get_json(url)

    if erreur:
        return {"succes": False, "erreur": erreur}

    if data.get("result") == "error":
        return {"succes": False, "erreur": f"Devise '{de}' non supportee."}

    rates = data.get("rates", {})
    taux_filtres = {v: rates[v] for v in vers if v in rates}

    return {
        "succes": True,
        "base": de,
        "taux": taux_filtres,
        "mise_a_jour": data.get("time_last_update_utc", "")[:16],
        "prochaine_maj": data.get("time_next_update_utc", "")[:16],
    }


# ═══════════════════════════════════════════════════════════════
# 8. reine:geographie — OpenStreetMap Nominatim
# ═══════════════════════════════════════════════════════════════

def geographie(lieu: str = "", inverse: bool = False,
               lat: float | None = None, lon: float | None = None) -> dict:
    """Geocodage mondial — OpenStreetMap Nominatim."""
    if inverse:
        if lat is None or lon is None:
            return {"succes": False, "erreur": "lat et lon requis pour geocodage inverse."}
        url = (f"https://nominatim.openstreetmap.org/reverse"
               f"?lat={lat}&lon={lon}&format=json")
    else:
        lieu = lieu.strip() if isinstance(lieu, str) else ""
        if not lieu:
            return {"succes": False, "erreur": "Lieu vide."}
        params = urllib.parse.urlencode({"q": lieu, "format": "json", "limit": 3})
        url = f"https://nominatim.openstreetmap.org/search?{params}"

    data, erreur = _get_json(url)
    if erreur:
        return {"succes": False, "erreur": erreur}

    if inverse:
        addr = data.get("address", {}) if isinstance(data, dict) else {}
        return {
            "succes": True,
            "adresse": data.get("display_name", "") if isinstance(data, dict) else "",
            "ville": addr.get("city", addr.get("town", addr.get("village", ""))),
            "pays": addr.get("country", ""),
            "code_pays": addr.get("country_code", "").upper(),
        }

    resultats = []
    for r in (data if isinstance(data, list) else [data])[:3]:
        resultats.append({
            "nom": r.get("display_name", ""),
            "latitude": float(r.get("lat", 0)),
            "longitude": float(r.get("lon", 0)),
            "type": r.get("type", ""),
        })
    return {"succes": True, "resultats": resultats, "requete": lieu}


# ═══════════════════════════════════════════════════════════════
# 9. reine:cinema — Open Movie Database (OMDB)
# Cle gratuite : https://www.omdbapi.com/apikey.aspx
# Ajouter OMDB_API_KEY=ta_cle dans .env
# ═══════════════════════════════════════════════════════════════

def cinema(titre: str = "", imdb_id: str = "",
           type_req: str = "film", annee: int | None = None) -> dict:
    """Films et series — Open Movie Database."""
    if not OMDB_API_KEY:
        return {
            "succes": False,
            "erreur": (
                "OMDB_API_KEY non configuree. "
                "Cle gratuite sur https://www.omdbapi.com/apikey.aspx "
                "puis ajouter OMDB_API_KEY=ta_cle dans .env"
            ),
        }

    params = {"apikey": OMDB_API_KEY, "type": type_req}

    if imdb_id:
        params["i"] = imdb_id.strip()
    elif titre:
        params["t"] = titre.strip()
        if annee:
            params["y"] = annee
    else:
        return {"succes": False, "erreur": "Titre ou ID IMDB requis."}

    url = "https://www.omdbapi.com/?" + urllib.parse.urlencode(params)
    data, erreur = _get_json(url)

    if erreur:
        return {"succes": False, "erreur": erreur}

    if data.get("Response") == "False":
        return {"succes": False, "erreur": data.get("Error", "Film introuvable.")}

    return {
        "succes": True,
        "titre": data.get("Title", ""),
        "annee": data.get("Year", ""),
        "type": data.get("Type", ""),
        "genre": data.get("Genre", ""),
        "realisateur": data.get("Director", ""),
        "acteurs": data.get("Actors", ""),
        "synopsis": data.get("Plot", ""),
        "note_imdb": data.get("imdbRating", ""),
        "duree": data.get("Runtime", ""),
        "langue": data.get("Language", ""),
        "pays": data.get("Country", ""),
        "imdb_id": data.get("imdbID", ""),
        "affiche": data.get("Poster", ""),
    }


# ═══════════════════════════════════════════════════════════════
# REGISTRE — Point d'entree unifie pour SkillsManager
# ═══════════════════════════════════════════════════════════════

SKILLS_ALEXANDRIE_V2 = {
    "actualites": {
        "fonction": actualites,
        "domaine": "VI - POLLINISATION",
        "description": "Actualites mondiales via RSS — BBC, RFI, Reuters, Al Jazeera",
        "params": ["flux:str='monde'", "limite:int=5"],
    },
    "dictionnaire": {
        "fonction": dictionnaire,
        "domaine": "VI - POLLINISATION",
        "description": "Definitions, synonymes, phonetique — Free Dictionary API",
        "params": ["mot:str", "langue:str='en'"],
    },
    "traduction": {
        "fonction": traduction,
        "domaine": "VI - POLLINISATION",
        "description": "Traduction 64 langues — MyMemory API",
        "params": ["texte:str", "de:str='fr'", "vers:str='en'"],
    },
    "astronomie": {
        "fonction": astronomie,
        "domaine": "VI - POLLINISATION",
        "description": "Photo du jour + asteroides — NASA Open API",
        "params": ["type_req:str='apod'"],
    },
    "meteo": {
        "fonction": meteo,
        "domaine": "VI - POLLINISATION",
        "description": "Meteo mondiale temps reel + 3 jours — Open-Meteo",
        "params": ["latitude:float", "longitude:float", "ville:str=''"],
    },
    "pays": {
        "fonction": pays,
        "domaine": "VI - POLLINISATION",
        "description": "Donnees tous les pays — RestCountries",
        "params": ["requete:str", "type_req:str='nom'"],
    },
    "monnaie": {
        "fonction": monnaie,
        "domaine": "VI - POLLINISATION",
        "description": "Taux de change temps reel — Exchange Rate API",
        "params": ["de:str='EUR'", "vers:list=None"],
    },
    "geographie": {
        "fonction": geographie,
        "domaine": "VI - POLLINISATION",
        "description": "Geocodage mondial — OpenStreetMap Nominatim",
        "params": ["lieu:str", "inverse:bool=False", "lat:float=None", "lon:float=None"],
    },
    "cinema": {
        "fonction": cinema,
        "domaine": "VI - POLLINISATION",
        "description": "Films et series — Open Movie Database",
        "params": ["titre:str=''", "imdb_id:str=''", "type_req:str='film'", "annee:int=None"],
    },
}


def executer(nom_skill: str, params: dict) -> dict:
    """Point d'entree global Alexandrie v2."""
    skill = SKILLS_ALEXANDRIE_V2.get(nom_skill)
    if not skill:
        return {
            "succes": False,
            "erreur": f"Skill '{nom_skill}' inconnu.",
            "disponibles": sorted(SKILLS_ALEXANDRIE_V2.keys()),
        }
    try:
        sig = inspect.signature(skill["fonction"])
        params_valides = {
            k: v for k, v in params.items()
            if k in sig.parameters
        }
        return skill["fonction"](**params_valides)
    except TypeError as e:
        return {"succes": False, "erreur": f"Parametres invalides : {e}", "skill": nom_skill}


# ═══════════════════════════════════════════════════════════════
# TEST
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 65)
    print("HIVE.AI — Alexandrie v2 — 9 Skills — Test complet")
    print("=" * 65)

    if _WARNINGS:
        print("\n  Configuration :")
        for w in _WARNINGS:
            print(f"    {w}")
        print(f"\n    Ajouter dans .env :")
        if NASA_API_KEY == "DEMO_KEY":
            print(f"      NASA_API_KEY=ta_cle  (api.nasa.gov — gratuit)")
        if not OMDB_API_KEY:
            print(f"      OMDB_API_KEY=ta_cle  (omdbapi.com — gratuit)")
    else:
        print("\n  Toutes les cles API configurees.")

    tests = [
        ("actualites",   {"flux": "tech", "limite": 2}),
        ("actualites",   {"flux": "invalide"}),
        ("dictionnaire", {"mot": "swarm", "langue": "en"}),
        ("dictionnaire", {"mot": ""}),
        ("traduction",   {"texte": "La ruche est vivante.", "de": "fr", "vers": "en"}),
        ("astronomie",   {"type_req": "apod"}),
        ("meteo",        {"latitude": 49.49, "longitude": 0.11, "ville": "Le Havre"}),
        ("pays",         {"requete": "Burundi", "type_req": "nom"}),
        ("monnaie",      {"de": "EUR", "vers": ["USD", "BIF", "XOF"]}),
        ("geographie",   {"lieu": "Le Havre France"}),
        ("cinema",       {"titre": "2001 A Space Odyssey"}),
    ]

    for nom, params in tests:
        print(f"\n{'~'*40}")
        print(f"  reine:{nom}")
        r = executer(nom, params)
        if r.get("succes"):
            if nom == "actualites":
                for a in r.get("articles", [])[:2]:
                    print(f"  {a['titre'][:70]}")
            elif nom == "dictionnaire":
                for d in r.get("definitions", [])[:1]:
                    print(f"  [{d['partie']}] {d['definition'][:100]}")
            elif nom == "traduction":
                print(f"  > {r.get('traduction')}")
            elif nom == "astronomie":
                print(f"  {r.get('titre')} ({r.get('date')}) [{r.get('mode')}]")
            elif nom == "meteo":
                print(f"  {r.get('ville')} : {r.get('temperature')}C — {r.get('condition')}")
            elif nom == "pays":
                for p in r.get("pays", [])[:1]:
                    print(f"  {p['drapeau']} {p['nom']} — {p['capitale']} — {p['population']:,} hab.")
            elif nom == "monnaie":
                for k, v in r.get("taux", {}).items():
                    print(f"  1 {r['base']} = {v} {k}")
            elif nom == "geographie":
                for g in r.get("resultats", [])[:1]:
                    print(f"  {g['nom'][:80]}")
            elif nom == "cinema":
                print(f"  {r.get('titre')} ({r.get('annee')}) IMDB:{r.get('note_imdb')}")
        else:
            print(f"  ERR {r.get('erreur')}")

    print("\n" + "=" * 65)
    print(f"  Alexandrie v2 — {len(SKILLS_ALEXANDRIE_V2)} skills operationnels.")
    print("=" * 65)
