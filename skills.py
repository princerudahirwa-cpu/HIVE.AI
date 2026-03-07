# skills.py - Point d'entree unifie des Skills HIVE.AI
# Agregation des 37 Skills Souverains (Reine) + 9 Skills Worker
# "Polyvalente et digne. Jamais etroitement specialisee."
#
# Swarmly SAS - 2026

from skills_reine import SKILLS_SOUVERAINS
from skills_worker import SKILLS_WORKER, executer_skill as executer_worker
from skill_consulter import SKILL_INFO as CONSULTER_INFO, executer as executer_consulter
from skill_bibliotheque import SKILL_INFO as BIBLIO_INFO, executer as executer_bibliotheque
from skill_science import SKILL_INFO as SCIENCE_INFO, executer as executer_science
from skill_medecine import SKILL_INFO as MEDECINE_INFO, executer as executer_medecine
from skill_alexandrie_v2 import (
    SKILLS_ALEXANDRIE_V2, SKILL_INFO as ALEX_INFO,
    executer as executer_alexandrie,
)


class SkillsManager:
    """Gestionnaire unifie de tous les skills du HIVE."""

    def __init__(self):
        self._souverains = {**SKILLS_SOUVERAINS, "consulter": {
            "numero": 25,
            "domaine": CONSULTER_INFO["domaine"],
            "description": CONSULTER_INFO["description"],
            "version": CONSULTER_INFO["version"],
            "module": "skill_consulter",
        }, "bibliotheque": {
            "numero": 26,
            "domaine": BIBLIO_INFO["domaine"],
            "description": BIBLIO_INFO["description"],
            "version": BIBLIO_INFO["version"],
            "module": "skill_bibliotheque",
        }, "science": {
            "numero": 27,
            "domaine": SCIENCE_INFO["domaine"],
            "description": SCIENCE_INFO["description"],
            "version": SCIENCE_INFO["version"],
            "module": "skill_science",
        }, "medecine": {
            "numero": 28,
            "domaine": MEDECINE_INFO["domaine"],
            "description": MEDECINE_INFO["description"],
            "version": MEDECINE_INFO["version"],
            "module": "skill_medecine",
        }}

        # Alexandrie v2 — 9 skills (#29-#37)
        _alex_names = [
            "actualites", "dictionnaire", "traduction",
            "astronomie", "meteo", "pays",
            "monnaie", "geographie", "cinema",
        ]
        for i, nom in enumerate(_alex_names, 29):
            info = SKILLS_ALEXANDRIE_V2[nom]
            self._souverains[nom] = {
                "numero": i,
                "domaine": info["domaine"],
                "description": info["description"],
                "version": ALEX_INFO["version"],
                "module": "skill_alexandrie_v2",
            }

        self._workers = SKILLS_WORKER

    def list_skills(self):
        """Retourne la liste de tous les noms de skills."""
        souverains = {f"reine:{nom}" for nom in self._souverains}
        workers = {f"worker:{nom}" for nom in self._workers}
        return souverains | workers

    def count(self):
        """Nombre total de skills."""
        return len(self._souverains) + len(self._workers)

    def get(self, nom):
        """Retourne les metadonnees d'un skill par nom."""
        if ":" in nom:
            scope, key = nom.split(":", 1)
            if scope == "reine" and key in self._souverains:
                return {"scope": "reine", "nom": key, **self._souverains[key]}
            if scope == "worker" and key in self._workers:
                info = self._workers[key]
                return {"scope": "worker", "nom": key, "categorie": info["categorie"], "description": info["description"]}
        if nom in self._souverains:
            return {"scope": "reine", "nom": nom, **self._souverains[nom]}
        if nom in self._workers:
            info = self._workers[nom]
            return {"scope": "worker", "nom": nom, "categorie": info["categorie"], "description": info["description"]}
        return None

    def list_souverains(self):
        """Retourne les noms des skills souverains."""
        return sorted(self._souverains.keys())

    def list_workers(self):
        """Retourne les noms des 9 skills worker."""
        return sorted(self._workers.keys())

    def executer_worker(self, nom, *args, **kwargs):
        """Execute un skill worker par nom."""
        return executer_worker(nom, *args, **kwargs)

    def consulter(self, params):
        """Execute reine:consulter (Wikipedia)."""
        return executer_consulter(params)

    def bibliotheque(self, params):
        """Execute reine:bibliotheque (OpenLibrary)."""
        return executer_bibliotheque(params)

    def science(self, params):
        """Execute reine:science (arXiv)."""
        return executer_science(params)

    def medecine(self, params):
        """Execute reine:medecine (PubMed)."""
        return executer_medecine(params)

    def alexandrie(self, nom_skill, params):
        """Execute un skill Alexandrie v2 par nom."""
        return executer_alexandrie(nom_skill, params)
