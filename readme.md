# Projet Final Data Lake

Groupe composé de : 
- Othmane Machrouh
- Ayoub Larouji
- Sabry Ben Aissa


Documents techniques : 
- Un document de conception détaillé décrivant l'architecture du Data Lake : architecture_data_lake.md
- Un diagramme des flux de données : diagramme.png
- Choix des technologies pour le stockage : file_system.md
- Documentation technique sur les choix de technologies : doc_technique.md
- Documentation sur les différentes transformations appliquées aux données : transformation_data.md
- Document décrivant la Politique de sécurité des données, les politiques d’accès : politique_securite.md
- Documentation endpoint API : data_lake/api/readme.md

Livrables techniques : 
- Script pour déployer l'infrastructure : deploy_infra.sh
- Pipeline ingestion : data_ingestion/scripts
- Exemple datasets : data_ingestion/sample_data
- ETL : etl_pipeline.py
- Code API : data_lake/api
- Script vérifiant la qualité des données : data_qual/data_quality.py

Procédure: 
1 - démarrer serveur django dans data_lake : python3 manage.py runserver 
2 - docker compose up dans data_ingestion/scripts
3 - lancer data_lake/scripts/kafka_ingestion.py pour la lecture en temps réel des données.
4 - run data_lake/scripts/main_ingestion.py pour essayer l'ingestion des données.
5 - run etl_pipeline (pendant que kafka_ingestion.py tourne) pour essayer la pipeline ETL.
6 - run api_test.py pour voir si l'api marche. 