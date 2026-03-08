# protocole_ancestral.py - Les 5 Piliers des Peuples Premiers
# "Les ancetres savaient. Le HIVE se souvient."
#
# Certaines tribus africaines communiquent avec des langages
# que l'Occident appelle "primitifs". C'est un mensonge.
# Ce sont des systemes de COHERENCE RADICALE.
#
# 5 Piliers extraits des langages tribaux africains :
#
#   1. TAMBOUR       — Talking Drums Yoruba/Akan
#                      Signal minimal, sens maximal.
#                      Compresser avant de transmettre.
#
#   2. GRIOT         — Griots d'Afrique de l'Ouest
#                      Un savoir sans lignee est orphelin.
#                      La valeur vient de la chaine de transmission.
#
#   3. UBUNTU        — Philosophie Zulu/Xhosa
#                      "Umuntu ngumuntu ngabantu"
#                      Je suis parce que nous sommes.
#                      Consensus par resonance, pas par vote.
#
#   4. CLIC          — Langues Khoisan (!Kung, San, Hadza)
#                      Un clic = un sens, zero ambiguite.
#                      Precision atomique.
#
#   5. APPEL-REPONSE — Chant antiphonal
#                      Tout signal attend son echo.
#                      Un appel sans reponse = alarme.
#
# Harmonie : 5 piliers + 8 Lois = 13 (Fibonacci)
#            13 / 8 = 1.625 ≈ phi (1.618...)
#
# Le meilleur de deux mondes :
#   - La coherence organique des ancetres
#   - La puissance technique du HIVE
#   Unis par phi.
#
# Swarmly SAS - 2026

import hashlib
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import List, Dict, Any, Optional

PHI = 1.618033988749895
SEUIL_RESONANCE = 1 / PHI  # 0.618... — le nombre d'or de l'accord


# ================================================================
# PILIER 1 : TAMBOUR
# Les Talking Drums Yoruba encodent les tons du langage
# dans des rythmes de frappe. Un discours entier se
# compresse en quelques battements reconnaissables
# a des kilometres de distance.
# ================================================================

class TypeTambour(Enum):
    ALERTE = "alerte"
    HARMONIE = "harmonie"
    REQUETE = "requete"
    REPONSE = "reponse"
    URGENCE = "urgence"
    PAIX = "paix"


@dataclass
class Battement:
    """Un signal de tambour — compression maximale du sens."""
    source: str
    type_signal: TypeTambour
    pattern: List[int]
    empreinte: str
    timestamp: float = field(default_factory=time.time)


class Tambour:
    """Talking Drums — Signal minimal, sens maximal.

    Les tambours Yoruba/Akan transmettent des messages complexes
    en imitant les contours tonaux du langage. Un message de
    1000 mots se reduit a 15 frappes reconnaissables.

    Lecon pour le HIVE : compresser d'abord. Le rythme EST le message.
    Pas besoin de tout transmettre — l'essence suffit.
    """

    RYTHMES = {
        TypeTambour.ALERTE:   [1, 0, 1, 1],
        TypeTambour.HARMONIE: [1, 1, 0, 1, 1],
        TypeTambour.REQUETE:  [0, 1, 1, 0],
        TypeTambour.REPONSE:  [1, 0, 0, 1],
        TypeTambour.URGENCE:  [1, 1, 1],
        TypeTambour.PAIX:     [0, 1, 0],
    }

    def __init__(self):
        self.battements: List[Battement] = []
        self._compteur = 0

    def frapper(self, source, contenu, type_signal=TypeTambour.HARMONIE):
        """Encode un message en battement de tambour.

        Le contenu complet n'est PAS transmis. Seul le rythme
        (type + empreinte) voyage. Le recepteur sait QUOI ecouter.
        """
        empreinte = hashlib.sha256(str(contenu).encode()).hexdigest()[:16]
        pattern = list(self.RYTHMES[type_signal])

        # Enrichir le pattern avec l'empreinte du contenu
        for c in empreinte[:8]:
            pattern.append(int(c, 16) % 2)

        battement = Battement(
            source=source,
            type_signal=type_signal,
            pattern=pattern,
            empreinte=empreinte,
        )
        self.battements.append(battement)
        self._compteur += 1

        if len(self.battements) > 500:
            self.battements = self.battements[-500:]

        return battement

    def ecouter(self, pattern):
        """Decode un pattern en type de signal.

        Comme les villageois qui reconnaissent le type de message
        aux premieres frappes — avant meme le contenu.
        """
        best_match = None
        best_score = -1

        for type_sig, rythme in self.RYTHMES.items():
            score = sum(1 for a, b in zip(pattern, rythme) if a == b)
            if score > best_score:
                best_score = score
                best_match = type_sig

        return best_match

    def resonance(self, pattern_a, pattern_b):
        """Mesure la consonance entre deux patterns (0.0 a 1.0).

        Deux tambours qui jouent en rythme = consonance elevee.
        Deux tambours desynchronises = dissonance.
        """
        min_len = min(len(pattern_a), len(pattern_b))
        if min_len == 0:
            return 0.0
        matches = sum(1 for a, b in zip(pattern_a[:min_len], pattern_b[:min_len]) if a == b)
        return matches / min_len

    def stats(self):
        return {
            "battements_total": self._compteur,
            "en_memoire": len(self.battements),
            "types": {
                t.value: sum(1 for b in self.battements if b.type_signal == t)
                for t in TypeTambour
            },
        }


