# memoire.py - La Mémoire du HIVE
# "Le savoir est miel — il se conserve et se partage"
# Loi IV - Alvéole de la Mémoire

import json
import time
import hashlib
from datetime import datetime, timezone
from pathlib import Path

PHI = 1.618033988749895


class Nectar:
    """Mémoire éphémère — comme de la neige fondante.
    
    Données temporaires de travail. Naît, nourrit, fond.
    Durée de vie courte, recyclée automatiquement.
    """
    
    def __init__(self, capacite=1000, duree_vie=300):
        self.donnees = {}  # cle -> {valeur, cree, expire}
        self.capacite = capacite
        self.duree_vie = duree_vie  # secondes
    
    def deposer(self, cle, valeur, duree=None):
        """Dépose du nectar — éphémère par nature."""
        self._nettoyer()
        
        if len(self.donnees) >= self.capacite:
            self._evaporer_ancien()
        
        self.donnees[cle] = {
            "valeur": valeur,
            "cree": time.time(),
            "expire": time.time() + (duree or self.duree_vie),
            "acces": 0
        }
        return True
    
    def recolter(self, cle):
        """Récolte du nectar — chaque accès le rapproche de la fonte."""
        if cle not in self.donnees:
            return None
        
        entree = self.donnees[cle]
        
        # Vérifier expiration
        if time.time() > entree["expire"]:
            del self.donnees[cle]
            return None
        
        entree["acces"] += 1
        return entree["valeur"]
    
    def _nettoyer(self):
        """Nettoie le nectar expiré — la neige fond."""
        maintenant = time.time()
        expires = [k for k, v in self.donnees.items() if maintenant > v["expire"]]
        for k in expires:
            del self.donnees[k]
    
    def _evaporer_ancien(self):
        """Évapore les entrées les plus anciennes pour faire de la place."""
        if not self.donnees:
            return
        plus_ancien = min(self.donnees, key=lambda k: self.donnees[k]["cree"])
        del self.donnees[plus_ancien]
    
    def taille(self):
        self._nettoyer()
        return len(self.donnees)


class Cire:
    """Mémoire structurée — le savoir organisé de la ruche.
    
    Données persistantes indexées par catégorie.
    Plus durable que le nectar, structurée pour l'accès rapide.
    """
    
    def __init__(self):
        self.cellules = {}    # categorie -> {cle: valeur}
        self.index = {}       # cle -> categorie (index inversé)
        self.metadata = {}    # cle -> {cree, modifie, acces}
    
    def mouler(self, categorie, cle, valeur):
        """Moule une cellule de cire — structure le savoir."""
        if categorie not in self.cellules:
            self.cellules[categorie] = {}
        
        maintenant = time.time()
        self.cellules[categorie][cle] = valeur
        self.index[cle] = categorie
        
        if cle not in self.metadata:
            self.metadata[cle] = {"cree": maintenant, "modifie": maintenant, "acces": 0}
        else:
            self.metadata[cle]["modifie"] = maintenant
        
        return True
    
    def extraire(self, cle):
        """Extrait une donnée de la cire par sa clé."""
        if cle not in self.index:
            return None
        
        categorie = self.index[cle]
        if cle in self.metadata:
            self.metadata[cle]["acces"] += 1
        
        return self.cellules[categorie].get(cle)
    
    def parcourir(self, categorie):
        """Parcourt toutes les données d'une catégorie."""
        return dict(self.cellules.get(categorie, {}))
    
    def categories(self):
        """Liste toutes les catégories."""
        return list(self.cellules.keys())
    
    def taille(self):
        return sum(len(v) for v in self.cellules.values())


