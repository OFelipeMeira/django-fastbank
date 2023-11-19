from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from rest_framework_simplejwt import authentication as authenticationJWT

from core.models import Conta
from api import serializers

import random, decimal


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Conta.objects.all()
    authentication_classes = [authenticationJWT.JWTAuthentication]

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # return self.queryset.filter(user=self.request.user).order_by('-created_at').distinct()
        return self.queryset.filter(user=self.request.user).order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'create':
            return serializers.AccountDetailSerializer
        return serializers.AccountSerialzer
    
    def create(self, request, *args, **kwargs):
        serializer = serializers.AccountDetailSerializer(data=request.data)
        
        if serializer.is_valid():
            numero_conta = ""

            for i in range(16):
                numero_conta += f"{ random.randint(0,9) }"

            conta = Conta(
                user= self.request.user,
                numero= numero_conta,
                agencia= "0001"
            )

            conta.saldo = decimal.Decimal(0)

            conta.save()

            return Response({'message': 'Created'}, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=True, url_path='sacar')
    def sacar(self, request, pk=None):
        conta = Conta.objects.get(id=pk)
        serializer_recebido = serializers.SaqueSerialzier(data=request.data)

        if serializer_recebido.is_valid():
            valor_saque = decimal.Decimal(serializer_recebido.validated_data.get('value'))
            saldo = decimal.Decimal(conta.saldo)

            comparar = saldo.compare(valor_saque)

            if comparar == 0 or comparar == 1 :
                novo_valor = 0 if saldo - valor_saque <= 0 else saldo - valor_saque

                conta.saldo = novo_valor

                conta.save()

                return Response({"saldo": conta.saldo}, status=status.HTTP_200_OK)
            
            return Response({'message': 'Saldo insuficiente'}, status=status.HTTP_403_FORBIDDEN)
        
        return Response(serializer_recebido.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['POST'], detail=True, url_path='depositar')
    def depositar(self, request, pk=None):
        conta = Conta.objects.get(id=pk)
        serializer_recebido = serializers.DepositoSerialzier(data=request.data)
        
        if serializer_recebido.is_valid():
            # saldo = decimal.Decimal(conta.saldo)
            valor_depositado = decimal.Decimal(serializer_recebido.validated_data.get('value'))

            # conta.saldo = saldo + valor_depositado
            conta.saldo += valor_depositado
            conta.save()

            return Response({'saldo':conta.saldo}, status=status.HTTP_200_OK)

        return Response(serializer_recebido.errors, status=status.HTTP_400_BAD_REQUEST)