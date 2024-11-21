from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet, WebLogViewSet, CampaignViewSet

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'web-logs', WebLogViewSet, basename='weblog')
router.register(r'campaigns', CampaignViewSet, basename='campaign')

urlpatterns = [
    path('', include(router.urls)),
]