# file to verify and convert models into json format
import random

from rest_framework import serializers

from .models import (
    User,
    Address,
    Account,
    Card,
    Transactions
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'cpf',
            'photo'
        )

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            'id',
            'user',
            'address',
            'city',
            'state',
            'country',
            'complement',
            'cep'
        )

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'id',
            'user',
            'password',
            'account_number',
            'created_at',
        )
        extra_kwargs = {
            'account_number':{
                'read_only':True
            }
        }
        
class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = (
            'id',
            'account',
            'number',
            'cvv',
            'created_at',
            'expiration_date',
        )

class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = (
            'id',
            'sender',
            'receiver',
            'value',
            'description',
        )