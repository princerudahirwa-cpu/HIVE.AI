# ═══════════════════════════════════════════════════════════════
# HIVE.AI — Skill : reine:medecine
# Bibliotheque d'Alexandrie — PubMed / NCBI
# Sciences de la vie, medecine, sante publique mondiale.
#
# "Guerir est le premier devoir de l'intelligence."
#
# Philosophie :
#   - La sante est le nectar le plus precieux.
#   - PubMed est la ruche de la connaissance medicale —
#     35 millions d'alveoles de savoir, libres d'acces.
#   - On ne prescrit pas. On eclaire. Le medecin decide.
#
# Swarmly SAS — 2026
# ═══════════════════════════════════════════════════════════════

import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed

# ── Constantes ──────────────────────────────────────────────────

USER_AGENT = "HIVE.AI/1.0 (https://hive-ai.tech; prince@hive-ai.tech)"
BASE_SEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
BASE_FETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
BASE_SUMMARY = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
TIMEOUT_SECONDS = 10
MAX_RESULTATS = 10

SKILL_INFO = {
    "nom": "reine:medecine",
    "domaine": "VI - POLLINISATION",
    "categorie": "savoir",
    "description": (
        "Interroge PubMed (NCBI) — 35M+ articles medicaux et biologiques. "
        "Zero cle API. Maladies, traitements, recherche clinique, sante publique."
    ),
    "version": "1.0.0",
    "auteur": "HIVE.AI — Swarmly SAS",
    "source": "https://www.ncbi.nlm.nih.gov/books/NBK25501/",
}


# ── Appels HTTP ─────────────────────────────────────────────────

def _get_json(url: str) -> tuple[dict | None, str | None]:
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


# ── Recherche d'articles ────────────────────────────────────────

def chercher_articles(
    requete: str,
    limite: int = 5,
    tri_date: bool = False,
    annee_min: int | None = None,
) -> dict:
    """
    Recherche des articles medicaux sur PubMed.

    Args:
        requete    : Termes de recherche (anglais recommande)
        limite     : Nombre de resultats (max MAX_RESULTATS)
        tri_date   : Trier par date de publication (defaut: pertinence)
        annee_min  : Filtrer articles depuis cette annee (ex: 2020)
    """
    requete = requete.strip() if isinstance(requete, str) else ""
    if not requete:
        return {"succes": False, "erreur": "Requete vide.", "requete": ""}

    query = requete
    if annee_min:
        query += f" AND {annee_min}[pdat]"

    sort = "pub+date" if tri_date else "relevance"

    params = urllib.parse.urlencode({
        "db": "pubmed",
        "term": query,
        "retmax": min(limite, MAX_RESULTATS),
        "retmode": "json",
        "sort": sort,
    })
    url = f"{BASE_SEARCH}?{params}"

    data, erreur = _get_json(url)
    if erreur:
        return {"succes": False, "erreur": erreur, "requete": requete}

    result = data.get("esearchresult", {})
    ids = result.get("idlist", [])
    total = int(result.get("count", 0))

    if not ids:
        return {
            "succes": True,
            "total": 0,
            "articles": [],
            "requete": requete,
        }

    articles, err = _fetch_summaries(ids)
    if err:
        return {"succes": False, "erreur": err, "requete": requete}

    return {
        "succes": True,
        "total": total,
        "articles": articles,
        "requete": requete,
    }


def _fetch_summaries(ids: list) -> tuple[list, str | None]:
    """Recupere les metadonnees des articles par leurs IDs PubMed."""
    params = urllib.parse.urlencode({
        "db": "pubmed",
        "id": ",".join(ids),
        "retmode": "json",
    })
    url = f"{BASE_SUMMARY}?{params}"
    data, erreur = _get_json(url)

    if erreur:
        return [], erreur

    articles = []
    uids = data.get("result", {}).get("uids", [])

    for uid in uids:
        doc = data.get("result", {}).get(uid, {})
        if not doc:
            continue

        auteurs = [
            a.get("name", "")
            for a in doc.get("authors", [])[:4]
        ]

        titre = doc.get("title", "").rstrip(".")
        journal = doc.get("fulljournalname", doc.get("source", ""))
        date = doc.get("pubdate", "")[:7]

        articles.append({
            "pmid": uid,
            "titre": titre,
            "auteurs": auteurs,
            "journal": journal,
            "date": date,
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{uid}/",
        })

    return articles, None


# ── Detail d'un article ─────────────────────────────────────────

