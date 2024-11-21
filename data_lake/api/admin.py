from django.contrib import admin
from .models import Transaction, WebLog, Campaign

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'customer_id', 'amount', 'transaction_date', 'is_high_value')
    list_filter = ('is_high_value', 'transaction_date')
    search_fields = ('transaction_id', 'customer_id')

@admin.register(WebLog)
class WebLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'request_count', 'error_count', 'total_bytes')
    list_filter = ('year', 'month', 'day')

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('campaign_id', 'total_clicks', 'total_cost', 'unique_users')
    search_fields = ('campaign_id',)