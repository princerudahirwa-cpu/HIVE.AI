# ═══════════════════════════════════════════════════════════════
# HIVE.AI — Skill : reine:bibliotheque
# Bibliotheque d'Alexandrie — OpenLibrary / Internet Archive
# 20+ millions de livres. Savoir de l'humanite. Libre.
#
# "Une bibliotheque qui brule, c'est une voix qui se tait."
#
# Philosophie :
#   - Le savoir ecrit est le miel de l'humanite.
#   - Chaque livre est une alveole de memoire preservee.
#   - Libre d'acces, jamais possede — consulte avec respect.
#   - L'essaim butine en parallele, chaque agent son sujet.
#
# Swarmly SAS — 2026
# ═══════════════════════════════════════════════════════════════

import urllib.request
import urllib.parse
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# ── Constantes ──────────────────────────────────────────────────

USER_AGENT = "HIVE.AI/1.0 (https://hive-ai.tech; prince@hive-ai.tech)"
BASE_SEARCH = "https://openlibrary.org/search.json"
BASE_WORKS = "https://openlibrary.org"
TIMEOUT_SECONDS = 8
MAX_RESULTATS = 10

SKILL_INFO = {
    "nom": "reine:bibliotheque",
    "domaine": "VI - POLLINISATION",
    "categorie": "savoir",
    "description": (
        "Interroge OpenLibrary (Internet Archive) — 20M+ livres. "
        "Recherche par titre, auteur ou sujet. "
        "La ruche accede a la memoire ecrite de l'humanite."
    ),
    "version": "1.0.0",
    "auteur": "HIVE.AI — Swarmly SAS",
    "source": "https://openlibrary.org/developers/api",
}

# ── Mapping langues 2 lettres → 3 lettres (ISO 639-1 → 639-2/B) ─
# Alignement avec reine:consulter qui utilise les codes 2 lettres.

LANGUES_2_VERS_3 = {
    "fr": "fre", "en": "eng", "es": "spa", "pt": "por", "de": "ger",
    "it": "ita", "nl": "dut", "ru": "rus", "zh": "chi", "ja": "jpn",
    "ko": "kor", "ar": "ara", "hi": "hin", "tr": "tur", "pl": "pol",
    "sv": "swe", "da": "dan", "no": "nor", "fi": "fin", "cs": "cze",
    "hu": "hun", "ro": "rum", "el": "gre", "he": "heb", "fa": "per",
    "uk": "ukr", "vi": "vie", "th": "tha", "id": "ind", "ms": "may",
    "sw": "swa", "am": "amh", "yo": "yor", "ha": "hau", "rw": "kin",
    "af": "afr", "ca": "cat", "hr": "hrv", "sr": "srp", "bg": "bul",
    "sk": "slo", "sl": "slv", "lt": "lit", "lv": "lav", "et": "est",
    "sq": "alb", "mk": "mac", "bn": "ben", "ta": "tam", "te": "tel",
}


def _normaliser_langue(code: str | None) -> str | None:
    """Accepte un code 2 ou 3 lettres, retourne toujours le code 3 lettres."""
    if not code:
        return None
    code = code.strip().lower()
    if len(code) == 2:
        return LANGUES_2_VERS_3.get(code)
    if len(code) == 3:
        return code
    return None


# ── Appel HTTP ──────────────────────────────────────────────────

def _get(url: str) -> tuple[dict | None, str | None]:
    """
    Appel HTTP GET — pas de dependance externe.
    Retourne (data, None) en cas de succes, (None, message_erreur) en cas d'echec.
    """
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


# ── Recherche de livres ─────────────────────────────────────────

