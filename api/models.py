from django.db import models

import random


class User(models.Model):
    name  = models.CharField(max_length=255, verbose_name="Name")
    cpf   = models.CharField(max_length=12, verbose_name="CPF")
    photo = models.CharField(max_length=255, null=True, verbose_name="Photo path")

    class Meta:
        verbose_name        = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return self.name


class Address(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
   
    address    = models.CharField(max_length=255, verbose_name="Address")               # {street name}, {number}  -> number splited by a comma
    city       = models.CharField(max_length=255, verbose_name="City")                  # {city name}
    state      = models.CharField(max_length=255, verbose_name="State")                 # {state}
    country    = models.CharField(max_length=255, verbose_name="Contry")                # {country}
    complement = models.CharField(max_length=255, null=True, verbose_name="Complement") # {complement}
    cep        = models.CharField(max_length=  8, verbose_name="CEP")                   # {00000000} -> 'postal code' without slashes and dots
    
    class Meta:
        verbose_name        = "Address"
        verbose_name_plural = "Addresses"


class Account(models.Model):
    user           = models.ForeignKey(User, on_delete=models.CASCADE)     # Referenced User
    account_number = models.CharField(max_length=255, verbose_name="Account number")        # Number of the account
    password       = models.CharField(max_length=255, verbose_name="Password")              # User Password
    
    created_at     = models.DateField(auto_now_add=True, verbose_name="Created at")         # Date of an account is created
    is_active      = models.BooleanField(default=True, verbose_name="Is active")            # Boolean if the account is active
    
    class Meta:
        verbose_name        = "Account"
        verbose_name_plural = "Accounts"

    def save(self, *args, **kwargs):
        for i in range(4):
            self.account_number += f"{random.randint(1000,9999)}"

    def __str__(self):
        return self.user.name
    

class Card(models.Model):
    account         = models.ForeignKey(Account, on_delete=models.PROTECT, verbose_name="Account")  #
    number          = models.CharField(max_length=255, verbose_name="Card number")                  #
    cvv             = models.CharField(max_length=3, verbose_name="CVV")                        #
    created_at      = models.DateField(auto_now_add=True, verbose_name="Created at")                   #
    expiration_date = models.DateField(verbose_name="Expriration Date")                                    #

    class Meta:
        verbose_name        = "Card"
        verbose_name_plural = "Cards"
    
    def __str__(self) -> str:
        return self.number


class Transactions(models.Model):
    sender      = models.ForeignKey(Account, on_delete=models.PROTECT, null=True, related_name="sender")
    receiver    = models.ForeignKey(Account, on_delete=models.PROTECT, null=True, related_name="receiver")
    value       = models.DecimalField(max_digits=100, decimal_places=2)
    description = models.CharField(max_length=255, null=True)
    
    class Meta:
        verbose_name        = "Transaction"
        verbose_name_plural = "Transactions"
