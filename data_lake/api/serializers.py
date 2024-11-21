from rest_framework import serializers
from .models import Transaction, WebLog, Campaign

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class WebLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebLog
        fields = '__all__'

class CampaignSerializer(serializers.ModelSerializer):
    duration_days = serializers.IntegerField(read_only=True)
    cost_per_click = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Campaign
        fields = '__all__'

class TransactionSummarySerializer(serializers.Serializer):
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    transaction_count = serializers.IntegerField()
    avg_amount = serializers.DecimalField(max_digits=10, decimal_places=2)

class WebLogMetricsSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    day = serializers.IntegerField(required=False)
    hour = serializers.IntegerField(required=False)
    total_requests = serializers.IntegerField()
    total_errors = serializers.IntegerField()
    total_bytes = serializers.IntegerField()

class CampaignPerformanceSerializer(serializers.Serializer):
    campaign_id = serializers.CharField()
    click_through_rate = serializers.FloatField()
    cost_per_click = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    duration_days = serializers.IntegerField()