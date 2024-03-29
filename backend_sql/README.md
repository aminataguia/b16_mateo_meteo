# b16_mateo
## Mateo - Application d'IA Météorologique

### introduction
Dans un monde où les conditions météorologiques jouent un rôle crucial dans la planification quotidienne et les décisions stratégiques, il est essentiel de disposer d'outils efficaces pour accéder à des informations météorologiques précises et actualisées. Cependant, de nombreuses applications météorologiques actuelles manquent d'interactivité et de personnalisation, ce qui limite leur utilité pour les utilisateurs. Afin de combler cette lacune, le projet Mateo propose le développement d'une application d'IA météorologique novatrice, offrant une expérience utilisateur améliorée grâce à des fonctionnalités de synthèse vocale, de personnalisation et d'interactivité.

### mon-application/
│
├── backend/                 # Dossier contenant le back-end de l'application
│   ├── app/                 # Dossier contenant les fichiers principaux de l'application
│   │   ├── main.py          # Point d'entrée de l'application
│   │   ├── fonctions.py     # Contient des fonctions utilitaires ou spécifiques à l'application
│   │   ├── raffraichisseur_data.ps1 # Script PowerShell pour rafraîchir les données (à vérifier si nécessaire)
│   │   ├── recup.py         # Script pour récupérer les données météorologiques
│   │   └── villes.py        # Liste des villes pour lesquelles les données météorologiques sont récupérées
│   ├── generator/           # Dossier contenant des scripts ou des outils pour générer des données
│   │   └── voice_generator.py # Script pour générer des voix (à vérifier si nécessaire)
│   └── Dockerfiles/         # Dossiers contenant les Dockerfiles pour la construction des images Docker
│
├── frontend/                 # Dossier contenant le front-end de l'application
│   ├── index.html            # Page d'accueil HTML
│   ├── styles.css            # Fichiers CSS pour le style de l'application
│   └── scripts.js            # Fichiers JavaScript pour la logique de l'application
│
├── .gitignore                # Fichiers et dossiers à ignorer par Git
├── README.md                 # Documentation du projet
└── ...                       # Autres fichiers et dossiers spécifiques au projet

d'autre fichier sont en cours de création :)
