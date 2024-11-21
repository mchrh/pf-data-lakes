# Documentation de l'API Data Lake

## Vue d'ensemble
Cette API REST expose les données du Data Lake transformées (zone silver) via des endpoints HTTP. Elle permet d'accéder aux données des transactions, logs web, médias sociaux et campagnes publicitaires.

## Base URL
```
http://localhost:8000/api/v1/
```

## Authentification
Utilise l'authentification par token JWT. Inclure le token dans le header :
```
Authorization: Bearer <token>
```

## Endpoints

### 1. Transactions

#### GET /api/v1/transactions/
Récupère la liste des transactions avec possibilité de filtrage.

**Paramètres de requête :**
- `start_date` (optionnel) : Date de début (YYYY-MM-DD)
- `end_date` (optionnel) : Date de fin (YYYY-MM-DD)
- `customer_id` (optionnel) : ID du client
- `min_amount` (optionnel) : Montant minimum

**Exemple de réponse :**
```json
[
    {
        "transaction_id": "T123",
        "customer_id": "C456",
        "amount": 199.99,
        "transaction_date": "2024-01-15T10:30:00Z",
        "is_high_value": false
    }
]
```

#### GET /api/v1/transactions/customer_summary/
Récupère un résumé des transactions pour un client spécifique.

**Paramètres de requête :**
- `customer_id` (requis) : ID du client

**Exemple de réponse :**
```json
{
    "total_spent": 1500.50,
    "transaction_count": 10,
    "avg_transaction": 150.05
}
```

### 2. Logs Web

#### GET /api/v1/web-logs/metrics/
Récupère les métriques des logs web avec une granularité spécifiée.

**Paramètres de requête :**
- `start_date` (optionnel) : Date de début
- `end_date` (optionnel) : Date de fin
- `granularity` (optionnel) : "hour", "day", ou "month" (défaut: "hour")

**Exemple de réponse :**
```json
[
    {
        "year": 2024,
        "month": 1,
        "day": 15,
        "hour": 10,
        "total_requests": 1500,
        "total_errors": 23,
        "total_bytes": 1500000,
        "total_visitors": 450
    }
]
```

### 3. Médias Sociaux

#### GET /api/v1/social-media/
Récupère les posts des médias sociaux.

**Paramètres de requête :**
- `platform` (optionnel) : Plateforme spécifique (ex: "twitter", "facebook")
- `min_sentiment` (optionnel) : Score de sentiment minimum

**Exemple de réponse :**
```json
[
    {
        "post_id": "P789",
        "user_id": "U123",
        "content": "Great product!",
        "timestamp": "2024-01-15T11:20:00Z",
        "sentiment_score": 0.8,
        "platform": "twitter",
        "tag_count": 2
    }
]
```

#### GET /api/v1/social-media/sentiment_analysis/
Récupère l'analyse de sentiment globale.

**Paramètres de requête :**
- `platform` (optionnel) : Filtrer par plateforme

**Exemple de réponse :**
```json
{
    "avg_sentiment": 0.65,
    "total_posts": 1200
}
```

### 4. Campagnes Publicitaires

#### GET /api/v1/campaigns/{campaign_id}/metrics/
Récupère les métriques d'une campagne spécifique.

**Paramètres de chemin :**
- `campaign_id` : ID de la campagne

**Exemple de réponse :**
```json
{
    "campaign_id": "C001",
    "total_clicks": 15000,
    "total_cost": 750.50,
    "unique_users": 12000,
    "avg_cpc": 0.05
}
```

## Codes d'Erreur

- 200 : Succès
- 400 : Requête invalide
- 401 : Non authentifié
- 403 : Non autorisé
- 404 : Ressource non trouvée
- 500 : Erreur serveur

## Pagination

L'API utilise la pagination standard de Django REST Framework.

**Exemple de réponse paginée :**
```json
{
    "count": 100,
    "next": "http://api/v1/transactions/?page=2",
    "previous": null,
    "results": [...]
}
```

## Limites de Taux

- 1000 requêtes par heure par utilisateur authentifié
- 100 requêtes par heure pour les utilisateurs non authentifiés

## Format des Dates

- Toutes les dates doivent être au format ISO 8601
- Les timestamps incluent le fuseau horaire
- Format d'entrée des dates : YYYY-MM-DD
- Format d'entrée des timestamps : YYYY-MM-DDTHH:MM:SSZ

## Performances

- Les requêtes sont limitées à 100 résultats par page par défaut
- Les requêtes volumineuses doivent utiliser la pagination
- Les agrégations complexes peuvent avoir une latence plus élevée

## Exemples d'Utilisation

### Curl

```bash
curl -H "Authorization: Bearer <token>" \
     "http://localhost:8000/api/v1/transactions/?customer_id=C456"

curl -H "Authorization: Bearer <token>" \
     "http://localhost:8000/api/v1/web-logs/metrics/?granularity=day"
```

### Python

```python
import requests

base_url = "http://localhost:8000/api/v1"
headers = {"Authorization": "Bearer <token>"}

response = requests.get(
    f"{base_url}/transactions/",
    params={"customer_id": "C456"},
    headers=headers
)
transactions = response.json()

response = requests.get(
    f"{base_url}/social-media/sentiment_analysis/",
    headers=headers
)
sentiment_data = response.json()
```

## Notes d'Implémentation

1. L'API utilise les modèles non gérés (unmanaged models) pour se connecter directement aux tables de la zone silver du Data Lake

2. Les vues sont en lecture seule pour garantir l'intégrité des données

3. La mise en cache est implémentée pour les requêtes fréquentes

4. Les requêtes lourdes sont optimisées via des agrégations au niveau de la base de données