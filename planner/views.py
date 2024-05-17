from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic

from planner.forms import RegisterForm
from planner.models import Category


def index(request):
    return render(request, "planner/index.html")


def register(request) -> HttpResponse:
    if request.method == "GET":
        form = RegisterForm()
        return render(request, "registration/register.html", {"form": form})

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "You have singed up successfully.")
            login(request, user)
            return redirect("planner:index")
        else:
            return render(request, "registration/register.html", {"form": form})


class CategoryListView(LoginRequiredMixin, generic.ListView):
    model = Category
    context_object_name = "category_list"
    template_name = "planner/category_list.html"

