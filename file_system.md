## 1. Contexte du Projet

### 1.1 Besoins Fonctionnels
Le Data Lake doit pouvoir gérer quatre types de données distincts :
- Données transactionnelles clients (structurées)
- Logs des serveurs web (non structurés)
- Données des médias sociaux au format JSON (semi-structurées)
- Données en temps réel des campagnes publicitaires

### 1.2 Contraintes Techniques
- Déploiement sur une machine locale
- Ressources matérielles limitées
- Nécessité d'une maintenance simple
- Budget limité (environnement de développement)

## 2. Analyse des Solutions Disponibles

### 2.1 HDFS (Hadoop Distributed File System)

#### Avantages
- Conçu spécifiquement pour le Big Data
- Excellente intégration avec l'écosystème Hadoop
- Support natif des données distribuées
- Hautement scalable

#### Inconvénients
- Complexité d'installation sur une machine unique
- Consommation importante de ressources
- Configuration complexe requérant expertise
- Overhead non justifié pour un environnement local
- Dépendances multiples (Java, configuration réseau)

### 2.2 Amazon S3

#### Avantages
- Hautement scalable
- Excellent support des outils modernes
- Gestion automatique de l'infrastructure

#### Inconvénients
- Non pertinent pour un déploiement local
- Coûts associés
- Dépendance à une connexion Internet

### 2.3 Système de Fichiers Local

#### Avantages
- Disponibilité immédiate
- Simplicité d'utilisation et de maintenance
- Faible consommation de ressources
- Facilité de sauvegarde et restauration
- Compatibilité universelle avec les outils de développement
- Possibilité d'émuler la structure d'un Data Lake
- Pas de coûts additionnels

#### Inconvénients
- Pas de fonctionnalités distribuées natives
- Performances limitées aux capacités du disque local
- Scalabilité limitée

## 3. Solution Recommandée

### 3.1 Choix Technologique
Nous recommandons l'utilisation du **Système de Fichiers Local** avec une organisation hiérarchique structurée.

### 3.2 Structure Proposée
```
data_lake/
├── raw/                  # Données brutes
│   ├── transactions/     # Données transactionnelles
│   ├── web_logs/        # Logs des serveurs
│   ├── social_media/    # Données sociales
│   └── advertising/     # Données publicitaires
├── bronze/              # Données nettoyées
│   └── cleaned_data/
├── silver/              # Données transformées
│   └── transformed_data/
└── gold/               # Données préparées pour analyse
    └── curated_data/
```

## 4. Justification du Choix

### 4.1 Alignement avec les Principes Data Lake
- Respect de l'organisation en couches (raw → bronze → silver → gold)
- Possibilité de stocker les données dans leur format natif
- Support de tous les types de données requis
- Application du schéma à la lecture ("schema on read")

### 4.2 Avantages Pratiques
- **Simplicité** : Focus sur la logique métier plutôt que l'infrastructure
- **Développement** : Facilité de développement et débogage
- **Maintenance** : Gestion simple des sauvegardes et restaurations
- **Évolutivité** : Migration possible vers HDFS/S3 sans changement majeur de structure

### 4.3 Optimisations Possibles
- Utilisation de formats optimisés (Parquet) pour les données structurées
- Mise en place d'index applicatifs
- Compression des données par couche
- Partitionnement des données par date/catégorie

## 5. Stratégie d'Évolution

### 5.1 Court Terme
- Implémentation de la structure de base
- Mise en place des processus ETL
- Validation des performances sur données réelles

### 5.2 Moyen Terme
- Optimisation des formats de stockage
- Amélioration des processus de nettoyage
- Mise en place d'index et métriques

### 5.3 Long Terme
- Possibilité de migration vers une solution distribuée
- Conservation de la structure logique
- Réutilisation des scripts et processus

## 6. Conclusion

Le choix du système de fichiers local représente la solution la plus adaptée pour ce projet en environnement local. Il permet de :
- Démontrer les concepts d'un Data Lake
- Développer et tester les processus de traitement
- Maintenir une structure évolutive
- Optimiser l'utilisation des ressources disponibles

