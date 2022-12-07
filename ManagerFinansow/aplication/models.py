from os import access
from django.db import models
from django.contrib.auth.models import User
import uuid

from UsersApp.models import Profile, Currency, Category, Subcategory

# Create your models here.

class Account(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    is_shared = models.BooleanField(default=False)
    description = models.CharField(max_length=100, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name

    # Obliczenie bilansu konta
    def calculate_balance(self):
        balance = 0
        transactions = Transaction.objects.filter(id_account=self)
        for transaction in transactions:
            balance += transaction.converted_amount
        return balance

    def transactions(self):
        return Transaction.objects.filter(id_account=self).order_by('-transaction_date')

    #wyświetlenie opisu jeśli istnieje
    def print_description(self):
        if self.description!=None:
            return self.description
        else:
            return ""


class User_Account(models.Model):
    id_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    id_account = models.ForeignKey(Account, on_delete=models.CASCADE)
    access_level = models.IntegerField(default=0)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"[{self.id_user}] - [{self.id_account}] - {self.access_level}"

class Transaction(models.Model):
    id_account = models.ForeignKey(Account, on_delete=models.CASCADE)
    id_user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True) #konto z którego dokonano transakcji zostało usunięte ale transakcja ma pozostać 
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    id_subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    is_periodic = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    converted_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateField()
    description = models.CharField(max_length=255, blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return (f"{self.name} - {self.id_account.name} - {self.id_user.name} - "
                f"{self.id_category} - {self.id_subcategory} - {self.is_periodic} - "
                f"{self.amount} - {self.converted_amount} - {self.transaction_date} - {self.description}")
