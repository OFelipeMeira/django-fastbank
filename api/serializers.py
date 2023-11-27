from rest_framework import serializers
from core.models import *
from user.serializers import UserSerializer

class AccountSerialzer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Account
        fields = ['id','agency', 'number',"user"]
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
    # sender = serializers.PrimaryKeyRelatedField(
    #     queryset = Account.objects.all(),
    #     many=False
    # )
    sender = AccountSerialzer()
    # receiver = serializers.PrimaryKeyRelatedField(
    #     queryset = Account.objects.all(),
    #     many=False
    # )
    receiver = AccountSerialzer()
    value = serializers.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        model = Transfer
        fields = ['value', "sender", "receiver","description"]

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'
        extra_kwargs = {
            "description": {
                'required':False
                }
            }
