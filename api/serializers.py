from rest_framework import serializers
from core.models import *


class AccountSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id','agency', 'number']
        read_only_fields = ['number']


class AccountDetailSerializer(AccountSerialzer):
    class Meta(AccountSerialzer.Meta):
        fields = AccountSerialzer.Meta.fields + ['id', 'balance', 'created_at']
        read_only_fields = AccountSerialzer.Meta.fields + ['id', 'balance', 'created_at']


class ValueSerialzier(serializers.Serializer):
    value = serializers.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        fields = ['value']

class TransferSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(
        queryset = Account.objects.all(),
        many=False
    )
    receiver = serializers.PrimaryKeyRelatedField(
        queryset = Account.objects.all(),
        many=False
    )
    value = serializers.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        model = Transfer
        fields = ['value', "sender", "receiver","description"]

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'
