from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from planner.models import Budget, Transaction, Transfer


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["transaction_type", "amount", "budget", "category", "date"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["budget"].queryset = Budget.objects.filter(owner=user)

    def clean(self):
        cleaned_data = super().clean()
        budget = cleaned_data.get("budget")
        amount = cleaned_data.get("amount")

        if budget and amount:
            if budget.balance.currency != amount.currency:
                raise forms.ValidationError("The budget and transaction amount must have the same currency.")

        return cleaned_data


class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ["from_budget", "to_budget", "amount", "date"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["from_budget"].queryset = Budget.objects.filter(owner=user)
        self.fields["to_budget"].queryset = Budget.objects.filter(owner=user)

    def clean(self):
        cleaned_data = super().clean()
        from_budget = cleaned_data.get("from_budget")
        to_budget = cleaned_data.get("to_budget")

        if from_budget and to_budget:
            if from_budget.balance.currency != to_budget.balance.currency:
                raise forms.ValidationError("Both budgets must have the same currency for a transfer.")

        return cleaned_data
