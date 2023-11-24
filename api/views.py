from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from rest_framework_simplejwt import authentication as authenticationJWT

from core import models
from api import serializers

import random, decimal


class AccountViewSet(viewsets.ModelViewSet):
    queryset = models.Account.objects.all()
    authentication_classes = [authenticationJWT.JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'create':
            return serializers.AccountDetailSerializer
        return serializers.AccountSerialzer
    
    def create(self, request, *args, **kwargs):
        serializer = serializers.AccountDetailSerializer(data=request.data)
        
        if serializer.is_valid():
            account_number = ""

            for _ in range(16):
                account_number += f"{ random.randint(0,9) }"

            account = models.Account(
                user= self.request.user,
                number= account_number,
                agency= "0001",
            )

            account.balance = decimal.Decimal(0)

            account.save()

            return Response({'message': 'Account created'}, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=True, url_path='sacar')
    def withdraw(self, request, pk=None):
        account = models.Account.objects.get(id=pk)
        serializer = serializers.ValueSerialzier(data=request.data)

        if serializer.is_valid():
            withdraw_value = decimal.Decimal(serializer.validated_data.get('value'))
            balance = decimal.Decimal(account.balance)

            comparar = balance.compare(withdraw_value)

            if comparar == 0 or comparar == 1 :
                account.balance = 0 if balance - withdraw_value <= 0 else balance - withdraw_value
                account.save()

                return Response({"balance": account.balance}, status=status.HTTP_200_OK)
            
            return Response({'message': 'Insufficient balance'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['POST'], detail=True, url_path='depositar')
    def deposit(self, request, pk=None):
        account = models.Account.objects.get(id=pk)
        serializer = serializers.ValueSerialzier(data=request.data)
        
        if serializer.is_valid():
            account.balance += decimal.Decimal(serializer.validated_data.get('value'))
            account.save()

            return Response({'balance':account.balance}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TansferViewSet(viewsets.GenericViewSet):
    queryset = models.Transfer.objects.all()
    serializer_class = serializers.TransferenciaSerializer

    def get_user(self):
        return self.request.user
    
    def verify_account_balance(self, account_id, value):
        if value <= 0 or models.Account.objects.get(id=account_id).balance < value:
            return False
        return True

    def create(self, request):
        sender = request.data.get("sender")
        receiver = request.data.get("receiver")
        value = request.data.get("value")
        description = request.data.get("description")

        if self.verify_account_balance(sender, value):

            transfer_serializer = serializers.TransferenciaSerializer(
                data={
                    "sender": sender,
                    "receiver": receiver,
                    "value": value,
                    "description": description
                    }
                )
            transfer_serializer.is_valid(raise_exception=True)

            accound_sender = models.Account.objects.get(id=sender)
            accound_sender.balance -= value
            accound_sender.save()

            accound_receiver = models.Account.objects.get(id=receiver)
            accound_receiver.balance += value
            accound_receiver.save()

            return Response({'message': 'Transferido'}, status=status.HTTP_200_OK)
        
        return Response({'message': 'Erro na transferencia'}, status=status.HTTP_400_BAD_REQUEST)
    
class LoanViewSet(generics.ListCreateAPIView):
    queryset = models.Loan.objects.all()
    serializer_class = serializers.LoanSerializer
    authentication_classes = [authenticationJWT.JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def verify_info(self, value, installmets):
        if value > 0 or installmets > 0:
            return True
        return False

    def create(self, request):
        value = request.data.get("value")
        installments = request.data.get("installments")
        request_date = request.data.get("request_date")
        account = request.data.get("account")
        fees = request.data.get("fees")

        if self.verify_info(value, installments):
            loan_serializer = serializers.LoanSerializer(
                data={
                    "value":value,
                    "installments":installments,
                    "request_date":request_date,
                    "account":account,
                    "fees":fees,
                }
            )
            loan_serializer.is_valid(raise_exception=True)
            loan_serializer.save()

            return Response({'message': 'Loan Recieved'}, status=status.HTTP_201_CREATED)

