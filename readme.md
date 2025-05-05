
# 🏴‍☠️ Heart Pirates

**Heart Pirates** est une application médicale web développée avec **Django**. Elle permet de :
- Gérer des patients
- Enregistrer des consultations
- Émettre des ordonnances et factures
- Télécharger les documents générés au format PDF

---

## 🚀 Fonctionnalités

- Création et gestion de patients
- Ajout de consultations médicales
- Génération d’ordonnances et factures
- Téléchargement des ordonnances et factures en PDF
- Interface utilisateur stylisée avec **Tailwind CSS**

---

## ⚙️ Prérequis

Avant de démarrer, assure-toi d’avoir installé :

- Python 3.x
- MySQL (ou MariaDB)
- pip

---

## 🛠️ Installation

1. **Cloner le projet**
   ```bash
   git clone [https://github.com/ton-utilisateur/heart-pirates.git](https://github.com/POO-AVANCE-PROJET-IAI/GLSI-A-OURO-BANG-NA-Taoufik.git)
   cd heart-pirates
   ```

2. **Créer un environnement virtuel**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. **Installer les dépendances**

   ```bash
   pip install django mysqlclient xhtml2pdf
   ```

4. **Configurer la base de données**

   - Crée une base de données MySQL (nom au choix)
   - Configure la connexion dans le fichier `settings.py` :

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'nom_de_ta_base',
           'USER': 'ton_utilisateur',
           'PASSWORD': 'ton_mot_de_passe',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

5. **Appliquer les migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Créer les données de base**

   ⚠️ **L’ordre est important pour les commandes suivantes :**

   ```bash
   python manage.py create_users
   python manage.py create_act_type
   python manage.py create_acts
   python manage.py create_medicines
   ```

   - Les utilisateurs par défaut se trouvent dans le fichier :
     `management/commands/create_users.py`
   - Vous pouvez modifier les 3 utilisateurs par défaut :
     ```json
     {
         "username": "taoufik",
         "email": "taoufik@gmail.com",
         "password": "taoufik"
     },
     {
         "username": "mei",
         "email": "mei@gmail.com",
         "password": "taoufik"
     },
     {
         "username": "fifi",
         "email": "fifi@gmail.com",
         "password": "taoufik"
     }
     ```

   👉 Il n’y a **pas de page d’inscription** dans l’application. Ces utilisateurs servent à la connexion.

7. **Lancer le serveur**
   ```bash
   python manage.py runserver
   ```

---

## 📄 Génération de PDF

L’application utilise `xhtml2pdf` pour générer les ordonnances et factures en PDF. Assure-toi que cette bibliothèque est bien installée :

```bash
pip install xhtml2pdf
```

---

## 🎨 Interface utilisateur

- Frontend simple basé sur **Tailwind CSS**
- Utilisation du moteur de templates de Django (`{{ }}`)

---

## 👤 Auteur

Développé par Taoufik OURO-BANG'NA.

