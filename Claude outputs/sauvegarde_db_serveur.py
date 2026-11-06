"""
Sauvegarde de la base PostgreSQL du serveur (paramètres lus dans le .env, comme Django).
Lancement depuis le Mac :
  ssh -p 2222 padeb@187.77.163.177 "cd /var/www/carscosts/dBSolutionV3 && /var/www/carscosts/.venv/bin/python -" < "sauvegarde_db_serveur.py"
"""
import datetime
import os
import subprocess

import environ

env = environ.Env()
env.read_env(".env")
fichier = os.path.expanduser(f"~/avant_particuliers_{datetime.date.today():%Y-%m-%d}.dump")
os.environ["PGPASSWORD"] = env("DB_PASSWORD")
subprocess.run(
    ["pg_dump", "-Fc", "-h", env("DB_HOST", default="localhost"), "-p", str(env("DB_PORT", default="5432")),
     "-U", env("DB_USER"), "-f", fichier, env("DB_NAME")],
    check=True,
)
print(f"Sauvegarde : {fichier} ({os.path.getsize(fichier) / 1024 / 1024:.1f} Mo)")
