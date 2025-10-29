# Application de Gestion des Tickets – Helpdesk Eneo Cameroon
![Aperçu de l'application](illustration.png)
## Description du projet

Cette application a été développée en Python avec Tkinter pour l’interface graphique et MySQL pour la gestion des données.
Elle permet de gérer les tickets de support technique (Helpdesk) au sein d’une entreprise, notamment :

- L’enregistrement des nouveaux tickets (clients, matériel, technicien, etc.)
- La modification, suppression et mise à jour de tickets existants
- Le suivi des statuts : Helpdesk, Labo, Prestataire, Terminé
- Le filtrage et la visualisation des tickets selon leur statut
- L’affichage en temps réel du nombre total de tickets pour chaque catégorie

L’interface est simple, fluide et intuitive, permettant à un technicien ou un gestionnaire du support de suivre efficacement les interventions.

## Fonctionnalités principales
### Gestion des tickets

- Création automatique d’un matricule unique pour chaque ticket (ex : Helpdesk_1, Helpdesk_2, …).

- Enregistrement des informations client et matériel.

- Suivi du diagnostic, des solutions proposées et du statut du ticket.

### Interface utilisateur (Tkinter)

- Formulaire complet pour la saisie et la mise à jour des informations.

- Listes déroulantes pour la date et les statuts.

- Tableau interactif pour visualiser les tickets enregistrés.

- Filtres dynamiques (tous, non terminés, helpdesk, labo, prestataire, terminés).

### Base de données MySQL

- Table principale : `Client`

- Gestion sécurisée des connexions avec `mysql.connector`.

- Requêtes SQL pour toutes les opérations CRUD (Create, Read, Update, Delete).

### Structure de la base de données

Table : Client

| Colonne            | Type          | Description                          |
|--------------------|---------------|--------------------------------------|
| matricule          | VARCHAR(50)   | Identifiant unique (ex : Helpdesk_1) |
| nom                | VARCHAR(100)  | Nom du client                        |
| prenom             | VARCHAR(100)  | Prénom du client                     |
| telephone          | VARCHAR(20)   | Numéro de téléphone                  |
| Unite              | VARCHAR(100)  | Unité ou service concerné            |
| Materiel           | VARCHAR(100)  | Type de matériel                     |
| numero_serie       | VARCHAR(100)  | Numéro de série du matériel          |
| Modele             | VARCHAR(100)  | Modèle du matériel                   |
| Nom_technicien     | VARCHAR(100)  | Nom du technicien assigné            |
| date               | DATE          | Date de création/modification        |
| diagnostics        | TEXT          | Diagnostic effectué                  |
| solutions_propose  | TEXT          | Solutions proposées                  |
| statut             | VARCHAR(50)   | Statut du ticket                     |


 ## Installation et configuration
### Prérequis

- Python 3.8 ou supérieur

- MySQL Server installé et configuré

- Les bibliothèques Python suivantes :

`pip install mysql-connector-python`

### Création de la base de données

Exécuter dans MySQL :

`CREATE DATABASE Helpdesk; USE Helpdesk;`

`CREATE TABLE Client (matricule VARCHAR(50) PRIMARY KEY, nom VARCHAR(100),`
    `prenom VARCHAR(100), telephone VARCHAR(20), Unite VARCHAR(100),`
    `Materiel VARCHAR(100), numero_serie VARCHAR(100), Modele VARCHAR(100),`
    `Nom_technicien VARCHAR(100), date DATE, diagnostics TEXT,`
    `solutions_propose TEXT, statut VARCHAR(50));`

### Configuration du mot de passe

Dans le script Python, mets à jour tes identifiants de connexion :

`return mysc.connect(host="localhost", user="root", password="ROOT", database="Helpdesk")`


⚠️ Remplace "ROOT" par ton propre mot de passe MySQL si besoin.

## Exécution du programme

Lance le fichier Python :

`python gestion_tickets.py`


L’interface s’ouvrira automatiquement.

Tu pourras ajouter, modifier, supprimer ou filtrer les tickets selon tes besoins.

## Interface utilisateur
| Élément            | Description   |
|--------------------|---------------|
| Formulaire à gauche	| Permet la saisie des informations client et matériel  |
| Liste des tickets à droite                | Affiche tous les tickets selon le filtre sélectionné |
| Filtres en haut du tableau	Sélection rapide|             | Tous, Non clôturés, Helpdesk, Labo, Prestataire, Terminés |
| Boutons d’action|Enregistrer, Modifier, Supprimer|
	
## Technologies utilisées

- <b>Langage</b> : Python 3 

- <b>Interface graphique </b>: Tkinter

- <b>Base de données </b>: MySQL

- <b>Librairies </b>: mysql, tkinter.ttk, messagebox

## Auteur

- <b>Développé par </b>: Cyr DJOKI
- <b>Organisation </b>: Eneo Cameroon – Département Helpdesk
- <b>Contact </b>: djokicyr@gmail.com

