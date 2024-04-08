# Utiliser une image nginx comme base
FROM nginx:alpine

# Copier les fichiers statiques dans le répertoire de travail de nginx
COPY . /usr/share/nginx/html

# Copier le fichier de configuration nginx personnalisé
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exposer le port 80 pour nginx
EXPOSE 80

# Commande par défaut pour démarrer nginx
CMD ["nginx", "-g", "daemon off;"]
#http://localhost:80