def detail_article(pmid: str) -> dict:
    """
    Recupere le resume complet (abstract) d'un article PubMed.
    Gere les abstracts structures (OBJECTIVE, METHODS, RESULTS...).

    Args:
        pmid : Identifiant PubMed (ex: '37012345')
    """
    pmid = str(pmid).strip()
    if not pmid:
        return {"succes": False, "erreur": "PMID vide."}

    params = urllib.parse.urlencode({
        "db": "pubmed",
        "id": pmid,
        "retmode": "xml",
        "rettype": "abstract",
    })
    url = f"{BASE_FETCH}?{params}"
    root, erreur = _get_xml(url)

    if erreur:
        return {"succes": False, "erreur": erreur, "pmid": pmid}

    # Reconstruction de l'abstract complet (structures ou non)
    abstract_parts = root.findall(".//AbstractText")
    if abstract_parts:
        sections = []
        for part in abstract_parts:
            label = part.get("Label", "")
            text = part.text or ""
            if label:
                sections.append(f"{label}: {text}")
            else:
                sections.append(text)
        abstract = "\n".join(sections)
    else:
        abstract = "Resume non disponible."

    titre_el = root.find(".//ArticleTitle")
    titre = titre_el.text if titre_el is not None else ""

    return {
        "succes": True,
        "pmid": pmid,
        "titre": titre,
        "abstract": abstract[:2000] if abstract else None,
        "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
    }


# ── Recherche multiple (parallele) ──────────────────────────────

def chercher_multiple(
    requetes: list,
    annee_min: int | None = None,
    max_workers: int = 3,
) -> list:
    """
    Recherche plusieurs sujets en parallele.
    Note : NCBI limite a 3 req/s sans cle API — max_workers=3 par defaut.
    """
    resultats = [None] * len(requetes)

    with ThreadPoolExecutor(max_workers=min(max_workers, len(requetes))) as pool:
        futures = {
            pool.submit(chercher_articles, req, 3, False, annee_min): i
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
        return f"[MEDECINE] Aucun resultat : {resultat.get('erreur', 'inconnu')}"

    lignes = [f"[MEDECINE — '{resultat['requete']}' — {resultat['total']} articles PubMed]"]
    for i, a in enumerate(resultat.get("articles", []), 1):
        auteurs = ", ".join(a["auteurs"]) if a["auteurs"] else "Auteurs inconnus"
        date = f" ({a['date']})" if a["date"] else ""
        journal = f" · {a['journal']}" if a["journal"] else ""
        lignes.append(f"\n  {i}. {a['titre']}{date}{journal}")
        lignes.append(f"     {auteurs}")
        lignes.append(f"     > {a['url']}")
    return "\n".join(lignes)


# ── Interface standard SkillsManager ─────────────────────────────

def executer(params: dict) -> dict:
    """
    Point d'entree standard SkillsManager HIVE.AI.

    params:
        requete      (str)  : Termes de recherche — obligatoire
        limite       (int)  : Nb resultats — defaut 5
        tri_date     (bool) : Trier par date — defaut False
        annee_min    (int)  : Annee minimum — optionnel
        detail       (str)  : PMID pour abstract complet — optionnel
        format_agent (bool) : Texte formate — defaut False
    """
    if params.get("detail"):
        return detail_article(str(params["detail"]))

    resultat = chercher_articles(
        requete=params.get("requete", ""),
        limite=params.get("limite", 5),
        tri_date=params.get("tri_date", False),
        annee_min=params.get("annee_min"),
    )

    if params.get("format_agent", False):
        resultat["texte"] = formater_pour_agent(resultat)

    return resultat


# ── Test ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("HIVE.AI — reine:medecine — Test PubMed")
    print("=" * 60)

    tests = [
        {"requete": "artificial intelligence diagnostics", "limite": 3},
        {"requete": "malaria Africa treatment", "limite": 3, "annee_min": 2022},
        {"requete": "mental health digital therapy", "limite": 3, "tri_date": True},
        {"requete": ""},
    ]

    for t in tests:
        print(f"\n  '{t.get('requete', '')}'")
        r = executer({**t, "format_agent": True})
        if r["succes"]:
            print(f"  OK  {r['total']} articles")
            for a in r["articles"][:2]:
                print(f"      {a['titre'][:80]}")
        else:
            print(f"  ERR {r['erreur']}")

    # Test detail (abstract structure)
    print(f"\n  --- Test detail ---")
    # Recherche un PMID reel pour tester
    r = chercher_articles("CRISPR gene therapy", limite=1)
    if r["succes"] and r["articles"]:
        pmid = r["articles"][0]["pmid"]
        d = detail_article(pmid)
        if d["succes"]:
            print(f"  OK  {d['titre']}")
            print(f"      Abstract: {d['abstract'][:200]}...")
        else:
            print(f"  ERR {d['erreur']}")

    # Test parallele
    print(f"\n  --- Test parallele ---")
    sujets = ["diabetes prevention", "tuberculosis vaccine", "COVID long term"]
    resultats = chercher_multiple(sujets, annee_min=2023)
    for r in resultats:
        if r["succes"]:
            print(f"  OK  '{r['requete']}' — {r['total']} articles")
        else:
            print(f"  ERR '{r['requete']}' — {r['erreur']}")

    print("\n" + "=" * 60)
    print(f"  reine:medecine v{SKILL_INFO['version']}")
    print("  La medecine est dans la ruche.")
    print("=" * 60)
