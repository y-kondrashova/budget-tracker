from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from moneyed import Money

User = get_user_model()


class Budget(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="budgets")
    title = models.CharField(max_length=100)
    balance = MoneyField(
        max_digits=10, decimal_places=2, null=True, default_currency="USD"
    )

    def __str__(self):
        return f"{self.title} (balance: {self.balance})"


class Category(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")

    def __str__(self):
        return self.title


class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        INCOME = "Income", _("Income")
        OUTCOME = "Outcome", _("Outcome")

    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="transactions"
    )
    transaction_type = models.CharField(max_length=50, choices=TransactionType.choices)
    amount = MoneyField(max_digits=10, decimal_places=2, default_currency="USD")
    date = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ["-date", "category"]

    def save(self, *args, **kwargs):
        if self.pk:
            old_transaction = Transaction.objects.get(pk=self.pk)
            if old_transaction.transaction_type == self.TransactionType.INCOME:
                self.budget.balance -= old_transaction.amount
            elif old_transaction.transaction_type == self.TransactionType.OUTCOME:
                self.budget.balance += old_transaction.amount

        if self.transaction_type == self.TransactionType.INCOME:
            self.budget.balance += self.amount
        elif self.transaction_type == self.TransactionType.OUTCOME:
            self.budget.balance -= self.amount

        self.budget.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.transaction_type == self.TransactionType.INCOME:
            self.budget.balance -= self.amount
        elif self.transaction_type == self.TransactionType.OUTCOME:
            self.budget.balance += self.amount
        self.budget.save()
        super(Transaction, self).delete(*args, **kwargs)


class Transfer(models.Model):
    from_budget = models.ForeignKey(
        Budget, on_delete=models.CASCADE, related_name="outcomes"
    )
    to_budget = models.ForeignKey(
        Budget, on_delete=models.CASCADE, related_name="incomes"
    )
    amount = MoneyField(max_digits=10, decimal_places=2, default_currency="USD")
    date = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ["-date"]

    def clean(self):
        if self.from_budget == self.to_budget:
            raise ValidationError("From and To budgets cannot be the same.")
        if self.amount <= Money(0, self.amount.currency):
            raise ValidationError("Transfer amount must be greater than zero.")
        if self.from_budget.balance < self.amount:
            raise ValidationError("Insufficient funds in the source budget.")

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
