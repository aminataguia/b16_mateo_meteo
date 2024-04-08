# Utiliser une image de base Python
FROM python:3.8-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers nécessaires dans le conteneur
COPY . /app

# Installer les dépendances
RUN pip install meteofrance_api psycopg2-binary

# Exécuter le script Python
CMD CMD ["uvicorn", "bulletin_voice:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
