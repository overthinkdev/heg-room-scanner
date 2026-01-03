# HEG Room Scanner

**HEG Room Scanner** est une application Python avec interface graphique (Tkinter) permettant de vérifier en temps réel la disponibilité des salles à la HEG Genève.  
Elle interroge le site officiel de la HEG pour détecter si une salle est libre ou occupée, puis affiche les résultats de manière structurée par étage.

Ce projet a pour but de faciliter la vie des collaborateurs/étudiants pour des fins académiques.

---

## Fonctionnalités

- ✅ Interface utilisateur avec Tkinter
- ✅ Scan automatique des salles définies
- ✅ Affichage en arborescence des salles libres et occupées
- ✅ Double-clic pour ouvrir la page web d’une salle
- ✅ Barre de progression et animation pendant le scan
- ✅ Journal de log intégré (debug)

---

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/overthinkdev/heg-room-scanner.git
cd heg-room-scanner
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Lancer l’application

```bash
python gui.py
```

## Structure du projet

```
heg-room-scanner/
├── core.py           # Logique principale (scan des salles, requêtes HTTP)
├── gui.py            # Interface graphique (Tkinter)
├── README.md         # Documentation du projet
├── LICENSE           # Licence MIT
└── requirements.txt  # Dépendance externe (requests)
```

---

## À propos

Ce projet a été développé dans un cadre personnel par un étudiant de la HEG Genève afin de faciliter la recherche de salles disponibles sur le campus.  
Il est mis à disposition librement et peut être adapté à d'autres établissements ou contextes similaires.

## Licence

Ce projet est distribué sous la licence MIT.  
Vous êtes libre de l’utiliser, modifier et redistribuer en respectant les conditions de cette licence.

## Auteur

**Rami M.** — Étudiant en informatique de gestion à la HEG Genève  
GitHub : [@overthinkdev](https://github.com/overthinkdev)