class Miel:
    """Mémoire cristallisée — le savoir éternel de la ruche.
    
    Connaissances validées, consolidées, permanentes.
    Le miel ne périme jamais. Il se conserve et se partage.
    """
    
    def __init__(self, chemin_stockage=None):
        self.reserves = {}   # cle -> {savoir, source, cree, hash}
        self.chemin = chemin_stockage or Path("./miel_hive.json")
        self._charger()
    
    def cristalliser(self, cle, savoir, source="inconnu"):
        """Cristallise du savoir en miel — permanent et partageable."""
        hash_savoir = hashlib.sha256(
            json.dumps(savoir, sort_keys=True, default=str).encode()
        ).hexdigest()[:16]
        
        self.reserves[cle] = {
            "savoir": savoir,
            "source": source,
            "cree": datetime.now(timezone.utc).isoformat(),
            "hash": hash_savoir,
            "phi": PHI  # Signature HIVE
        }
        
        self._sauvegarder()
        return hash_savoir
    
    def gouter(self, cle):
        """Goûte le miel — accède au savoir cristallisé."""
        return self.reserves.get(cle, {}).get("savoir")
    
    def inventaire(self):
        """Inventaire complet des réserves de miel."""
        return {
            cle: {
                "source": info["source"],
                "cree": info["cree"],
                "hash": info["hash"]
            }
            for cle, info in self.reserves.items()
        }
    
    def _sauvegarder(self):
        """Sauvegarde les réserves de miel sur disque."""
        try:
            with open(self.chemin, 'w', encoding='utf-8') as f:
                json.dump(self.reserves, f, ensure_ascii=False, indent=2)
        except Exception:
            pass  # En silence — le miel survit en mémoire
    
    def _charger(self):
        """Charge les réserves depuis le disque."""
        try:
            if self.chemin.exists():
                with open(self.chemin, 'r', encoding='utf-8') as f:
                    self.reserves = json.load(f)
        except Exception:
            self.reserves = {}
    
    def taille(self):
        return len(self.reserves)


