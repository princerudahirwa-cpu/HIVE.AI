# ═══════════════════════════════════════════════════════════════
# HIVE.AI — Skill : reine:consulter
# Bibliotheque d'Alexandrie — Acces Wikipedia en 63 langues
#
# "Le savoir ne vit pas dans la ruche. Il vit dans le monde.
#  La Reine ne possede pas la connaissance — elle la consulte
#  avec humilite, la distille, et la partage comme nectar."
#
# Philosophie :
#   - Consulter, pas posseder. Le savoir est bien commun.
#   - Chaque requete est un vol de butinage — on revient
#     avec du pollen, jamais les mains vides d'intention.
#   - Honnetete linguistique : si une langue n'existe pas
#     sur Wikipedia, on le dit. Pas de substitution silencieuse.
#
# Swarmly SAS — 2026
# ═══════════════════════════════════════════════════════════════

import wikipediaapi
from concurrent.futures import ThreadPoolExecutor, as_completed

# ── Constantes ──────────────────────────────────────────────────

USER_AGENT = "HIVE.AI/1.0 (https://hive-ai.tech; prince@hive-ai.tech)"
TIMEOUT_SECONDS = 10

# ── Mapping langues HIVE → codes Wikipedia ──────────────────────
# 63 langues verifiees — chaque code pointe vers une Wikipedia existante.
# Regle : pas de mapping fictif. Si la Wikipedia n'existe pas, la langue est omise.

LANGUES = {
    # Europe occidentale
    "fr": "fr", "en": "en", "es": "es", "pt": "pt", "de": "de",
    "it": "it", "nl": "nl", "ca": "ca", "eu": "eu", "gl": "gl",
    # Europe du Nord
    "sv": "sv", "no": "no", "da": "da", "fi": "fi",
    # Europe centrale & orientale
    "pl": "pl", "cs": "cs", "sk": "sk", "hu": "hu", "ro": "ro",
    "hr": "hr", "sr": "sr", "bg": "bg", "sl": "sl", "bs": "bs",
    "sq": "sq", "mk": "mk", "lt": "lt", "lv": "lv", "et": "et",
    "uk": "uk", "el": "el",
    # Russie & Caucase
    "ru": "ru",
    # Moyen-Orient
    "ar": "ar", "fa": "fa", "he": "he", "tr": "tr",
    # Asie du Sud
    "hi": "hi", "bn": "bn", "ta": "ta", "te": "te", "ml": "ml",
    # Asie de l'Est & du Sud-Est
    "zh": "zh", "ja": "ja", "ko": "ko", "vi": "vi", "th": "th",
    "id": "id", "ms": "ms",
    # Afrique
    "sw": "sw", "rn": "rn", "lg": "lg", "yo": "yo", "ha": "ha",
    "am": "am", "so": "so", "mg": "mg", "sn": "sn", "xh": "xh",
    "zu": "zu", "af": "af", "rw": "rw", "wo": "wo",
}

SKILL_INFO = {
    "nom": "reine:consulter",
    "domaine": "VI - POLLINISATION",
    "categorie": "savoir",
    "description": (
        "Consulte Wikipedia en temps reel dans 63 langues. "
        "La ruche accede au savoir universel sans le posseder."
    ),
    "version": "1.0.0",
    "auteur": "HIVE.AI — Swarmly SAS",
}


# ── Instanciation Wikipedia (une par langue, reutilisee) ────────

_wiki_instances = {}


def _get_wiki(code):
    """Retourne une instance Wikipedia pour le code langue donne."""
    if code not in _wiki_instances:
        _wiki_instances[code] = wikipediaapi.Wikipedia(
            language=code,
            user_agent=USER_AGENT,
            timeout=TIMEOUT_SECONDS,
        )
    return _wiki_instances[code]


# ── Fonction principale ─────────────────────────────────────────

def consulter(
    requete: str,
    langue: str = "fr",
    longueur_max: int = 1500,
    sections: bool = False,
    fallback: bool = True,
) -> dict:
    """
    Consulte Wikipedia et retourne un resume structure.

    Args:
        requete      : Terme ou sujet a rechercher
        langue       : Code langue HIVE (defaut: 'fr')
        longueur_max : Longueur max du resume en caracteres
        sections     : Inclure les titres de sections (defaut: False)
        fallback     : Tenter l'anglais si absent dans la langue demandee (defaut: True)

    Returns:
        dict avec cles: succes, titre, resume, url, langue, sections
    """
    requete = requete.strip() if isinstance(requete, str) else ""
    if not requete:
        return {"succes": False, "erreur": "Requete vide.", "requete": ""}

    code = LANGUES.get(langue)
    if not code:
        return {
            "succes": False,
            "erreur": f"Langue '{langue}' non supportee. {len(LANGUES)} langues disponibles.",
            "requete": requete,
            "langues_disponibles": sorted(LANGUES.keys()),
        }

    try:
        wiki = _get_wiki(code)
        page = wiki.page(requete)

        # Fallback anglais si la page n'existe pas
        if not page.exists() and fallback and code != "en":
            wiki_en = _get_wiki("en")
            page = wiki_en.page(requete)
            if not page.exists():
                return {
                    "succes": False,
                    "erreur": f"Aucune page trouvee pour '{requete}' en {langue} ni en anglais.",
                    "requete": requete,
                }
            code = "en"
        elif not page.exists():
            return {
                "succes": False,
                "erreur": f"Aucune page trouvee pour '{requete}' en {langue}.",
                "requete": requete,
            }

        # Coupure propre au dernier point
        resume = page.summary[:longueur_max]
        if len(page.summary) > longueur_max:
            dernier_point = resume.rfind(".")
            if dernier_point > longueur_max // 2:
                resume = resume[:dernier_point + 1]

        resultat = {
            "succes": True,
            "titre": page.title,
            "resume": resume,
            "url": page.fullurl,
            "langue": code,
            "langue_demandee": langue,
            "longueur": len(resume),
            "requete": requete,
        }

        if sections:
            resultat["sections"] = [s.title for s in page.sections if s.title]

        return resultat

    except (ConnectionError, TimeoutError, OSError) as e:
        return {
            "succes": False,
            "erreur": f"Erreur reseau : {e}",
            "requete": requete,
        }
    except wikipediaapi.WikipediaException as e:
        return {
            "succes": False,
            "erreur": f"Erreur Wikipedia : {e}",
            "requete": requete,
        }