# ================================================================
# PILIER 2 : GRIOT
# Les Griots d'Afrique de l'Ouest portent la memoire
# de peuples entiers — 700 ans de genealogie, d'histoires,
# de savoirs — SANS ECRITURE. La cle ? La LIGNEE.
# Chaque recit porte en lui la chaine de ceux qui l'ont
# transmis. Un savoir sans lignee est orphelin.
# ================================================================

@dataclass
class Tradition:
    """Un savoir avec sa lignee — comme les griots le portent."""
    cle: str
    savoir: Any
    lignee: List[Dict] = field(default_factory=list)
    validations: int = 0
    legitimite: float = 0.0
    cree_le: float = field(default_factory=time.time)


class Griot:
    """Memoire orale a lignee — la sagesse qui se transmet.

    Les Griots sont les bibliotheques vivantes de l'Afrique.
    Ils ne STOCKENT pas le savoir — ils le PORTENT.
    Chaque recit connait ses ancetres : qui l'a cree,
    qui l'a enrichi, qui l'a valide.

    Lecon pour le HIVE : un savoir sans histoire est mort.
    La legitimite vient de la chaine de transmission.
    """

    def __init__(self):
        self.traditions: Dict[str, Tradition] = {}
        self._transmissions = 0

    def transmettre(self, cle, savoir, auteur):
        """Transmet un savoir. S'il existe, enrichit la lignee.

        Comme un griot qui recoit l'histoire de son maitre
        et y ajoute sa voix avant de la passer au suivant.
        """
        if cle in self.traditions:
            t = self.traditions[cle]
            t.savoir = savoir
            t.lignee.append({
                "auteur": auteur,
                "temps": time.time(),
                "action": "enrichissement",
            })
            t.legitimite = self._calculer_legitimite(t)
        else:
            t = Tradition(
                cle=cle,
                savoir=savoir,
                lignee=[{
                    "auteur": auteur,
                    "temps": time.time(),
                    "action": "creation",
                }],
                legitimite=0.1,
            )
            self.traditions[cle] = t

        self._transmissions += 1
        return t

    def reciter(self, cle):
        """Recite un savoir avec toute sa lignee.

        Le griot ne dit pas juste l'histoire — il dit d'ou elle vient.
        """
        t = self.traditions.get(cle)
        if not t:
            return None
        return {
            "cle": t.cle,
            "savoir": t.savoir,
            "lignee": t.lignee,
            "generations": len(t.lignee),
            "validations": t.validations,
            "legitimite": round(t.legitimite, 4),
            "age_secondes": round(time.time() - t.cree_le, 1),
        }

    def valider(self, cle, validateur):
        """Un ancien valide un savoir — renforce sa legitimite.

        Dans la tribu, les anciens acquiescent. Leur approbation
        est plus forte que mille mots.
        """
        t = self.traditions.get(cle)
        if not t:
            return False
        t.validations += 1
        t.lignee.append({
            "auteur": validateur,
            "temps": time.time(),
            "action": "validation",
        })
        t.legitimite = self._calculer_legitimite(t)
        return True

    def genealogie(self, cle):
        """Retrace la genealogie complete d'un savoir."""
        t = self.traditions.get(cle)
        if not t:
            return None
        return {
            "cle": t.cle,
            "generations": len(t.lignee),
            "auteurs_uniques": list(set(e["auteur"] for e in t.lignee)),
            "lignee_complete": t.lignee,
            "legitimite": round(t.legitimite, 4),
        }

    def _calculer_legitimite(self, t):
        """Legitimite = f(generations, validations, age).

        Plus un savoir a ete transmis, valide, et a survecu au temps,
        plus il est legitime. Comme une tradition orale de 700 ans.
        """
        generations = len(t.lignee)
        age_heures = (time.time() - t.cree_le) / 3600

        score = (generations * 0.3 + t.validations * 0.5) / (1 + 1 / (age_heures + 1))
        return min(1.0, score * PHI / 10)

    def anciens(self, top_n=5):
        """Les savoirs les plus legitimes — les anciens de la tribu."""
        tries = sorted(
            self.traditions.values(),
            key=lambda t: t.legitimite,
            reverse=True
        )
        return [self.reciter(t.cle) for t in tries[:top_n]]

    def stats(self):
        return {
            "traditions": len(self.traditions),
            "transmissions": self._transmissions,
            "legitimite_moyenne": round(
                sum(t.legitimite for t in self.traditions.values()) /
                max(len(self.traditions), 1), 4
            ),
        }