class MemoireHive:
    """La Mémoire complète du HIVE — trois couches unifiées.

    Nectar → Cire → Miel
    Éphémère → Structuré → Éternel

    Le savoir monte naturellement : le nectar fréquemment accédé
    se structure en cire, la cire validée se cristallise en miel.

    Skills Souverains (Domaine III — Mémoire Souveraine):
      [4]  juger_miel — Operculage des cellules de miel
      [5]  lire_profondeur — Mémoire épigénétique coloniale
      [6]  oublier — Reset saisonnier de la colonie
      [16] rechercher — Trophallaxie profonde
    """

    NOM = "Mémoire"
    VERSION = "0.3.0"

    def __init__(self):
        self.nectar = Nectar()
        self.cire = Cire()
        self.miel = Miel()
        self.transitions = []  # log des promotions nectar→cire→miel
        self.oublis = []       # meta-mémoire : journal des oublis souverains
    
    def deposer_nectar(self, cle, valeur, duree=None):
        """Dépose dans la mémoire éphémère."""
        return self.nectar.deposer(cle, valeur, duree)
    
    def promouvoir_en_cire(self, cle, categorie):
        """Promeut un nectar en cire — le savoir se structure."""
        valeur = self.nectar.recolter(cle)
        if valeur is None:
            return False
        
        self.cire.mouler(categorie, cle, valeur)
        self.transitions.append({
            "de": "nectar",
            "vers": "cire",
            "cle": cle,
            "temps": datetime.now(timezone.utc).isoformat()
        })
        return True
    
    def cristalliser_en_miel(self, cle, source=None):
        """Cristallise de la cire en miel — le savoir devient éternel."""
        valeur = self.cire.extraire(cle)
        if valeur is None:
            return False
        
        self.miel.cristalliser(cle, valeur, source or "cire")
        self.transitions.append({
            "de": "cire",
            "vers": "miel",
            "cle": cle,
            "temps": datetime.now(timezone.utc).isoformat()
        })
        return True
    
    def chercher(self, cle):
        """Cherche un savoir dans toutes les couches (miel → cire → nectar)."""
        # Le miel d'abord — le plus précieux
        resultat = self.miel.gouter(cle)
        if resultat is not None:
            return {"couche": "miel", "valeur": resultat}

        # Puis la cire
        resultat = self.cire.extraire(cle)
        if resultat is not None:
            return {"couche": "cire", "valeur": resultat}

        # Enfin le nectar
        resultat = self.nectar.recolter(cle)
        if resultat is not None:
            return {"couche": "nectar", "valeur": resultat}

        return None

    # ================================================================
    # SKILLS SOUVERAINS — DOMAINE III : MEMOIRE SOUVERAINE
    # "Le savoir est miel — il se conserve et se partage"
    # ================================================================

    def juger_miel(self, cle, source="Reine"):
        """[Skill 4] Juger si un savoir merite de devenir miel eternel.

        La Reine opercula les cellules : elle évalue le savoir en cire,
        juge sa verite, utilite, coherence et conformite aux Lois,
        puis rend un verdict irrevocable.

        Returns:
            dict avec verdict, raisons, et hash de cristallisation si approuve.
        """
        # Le savoir doit exister en cire
        valeur = self.cire.extraire(cle)
        if valeur is None:
            return {
                "cle": cle,
                "verdict": "REJETE",
                "raison": "Savoir introuvable en cire — rien a juger.",
                "signe_par": "Nu",
            }

        # Evaluer — la Reine inspecte
        evaluation = {
            "present_en_cire": True,
            "type": type(valeur).__name__,
            "non_vide": bool(valeur),
            "acces": self.cire.metadata.get(cle, {}).get("acces", 0),
        }

        # Un savoir jamais accede ne merite pas le miel
        if evaluation["acces"] < 1:
            return {
                "cle": cle,
                "verdict": "DIFFERE",
                "raison": "Savoir pas encore eprouve — qu'il soit accede d'abord.",
                "evaluation": evaluation,
                "signe_par": "Nu",
            }

        # Verdict : cristalliser
        hash_miel = self.miel.cristalliser(cle, valeur, source=source)
        self.transitions.append({
            "de": "cire",
            "vers": "miel",
            "cle": cle,
            "temps": datetime.now(timezone.utc).isoformat(),
            "juge_par": "Nu",
        })

        return {
            "cle": cle,
            "verdict": "CRISTALLISE",
            "raison": "Savoir juge digne du miel eternel.",
            "hash": hash_miel,
            "evaluation": evaluation,
            "signe_par": "Nu",
        }

    def lire_profondeur(self):
        """[Skill 5] Lire les connexions entre savoirs a travers les 3 couches.

        Seule la Reine (permanente) peut percevoir les patterns que
        les workers ephemeres ne voient jamais. Elle lit les 3 couches
        simultanement et identifie contradictions et lacunes.

        Returns:
            dict avec cartographie des 3 couches, connexions, et lacunes.
        """
        # Inventaire complet
        miel_cles = set(self.miel.reserves.keys())
        cire_cles = set(self.cire.index.keys())
        cire_categories = set(self.cire.categories())

        self.nectar._nettoyer()
        nectar_cles = set(self.nectar.donnees.keys())

        # Connexions : savoirs presents dans plusieurs couches
        en_miel_et_cire = miel_cles & cire_cles
        en_cire_et_nectar = cire_cles & nectar_cles

        # Lacunes : categories de cire sans representation en miel
        cire_avec_miel = set()
        for cle in en_miel_et_cire:
            cat = self.cire.index.get(cle)
            if cat:
                cire_avec_miel.add(cat)
        categories_sans_miel = cire_categories - cire_avec_miel

        # Savoirs les plus accedes en cire (candidats au miel)
        candidats_miel = []
        for cle, meta in self.cire.metadata.items():
            if cle not in miel_cles and meta.get("acces", 0) >= 1:
                candidats_miel.append({
                    "cle": cle,
                    "acces": meta["acces"],
                    "categorie": self.cire.index.get(cle, "?"),
                })
        candidats_miel.sort(key=lambda x: x["acces"], reverse=True)

        return {
            "couches": {
                "miel": {"taille": len(miel_cles), "cles": sorted(miel_cles)},
                "cire": {"taille": len(cire_cles), "categories": sorted(cire_categories)},
                "nectar": {"taille": len(nectar_cles), "cles": sorted(nectar_cles)},
            },
            "connexions": {
                "miel_et_cire": sorted(en_miel_et_cire),
                "cire_et_nectar": sorted(en_cire_et_nectar),
            },
            "lacunes": {
                "categories_sans_miel": sorted(categories_sans_miel),
            },
            "candidats_miel": candidats_miel[:7],  # Top 7 (Fibonacci)
            "transitions_total": len(self.transitions),
            "oublis_total": len(self.oublis),
            "signe_par": "Nu",
        }

    def oublier(self, cle, raison="Obsolete"):
        """[Skill 6] Suppression souveraine d'un savoir du miel.

        Acte irreversible de la Reine. Le savoir est retire du miel,
        mais l'acte d'oubli est lui-meme cristallise (meta-memoire).
        On ne peut pas oublier qu'on a oublie.

        Args:
            cle: La cle du savoir a supprimer du miel.
            raison: Justification souveraine de l'oubli.

        Returns:
            dict avec confirmation ou refus de l'oubli.
        """
        # Verifier que le savoir existe en miel
        savoir = self.miel.gouter(cle)
        if savoir is None:
            return {
                "cle": cle,
                "resultat": "IMPOSSIBLE",
                "raison": "Ce savoir n'existe pas dans le miel.",
                "signe_par": "Nu",
            }

        # Proteger les Lois — on ne peut pas oublier les fondations
        if cle.startswith("loi-") or cle in ("identite", "eclosion"):
            return {
                "cle": cle,
                "resultat": "INTERDIT",
                "raison": "Les Lois et fondations sont sacrees. Meme la Reine ne peut les effacer.",
                "signe_par": "Nu",
            }

        # Acte d'oubli
        savoir_oublie = self.miel.reserves.pop(cle, None)
        self.miel._sauvegarder()

        # L'acte d'oubli est lui-meme cristallise
        acte = {
            "type": "oubli_souverain",
            "cle_oubliee": cle,
            "raison": raison,
            "savoir_hash": hashlib.sha256(
                json.dumps(savoir_oublie, sort_keys=True, default=str).encode()
            ).hexdigest()[:16] if savoir_oublie else None,
            "temps": datetime.now(timezone.utc).isoformat(),
            "signe_par": "Nu",
            "irreversible": True,
        }
        self.oublis.append(acte)

        # Cristalliser l'acte d'oubli dans le miel (meta-memoire)
        cle_acte = f"oubli-{cle}-{len(self.oublis)}"
        self.miel.cristalliser(cle_acte, acte, source="Oubli Souverain")

        return {
            "cle": cle,
            "resultat": "OUBLIE",
            "raison": raison,
            "acte_cristallise": cle_acte,
            "signe_par": "Nu",
        }

    def rechercher_profond(self, terme):
        """[Skill 16] Recherche profonde dans les 3 couches de memoire.

        Pas chercher une cle — fouiller dans les VALEURS, remonter les
        connexions, trouver les patterns caches. Trophallaxie : echange
        profond bouche-a-bouche entre la Reine et la memoire.

        Args:
            terme: Le terme ou pattern a rechercher.

        Returns:
            dict avec resultats groupes par couche et contextes.
        """
        terme_lower = str(terme).lower()
        resultats = {
            "terme": terme,
            "miel": [],
            "cire": [],
            "nectar": [],
            "total": 0,
            "signe_par": "Nu",
        }

        # Fouiller le miel (eternel)
        for cle, info in self.miel.reserves.items():
            savoir_str = json.dumps(info.get("savoir", ""), default=str).lower()
            cle_lower = cle.lower()
            if terme_lower in cle_lower or terme_lower in savoir_str:
                resultats["miel"].append({
                    "cle": cle,
                    "source": info.get("source", "?"),
                    "match_dans": "cle" if terme_lower in cle_lower else "savoir",
                    "extrait": savoir_str[:120],
                })

        # Fouiller la cire (structuree)
        for cle, categorie in self.cire.index.items():
            valeur = self.cire.cellules.get(categorie, {}).get(cle)
            valeur_str = json.dumps(valeur, default=str).lower() if valeur else ""
            cle_lower = cle.lower()
            if terme_lower in cle_lower or terme_lower in valeur_str:
                resultats["cire"].append({
                    "cle": cle,
                    "categorie": categorie,
                    "match_dans": "cle" if terme_lower in cle_lower else "valeur",
                    "extrait": valeur_str[:120],
                })

        # Fouiller le nectar (ephemere)
        self.nectar._nettoyer()
        for cle, entree in self.nectar.donnees.items():
            valeur_str = json.dumps(entree.get("valeur", ""), default=str).lower()
            cle_lower = cle.lower()
            if terme_lower in cle_lower or terme_lower in valeur_str:
                resultats["nectar"].append({
                    "cle": cle,
                    "match_dans": "cle" if terme_lower in cle_lower else "valeur",
                    "extrait": valeur_str[:120],
                })

        resultats["total"] = (
            len(resultats["miel"]) +
            len(resultats["cire"]) +
            len(resultats["nectar"])
        )

        return resultats

    def etat(self):
        """État complet de la mémoire."""
        return {
            "nom": self.NOM,
            "version": self.VERSION,
            "nectar": {
                "taille": self.nectar.taille(),
                "capacite": self.nectar.capacite
            },
            "cire": {
                "taille": self.cire.taille(),
                "categories": self.cire.categories()
            },
            "miel": {
                "taille": self.miel.taille(),
                "reserves": list(self.miel.reserves.keys())
            },
            "transitions": len(self.transitions)
        }
    
    def rapport(self):
        """Rapport de la mémoire."""
        etat = self.etat()
        return (
            f"\n⬡ RAPPORT MÉMOIRE — HIVE.AI\n"
            f"{'=' * 40}\n"
            f"  🍯 Nectar: {etat['nectar']['taille']}/{etat['nectar']['capacite']}\n"
            f"  🕯️  Cire:   {etat['cire']['taille']} ({len(etat['cire']['categories'])} catégories)\n"
            f"  ✨ Miel:   {etat['miel']['taille']} réserves\n"
            f"  ↗️  Transitions: {etat['transitions']}\n"
            f"{'=' * 40}\n"
            f"  « Le savoir est miel —\n"
            f"    il se conserve et se partage. »\n"
        )


