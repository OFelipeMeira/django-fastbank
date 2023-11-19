from django.urls import path, include
from api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('accounts', views.AccountViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls))
]