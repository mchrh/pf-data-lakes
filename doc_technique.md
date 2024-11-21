# Documentation Technique de l'Infrastructure Data Lake

## 1. Vue d'ensemble de l'Architecture

Notre infrastructure repose sur trois composants principaux :
- Un système de fichiers local pour la structure du Data Lake
- Hadoop en mode pseudo-distribué pour le stockage distribué
- Spark pour le traitement distribué des données

## 2. Choix Technologiques

### 2.1 Versions des Composants
- Hadoop 3.3.6
- Spark 3.5.0
- Java 11
- Scala 2.12

### 2.2 Justification des Choix

#### Hadoop en Mode Pseudo-distribué
- **Justification** : 
  * Permet de simuler un environnement distribué sur une machine unique
  * Compatible avec les besoins du projet définis dans les slides
  * Facilite la transition future vers un cluster réel
  * Permet l'utilisation de HDFS pour le stockage distribué
- **Configuration** :
  * NameNode et DataNode sur la même machine
  * Replication factor = 1 pour économiser l'espace
  * YARN comme gestionnaire de ressources

#### Apache Spark
- **Justification** :
  * Traitement in-memory pour de meilleures performances
  * Support natif de multiples formats de données
  * API unifiée pour batch et streaming
  * Intégration native avec Hadoop
- **Configuration** :
  * Mode YARN pour la gestion des ressources
  * Mémoire limitée pour s'adapter à une machine locale
  * Support du streaming pour les données en temps réel

## 3. Organisation du Stockage

### 3.1 Structure HDFS
```
/data_lake/
├── raw/              # Données brutes
├── bronze/           # Données nettoyées
├── silver/           # Données transformées
└── gold/            # Données analysées
```

### 3.2 Configuration du Stockage
- Système de fichiers local pour les données temporaires
- HDFS pour le stockage persistant
- Réplication minimale pour économiser l'espace

## 4. Configuration des Ressources

### 4.1 Hadoop
- NameNode : 512MB de mémoire
- DataNode : 512MB de mémoire
- YARN ResourceManager : 512MB de mémoire

### 4.2 Spark
- Driver : 512MB de mémoire
- Executor : 512MB de mémoire
- Application Master : 512MB de mémoire

## 5. Procédures de Déploiement

### 5.1 Prérequis
- Ubuntu/Debian OS
- Minimum 8GB RAM
- 20GB espace disque disponible
- Accès administrateur

### 5.2 Étapes de Déploiement
1. Installation des dépendances
2. Configuration SSH
3. Installation et configuration Hadoop
4. Installation et configuration Spark
5. Initialisation HDFS
6. Création structure Data Lake

## 6. Démarrage des Services

### 6.1 Ordre de Démarrage
1. Démarrer HDFS :
```bash
start-dfs.sh
```

2. Démarrer YARN :
```bash
start-yarn.sh
```

3. Vérifier les services :
```bash
jps
```

### 6.2 Vérification du Déploiement
- Interface Web HDFS : http://localhost:9870
- Interface Web YARN : http://localhost:8088
- Interface Web Spark : http://localhost:4040 (actif pendant les jobs)

## 7. Considérations de Performance

### 7.1 Optimisations
- Configuration mémoire adaptée à une machine locale
- Limitation du parallélisme pour éviter la surcharge
- Utilisation du stockage local pour les données temporaires

### 7.2 Limitations
- Performances limitées par les ressources de la machine
- Pas de haute disponibilité
- Capacité de stockage limitée

## 8. Sécurité

### 8.1 Configuration Minimale
- SSH avec clés pour l'authentification
- Ports par défaut pour le développement
- Pas d'authentification Kerberos (environnement local)

## 9. Maintenance

### 9.1 Tâches Régulières
- Nettoyage des fichiers temporaires
- Vérification des logs
- Monitoring des ressources

### 9.2 Dépannage
- Logs Hadoop : `$HADOOP_HOME/logs/`
- Logs Spark : `$SPARK_HOME/logs/`
- Logs YARN : Interface web YARN

## 10. Évolution Future

### 10.1 Possibilités d'Extension
- Migration vers un cluster réel
- Ajout de nœuds worker
- Intégration d'outils complémentaires (Hive, HBase)

### 10.2 Points d'Attention
- Dimensionnement des ressources
- Gestion de la scalabilité
- Sécurisation de l'infrastructure