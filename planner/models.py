from django.db import models
from django.contrib.auth.models import AbstractUser, User
from djmoney.models.fields import MoneyField


class Budget(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    balance = MoneyField(max_digits=10, decimal_places=2, null=True, default_currency="USD")


class Category(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)


class Transaction(models.Model):
    type_choices = (
        ("Income", "Income"),
        ("Outcome", "Outcome"),
        ("Transfer", "Transfer"),
    )
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=type_choices)
    amount = MoneyField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def income(self, *args, **kwargs):
        self.budget.balance += self.amount
        self.budget.save()
        super(Transaction, self).save(*args, **kwargs)

    def outcome(self, *args, **kwargs):
        self.budget.balance -= self.amount
        self.budget.save()
        super(Transaction, self).delete(*args, **kwargs)