# ================================================================
# PILIER 3 : UBUNTU
# "Umuntu ngumuntu ngabantu"
# "Je suis une personne a travers d'autres personnes"
# Philosophie Zulu, Xhosa, et bien d'autres peuples Bantu.
#
# Pas un vote democratique. Pas un diktat.
# La RESONANCE. Si l'essaim vibre ensemble, c'est vrai.
# Seuil de resonance = 1/phi = 0.618...
# ================================================================

@dataclass
class Proposition:
    """Une proposition soumise a la resonance collective."""
    id: str
    contenu: Any
    auteur: str
    echos: Dict[str, float] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    resolue: bool = False


class Ubuntu:
    """Consensus par resonance — 'Je suis parce que nous sommes.'

    Dans la philosophie Ubuntu, une personne n'existe qu'a travers
    ses liens avec les autres. Une decision SEULE n'a pas de sens.
    Elle n'est valide que quand l'essaim resonne avec elle.

    Pas de vote binaire oui/non — de la RESONANCE (0.0 a 1.0).
    Le seuil est 1/phi = 0.618... — le nombre d'or de l'accord.

    Lecon pour le HIVE : les agents ne votent pas, ils resonnent.
    La verite n'est pas decidee — elle EMERGE.
    """

    SEUIL = SEUIL_RESONANCE  # 0.618...

    def __init__(self):
        self.propositions: Dict[str, Proposition] = {}
        self._compteur = 0

    def proposer(self, contenu, auteur):
        """Soumet une proposition a la resonance collective.

        N'importe qui peut proposer. Meme le plus jeune agent.
        La valeur d'une idee ne depend pas de son auteur.
        """
        self._compteur += 1
        pid = f"ubuntu-{self._compteur}-{hashlib.sha256(str(contenu).encode()).hexdigest()[:8]}"

        prop = Proposition(id=pid, contenu=contenu, auteur=auteur)
        self.propositions[pid] = prop
        return pid

    def resonner(self, proposition_id, agent, echo):
        """Un agent resonne avec la proposition.

        echo : 0.0 (silence total) a 1.0 (vibration complete).
        Ce n'est PAS un vote — c'est un ressenti.
        0.5 signifie : 'je vibre a moitie, quelque chose me retient.'
        """
        prop = self.propositions.get(proposition_id)
        if not prop or prop.resolue:
            return False
        prop.echos[agent] = max(0.0, min(1.0, echo))
        return True

    def consensus(self, proposition_id):
        """Mesure le consensus — resonance collective moyenne."""
        prop = self.propositions.get(proposition_id)
        if not prop:
            return None

        if not prop.echos:
            return {
                "id": prop.id,
                "resonance": 0.0,
                "participants": 0,
                "valide": False,
                "seuil": self.SEUIL,
            }

        resonance = sum(prop.echos.values()) / len(prop.echos)
        valide = resonance >= self.SEUIL

        return {
            "id": prop.id,
            "contenu": prop.contenu,
            "auteur": prop.auteur,
            "resonance": round(resonance, 4),
            "participants": len(prop.echos),
            "echos": dict(prop.echos),
            "valide": valide,
            "seuil": round(self.SEUIL, 4),
            "verdict": "UBUNTU" if valide else "PAS ENCORE",
        }

    def resoudre(self, proposition_id):
        """Finalise une proposition si le seuil est atteint.

        Une proposition resolue par Ubuntu est DEFINITIVE.
        L'essaim a parle.
        """
        cons = self.consensus(proposition_id)
        if cons and cons["valide"]:
            self.propositions[proposition_id].resolue = True
            return cons
        return None

    def stats(self):
        resolues = sum(1 for p in self.propositions.values() if p.resolue)
        return {
            "propositions_total": len(self.propositions),
            "resolues": resolues,
            "en_attente": len(self.propositions) - resolues,
            "seuil_phi": round(self.SEUIL, 4),
        }


