from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Avg, Count
from django.utils.dateparse import parse_date
from django.shortcuts import get_object_or_404
from .models import Transaction, WebLog, Campaign
from .serializers import (
    TransactionSerializer, WebLogSerializer, CampaignSerializer,
    TransactionSummarySerializer, WebLogMetricsSerializer,
    CampaignPerformanceSerializer
)

class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        queryset = Transaction.objects.all()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        customer_id = self.request.query_params.get('customer_id')
        min_amount = self.request.query_params.get('min_amount')

        if start_date:
            queryset = queryset.filter(transaction_date__gte=parse_date(start_date))
        if end_date:
            queryset = queryset.filter(transaction_date__lte=parse_date(end_date))
        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)
        if min_amount:
            queryset = queryset.filter(amount__gte=min_amount)

        return queryset

    @action(detail=False, methods=['get'])
    def summary(self, request):
        queryset = self.get_queryset()
        summary_data = {
            'total_amount': queryset.aggregate(Sum('amount'))['amount__sum'] or 0,
            'transaction_count': queryset.count(),
            'avg_amount': queryset.aggregate(Avg('amount'))['amount__avg'] or 0
        }
        serializer = TransactionSummarySerializer(summary_data)
        return Response(serializer.data)

class WebLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WebLogSerializer
    queryset = WebLog.objects.all()

    @action(detail=False, methods=['get'])
    def metrics(self, request):
        granularity = request.query_params.get('granularity', 'hour')
        group_by = ['year', 'month']
        
        if granularity in ['day', 'hour']:
            group_by.append('day')
        if granularity == 'hour':
            group_by.append('hour')

        metrics = self.queryset.values(*group_by).annotate(
            total_requests=Sum('request_count'),
            total_errors=Sum('error_count'),
            total_bytes=Sum('total_bytes')
        ).order_by(*group_by)

        serializer = WebLogMetricsSerializer(metrics, many=True)
        return Response(serializer.data)

class CampaignViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CampaignSerializer
    queryset = Campaign.objects.all()

    @action(detail=True, methods=['get'])
    def performance(self, request, pk=None):
        campaign = self.get_object()
        performance_data = {
            'campaign_id': campaign.campaign_id,
            'click_through_rate': campaign.total_clicks / campaign.unique_users if campaign.unique_users > 0 else 0,
            'cost_per_click': campaign.cost_per_click,
            'total_cost': campaign.total_cost,
            'duration_days': campaign.duration_days
        }
        
        serializer = CampaignPerformanceSerializer(performance_data)
        return Response(serializer.data)