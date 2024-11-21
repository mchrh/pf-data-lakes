from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Transaction, WebLog, Campaign
from datetime import datetime, timedelta
from decimal import Decimal

class TransactionTests(APITestCase):
    def setUp(self):
        Transaction.objects.create(
            transaction_id="T1",
            customer_id="C1",
            amount=100.00,
            transaction_date=datetime.now(),
            is_high_value=False
        )
        Transaction.objects.create(
            transaction_id="T2",
            customer_id="C1",
            amount=2000.00,
            transaction_date=datetime.now(),
            is_high_value=True
        )

    def test_list_transactions(self):
        url = reverse('transaction-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_transaction_summary(self):
        url = reverse('transaction-summary')
        response = self.client.get(url, {'customer_id': 'C1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['transaction_count'], 2)
        self.assertEqual(float(response.data['total_amount']), 2100.00)

class WebLogTests(APITestCase):
    def setUp(self):
        WebLog.objects.create(
            timestamp=datetime.now(),
            year=2024,
            month=1,
            day=1,
            hour=10,
            request_count=100,
            error_count=5,
            total_bytes=10000
        )

    def test_web_log_metrics(self):
        """Test des métriques des logs web"""
        url = reverse('weblog-metrics')
        response = self.client.get(url, {'granularity': 'day'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['total_requests'], 100)

class CampaignTests(APITestCase):
    def setUp(self):
        self.campaign = Campaign.objects.create(
            campaign_id="CAMP1",
            total_clicks=1000,
            total_cost=Decimal('500.00'),
            unique_users=800,
            start_date=datetime.now() - timedelta(days=10),
            end_date=datetime.now()
        )

    def test_campaign_performance(self):
        url = reverse('campaign-performance', kwargs={'pk': 'CAMP1'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['campaign_id'], 'CAMP1')
        self.assertEqual(float(response.data['cost_per_click']), 0.50)