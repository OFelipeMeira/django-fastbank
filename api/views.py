# importing generics from django-rest - Creates simple CRUD
from rest_framework import mixins, viewsets

from .models import User
from .serializers import UserSerializer

# Creating ViewSet
class UserViewSet(
    mixins.ListModelMixin,      # - Get all registers
    mixins.RetrieveModelMixin,  # - Get single register
    mixins.CreateModelMixin,    # - Create new register
    mixins.UpdateModelMixin,    # - Update single register
    mixins.DestroyModelMixin,   # - Delete single register
    viewsets.GenericViewSet     # - implements methods as 'get_object' or 'get_queryset'
):
    queryset = User.objects.all()
    serializer_class = UserSerializer