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


class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ["from_budget", "to_budget", "amount", "date"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["from_budget"].queryset = Budget.objects.filter(owner=user)
        self.fields["to_budget"].queryset = Budget.objects.filter(owner=user)
