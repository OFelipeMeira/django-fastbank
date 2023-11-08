#imports
from django.db import models

#creating a 'table'
class User(models.Model):
    #setting each column
    name = models.CharField(max_length=255)
    cpf = models.CharField(max_length=12)

    # extra configuration
    class Meta:
        # name to be show outside of 'backend'
        verbose_name = "User"
        verbose_name_plural = "Users"

    # table 'toString'
    def __str__(self) -> str:
        return self.name

# 
# class Transactions(models.Model):
#     sender_user_id = models.ManyToManyField(Users)
#     reciver_user_id = models.ManyToManyField(Users)
#     value = models.DecimalField(max_digits=1000000, decimal_places=2)

#     class Meta:
#         verbose_name = "Trasaction"
#         verbose_name_plural = "Trasactions"

#     def __str__(self) -> str:
#         return self.pk