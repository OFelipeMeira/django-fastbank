# importing generics from django-rest - Creates simple CRUD
from rest_framework import generics

from .models import User
from .serializers import UserSerializer

# Creating a ApiView
class UserAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()