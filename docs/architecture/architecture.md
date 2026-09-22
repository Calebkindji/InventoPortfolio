# Architecture INVENTO

## Architecture générale

React + TypeScript → REST API → Django + DRF → PostgreSQL

Services complémentaires :
- stockage média
- service email
- statistiques
- modération

## Organisation

Le backend est organisé par domaine fonctionnel.
Le frontend est organisé par fonctionnalités et composants réutilisables.

## API

Préfixe prévu : `/api/v1/`
