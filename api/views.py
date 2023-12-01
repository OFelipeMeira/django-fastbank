from rest_framework import viewsets, status, generics, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from rest_framework_simplejwt import authentication as authenticationJWT

from django.db.models import Q

from core import models
from api import serializers

import random, decimal, datetime
from dateutil.relativedelta import relativedelta


class AccountViewSet(viewsets.ModelViewSet):
    queryset = models.Account.objects.all()
    authentication_classes = [authenticationJWT.JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'create':
            return serializers.AccountDetailSerializer
        return serializers.AccountSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = serializers.AccountDetailSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                nickname = request.data['nickname']
            except:
                return Response({"error": "no nickname"}, status=status.HTTP_400_BAD_REQUEST)
            
            account_number = ""

            for _ in range(16):
                account_number += f"{ random.randint(0,9) }"

            account = models.Account(
                user= self.request.user,
                number= account_number,
                agency= "0001",
                nickname= nickname
            )

            account.balance = decimal.Decimal(0)

            account.save()

            return Response({'message': 'Account created'}, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=True, url_path='withdraw')
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

                self.save_in_tranfer(account.id, None, withdraw_value)

                return Response({"balance": account.balance}, status=status.HTTP_200_OK)
            
            return Response({'message': 'Insufficient balance'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['POST'], detail=True, url_path='deposit')
    def deposit(self, request, pk=None):
        account = models.Account.objects.get(id=pk)
        serializer = serializers.ValueSerialzier(data=request.data)
        
        if serializer.is_valid():
            account.balance += decimal.Decimal(serializer.validated_data.get('value'))
            account.save()

            self.save_in_tranfer(None, account.id, serializer.validated_data.get('value'))

            return Response({'balance':account.balance}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def save_in_tranfer(self, sender, receiver, value):
        transfer_serializer = serializers.CreateTransferDetailSerializer(
            data={
                "sender": sender,
                "receiver": receiver,
                "value": value,
                "description": ""
            }
        )
        transfer_serializer.is_valid(raise_exception=True)
        transfer_serializer.save()
    

class TansferViewSet(viewsets.GenericViewSet):
    queryset = models.Transfer.objects.all()
    # serializer_class = serializers.TransferSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'create':
            return serializers.TransferDetailSerializer
        return serializers.TransferSerializer

    def get_user(self):
        return self.request.user
    
    def verify_account_balance(self, account_id, value):
        if value <= 0 or models.Account.objects.get(id=account_id).balance < value:
            return False
        return True

    def create(self, request):
        sender = request.data.get("sender")
        receiver = request.data.get("receiver")
        value = round(decimal.Decimal(request.data.get("value")), 2)
        description = request.data.get("description")

        
        if value < 0:
            # If trys to transfer <=0
            return Response({'message': 'Invalid value for transfer'}, status=status.HTTP_403_FORBIDDEN)
        
        elif models.Account.objects.get(id=sender).balance < value:
            # if there is no balance enough
            return Response({'message': 'No balance enough'}, status=status.HTTP_403_FORBIDDEN)
        
        else:

            # Verify if the 'sender' is an id from an Account from the logged user:
            if models.Account.objects.get(id=sender).user.id == request.user.id:

                transfer_serializer = serializers.TransferSerializer(
                    data={
                        "sender": sender,
                        "receiver": receiver,
                        "value": value,
                        "description": description
                        }
                    )
                transfer_serializer.is_valid(raise_exception=True)
                transfer_serializer.save()

                accound_sender = models.Account.objects.get(id=sender)
                accound_sender.balance -=  value
                accound_sender.save()

                accound_receiver = models.Account.objects.get(id=receiver)
                accound_receiver.balance += value
                accound_receiver.save()

                return Response({'message': 'Transfered'}, status=status.HTTP_200_OK)
            
            else:
                return Response({'message': 'This account is not from the logged user'}, status=status.HTTP_403_FORBIDDEN)

    @action(methods=['GET'],detail=True, url_path='statement')
    def statement(self, request, pk=None):
        queryset = models.Transfer.objects.filter(
            Q(sender=pk) | Q(receiver=pk)
        ).order_by('-created_at')
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
        

class LoanViewSet(generics.ListCreateAPIView):
    queryset = models.Loan.objects.all()
    serializer_class = serializers.LoanSerializer
    authentication_classes = [authenticationJWT.JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        account = request.data.get("account")
        value = decimal.Decimal(request.data.get("value"))
        installments = request.data.get("installments")

        min_value = 1000
        min_installments = 1
        
        if value <= min_value:
            return Response({'message': f'the value to loan needs to be at least {min_value}'})
        
        elif installments <= min_installments:
            return Response({'message': f'the number of installments needs to be at least {min_installments}'})
        
        else:
            
            # registering the loan
            loan_serializer = serializers.LoanSerializer(
                data={
                    "value":value,
                    "installments":installments,
                    "account": account,
                }
            )
            loan_serializer.is_valid(raise_exception=True)
            loan_serializer.save()

            last_loan = models.Loan.objects.latest('id')

            # creating installments
            for i in range(installments):
                installment_serializer = serializers.LoanInstallmentsSerializer(
                    data={
                        
                        # value = initial_value / installmenst + fees:
                        "value": round( (value / installments * (last_loan.fees * i ) ) ,2) ,
                        
                        # on each iteration +1 month
                        "due_date": datetime.datetime.combine(datetime.date.today() +  relativedelta(months=+i), datetime.datetime.min.time()),

                        "loanId": last_loan.pk,

                        "payed_date": None

                    }
                )

                installment_serializer.is_valid(raise_exception=True)
                installment_serializer.save()

            user = models.Account.objects.get( id=account )
            user.balance += value
            user.save()

            return Response({'message': 'Loan Recieved'}, status=status.HTTP_201_CREATED)

class CreditViewSet(generics.ListCreateAPIView):
    queryset = models.Credit.objects.all()
    serializer_class = serializers.CreditSerializer
    authentication_classes = [authenticationJWT.JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        account = request.data.get("account")
        value = decimal.Decimal(request.data.get("value"))
        installments = request.data.get("installments")

        max_value = 1000
        min_installments = 1

        if value > max_value:
            return Response({'message': f'the value needs to be less than {max_value}'})
        
        elif installments <= min_installments:
            return Response({'message': f'the number of installments needs to be at least {min_installments}'})
        
        else:
            credit_serializer = serializers.CreditSerializer(
                data={
                    "account": account,
                    "installments": installments,
                    "value": value
                }
            )
            credit_serializer.is_valid(raise_exception=True)
            credit_serializer.save()

            last_credit = models.Credit.objects.latest("id")

            for i in range(installments):

                # today + x monthes with fixed day(5)
                due_date = datetime.datetime.now() + relativedelta(months=+i)
                due_date = datetime.datetime.combine( due_date , datetime.datetime.min.time())

                installments_serializer = serializers.CreditInstallmentsSerializer(
                    data={
                        "creditId": last_credit.pk,
                        "value": round( (value/installments) , 2),
                        "due_date": due_date.replace(day=5)
                    }
                )

                installments_serializer.is_valid(raise_exception=True)
                installments_serializer.save()
            return Response({'message': 'Credit Buy done'}, status=status.HTTP_201_CREATED)
    

    def list(self, request, pk=None):
        queryset = models.Credit.objects.filter(account=pk)

        serializer = serializers.CreditSerializer(queryset, many=True)

        return Response(serializer.data)
