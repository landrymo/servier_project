# SERVIER


## Partie 1 - PYTHON

### SERVIER CLASS

>- Cette classe est utilisée pour extraire les articles pour chaque médicament. Cette classe contient 3 fonctions:
>>- create_graph() : Cette fonction crée un Dataframe afin de représenter le graphique. Nous choisissons de représenter le graphique sous forme de Dataframe car nous pouvons facilement le convertir en json, il sera ensuite plus facile à manipuler.
>>- preprocessing() : prétraitement du jeu de données afin d'éviter les doublons et de supprimer les lignes inutiles afin de gagner du temps si nous traitons un jeu de données plus important.
>>- Extraction(): Pour chaque médicament, on va extraire les articles qui le citent.

>- Les fonctions extraction() et de preprocessing() traitent un seul jeu de données à la fois. J'ai choisi de les construire ainsi afin de paralléliser l'exécution pour chaque jeu de données.
En effet, le graphique est créé de telle sorte que nous pouvons être alimentés simultanément avec les publications médicales et les articles scientifiques. 
Nous appliquons ensuite 'set' à la colonne des journaux, afin d'éviter de le compter deux fois (dans le cas où deux articles du même journal citent le même médicament le même jour).

### TRAITEMENT_ADHOC

>- Fonction qui récupère tous les journaux dans notre graphique et utilise Counter pour avoir le nombre d'occurrences pour chaque journal.


### PROSPECTIVES

>- Ce code peut être parallélisé. Nous pouvons le changer en utilisant la bibliothèque multiprocessing de python.
>- Ce code utilise l'ensemble du jeu de données lors de son execution. Nous pouvons le modifier en l'appelant sur une des parties du jeu de données. Il faudrait alors définir une nouvelle fonction en selectionnant une partie du dataset. 

## Partie 2 - SQL

>- Le code SQL est disponible dans le fichier suivant SQL.sql 
