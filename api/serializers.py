from rest_framework import serializers
from core.models import *
from user.serializers import UserSerializer

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id','agency', 'number','nickname']
        read_only_fields = ['number']

class AccountUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Account
        fields = ['id','agency', 'number',"user",'nickname']
        read_only_fields = ['number']

class AccountDetailSerializer(AccountSerializer):
    class Meta(AccountSerializer.Meta):
        fields = AccountSerializer.Meta.fields + ['id', 'balance', 'created_at', 'nickname']
        read_only_fields = AccountSerializer.Meta.fields + ['id', 'balance', 'created_at']


class ValueSerialzier(serializers.Serializer):
    value = serializers.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        fields = ['value']

class TransferDetailSerializer(serializers.ModelSerializer):
    sender = AccountUserSerializer()
    receiver = AccountUserSerializer()
    value = serializers.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        model = Transfer
        fields = ['value', "sender", "receiver","description"]

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
        fields = ['account','installments','value']

class LoanInstallmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanInstallments
        fields = '__all__'

class CreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit
        fields =  ['account','installments','value']

# class CardSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Card
#         fields = '__all__'
#         read_only_fields = ['number','cvv', 'expiration_date']

class CreditInstallmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditInstallments
        fields = ['creditId',
                    'payed_date',
                    "due_date",
                    'value']

# class CreditReadSerializer(serializers.ModelSerializer):
#     # related_installment = CreditInstallmentsSerializer()
#     related_installment = CreditInstallmentsSerializer(instance='related_installment')
#     class Meta:
#         model = Credit
#         fields =  ['account', 'installments', 'value', 'related_installment']