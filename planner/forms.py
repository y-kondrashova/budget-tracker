from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from moneyed import Money

from planner.models import Budget, Transaction, Transfer, Category

User = get_user_model()


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
        self.fields["category"].queryset = Category.objects.filter(owner=user)

    def clean(self):
        cleaned_data = super().clean()
        budget = cleaned_data.get("budget")
        amount = cleaned_data.get("amount")
        total_digits = len(
            str(amount).replace('.', '').replace(',', '')
        )

        if budget and amount:
            if total_digits > 10:
                raise ValidationError(
                    "The total number of digits in the amount"
                    " must not exceed 8."
                )
            if budget.balance.currency != amount.currency:
                raise forms.ValidationError(
                    "The budget and transaction amount "
                    "must have the same currency."
                )

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
        amount = cleaned_data.get("amount")
        total_digits = len(
            str(amount).replace('.', '').replace(',', '')
        )

        if amount is None:
            raise ValidationError(
                "The total number of digits in the amount must not exceed 8."
            )

        if (
            from_budget
            and to_budget
            and from_budget.balance.currency != to_budget.balance.currency
        ):
            raise forms.ValidationError(
                "Both budgets must have the same currency for a transfer."
            )
        if from_budget == to_budget:
            raise ValidationError("From and To budgets cannot be the same.")
        if amount <= Money(0, amount.currency):
            raise ValidationError("Transfer amount must be greater than zero.")
        if from_budget.balance < amount:
            raise ValidationError("Insufficient funds in the source budget.")

        return cleaned_data


class DateSearchForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), required=False
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), required=False
    )