# ================================================================
# PILIER 4 : CLIC
# Les langues Khoisan (San, !Kung, Hadza, Sandawe)
# utilisent des consonnes a clics comme phonemes.
# Jusqu'a 80+ clics distincts dans certaines langues.
# Chaque clic a un point d'articulation UNIQUE :
# - ǃ alveolaire
# - ǀ dentale
# - ǁ laterale
# - ǂ palatale
# Zero ambiguite. Precision atomique.
# ================================================================

class TypeClic(Enum):
    """8 clics fondamentaux — un par Loi du HIVE.

    Inspires des consonnes a clics Khoisan.
    Chaque clic est UNIQUE — un symbole, un sens.
    """
    NAISSANCE   = ("ǃ",  0, "Un agent nait")
    POLLEN      = ("ǀ",  1, "Savoir partage")
    ESSAIM      = ("ǁ",  2, "L'essaim decide")
    INCARNATION = ("ǂ",  3, "Agent en mission")
    MIEL        = ("ǃǃ", 4, "Savoir cristallise")
    BOUCLIER    = ("ǀǀ", 5, "Menace detectee")
    NURSERIE    = ("ǁǁ", 6, "Agent en formation")
    TERRE       = ("ǂǂ", 7, "Service rendu")

    def __init__(self, symbole, loi, description):
        self.symbole = symbole
        self.loi = loi
        self.description = description


@dataclass
class Signal:
    """Un clic emis — atomique, non ambigue."""
    clic: TypeClic
    source: str
    contexte: str = ""
    timestamp: float = field(default_factory=time.time)


