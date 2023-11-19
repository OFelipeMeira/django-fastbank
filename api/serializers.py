from rest_framework import serializers
from core.models import Conta

class AccountSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Conta
        fields = ['agencia', 'numero']
        read_only_fields = ['agencia', 'numero']

class AccountDetailSerializer(AccountSerialzer):
    class Meta(AccountSerialzer.Meta):
        fields = AccountSerialzer.Meta.fields + ['id', 'saldo', 'created_at']
        read_only_fields = AccountSerialzer.Meta.fields + ['id', 'saldo', 'created_at']
