# Simulation Poule Renard Vipère

Ce projet Python simule un environnement de jeu en utilisant la bibliothèque pygame. Le jeu implique trois types d'entités : des serpents, des poules et des renards, chacun ayant des comportements et des interactions spécifiques. Les entités se déplacent dans la fenêtre de jeu, évitant les obstacles et certaines zones restreintes tout en essayant de capturer ou d'échapper à d'autres entités.

## Règles du jeu
1. Les serpents chassent les renards et fuient les poules.
2. Les poules chassent les serpents et fuient les renards.
3. Les renards chassent les poules et fuient les serpents.
4. Les entités se déplacent en évitant les obstacles et les zones restreintes spécifiques à chaque tribu.
5. Le groupe d'animaux ayant attrapé l'ensemble de ses proies a gagné.
#
## Structure du code 

Le code est structuré en plusieurs sections principales :

1. Initialisation de pygame et définition des constantes.
2. Chargement des images de fond, des icônes des entités et des obstacles.
3. Définition des classes Entity et Obstacle.
4. Définition des fonctions utilitaires.
5. Création des entités et des obstacles.
6. Boucle principale du jeu.
## Documentation

[Documentation](./Documentation.pdf)


## Installation

Assurez-vous que Python est installé sur votre système.
Installez les bibliothèques nécessaires :

```bash
  pip install pygame
```
## Utilisation
Pour exécuter le jeu, utilisez la commande suivante :

```python
simulation.py
```
