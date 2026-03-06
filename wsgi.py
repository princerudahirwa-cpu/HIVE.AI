# wsgi.py -- Point d'entree WSGI pour production
# Gunicorn cible ce fichier : gunicorn wsgi:app
#
# La Reine s'eveille. Le Bureau de Commandement ouvre ses portes.
#
# Swarmly SAS · 2026

import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv optionnel en dev

from serveur_hive import app, boot_sequence

# Boot au demarrage du worker Gunicorn
boot_sequence()
