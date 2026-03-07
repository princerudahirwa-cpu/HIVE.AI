# ═══════════════════════════════════════════════════════════════
# HIVE.AI — Skill : reine:science
# Bibliotheque d'Alexandrie — arXiv
# Recherche scientifique mondiale. Physique, IA, Maths, Bio.
#
# "La science est le miel le plus pur de l'espece humaine."
#
# Philosophie :
#   - Le savoir scientifique est bien commun — arXiv le prouve.
#   - Chaque article est une alveole de decouverte preservee.
#   - L'essaim ne publie pas — il butine, distille, partage.
#
# Swarmly SAS — 2026
# ═══════════════════════════════════════════════════════════════

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed

# ── Constantes ──────────────────────────────────────────────────

USER_AGENT = "HIVE.AI/1.0 (https://hive-ai.tech; prince@hive-ai.tech)"
BASE_URL = "https://export.arxiv.org/api/query"
TIMEOUT_SECONDS = 10
MAX_RESULTATS = 10

SKILL_INFO = {
    "nom": "reine:science",
    "domaine": "VI - POLLINISATION",
    "categorie": "savoir",
    "description": (
        "Interroge arXiv — millions d'articles scientifiques en acces libre. "
        "IA, physique, mathematiques, biologie, economie. Zero cle API."
    ),
    "version": "1.0.0",
    "auteur": "HIVE.AI — Swarmly SAS",
    "source": "https://arxiv.org/help/api",
}

# ── Categories arXiv ────────────────────────────────────────────

CATEGORIES = {
    "ia": "cs.AI",
    "ml": "cs.LG",
    "nlp": "cs.CL",
    "vision": "cs.CV",
    "robotique": "cs.RO",
    "physique": "physics",
    "maths": "math",
    "biologie": "q-bio",
    "economie": "econ",
    "statistiques": "stat",
    "finance": "q-fin",
    "informatique": "cs",
}

# ── Namespaces XML ──────────────────────────────────────────────

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
    "opensearch": "http://a9.com/-/spec/opensearch/1.1/",
}


# ── Appel HTTP ──────────────────────────────────────────────────

def _get_xml(url: str) -> tuple[ET.Element | None, str | None]:
    """
    Appel HTTP GET vers arXiv, retourne du XML parse.
    Retourne (element, None) ou (None, message_erreur).
    """
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


# ── Recherche d'articles ────────────────────────────────────────

def chercher_articles(
    requete: str,
    categorie: str | None = None,
    limite: int = 5,
    trier_par: str = "relevance",
) -> dict:
    """
    Recherche des articles scientifiques sur arXiv.

    Args:
        requete    : Termes de recherche
        categorie  : 'ia'|'ml'|'nlp'|'physique'|'maths'|'biologie'... (optionnel)
        limite     : Nombre de resultats (max MAX_RESULTATS)
        trier_par  : 'relevance' | 'date'
    """
    requete = requete.strip() if isinstance(requete, str) else ""
    if not requete:
        return {"succes": False, "erreur": "Requete vide.", "requete": ""}

    # Construction de la query arXiv — PAS de pre-encodage,
    # urlencode s'en charge via le parametre search_query.
    query = f"all:{requete}"
    if categorie:
        cat_code = CATEGORIES.get(categorie, categorie)
        query += f" AND cat:{cat_code}"

    sort_map = {"relevance": "relevance", "date": "submittedDate"}
    sort_by = sort_map.get(trier_par, "relevance")

    url = (
        f"{BASE_URL}?"
        f"search_query={urllib.parse.quote(query, safe=':+')}"
        f"&start=0"
        f"&max_results={min(limite, MAX_RESULTATS)}"
        f"&sortBy={sort_by}"
        f"&sortOrder=descending"
    )

    root, erreur = _get_xml(url)
    if erreur:
        return {"succes": False, "erreur": erreur, "requete": requete}

    total_el = root.find("opensearch:totalResults", NS)
    total = int(total_el.text) if total_el is not None else 0

    articles = []
    for entry in root.findall("atom:entry", NS):
        titre = entry.find("atom:title", NS)
        resume = entry.find("atom:summary", NS)
        publie = entry.find("atom:published", NS)
        lien = entry.find("atom:id", NS)

        auteurs = [
            a.find("atom:name", NS).text
            for a in entry.findall("atom:author", NS)
            if a.find("atom:name", NS) is not None
        ][:4]

        categories_art = [
            c.get("term", "")
            for c in entry.findall("atom:category", NS)
        ][:4]

        resume_txt = resume.text.strip().replace("\n", " ") if resume is not None else ""
        resume_court = resume_txt[:600] + "..." if len(resume_txt) > 600 else resume_txt

        articles.append({
            "titre": titre.text.strip().replace("\n", " ") if titre is not None else "",
            "auteurs": auteurs,
            "resume": resume_court,
            "date": publie.text[:10] if publie is not None else None,
            "categories": categories_art,
            "url": lien.text.strip() if lien is not None else None,
        })

    return {
        "succes": True,
        "total": total,
        "articles": articles,
        "requete": requete,
        "categorie": categorie,
    }


