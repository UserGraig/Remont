# Utilisation de l'image de base Python 3.9
FROM python:3.9

# Définition du répertoire de travail
WORKDIR /app

# Mise à jour de pip
RUN pip install --upgrade pip

# Copie du fichier requirements.txt et installation des dépendances
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copie des fichiers du projet dans le conteneur
COPY . /app

# Exposition du port 8000 pour le serveur Django
EXPOSE 8000

# Démarrage du serveur Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
