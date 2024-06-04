from datetime import datetime

from django.contrib.auth.models import AbstractUser, User
from django.db import models
from djmoney.models.fields import MoneyField


class Budget(models.Model):
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name="budgets")
    title = models.CharField(max_length=100)
    balance = MoneyField(max_digits=10,
                         decimal_places=2,
                         null=True,
                         default_currency="USD")

    def __str__(self):
        return f"{self.title} (balance: {self.balance})"


class Category(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name="categories")

    def __str__(self):
        return self.title


class Transaction(models.Model):
    type_choices = (
        ("Income", "Income"),
        ("Outcome", "Outcome"),
    )
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name="transactions")
    transaction_type = models.CharField(max_length=50, choices=type_choices)
    amount = MoneyField(max_digits=10,
                        decimal_places=2,
                        default_currency="USD")
    date = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ["-date", "category"]

    def save(self, *args, **kwargs):
        if self.pk:
            old_transaction = Transaction.objects.get(pk=self.pk)
            if old_transaction.transaction_type == "Income":
                self.budget.balance -= old_transaction.amount
            elif old_transaction.transaction_type == "Outcome":
                self.budget.balance += old_transaction.amount

        if self.transaction_type == "Income":
            self.budget.balance += self.amount
        elif self.transaction_type == "Outcome":
            self.budget.balance -= self.amount

        self.budget.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.transaction_type == "Income":
            self.budget.balance -= self.amount
        elif self.transaction_type == "Outcome":
            self.budget.balance += self.amount
        self.budget.save()
        super(Transaction, self).delete(*args, **kwargs)


class Transfer(models.Model):
    from_budget = models.ForeignKey(Budget,
                                    on_delete=models.CASCADE,
                                    related_name="outcomes")
    to_budget = models.ForeignKey(Budget,
                                  on_delete=models.CASCADE,
                                  related_name="incomes")
    amount = MoneyField(max_digits=10,
                        decimal_places=2,
                        default_currency="USD")
    date = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ["-date"]

    def save(self, *args, **kwargs):
        if self.pk:
            old_transfer = Transfer.objects.get(pk=self.pk)
            self.from_budget.balance += old_transfer.amount
            self.to_budget.balance -= old_transfer.amount

            old_transfer.from_budget.save()
            old_transfer.to_budget.save()

        self.from_budget.balance -= self.amount
        self.to_budget.balance += self.amount
        self.from_budget.save()
        self.to_budget.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if not self.pk:
            self.from_budget.balance += self.amount
            self.to_budget.balance -= self.amount
        self.from_budget.save()
        self.to_budget.save()
        super(Transfer, self).delete(*args, **kwargs)
