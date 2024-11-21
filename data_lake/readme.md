# Documentation des Endpoints de l'API Data Lake

## Base URL
```
http://localhost:8000/api/
```

## 1. Endpoints Transactions

### 1.1 Liste des Transactions
```
GET /api/transactions/
```

Récupère la liste des transactions avec possibilité de filtrage.

**Paramètres de requête**
- `start_date` (optionnel) : Date de début (format: YYYY-MM-DD)
- `end_date` (optionnel) : Date de fin (format: YYYY-MM-DD)
- `customer_id` (optionnel) : ID du client
- `min_amount` (optionnel) : Montant minimum

**Exemple de requête**
```bash
curl -X GET "http://localhost:8000/api/transactions/?customer_id=C123&min_amount=100"
```

**Exemple de réponse**
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "transaction_id": "T123",
            "customer_id": "C123",
            "amount": "150.00",
            "transaction_date": "2024-01-15T10:30:00Z",
            "is_high_value": false
        },
        {
            "transaction_id": "T124",
            "customer_id": "C123",
            "amount": "1200.00",
            "transaction_date": "2024-01-15T14:20:00Z",
            "is_high_value": true
        }
    ]
}
```

### 1.2 Résumé des Transactions
```
GET /api/transactions/summary/
```

Fournit un résumé statistique des transactions.

**Paramètres de requête**
- `customer_id` (optionnel) : Pour filtrer par client

**Exemple de requête**
```bash
curl -X GET "http://localhost:8000/api/transactions/summary/?customer_id=C123"
```

**Exemple de réponse**
```json
{
    "total_amount": "1350.00",
    "transaction_count": 2,
    "avg_amount": "675.00"
}
```

## 2. Endpoints Logs Web

### 2.1 Liste des Logs
```
GET /api/web-logs/
```

Récupère la liste des logs web.

**Exemple de réponse**
```json
{
    "count": 1,
    "results": [
        {
            "timestamp": "2024-01-15T10:00:00Z",
            "year": 2024,
            "month": 1,
            "day": 15,
            "hour": 10,
            "request_count": 100,
            "error_count": 5,
            "total_bytes": 15000
        }
    ]
}
```

### 2.2 Métriques des Logs
```
GET /api/web-logs/metrics/
```

Fournit des métriques agrégées des logs web.

**Paramètres de requête**
- `granularity` : 'hour' (défaut), 'day', ou 'month'

**Exemple de requête**
```bash
curl -X GET "http://localhost:8000/api/web-logs/metrics/?granularity=day"
```

**Exemple de réponse**
```json
[
    {
        "year": 2024,
        "month": 1,
        "day": 15,
        "total_requests": 2500,
        "total_errors": 50,
        "total_bytes": 500000
    }
]
```

## 3. Endpoints Campagnes

### 3.1 Liste des Campagnes
```
GET /api/campaigns/
```

Liste toutes les campagnes publicitaires.

**Exemple de réponse**
```json
{
    "count": 1,
    "results": [
        {
            "campaign_id": "CAMP001",
            "total_clicks": 1000,
            "total_cost": "500.00",
            "unique_users": 800,
            "start_date": "2024-01-01T00:00:00Z",
            "end_date": "2024-01-31T23:59:59Z",
            "duration_days": 31,
            "cost_per_click": "0.50"
        }
    ]
}
```

### 3.2 Performance d'une Campagne
```
GET /api/campaigns/{campaign_id}/performance/
```

Obtient les métriques de performance détaillées d'une campagne.

**Exemple de requête**
```bash
curl -X GET "http://localhost:8000/api/campaigns/CAMP001/performance/"
```

**Exemple de réponse**
```json
{
    "campaign_id": "CAMP001",
    "click_through_rate": 1.25,
    "cost_per_click": "0.50",
    "total_cost": "500.00",
    "duration_days": 31
}
```

## Authentification

Toutes les requêtes nécessitent une authentification. Envoyez les credentials via:

```bash
curl -H "Authorization: Bearer <your-token>" http://localhost:8000/api/...
```

## Codes de Statut HTTP

- 200 : Succès
- 400 : Requête invalide
- 401 : Non authentifié
- 403 : Non autorisé
- 404 : Ressource non trouvée
- 500 : Erreur serveur

## Pagination

La pagination est activée par défaut :
- Taille de page par défaut : 10 éléments
- Paramètres de pagination :
  * `page` : Numéro de page
  * `page_size` : Nombre d'éléments par page (max: 100)

## Format des Dates

- Toutes les dates doivent être au format ISO 8601
- Les dates d'entrée acceptent le format YYYY-MM-DD
- Les timestamps de sortie sont au format YYYY-MM-DDTHH:MM:SSZ

## Limites et Restrictions

- Maximum de 100 éléments par page
- Limite de rate : 1000 requêtes par heure par utilisateur
- Les requêtes en écriture (POST, PUT, DELETE) ne sont pas autorisées