def chercher_livres(
    requete: str,
    type_recherche: str = "titre",
    limite: int = 5,
    langue: str | None = None,
) -> dict:
    """
    Recherche des livres sur OpenLibrary.

    Args:
        requete         : Terme de recherche
        type_recherche  : 'titre' | 'auteur' | 'sujet' | 'libre'
        limite          : Nombre de resultats (max MAX_RESULTATS)
        langue          : Code langue 2 ou 3 lettres — optionnel

    Returns:
        dict avec cles: succes, total, livres, requete
    """
    requete = requete.strip() if isinstance(requete, str) else ""
    if not requete:
        return {"succes": False, "erreur": "Requete vide.", "requete": ""}

    champs = {
        "titre": "title",
        "auteur": "author",
        "sujet": "subject",
        "libre": "q",
    }
    champ = champs.get(type_recherche, "q")

    params = {
        champ: requete,
        "limit": min(limite, MAX_RESULTATS),
        "fields": "key,title,author_name,first_publish_year,subject,language,number_of_pages_median,cover_i",
    }

    code_langue = _normaliser_langue(langue)
    if langue and not code_langue:
        return {
            "succes": False,
            "erreur": f"Langue '{langue}' non reconnue.",
            "requete": requete,
        }
    if code_langue:
        params["language"] = code_langue

    url = BASE_SEARCH + "?" + urllib.parse.urlencode(params)
    data, erreur = _get(url)

    if erreur:
        return {"succes": False, "erreur": erreur, "requete": requete}

    livres = []
    for doc in data.get("docs", []):
        livre = {
            "titre": doc.get("title", "Inconnu"),
            "auteurs": doc.get("author_name", [])[:3],
            "annee": doc.get("first_publish_year"),
            "pages": doc.get("number_of_pages_median"),
            "sujets": doc.get("subject", [])[:5],
            "langues": doc.get("language", [])[:3],
            "url": f"https://openlibrary.org{doc['key']}" if doc.get("key") else None,
            "couverture": f"https://covers.openlibrary.org/b/id/{doc['cover_i']}-M.jpg" if doc.get("cover_i") else None,
        }
        livres.append(livre)

    return {
        "succes": True,
        "total": data.get("numFound", 0),
        "livres": livres,
        "requete": requete,
        "type": type_recherche,
    }


# ── Detail d'un livre ───────────────────────────────────────────

def detail_livre(cle_ol: str) -> dict:
    """
    Recupere le detail complet d'un livre via sa cle OpenLibrary.
    Ex: cle_ol = '/works/OL45804W'
    """
    cle_ol = cle_ol.strip()
    if not cle_ol:
        return {"succes": False, "erreur": "Cle OpenLibrary vide."}

    if not cle_ol.startswith("/"):
        cle_ol = "/" + cle_ol

    url = f"{BASE_WORKS}{cle_ol}.json"
    data, erreur = _get(url)

    if erreur:
        return {"succes": False, "erreur": erreur, "cle": cle_ol}

    description = data.get("description", "")
    if isinstance(description, dict):
        description = description.get("value", "")

    return {
        "succes": True,
        "titre": data.get("title", ""),
        "description": description[:1500] if description else None,
        "sujets": data.get("subjects", [])[:10],
        "date_creation": data.get("created", {}).get("value", "")[:10] if data.get("created") else None,
        "url": f"https://openlibrary.org{cle_ol}",
        "cle": cle_ol,
    }


# ── Recherche multiple (parallele) ──────────────────────────────

def chercher_multiple(
    requetes: list,
    type_recherche: str = "titre",
    langue: str | None = None,
    max_workers: int = 4,
) -> list:
    """
    Recherche plusieurs sujets en parallele via ThreadPoolExecutor.
    L'essaim butine — chaque agent son livre.
    """
    resultats = [None] * len(requetes)

    with ThreadPoolExecutor(max_workers=min(max_workers, len(requetes))) as pool:
        futures = {
            pool.submit(chercher_livres, req, type_recherche, 3, langue): i
            for i, req in enumerate(requetes)
        }
        for future in as_completed(futures):
            idx = futures[future]
            resultats[idx] = future.result()

    return resultats


# ── Formatage pour depot en memoire collective ───────────────────