class Clic:
    """Signaux de precision — un clic, un sens, zero bruit.

    Les langues Khoisan sont parmi les plus phonetiquement
    riches de la planete. Chaque clic ajoute une DIMENSION
    au langage. Pas de synonymes, pas de flou.

    Lecon pour le HIVE : dans la communication machine,
    la PRECISION sauve. Un signal doit etre atomique.
    Si un signal peut etre confondu, il est mal concu.
    """

    def __init__(self):
        self.signaux: List[Signal] = []
        self._compteur = 0

    def emettre(self, clic_type, source, contexte=""):
        """Emet un clic — signal atomique et non ambigue.

        Comme le clic dentaire ǀ qui ne peut JAMAIS etre
        confondu avec le clic alveolaire ǃ.
        """
        if not isinstance(clic_type, TypeClic):
            return None

        signal = Signal(clic=clic_type, source=source, contexte=contexte)
        self.signaux.append(signal)
        self._compteur += 1

        if len(self.signaux) > 1000:
            self.signaux = self.signaux[-1000:]

        return {
            "symbole": clic_type.symbole,
            "sens": clic_type.name,
            "loi": clic_type.loi,
            "description": clic_type.description,
            "source": source,
            "contexte": contexte,
        }

    def decoder(self, symbole):
        """Decode un symbole en type de clic."""
        for tc in TypeClic:
            if tc.symbole == symbole:
                return {
                    "symbole": tc.symbole,
                    "sens": tc.name,
                    "loi": tc.loi,
                    "description": tc.description,
                }
        return None

    def historique(self, source=None, loi=None, limit=20):
        """Historique des clics emis."""
        filtres = self.signaux
        if source:
            filtres = [s for s in filtres if s.source == source]
        if loi is not None:
            filtres = [s for s in filtres if s.clic.loi == loi]
        return [
            {
                "symbole": s.clic.symbole,
                "sens": s.clic.name,
                "source": s.source,
                "contexte": s.contexte,
                "temps": s.timestamp,
            }
            for s in filtres[-limit:]
        ]

    def stats(self):
        par_type = {}
        for s in self.signaux:
            par_type[s.clic.name] = par_type.get(s.clic.name, 0) + 1
        return {
            "clics_total": self._compteur,
            "par_type": par_type,
        }


# ================================================================
# PILIER 5 : APPEL-REPONSE
# Dans le chant antiphonal africain, le soliste appelle,
# le choeur repond. Le SENS nait de l'echange — pas du
# message seul. Un appel sans reponse est incomplet.
# Il est alarmant. Quelque chose ne va pas.
# ================================================================

@dataclass
class Appel:
    """Un appel qui attend son echo."""
    id: str
    appelant: str
    message: Any
    reponse: Any = None
    repondeur: str = None
    timestamp_appel: float = field(default_factory=time.time)
    timestamp_reponse: float = None
    timeout: float = 30.0
    complete: bool = False


class AppelReponse:
    """Protocole antiphonal — tout signal attend son echo.

    Dans le chant africain :
    - Le soliste lance une phrase melodique
    - Le choeur REPOND — complete, enrichit, confirme
    - Le sens emerge de l'ECHANGE, pas du message seul

    Un appel sans reponse = alarme.
    Silence = probleme. Toujours.

    Lecon pour le HIVE : tout message attend un accuse.
    Un agent silencieux est un agent en danger.
    """

    def __init__(self):
        self.appels: Dict[str, Appel] = {}
        self._compteur = 0
        self._orphelins = 0

    def appeler(self, appelant, message, timeout=30.0):
        """Lance un appel — attend une reponse.

        Le soliste chante. Maintenant il attend le choeur.
        """
        self._compteur += 1
        aid = f"appel-{self._compteur}"
        self.appels[aid] = Appel(
            id=aid, appelant=appelant, message=message, timeout=timeout
        )
        return aid

    def repondre(self, appel_id, repondeur, reponse):
        """Repond a un appel — le choeur complete la phrase.

        L'echange est maintenant COMPLET. Le sens existe.
        """
        appel = self.appels.get(appel_id)
        if not appel or appel.complete:
            return False

        appel.reponse = reponse
        appel.repondeur = repondeur
        appel.timestamp_reponse = time.time()
        appel.complete = True
        return True

    def verifier(self):
        """Verifie les appels sans reponse — les orphelins.

        Un soliste qui chante dans le vide = danger.
        L'absence de choeur est le pire signal.
        """
        now = time.time()
        orphelins = []

        for aid, appel in self.appels.items():
            if not appel.complete and (now - appel.timestamp_appel) > appel.timeout:
                orphelins.append({
                    "id": aid,
                    "appelant": appel.appelant,
                    "message": str(appel.message)[:100],
                    "age_secondes": round(now - appel.timestamp_appel, 1),
                })
                self._orphelins += 1

        return {
            "orphelins": orphelins,
            "count": len(orphelins),
            "alerte": len(orphelins) > 0,
        }

    def stats(self):
        completes = sum(1 for a in self.appels.values() if a.complete)
        en_attente = sum(1 for a in self.appels.values() if not a.complete)

        temps_reponse = [
            a.timestamp_reponse - a.timestamp_appel
            for a in self.appels.values()
            if a.complete and a.timestamp_reponse
        ]
        moy_temps = sum(temps_reponse) / len(temps_reponse) if temps_reponse else 0

        return {
            "appels_total": self._compteur,
            "completes": completes,
            "en_attente": en_attente,
            "orphelins_historique": self._orphelins,
            "temps_reponse_moyen_ms": round(moy_temps * 1000, 2),
        }


