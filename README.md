# SPYTHOON

## Le Splatoon® en Python

## Description

Spythoon est un jeu développé en Python, s'appuyant sur la librairie [PytactX par Jusdeliens](https://jusdeliens.com/). et inspiré du jeu vidéo Splatoon®.

> Une équipe de 3 robots se défient sur une arène, dans l'objectif de recouvrir la plus grande surface de cette arène de la couleur de son équipe dans le temps imparti.

## Contexte & Cahier des charges

J'ai développé ce jeu dans le cadre d'une formation en développement d'applications. Le sujet du module portait sur le langage Python et le bonnes pratiques de programmation (SOLID, POO, ...).

L'objectif a été de réaliser un jeu pour des apprenants, afin de les initier à la programmation et à Python.

## Objectif du jeu

Recouvrir le plus de cases possibles de la couleur d'équipe en un temps donné.
_Taille du terrain : 12x26_

## Règles du jeu

![maquette du jeu](docs/maquette.png)

Le jeu se compose d'une arène de 12x26 cases.

Chaque équipe possède 3 robots, pouvant se déplacer dans toutes les directions horizontales et verticales.

Ces robots ont la capacité de peindre chacune des cases de l'arène afin d'augmenter le score de leur équipe.

L'équipe gagnante est celle ayant le plus grand score, donc le plus de cases colorées de sa couleur.

## Use Cases

### Capacités de l'agent du joueur

-[x] Apparition dans l'arène, dans une zone d'équipe circulaire définie en amont par la carte -[x] Se déplacer sur la carte en relatif, en X et en Y, sur la direction du regard -[x] Pivoter sur lui-même dans les 4 directions : N, S, E, W

- Identifier si une case est "neutre" (= sans peinture) / Identifier si une case est recouverte de sa couleur ou de celle de l'adversaire. ~~Identifie les cases sur une surface de 5x5 cases~~.
- [x] Activer le spray pour colorer les cases
  - [x] Lorsque on active le spray, toutes les cases sur lesquelles le robot passe se colorent de la couleur de l'équipe de manière permanente tant qu'un adversaire ne passe pas dessus
  - [x] Lorsque le spray est activée, la vitesse de déplacement du robot est réduite
- [x] Recouvrir les cases déjà couvertes par un adversaire lorsque l'agent arrive dessus
- [x] Il est possible de savoir quel agent se trouve dans notre range, et d'identifier si c'est un allié ou un ennemi

#### Options supplémentaires envisageable dans une prochaine version

- Identifier des cases de "loot"
- Se déplacer vers des cases de "loot" de manière absolue en automatique (implémenter le _moveToward()_ dans le painter Spythoon), tout en gardant la possibilité d'interrompre le déplacement
- les cases de loots permettent d'avoir un boost temporaire de spray, modifiant la largeur du spray

## Développements

### Tâches en cours

#### Création d'une interface graphique

Création d'une interface graphique à l'aide de PyQt5, à destination de l'arbitre et des joueurs dans l'idéal.

**Étapes validées**

- [x] affichage d'une fenêtre de bureau avec les visuels de l'arène
- [x] générer une grille invisible correspondant aux cases de l'arène
- [x] pouvoir colorer les cases de la grille selon leur état dans le jeu

**Étapes en cours**

- [ ] décomposer les différents éléments de l'interface en classes
- [ ] mettre à jour le temps restant
- [ ] mettre à jour les scores des équipes
- [ ] afficher les joueurs sur l'interface
- [ ] déplacer les joueurs sur l'interface
- [ ] créer un onglet de connexion avant d'arriver sur l'arène
