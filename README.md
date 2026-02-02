## Contexte

Projet réalisé dans le cadre d’un stage de fin de formation
Objectif : concevoir une interface utilisateur moderne, sécurisée et maintenable.


---

## README — **Backend**
 Repo : `red-product-backend`

```md
# RED PRODUCT – Backend API

##  Description
Ce dépôt contient l’API REST de la plateforme RED PRODUCT.
Le backend gère l’authentification, les utilisateurs et les données
nécessaires au fonctionnement de l’application frontend.

L’API est sécurisée grâce à JWT et au package Djoser.

---

##  Technologies utilisées
- Python
- Django
- Django REST Framework (DRF)
- Djoser
- JWT (JSON Web Token)
- Base de données : SQLite / PostgreSQL (selon environnement)

---

##  Authentification & Sécurité
- Authentification par email et mot de passe
- Tokens JWT (`access` / `refresh`)
- Activation de compte par email
- Réinitialisation du mot de passe
- Protection des endpoints sensibles

---

##  Endpoints principaux

### Connexion
POST /api/auth/jwt/create/


### Inscription


POST /api/auth/users/


### Activation de compte


POST /api/auth/users/activation/


### Renvoyer email d’activation


POST /api/auth/users/resend_activation/


### Profil utilisateur connecté


GET /api/auth/users/me/


### Mot de passe oublié


POST /api/auth/users/reset_password/


### Réinitialisation du mot de passe


POST /api/auth/users/reset_password_confirm/


---

##  Installation

###  Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

## Installer les dépendances
pip install -r requirements.txt

## Migrations
python manage.py migrate

## Lancer le serveur
python manage.py runserver


L’API sera accessible sur :http://127.0.0.1:8000

## Variables d’environnement (exemple)
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=...
EMAIL_HOST=...

 Frontend

Cette API est consommée par le frontend React disponible ici :
 Repo Frontend : (ajouter le lien GitHub)

## Contexte

Projet réalisé dans le cadre d’un stage de fin de formation
Objectif : mettre en place une API REST sécurisée et professionnelle.
