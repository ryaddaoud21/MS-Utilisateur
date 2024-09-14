# Utilisation de l'image Python
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le reste du projet
COPY . .

# Exposer le port Flask
EXPOSE 5004

# Commande pour démarrer le serveur Flask
CMD ["waitress-serve", "--port=5004", "auth_api:app"]
