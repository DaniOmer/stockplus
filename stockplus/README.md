# Stockplus Clean Architecture

Ce répertoire contient l'implémentation de Stockplus suivant les principes de Clean Architecture et Clean Code.

## Structure du Projet

```
stockplus/
├── domain/           # Entités et règles métier
│   ├── models/       # Modèles de domaine purs (sans ORM)
│   ├── services/     # Services métier
│   └── exceptions/   # Exceptions spécifiques au domaine
├── application/      # Cas d'utilisation et logique d'application
│   ├── services/     # Services d'application
│   ├── interfaces/   # Interfaces pour les repositories
│   └── dto/          # Objets de transfert de données
├── infrastructure/   # Détails techniques et frameworks
│   ├── repositories/ # Implémentations des repositories
│   ├── orm/          # Modèles Django ORM
│   ├── api/          # Vues et sérialiseurs REST
│   └── auth/         # Authentification et autorisation
├── interfaces/       # Interfaces utilisateur
│   ├── web/          # Vues web
│   ├── api/          # API REST
│   └── cli/          # Commandes CLI
└── config/           # Configuration de l'application
```

## Principes de Clean Architecture

### 1. Indépendance des Frameworks

Les modèles de domaine et la logique métier sont indépendants de tout framework. Django est utilisé uniquement dans les couches externes (infrastructure et interfaces).

### 2. Testabilité

Chaque couche peut être testée indépendamment. Les dépendances sont injectées via des interfaces, ce qui permet de les remplacer par des mocks lors des tests.

### 3. Indépendance de l'Interface Utilisateur

La logique métier ne dépend pas de l'interface utilisateur. On peut facilement changer l'interface sans modifier la logique métier.

### 4. Indépendance de la Base de Données

La logique métier ne dépend pas de la base de données. On peut facilement changer de base de données sans modifier la logique métier.

### 5. Indépendance des Détails Externes

La logique métier ne dépend d'aucun élément externe. Les détails externes dépendent de la logique métier.

## Couches

### Domain Layer

Contient les entités et les règles métier. C'est le cœur de l'application, indépendant de tout framework ou détail technique.

### Application Layer

Contient les cas d'utilisation et la logique d'application. Cette couche orchestre les entités du domaine pour accomplir des tâches spécifiques.

### Infrastructure Layer

Contient les détails techniques comme la base de données, les frameworks, etc. Cette couche implémente les interfaces définies dans la couche application.

### Interfaces Layer

Contient les interfaces utilisateur comme l'API REST, les vues web, etc. Cette couche présente les données aux utilisateurs et interprète leurs actions.

## Flux de Données

1. L'utilisateur interagit avec l'interface utilisateur (Interfaces Layer)
2. L'interface utilisateur appelle les services d'application (Application Layer)
3. Les services d'application orchestrent les entités du domaine (Domain Layer)
4. Les entités du domaine contiennent la logique métier
5. Les services d'application utilisent les repositories (Infrastructure Layer) pour persister les données
6. Les repositories convertissent les entités du domaine en modèles ORM et vice versa
7. Les modèles ORM interagissent avec la base de données

## Injection de Dépendances

Les dépendances sont injectées via le module `config/dependencies.py`. Ce module fournit des fonctions pour obtenir les services et les repositories.

## Gestion des Erreurs

Les erreurs sont gérées via des exceptions spécifiques au domaine. Ces exceptions sont capturées par les couches supérieures et converties en réponses appropriées.

## Tests

Chaque couche peut être testée indépendamment. Les tests unitaires testent les entités du domaine et les services d'application. Les tests d'intégration testent les repositories et les interfaces utilisateur.
