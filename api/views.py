from rest_framework import mixins, viewsets

from .models import (
    User,
    Address,
    Account,
    Card,
    Transactions
    )
from .serializers import (
    UserSerializer,
    AddressSerializer,
    AccountSerializer,
    CardSerializer,
    TransactionsSerializer
    )


class UserViewSet(
    mixins.ListModelMixin,      # - Get all registers
    mixins.RetrieveModelMixin,  # - Get single register
    mixins.CreateModelMixin,    # - Create new register
    mixins.UpdateModelMixin,    # - Update single register
    # mixins.DestroyModelMixin,   # - Delete single register
    viewsets.GenericViewSet     # - implements methods as 'get_object' or 'get_queryset'
):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AddressViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    # mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class AccountViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    # mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class CardViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    # mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class TransactionsViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    # mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Transactions.objects.all()
    serializer_class = TransactionsSerializer