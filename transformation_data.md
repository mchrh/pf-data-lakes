# Documentation des Transformations de Données

## 1. Vue d'ensemble

Ce document décrit les différentes transformations appliquées aux données dans notre Data Lake, en suivant le processus ETL (Extract, Transform, Load) implémenté avec Apache Spark.

## 2. Pipeline de Transformation

### 2.1 Architecture Générale

Le pipeline suit une architecture en trois couches :
- **Raw Zone** : Données brutes ingérées
- **Silver Zone** : Données nettoyées et transformées
- **Gold Zone** : Données agrégées et prêtes à l'analyse

### 2.2 Technologies Utilisées

- **Apache Spark** : Framework de traitement distribué
- **PySpark** : API Python pour Spark
- **Parquet** : Format de stockage columaire optimisé

## 3. Transformations par Type de Données

### 3.1 Données Transactionnelles

#### Nettoyage :
- Suppression des doublons basée sur `transaction_id`
- Suppression des lignes avec valeurs nulles pour les champs critiques
- Conversion des types de données appropriés (timestamps, décimaux)

#### Enrichissement :
- Extraction des composants temporels (année, mois, jour, heure)
- Ajout d'indicateur pour transactions à haute valeur (> 1000)
- Calcul de métriques par client :
  * Total des dépenses
  * Nombre de transactions
  * Valeur moyenne des transactions

### 3.2 Logs Web

#### Nettoyage :
- Parsing structuré des logs
- Standardisation des timestamps
- Suppression des entrées en double

#### Enrichissement :
- Détection des appareils mobiles
- Identification des erreurs (status >= 400)
- Agrégation horaire avec métriques :
  * Nombre de requêtes
  * Nombre d'erreurs
  * Volume total de données
  * Visiteurs uniques

### 3.3 Données des Médias Sociaux

#### Nettoyage :
- Normalisation de la structure JSON
- Dédoublonnage basé sur `post_id`
- Standardisation des timestamps

#### Enrichissement :
- Extraction des composants temporels
- Analyse du contenu :
  * Comptage des tags
  * Longueur du contenu
  * Analyse de sentiment basique
  * Score de sentiment basé sur les mots-clés positifs/négatifs

### 3.4 Données Publicitaires

#### Nettoyage :
- Dédoublonnage des clics
- Standardisation des timestamps
- Conversion des types monétaires

#### Enrichissement :
- Métriques par campagne :
  * Total des clics
  * Coût total
  * Utilisateurs uniques
  * CPC moyen

## 4. Optimisations et Bonnes Pratiques

### 4.1 Performance
- Utilisation de Parquet pour le stockage optimisé
- Partitionnement des données par date
- Optimisation des jointures et agrégations

### 4.2 Qualité des Données
- Validation des types de données
- Gestion des valeurs nulles
- Dédoublonnage systématique
- Traçabilité des transformations

### 4.3 Maintenance
- Code modulaire et réutilisable
- Gestion des erreurs
- Logging des opérations
- Configuration externalisée

## 5. Utilisation du Pipeline

### 5.1 Prérequis
- Spark configuré en mode cluster ou local
- Python 3.x avec PySpark
- Accès aux zones raw et silver du Data Lake

### 5.2 Exécution
```bash
spark-submit transformation_pipeline.py
```

### 5.3 Monitoring
- Suivi via l'interface Spark UI
- Logs d'exécution
- Métriques de qualité des données

## 6. Extensions Futures

### 6.1 Améliorations Potentielles
- Analyse de sentiment plus sophistiquée
- Détection d'anomalies
- Enrichissement avec des sources externes
- Optimisation des performances

### 6.2 Points d'Attention
- Scaling des transformations
- Gestion de la mémoire
- Optimisation des agrégations
- Maintenance des dépendances

## 7. Architecture de Données

### 7.1 Modèle de Données Silver
Pour chaque type de données, le format suivant est utilisé dans la zone silver :

#### Transactions
```
- transaction_id: string (PK)
- customer_id: string (FK)
- amount: decimal(10,2)
- transaction_date: timestamp
- year: integer
- month: integer
- day: integer
- hour: integer
- is_high_value: boolean
- total_spent: decimal(10,2)
- transaction_count: integer
- avg_transaction_value: decimal(10,2)
```

#### Logs Web
```
- year: integer
- month: integer
- day: integer
- hour: integer
- request_count: long
- error_count: long
- total_bytes: long
- unique_visitors: long
```

#### Médias Sociaux
```
- post_id: string (PK)
- user_id: string
- content: string
- timestamp: timestamp
- year: integer
- month: integer
- day: integer
- hour: integer
- tag_count: integer
- content_length: integer
- sentiment_score: integer
```

#### Publicité
```
- campaign_id: string
- year: integer
- month: integer
- day: integer
- total_clicks: long
- total_cost: decimal(10,4)
- unique_users: long
- avg_cpc: decimal(10,4)
```