# ── Recherche multiple (parallele) ──────────────────────────────

def chercher_multiple(
    requetes: list,
    categorie: str | None = None,
    max_workers: int = 3,
) -> list:
    """
    Recherche plusieurs sujets en parallele.
    Note : arXiv limite a 3 req/s — max_workers=3 par defaut.
    """
    resultats = [None] * len(requetes)

    with ThreadPoolExecutor(max_workers=min(max_workers, len(requetes))) as pool:
        futures = {
            pool.submit(chercher_articles, req, categorie, 3): i
            for i, req in enumerate(requetes)
        }
        for future in as_completed(futures):
            idx = futures[future]
            resultats[idx] = future.result()

    return resultats


# ── Formatage pour depot en memoire collective ───────────────────

def formater_pour_agent(resultat: dict) -> str:
    """Formate les resultats en texte pret pour la memoire HIVE."""
    if not resultat.get("succes"):
        return f"[SCIENCE] Aucun resultat : {resultat.get('erreur', 'inconnu')}"

    lignes = [f"[SCIENCE — '{resultat['requete']}' — {resultat['total']} articles]"]
    for i, a in enumerate(resultat.get("articles", []), 1):
        auteurs = ", ".join(a["auteurs"]) if a["auteurs"] else "Auteurs inconnus"
        date = f" ({a['date']})" if a["date"] else ""
        lignes.append(f"\n  {i}. {a['titre']}{date}")
        lignes.append(f"     {auteurs}")
        if a["resume"]:
            lignes.append(f"     {a['resume'][:200]}...")
        if a["url"]:
            lignes.append(f"     > {a['url']}")
    return "\n".join(lignes)


# ── Interface standard SkillsManager ─────────────────────────────

def executer(params: dict) -> dict:
    """
    Point d'entree standard SkillsManager HIVE.AI.

    params:
        requete      (str)  : Termes de recherche — obligatoire
        categorie    (str)  : Domaine scientifique — optionnel
        limite       (int)  : Nb resultats — defaut 5
        trier_par    (str)  : 'relevance'|'date' — defaut 'relevance'
        format_agent (bool) : Texte formate — defaut False
    """
    resultat = chercher_articles(
        requete=params.get("requete", ""),
        categorie=params.get("categorie"),
        limite=params.get("limite", 5),
        trier_par=params.get("trier_par", "relevance"),
    )

    if params.get("format_agent", False):
        resultat["texte"] = formater_pour_agent(resultat)

    return resultat


# ── Test ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("HIVE.AI — reine:science — Test arXiv")
    print("=" * 60)

    tests = [
        {"requete": "multi-agent AI swarm", "categorie": "ia", "limite": 3},
        {"requete": "ephemeral computing", "categorie": "ml", "limite": 3},
        {"requete": "biomimicry optimization", "limite": 3},
        {"requete": "", "limite": 1},
    ]

    for t in tests:
        cat = t.get("categorie", "libre")
        print(f"\n  [{cat}] '{t['requete']}'")
        r = executer({**t, "format_agent": True})
        if r["succes"]:
            print(f"  OK  {r['total']} articles")
            for a in r["articles"][:2]:
                print(f"      {a['titre'][:80]}")
        else:
            print(f"  ERR {r['erreur']}")

    # Test parallele
    print(f"\n  --- Test parallele ---")
    sujets = ["quantum computing", "swarm intelligence", "neural architecture"]
    resultats = chercher_multiple(sujets, "ia")
    for r in resultats:
        if r["succes"]:
            print(f"  OK  '{r['requete']}' — {r['total']} articles")
        else:
            print(f"  ERR '{r['requete']}' — {r['erreur']}")

    print("\n" + "=" * 60)
    print(f"  reine:science v{SKILL_INFO['version']}")
    print("  La science est dans la ruche.")
    print("=" * 60)
