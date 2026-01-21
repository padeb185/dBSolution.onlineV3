import os

for root, dirs, files in os.walk('.'):
    if 'migrations' in root:
        for f in files:
            if f.endswith('.py') and f != '__init__.py':
                os.remove(os.path.join(root, f))
                print(f"Supprimé: {os.path.join(root, f)}")




import os

for root, dirs, files in os.walk("."):
    if "migrations" in root:  # seulement dans les dossiers migrations
        for file in files:
            if file.endswith(".pyc"):
                file_path = os.path.join(root, file)
                print(f"Supprimer {file_path}")
                os.remove(file_path)
