# Utilisez l'image Python officielle comme image de base
FROM python:3.9

# Définissez le répertoire de travail dans le conteneur
WORKDIR /app

# Copiez le fichier requirements.txt dans le conteneur
COPY requirements.txt /app/

# Installez les dépendances Python
RUN pip install -r requirements.txt

# Copiez le reste de l'application dans le conteneur
COPY . /app/

