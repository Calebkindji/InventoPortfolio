# INVENTO

Plateforme web de création, gestion et publication de portfolios professionnels.

## Maquette visuelle

Maquette Figma INVENTO :
https://www.figma.com/design/aQAZrIAtNRFF2gO22e0PUJ/invento?t=FF755xlCAlLsfMED-0

La maquette constitue la référence visuelle du projet.

## Vision

INVENTO permet à un utilisateur de créer une identité professionnelle numérique et de publier son portfolio sans devoir développer ou héberger lui-même un site web.

Flux principal :

1. Créer un compte
2. Compléter son profil
3. Ajouter compétences, expériences, formations et certifications
4. Ajouter des projets
5. Prévisualiser le portfolio
6. Publier ou masquer le portfolio
7. Partager son URL publique

Chaque utilisateur dispose d'une URL publique de type `/u/username`.

## Technologies

### Frontend
- React
- TypeScript
- Vite
- Material UI
- React Router
- Axios

### Backend
- Python
- Django
- Django REST Framework
- JWT

### Base de données
- PostgreSQL

## Structure

- `backend/` : API Django/DRF
- `frontend/` : application React
- `docs/` : documentation, cahier des charges et diagrammes
- `.github/` : workflows GitHub et modèles de contribution

## Démarrage

Le projet est actuellement un squelette destiné à accueillir le développement de l'équipe.

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Git

Branche principale :
- `main`

Branche de développement :
- `develop`

Exemples de branches :
- `feature/authentication`
- `feature/profile`
- `feature/projects`
- `feature/portfolio`
- `feature/exploration`
- `feature/admin`

Les fonctionnalités sont développées sur une branche dédiée puis intégrées à `develop` par Pull Request.

## Statut

Projet en phase de mise en place de l'architecture et du dépôt GitHub.
