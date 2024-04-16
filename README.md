# b16_mateo
## Mateo - Application d'IA Météorologique
## Sommaire 

Veillez trouver dans se read me les chapitres suivants :
1. Introduction
2. Requirements
3. Contenu des fichiers
4. Azure 

### introduction
Dans un monde où les conditions météorologiques jouent un rôle crucial dans la planification quotidienne et les décisions stratégiques, il est essentiel de disposer d'outils efficaces pour accéder à des informations météorologiques précises et actualisées. Cependant, de nombreuses applications météorologiques actuelles manquent d'interactivité et de personnalisation, ce qui limite leur utilité pour les utilisateurs. Afin de combler cette lacune, le projet Mateo propose le développement d'une application d'IA météorologique novatrice, offrant une expérience utilisateur améliorée grâce à des fonctionnalités de synthèse vocale, de personnalisation et d'interactivité.

### Requirements 
### Azur 
Il faut sachez que deux ficheir sont dockeriser et push sur azur , Pour se brief il sagit de la partie backend_nlp et de la partie front-end .
Dans le grouep de ressource taguiasimplon veillez trouver le registre de conteneur b16meteo contenant lui meme eux instances de conteneur : taguia front 

### Contenu des fichiers
mon-application/
│
├── backend/                 # Dossier contenant le back-end de l'application
│   ├── backend_nlp/         # l'application plus particulierement la generation de texte principaux de l'application
│   │   ├── main.py          # La generation de texte puis de voix
│   │   ├── fonctions.py     # Contient des fonctions utilitaires ou spécifiques à l'application
│   │   ├── connexion.py     # Contient le fichier de connexion à ma bdd
│   └── Dockerfiles/         # Dossiers contenant les Dockerfiles pour la construction des images Docker de cette partie
│
│   ├── backend_sql/         # l'application plus particulierement la generation de texte principaux de l'application
│   │   ├── main.py          # qui est le coeur de la recuperation de la data vers ma bdd
│   │   ├── connexion.py     # Contient le fichier de connexion à ma bdd
│   │   ├── fonctions.py     # Contient des fonctions utilitaires ou spécifiques à l'application
│   │   ├── raffraichisseur_data.ps1 # Script PowerShell pour rafraîchir les données (qui sera sans doute dans un gitignore)
│   │   ├── recup.py         # fonction pour récupérer les données météorologiques
│   │   ├── test.py          # test pour recuperer les données
│   │   └── villes.py        # Liste des villes pour lesquelles les données
│
├── frontend/                 # Dossier contenant le front-end de l'application
│   ├── index.html            # Page d'accueil HTML
│   ├── styles.css            # Fichiers CSS pour le style de l'application
│   └── scripts.js            # Fichiers JavaScript pour la logique de l'application
│
├── .gitignore                # Fichiers et dossiers à ignorer par Git
└── README.md                 # Le fichier que vous lisez actuellement

