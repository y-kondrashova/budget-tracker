from datetime import datetime

from django.contrib.auth.models import AbstractUser, User
from django.db import models
from djmoney.models.fields import MoneyField


class Budget(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    balance = MoneyField(max_digits=10,
                         decimal_places=2,
                         null=True,
                         default_currency="USD")

    def __str__(self):
        return f"{self.title} (balance: {self.balance})"


class Category(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Transaction(models.Model):
    type_choices = (
        ("Income", "Income"),
        ("Outcome", "Outcome"),
    )
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    transaction_type = models.CharField(max_length=50, choices=type_choices)
    amount = MoneyField(max_digits=10,
                        decimal_places=2,
                        default_currency="USD")
    date = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ["-date", "category"]

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.transaction_type == "Income":
                self.budget.balance += self.amount
            elif self.transaction_type == "Outcome":
                self.budget.balance -= self.amount
        self.budget.save()
        super(Transaction, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.transaction_type == "Income":
            self.budget.balance -= self.amount
        elif self.transaction_type == "Outcome":
            self.budget.balance += self.amount
        self.budget.save()
        super(Transaction, self).delete(*args, **kwargs)
