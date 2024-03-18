# Puissance 4 en Python avec Interface Futuriste

Ce guide offre un aperçu complet de la création d'un jeu Puissance 4 en Python, utilisant Pygame pour une interface utilisateur immersive et Dash pour l'analyse statistique des performances. 

## Prérequis

Pour débuter, assurez-vous que :

1. Python est installé sur votre appareil.
2. Pygame pour l'interface et Dash pour les analyses statistiques. Installez-les via pip :
   ```python
    pip install pygame dash
    ```
4. **Configuration graphique :** Le projet inclut des ressources visuelles clés (image3, image4, image5) dans son dossier. Modifiez les chemins d'accès dans `PROJET PYTHON PUISSANCE 4.py` de cette manière :

    ```python
    background_image = pygame.image.load("votre/chemin/vers/image3")
    ```
    Adaptez "votre/chemin/vers/image3" au chemin exact sur votre système.

5. **Démarrage de l'Application :** Ouvrez `code_serveur.py` et `code_client.py`. Lancez d'abord le serveur, puis le client pour une communication optimale entre les deux.

## Fonctionnalités Principales

- **Joueur vs IA :** Relevez le défi contre une IA de différents niveaux de difficulté.
- **Joueur vs Joueur :** Un mode compétitif qui permet de jouer en réseau.
- **Interface Graphique Utilisateur :** Une expérience utilisateur améliorée grâce à une interface futuriste développée avec Pygame.
- **Analyse Statistique :** Visualisation interactive des performances via Dash, incluant victoires, défaites, et probabilités de gagner.

## Architecture du Projet

Le jeu est principalement contenu dans **PROJET PYTHON PUISSANCE 4.py**, orchestrant l'ensemble des fonctionnalités.

## Documentation et Support

Le code est accompagné de docstrings pour une documentation exhaustive, facilitant la maintenance et l'extension du projet.

## Contributeurs

- Ramzi EL MOUSSAOUI
- Matteo GIANA

Préparez-vous à des heures de divertissement et d'analyse stratégique avec ce jeu de Puissance 4 modernisé !
