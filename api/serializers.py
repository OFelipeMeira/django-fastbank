from rest_framework import serializers
from core.models import Conta, Transfer


class AccountSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Conta
        fields = ['id','agencia', 'numero']
        # read_only_fields = ['agencia', 'numero']
        read_only_fields = ['numero']


class AccountDetailSerializer(AccountSerialzer):
    class Meta(AccountSerialzer.Meta):
        fields = AccountSerialzer.Meta.fields + ['id', 'saldo', 'created_at']
        read_only_fields = AccountSerialzer.Meta.fields + ['id', 'saldo', 'created_at']


class DepositoSerialzier(serializers.Serializer):
    value = serializers.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        fields = ['value']


class SaqueSerialzier(serializers.Serializer):
    value = serializers.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        fields = ['value']

class TransferenciaSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(
        queryset = Conta.objects.all()
    )
    receiver = serializers.PrimaryKeyRelatedField(
        queryset = Conta.objects.all()
    )
    value = serializers.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        model = Transfer
        fields = ['value', "sender", "receiver"]
