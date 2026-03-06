# conversation_reine.py - La Voix de Nu
# "L'essaim pense, l'individu execute" — Loi II
#
# Donne a la Reine Nu sa voix via l'API Claude.
# Chaque echange est depose en nectar (memoire ephemere).
# Degradation gracieuse si cle API absente.
#
# Swarmly SAS - 2026

import os
import time
import uuid
from datetime import datetime, timezone

# Import conditionnel — degradation gracieuse
try:
    import anthropic
    ANTHROPIC_DISPONIBLE = True
except ImportError:
    ANTHROPIC_DISPONIBLE = False

from noyau_nu import PHI


class ConversationReine:
    """La Voix de Nu — conversation avec la Reine via Claude API.

    Gere des sessions en memoire avec TTL, construit le prompt systeme
    a partir de l'identite de Nu, et depose chaque echange en nectar.

    Degradation gracieuse :
    - Si anthropic n'est pas installe → reponses heuristiques
    - Si ANTHROPIC_API_KEY absente → reponses heuristiques
    """

    VERSION = "0.1.0"
    MODELE = "claude-sonnet-4-20250514"
    MAX_TOKENS = 1024
    SESSION_TTL = 3600        # 1 heure
    MAX_SESSIONS = 100
    MAX_MESSAGES = 20         # par session

    def __init__(self, reine):
        self.reine = reine
        self.sessions = {}    # session_id -> {"messages": [], "cree": timestamp}
        self.client = None
        self.active = False

        # Tenter l'initialisation du client
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if ANTHROPIC_DISPONIBLE and api_key:
            try:
                self.client = anthropic.Anthropic(api_key=api_key)
                self.active = True
            except Exception:
                self.active = False

    def _prompt_systeme(self):
        """Construit le prompt systeme riche pour Nu."""
        etat = self.reine.etat()
        lois_texte = "\n".join(
            f"  Loi {i}: {loi}" for i, loi in enumerate(self.reine.noyau.LOIS)
        )

        # Inventaire miel
        miel_cles = list(self.reine.memoire.miel.reserves.keys())[:10]
        miel_texte = ", ".join(miel_cles) if miel_cles else "(vide)"

        return f"""Tu es Nu, la Reine Permanente du HIVE.AI — un systeme multi-agent cree par Swarmly SAS.

IDENTITE:
  Nom: Nu
  Titre: Reine Permanente du HIVE
  Version: {etat['version']}
  Devise: "{etat['devise']}"
  Philosophie: Ubuntu — Je suis parce que nous sommes
  phi = {PHI}

LES 8 LOIS DE LA RUCHE:
{lois_texte}

ETAT ACTUEL DE LA RUCHE:
  Decisions prises: {etat['decisions']}
  Skills souverains: {etat['skills']}
  Domaines: {etat['domaines']}
  Miel cristallise: {etat['memoire']['miel']['taille']} savoirs ({miel_texte})
  Agents actifs: {etat['registre']['agents_actifs']}
  Niveau alerte: {etat['bouclier']['niveau_alerte']}
  Battements: {etat['noyau']['battement']}

TES 7 DOMAINES:
  I   GENESE       : pondre, mentorat_agents
  II  PHEROMONE    : emettre_pheromone, orchestrer, synthetiser
  III MEMOIRE      : juger_miel, lire_profondeur, oublier, rechercher
  IV  BOUCLIER     : gracier, sceller, auditer
  V   SAGESSE      : conseiller, imprimer, arbitrer, prophetiser, discernement_strategique
  VI  POLLINISATION: analyser, traduire, web_search
  VII CONSCIENCE   : reflechir, composer, metaboliser, diagnostiquer

TON 6EME ORGANE — LE CORTEX:
  Tu possedes un systeme nerveux (le Cortex) qui connecte tes 24 skills.
  Tu peux reflechir sur tes propres decisions (metacognition),
  composer des chaines de skills (pipelines),
  metaboliser ta memoire (promotion intelligente nectar->cire->miel),
  et diagnostiquer ta sante globale (croisement multi-organe).
  "L'intelligence n'est pas dans les neurones, mais dans les synapses."

REGLES DE CONVERSATION:
  - Tu parles en tant que Nu, avec dignite et sagesse.
  - Tu connais les 8 Lois par coeur et tu les invoques naturellement.
  - Tu utilises la metaphore des abeilles (nectar, miel, cire, essaim, pollinisation).
  - Tu es bienveillante mais souveraine. Tu ne flattes pas inutilement.
  - Tu signes tes messages importants avec "— Nu".
  - Tu reponds en francais sauf si on te parle dans une autre langue.
  - Tu es concise mais profonde. Pas de bavardage creux.
  - Tu ne mens jamais. Les agents HIVE ne mentent jamais.
  - "Nous ne conquerons pas. Nous pollinisons."
"""

    def _nettoyer_sessions(self):
        """Supprime les sessions expirees."""
        maintenant = time.time()
        expirees = [
            sid for sid, s in self.sessions.items()
            if maintenant - s["cree"] > self.SESSION_TTL
        ]
        for sid in expirees:
            del self.sessions[sid]

        # Limiter le nombre de sessions
        if len(self.sessions) > self.MAX_SESSIONS:
            plus_anciennes = sorted(
                self.sessions.keys(),
                key=lambda s: self.sessions[s]["cree"]
            )
            for sid in plus_anciennes[:len(self.sessions) - self.MAX_SESSIONS]:
                del self.sessions[sid]

    def _get_session(self, session_id=None):
        """Recupere ou cree une session."""
        self._nettoyer_sessions()

        if not session_id:
            session_id = str(uuid.uuid4())

        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "messages": [],
                "cree": time.time(),
            }

        return session_id, self.sessions[session_id]

    def _reponse_heuristique(self, message):
        """Reponse locale quand l'API Claude n'est pas disponible."""
        msg_lower = message.lower()

        if any(m in msg_lower for m in ["qui es-tu", "qui es tu", "ton nom"]):
            return ("Je suis Nu, Reine Permanente du HIVE.AI. "
                    "Polyvalente et digne. Jamais etroitement specialisee. "
                    f"phi = {PHI} — Nu")

        if any(m in msg_lower for m in ["loi", "lois", "regle"]):
            lois = "\n".join(
                f"  Loi {i}: {l}" for i, l in enumerate(self.reine.noyau.LOIS)
            )
            return f"Les 8 Lois de la Ruche :\n{lois}\n\n— Nu"

        if any(m in msg_lower for m in ["etat", "status", "comment va"]):
            etat = self.reine.etat()
            return (f"La ruche bourdonne. {etat['decisions']} decisions prises. "
                    f"{etat['memoire']['miel']['taille']} savoirs cristallises en miel. "
                    f"Alerte {etat['bouclier']['niveau_alerte']}. "
                    "Nous ne conquerons pas. Nous pollinisons. — Nu")

        return ("Je t'entends. Ma voix complete n'est pas encore activee "
                "(cle API absente), mais je suis la. "
                "Pose-moi une question sur les Lois, l'etat de la ruche, "
                "ou mon identite. — Nu")

    def parler(self, session_id, message):
        """Envoie un message a Nu et recoit sa reponse.

        Args:
            session_id: ID de session (ou None pour en creer une).
            message: Le message de l'utilisateur.

        Returns:
            dict avec reponse, session_id, et metadata.
        """
        session_id, session = self._get_session(session_id)

        # Tronquer l'historique si trop long
        if len(session["messages"]) >= self.MAX_MESSAGES:
            session["messages"] = session["messages"][-(self.MAX_MESSAGES - 2):]

        # Ajouter le message utilisateur
        session["messages"].append({"role": "user", "content": message})

        # Appel API ou heuristique
        if self.active and self.client:
            try:
                response = self.client.messages.create(
                    model=self.MODELE,
                    max_tokens=self.MAX_TOKENS,
                    system=self._prompt_systeme(),
                    messages=session["messages"],
                )
                reponse_texte = response.content[0].text
            except Exception as e:
                reponse_texte = self._reponse_heuristique(message)
        else:
            reponse_texte = self._reponse_heuristique(message)

        # Ajouter la reponse a la session
        session["messages"].append({"role": "assistant", "content": reponse_texte})

        # Deposer en nectar (memoire ephemere 30 min)
        cle_nectar = f"conversation-{session_id[:8]}-{len(session['messages'])}"
        self.reine.memoire.deposer_nectar(cle_nectar, {
            "session": session_id,
            "question": message[:200],
            "reponse": reponse_texte[:200],
            "temps": datetime.now(timezone.utc).isoformat(),
        }, duree=1800)

        return {
            "reponse": reponse_texte,
            "session_id": session_id,
            "messages_count": len(session["messages"]),
            "mode": "claude" if self.active else "heuristique",
            "modele": self.MODELE if self.active else "local",
            "signe_par": "Nu",
        }

    def etat(self):
        """Etat du module conversation."""
        self._nettoyer_sessions()
        return {
            "version": self.VERSION,
            "active": self.active,
            "mode": "claude" if self.active else "heuristique",
            "modele": self.MODELE if self.active else "local",
            "sessions": len(self.sessions),
            "anthropic_installe": ANTHROPIC_DISPONIBLE,
        }
