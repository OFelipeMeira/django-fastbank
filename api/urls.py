"""
    API Endpoints
"""

from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import (
    UserViewSet
)

router = SimpleRouter()
router.register('users', UserViewSet)

# urlspatterns = [
#     path('users/',router.urls, name="users" ),
# ]
urlspatterns = router.urls