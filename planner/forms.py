from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from planner.models import Category, Budget


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["title", "budget"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["budget"].queryset = Budget.objects.filter(owner=user)
