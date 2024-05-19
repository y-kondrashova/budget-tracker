from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from planner.models import Budget, Transaction


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