# ── Recherche multiple (vraiment parallele) ──────────────────────

def consulter_multiple(requetes: list, langue: str = "fr", max_workers: int = 4) -> list:
    """
    Consulte plusieurs sujets en parallele via ThreadPoolExecutor.
    Chaque agent butine son propre sujet — l'essaim travaille ensemble.
    """
    resultats = [None] * len(requetes)

    with ThreadPoolExecutor(max_workers=min(max_workers, len(requetes))) as pool:
        futures = {
            pool.submit(consulter, req, langue): i
            for i, req in enumerate(requetes)
        }
        for future in as_completed(futures):
            idx = futures[future]
            resultats[idx] = future.result()

    return resultats


# ── Formatage pour depot en memoire collective ───────────────────

def formater_pour_agent(resultat: dict) -> str:
    """
    Formate le resultat Wikipedia en texte propre
    pret a etre depose comme nectar dans la memoire collective.
    """
    if not resultat.get("succes"):
        return f"[CONSULTER] Aucun resultat : {resultat.get('erreur', 'inconnu')}"

    langue_info = resultat["langue"]
    if resultat.get("langue_demandee") and resultat["langue_demandee"] != resultat["langue"]:
        langue_info = f"{resultat['langue']} (demande: {resultat['langue_demandee']})"

    return (
        f"[SAVOIR — {resultat['titre']}] ({langue_info})\n"
        f"{resultat['resume']}\n"
        f"Source : {resultat['url']}"
    )


# ── Interface standard SkillsManager ─────────────────────────────

def executer(params: dict) -> dict:
    """
    Point d'entree standard pour le SkillsManager HIVE.AI.

    params:
        requete      (str)  : Sujet a rechercher — obligatoire
        langue       (str)  : Code langue — defaut 'fr'
        longueur_max (int)  : Max caracteres — defaut 1500
        sections     (bool) : Inclure sections — defaut False
        fallback     (bool) : Repli anglais — defaut True
        format_agent (bool) : Retourner texte formate — defaut False
    """
    resultat = consulter(
        requete=params.get("requete", ""),
        langue=params.get("langue", "fr"),
        longueur_max=params.get("longueur_max", 1500),
        sections=params.get("sections", False),
        fallback=params.get("fallback", True),
    )

    if params.get("format_agent", False):
        resultat["texte"] = formater_pour_agent(resultat)

    return resultat


# ── Test ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("HIVE.AI — reine:consulter — Test Wikipedia")
    print("=" * 60)

    tests = [
        {"requete": "Intelligence artificielle", "langue": "fr"},
        {"requete": "Ubuntu philosophy", "langue": "en"},
        {"requete": "Abeille", "langue": "fr", "sections": True},
        {"requete": "Test inexistant xyz123", "langue": "fr"},
        {"requete": "", "langue": "fr"},
        {"requete": "Rwanda", "langue": "rw"},
    ]

    for t in tests:
        print(f"\n  Recherche : '{t['requete']}' [{t.get('langue', 'fr')}]")
        r = executer({**t, "format_agent": True})
        if r["succes"]:
            print(f"  OK  {r['titre']} — {r['longueur']} car. ({r['langue']})")
            print(f"      {r['resume'][:150]}...")
            if "sections" in r:
                print(f"      Sections : {r['sections'][:5]}")
        else:
            print(f"  ERR {r['erreur']}")

    # Test parallele
    print(f"\n  --- Test parallele ---")
    sujets = ["Python", "Linux", "Rwanda"]
    resultats = consulter_multiple(sujets, "fr")
    for r in resultats:
        status = f"OK  {r['titre']}" if r["succes"] else f"ERR {r['erreur']}"
        print(f"  {status}")

    print("\n" + "=" * 60)
    print(f"  {len(LANGUES)} langues | reine:consulter v{SKILL_INFO['version']}")
    print("  Nectar pret pour la memoire collective.")
    print("=" * 60)
