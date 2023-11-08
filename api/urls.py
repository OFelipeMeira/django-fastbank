"""
    API Endpoints
"""

from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import (
    UserViewSet,
    AccountViewSet,
    AddressViewSet,
    CardViewSet,
    TransactionsViewSet,
)

router = SimpleRouter()
router.register('users', UserViewSet)
router.register('accounts', AccountViewSet)
router.register('address', AddressViewSet)
router.register('cards', CardViewSet)
router.register('transactions', TransactionsViewSet)

urlspatterns = router.urls