def formater_pour_agent(resultat: dict) -> str:
    """
    Formate les resultats en texte pret pour depot
    dans la memoire collective HIVE.
    """
    if not resultat.get("succes"):
        return f"[BIBLIOTHEQUE] Aucun resultat : {resultat.get('erreur', 'inconnu')}"

    lignes = [f"[BIBLIOTHEQUE — '{resultat['requete']}' — {resultat['total']} resultats]"]
    for i, l in enumerate(resultat.get("livres", []), 1):
        auteurs = ", ".join(l["auteurs"]) if l["auteurs"] else "Auteur inconnu"
        annee = f" ({l['annee']})" if l["annee"] else ""
        lignes.append(f"  {i}. {l['titre']}{annee} — {auteurs}")
        if l["url"]:
            lignes.append(f"     > {l['url']}")
    return "\n".join(lignes)


# ── Interface standard SkillsManager ─────────────────────────────

def executer(params: dict) -> dict:
    """
    Point d'entree standard pour le SkillsManager HIVE.AI.

    params:
        requete         (str)  : Terme de recherche — obligatoire
        type_recherche  (str)  : 'titre'|'auteur'|'sujet'|'libre' — defaut 'titre'
        limite          (int)  : Nb resultats — defaut 5
        langue          (str)  : Code langue 2 ou 3 lettres — optionnel
        detail          (str)  : Cle OL pour detail d'un livre — optionnel
        format_agent    (bool) : Retourner texte formate — defaut False
    """
    if params.get("detail"):
        return detail_livre(params["detail"])

    resultat = chercher_livres(
        requete=params.get("requete", ""),
        type_recherche=params.get("type_recherche", "titre"),
        limite=params.get("limite", 5),
        langue=params.get("langue"),
    )

    if params.get("format_agent", False):
        resultat["texte"] = formater_pour_agent(resultat)

    return resultat


# ── Test ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("HIVE.AI — reine:bibliotheque — Test OpenLibrary")
    print("=" * 60)

    tests = [
        {"requete": "Ubuntu philosophy", "type_recherche": "sujet"},
        {"requete": "Amadou Hampate Ba", "type_recherche": "auteur"},
        {"requete": "Intelligence artificielle", "type_recherche": "titre", "limite": 3},
        {"requete": "Rwanda", "type_recherche": "libre", "langue": "fr"},
        {"requete": "", "type_recherche": "titre"},
        {"requete": "Python", "type_recherche": "titre", "langue": "xx"},
    ]

    for t in tests:
        print(f"\n  [{t['type_recherche']}] '{t['requete']}'" + (f" ({t['langue']})" if t.get("langue") else ""))
        r = executer({**t, "format_agent": True})
        if r["succes"]:
            print(f"  OK  {r['total']} livres trouves")
            for l in r["livres"][:2]:
                auteurs = ", ".join(l["auteurs"]) if l["auteurs"] else "?"
                print(f"      {l['titre']} — {auteurs}")
        else:
            print(f"  ERR {r['erreur']}")

    # Test parallele
    print(f"\n  --- Test parallele ---")
    sujets = ["Ubuntu", "Abeille", "Rwanda"]
    resultats = chercher_multiple(sujets, "titre", "fr")
    for r in resultats:
        if r["succes"]:
            print(f"  OK  '{r['requete']}' — {r['total']} resultats")
        else:
            print(f"  ERR '{r['requete']}' — {r['erreur']}")

    # Test detail
    print(f"\n  --- Test detail ---")
    d = detail_livre("/works/OL45804W")
    if d["succes"]:
        print(f"  OK  {d['titre']}")
        if d["description"]:
            print(f"      {d['description'][:120]}...")
    else:
        print(f"  ERR {d['erreur']}")

    print("\n" + "=" * 60)
    print(f"  reine:bibliotheque v{SKILL_INFO['version']}")
    print("  La bibliotheque est ouverte. Alexandrie vit.")
    print("=" * 60)