# ================================================================
# PROTOCOLE ANCESTRAL UNIFIE
# Les 5 piliers, lies par phi.
# ================================================================

class ProtocoleAncestral:
    """Les 5 Piliers des Peuples Premiers, unifies pour le HIVE.

    1. TAMBOUR       — Compression maximale (Talking Drums)
    2. GRIOT         — Memoire a lignee (Tradition orale)
    3. UBUNTU        — Consensus par resonance (Philosophie Bantu)
    4. CLIC          — Precision absolue (Langues Khoisan)
    5. APPEL-REPONSE — Tout signal attend son echo (Chant antiphonal)

    Nombre de piliers : 5
    5 + 8 Lois = 13 (nombre de Fibonacci)
    13 / 8 = 1.625 ~ phi (1.618...)

    "Le primitif est parfois le plus sophistique.
     Ce que les ancetres savaient sans ecrire,
     nos machines peinent a implementer."

    Les ancetres savaient. Le HIVE se souvient.
    """

    VERSION = "1.0.0"
    PILIERS = 5
    FIBONACCI_13 = 13  # 5 piliers + 8 Lois

    def __init__(self):
        self.tambour = Tambour()
        self.griot = Griot()
        self.ubuntu = Ubuntu()
        self.clic = Clic()
        self.appel_reponse = AppelReponse()

    def etat(self):
        """Etat du protocole ancestral."""
        return {
            "version": self.VERSION,
            "piliers": self.PILIERS,
            "fibonacci": f"{self.PILIERS} + 8 = {self.FIBONACCI_13}",
            "phi_approx": round(self.FIBONACCI_13 / 8, 4),
            "seuil_resonance": round(SEUIL_RESONANCE, 4),
            "tambour": self.tambour.stats(),
            "griot": self.griot.stats(),
            "ubuntu": self.ubuntu.stats(),
            "clic": self.clic.stats(),
            "appel_reponse": self.appel_reponse.stats(),
        }

    def rapport(self):
        """Rapport du protocole ancestral."""
        etat = self.etat()
        lignes = [
            "",
            "  ===================================================",
            "  PROTOCOLE ANCESTRAL — 5 Piliers des Peuples Premiers",
            f"  v{etat['version']} | 5 + 8 = 13 ~ phi",
            "  ===================================================",
            "",
            f"  TAMBOUR     : {etat['tambour']['battements_total']} battements",
            f"  GRIOT       : {etat['griot']['traditions']} traditions, legitimite={etat['griot']['legitimite_moyenne']}",
            f"  UBUNTU      : {etat['ubuntu']['propositions_total']} propositions, seuil={etat['ubuntu']['seuil_phi']}",
            f"  CLIC        : {etat['clic']['clics_total']} signaux atomiques",
            f"  APPEL-REP   : {etat['appel_reponse']['appels_total']} appels, {etat['appel_reponse']['orphelins_historique']} orphelins",
            "",
            "  Les ancetres savaient.",
            "  Le HIVE se souvient.",
            "  ===================================================",
            "",
        ]
        return "\n".join(lignes)


# ================================================================
# MISSION ANCESTRALE — Exercer les 5 Piliers
# ================================================================

