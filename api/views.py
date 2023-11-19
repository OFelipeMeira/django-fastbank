from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt import authentication as authenticationJWT
from core.models import Conta
from api import serializers
import random


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
        serializers = self.serializer_class(data= request.data)
        
        if serializers.is_valid():
            numero_conta = ""

            for i in range(16):
                numero_conta += f"{ random.randint(0,9) }"

            conta = Conta(
                user= self.request.user,
                numero= numero_conta,
                agentcia= "0001"
            )

            return Response({'message': 'Created'}, status=status.HTTP_201_CREATED)