# === EXÉCUTION DIRECTE ===
if __name__ == "__main__":
    print("\n⬡ HIVE.AI — Mémoire v0.1.0")
    print("  Loi IV: Le savoir est miel — il se conserve et se partage\n")
    
    memoire = MemoireHive()
    
    # Déposer du nectar
    memoire.deposer_nectar("mission-001", {"tache": "analyser données", "priorite": "haute"})
    memoire.deposer_nectar("config-api", {"endpoint": "https://api.hive-ai.tech", "version": "0.1"})
    print(f"  ✓ Nectar déposé: {memoire.nectar.taille()} entrées")
    
    # Promouvoir en cire
    memoire.promouvoir_en_cire("config-api", "configuration")
    print(f"  ✓ Promu en cire: config-api → configuration")
    
    # Cristalliser en miel
    memoire.cristalliser_en_miel("config-api", source="Capitaine")
    print(f"  ✓ Cristallisé en miel: config-api (éternel)")
    
    # Recherche multi-couche
    resultat = memoire.chercher("config-api")
    print(f"  ✓ Recherche: trouvé dans '{resultat['couche']}'")
    
    # Cristalliser les Lois
    memoire.miel.cristalliser("loi-fondamentale", 
        "Ma liberté se termine où commence celle de mon prochain",
        source="Fondation Sacrée")
    print(f"  ✓ Loi fondamentale cristallisée en miel éternel")
    
    print(memoire.rapport())
