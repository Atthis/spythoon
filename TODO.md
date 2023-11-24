## TODO

- [ ] definir des comportements specifiques pour pouvoir tester les differentes fonctions des joueurs -> fichier test_server
- [x] clarifier les différentes fonctions et refactoriser si possible
- [x] créer un bg sympa pour le fond de carte
- [ ] travailler sur le readme afin qu'il explicite les différentes règles du jeu
- [ ] ~~diminuer la portée du range des joueurs~~ Annulé pour le moment, les joueurs voient tout le monde
- [ ] ~~diminuer la portée de la map pour voir moins de cases~~ Annulé pour le moment, les joueurs voient toute la carte
- [ ] MAJ Majeure : empêcher les joueurs de se déplacer tant que tout le monde n'est pas connecté

### TODO bonus

- [x] définir un profil correspondant pour le ralentissement des joueurs lorsqu'ils tirent

### Problemes

- pas de reset de toutes les cases de la carte au reset de la partie -> voir comment faire dans la classe referee
- rotation des joueurs à leur connexion

### TODO annexes dev

- [ ] créer les diagrammes de classe et de séquences de l'écosystème

### PYQT5

#### Choses à voir

- [x] ajouter une image de fond à un widget
- [x] superposer 2 éléments l'un sur l'autre
- [x] caler toute l'interface pour avoir quelque chose de propre
- [ ] éclater les différentes créations d'éléments de l'interface dans des classes spécifiques
- [ ] prévoir une interface de connexion en amont de l'interface d'arène
  - [ ] créer les éléments d'interface
  - [ ] voir comment récupérer les valeurs entrées pour les envoyer dans la création de joueur
  - [x] voir comment charger l'interface sans être bloqué par une boucle de jeu
- [ ] brancher les données reçues via Pytactx à l'interface
- [ ] définir une méthode pour colorer les cases de la carte selon la valeur de celle-ci
- [ ] avoir l'affichage des joueurs sur l'interface

### Interrogations PyQt5

- ~~Comment gérer le dimensionnement de la fenêtre et de ses éléments~~
- Créer plusieurs fenêtres dans l'application (fenêtre de connexion / fenêtre d'arène)
- ~~Mettre la fenêtre en plein écran, et avoir des scroll bar si jamais la fenêtre est trop petite~~ -> option ignorée pour le moment, fenêtre de taille fixe choisie