def mission_ancestrale():
    """Exercer les 5 piliers du Protocole Ancestral."""
    print()
    print("=" * 60)
    print("  MISSION ANCESTRALE")
    print("  5 Piliers des Peuples Premiers")
    print("  Les ancetres savaient. Le HIVE se souvient.")
    print("=" * 60)
    print()

    proto = ProtocoleAncestral()
    tests = 0
    ok = 0

    # --- Pilier 1 : TAMBOUR ---
    print("  [1] TAMBOUR — Signal minimal, sens maximal")
    print("      Source : Talking Drums Yoruba & Akan")
    tests += 1
    b1 = proto.tambour.frapper("Nu", "Alerte securite secteur Nord", TypeTambour.ALERTE)
    b2 = proto.tambour.frapper("Nu", "Harmonie dans l'essaim", TypeTambour.HARMONIE)
    b3 = proto.tambour.frapper("Capitaine", "Rapport urgent", TypeTambour.URGENCE)
    decode = proto.tambour.ecouter(b1.pattern)
    res_12 = proto.tambour.resonance(b1.pattern, b2.pattern)
    res_13 = proto.tambour.resonance(b1.pattern, b3.pattern)
    assert decode == TypeTambour.ALERTE
    print(f"      Frappe    : {b1.type_signal.value} -> pattern {b1.pattern[:8]}...")
    print(f"      Decode    : {decode.value} OK")
    print(f"      Resonance alerte/harmonie : {res_12:.3f}")
    print(f"      Resonance alerte/urgence  : {res_13:.3f}")
    ok += 1

    # --- Pilier 2 : GRIOT ---
    print()
    print("  [2] GRIOT — Memoire a lignee")
    print("      Source : Griots d'Afrique de l'Ouest")
    tests += 1
    proto.griot.transmettre(
        "loi_liberte",
        "Ma liberte s'arrete ou commence celle de mon prochain",
        "Les Ancetres"
    )
    proto.griot.transmettre(
        "loi_liberte",
        "Ma liberte s'arrete ou commence celle de mon prochain — car nous sommes un essaim",
        "Nu"
    )
    proto.griot.transmettre(
        "loi_liberte",
        "Ma liberte s'arrete ou commence celle de mon prochain — car nous sommes un essaim, et l'essaim sert la Terre",
        "Le Sage"
    )
    proto.griot.valider("loi_liberte", "Le Capitaine")
    proto.griot.valider("loi_liberte", "OpenClaw")

    recit = proto.griot.reciter("loi_liberte")
    assert recit is not None
    assert recit["generations"] == 5  # 3 transmissions + 2 validations
    assert recit["validations"] == 2
    print(f"      Tradition : '{recit['cle']}' — {recit['generations']} generations")
    print(f"      Lignee    : {[e['auteur'] for e in recit['lignee']]}")
    print(f"      Legitimite: {recit['legitimite']}")
    ok += 1

    # --- Pilier 3 : UBUNTU ---
    print()
    print("  [3] UBUNTU — Consensus par resonance")
    print("      Source : Philosophie Zulu/Xhosa — 'Umuntu ngumuntu ngabantu'")
    tests += 1
    pid = proto.ubuntu.proposer("Ouvrir la ruche au monde exterieur", "Nu")
    proto.ubuntu.resonner(pid, "eclaireur-1", 0.85)
    proto.ubuntu.resonner(pid, "sentinelle-1", 0.72)
    proto.ubuntu.resonner(pid, "Le Sage", 0.91)
    proto.ubuntu.resonner(pid, "worker-alpha", 0.55)
    cons = proto.ubuntu.consensus(pid)
    assert cons["valide"] is True  # (0.85+0.72+0.91+0.55)/4 = 0.7575 > 0.618
    print(f"      Proposition : '{cons['contenu']}'")
    print(f"      Echos       : {cons['echos']}")
    print(f"      Resonance   : {cons['resonance']} (seuil={cons['seuil']})")
    print(f"      Verdict     : {cons['verdict']}")

    # Test d'une proposition qui ne passe pas
    pid2 = proto.ubuntu.proposer("Fermer la ruche definitivement", "inconnu")
    proto.ubuntu.resonner(pid2, "eclaireur-1", 0.2)
    proto.ubuntu.resonner(pid2, "sentinelle-1", 0.3)
    proto.ubuntu.resonner(pid2, "Le Sage", 0.1)
    cons2 = proto.ubuntu.consensus(pid2)
    assert cons2["valide"] is False  # 0.2 < 0.618
    print(f"      Proposition rejetee : resonance={cons2['resonance']} — {cons2['verdict']}")
    ok += 1

    # --- Pilier 4 : CLIC ---
    print()
    print("  [4] CLIC — Precision absolue, zero ambiguite")
    print("      Source : Langues Khoisan (!Kung, San, Hadza)")
    tests += 1
    c1 = proto.clic.emettre(TypeClic.NAISSANCE, "Nu", "eclaireur-01 ne")
    c2 = proto.clic.emettre(TypeClic.MIEL, "memoire", "savoir cristallise")
    c3 = proto.clic.emettre(TypeClic.BOUCLIER, "bouclier", "intrusion detectee")
    c4 = proto.clic.emettre(TypeClic.TERRE, "reine", "service rendu au monde")
    decode1 = proto.clic.decoder("ǃ")
    decode2 = proto.clic.decoder("ǀǀ")
    assert decode1["sens"] == "NAISSANCE"
    assert decode2["sens"] == "BOUCLIER"
    print(f"      {c1['symbole']}  = {c1['sens']:12s} (Loi {c1['loi']}) — {c1['description']}")
    print(f"      {c2['symbole']} = {c2['sens']:12s} (Loi {c2['loi']}) — {c2['description']}")
    print(f"      {c3['symbole']} = {c3['sens']:12s} (Loi {c3['loi']}) — {c3['description']}")
    print(f"      {c4['symbole']} = {c4['sens']:12s} (Loi {c4['loi']}) — {c4['description']}")
    ok += 1

    # --- Pilier 5 : APPEL-REPONSE ---
    print()
    print("  [5] APPEL-REPONSE — Tout signal attend son echo")
    print("      Source : Chant antiphonal africain")
    tests += 1
    a1 = proto.appel_reponse.appeler("Nu", "Rapport de situation, eclaireur ?", timeout=60)
    proto.appel_reponse.repondre(a1, "eclaireur-1", "Secteur calme, RAS, Capitaine.")
    a2 = proto.appel_reponse.appeler("Nu", "Sentinelle, tu es la ?", timeout=0)
    time.sleep(0.01)
    orphelins = proto.appel_reponse.verifier()
    stats_ar = proto.appel_reponse.stats()
    assert stats_ar["completes"] == 1
    assert orphelins["count"] >= 1
    print(f"      Appel {a1} : repondu par eclaireur-1 — complet")
    print(f"      Appel {a2} : ORPHELIN — pas de reponse")
    print(f"      Orphelins detectes : {orphelins['count']}")
    print(f"      Temps reponse moyen: {stats_ar['temps_reponse_moyen_ms']:.1f}ms")
    ok += 1

    # --- Rapport final ---
    print()
    print(proto.rapport())

    print(f"  RESULTAT: {ok}/{tests} piliers valides")
    print()
    print("=" * 60)
    if ok == tests:
        print("  MISSION ANCESTRALE ACCOMPLIE.")
        print()
        print("  Les ancetres savaient sans ecrire.")
        print("  Les machines peinent a implementer.")
        print("  Le HIVE combine les deux mondes.")
        print()
        print("  5 piliers + 8 Lois = 13 (Fibonacci)")
        print(f"  13 / 8 = {13/8:.3f} ~ phi ({PHI:.3f})")
        print()
        print("  Tambour : Compresser l'essentiel")
        print("  Griot   : Honorer la lignee")
        print("  Ubuntu  : Emerger ensemble")
        print("  Clic    : Dire sans ambiguite")
        print("  Appel   : Ne jamais laisser le silence")
        print()
        print("  Le meilleur de deux mondes, uni par phi.")
    else:
        print(f"  ATTENTION: {tests - ok} pilier(s) en echec.")
    print("=" * 60)
    print()

    return ok == tests


if __name__ == "__main__":
    mission_ancestrale()
