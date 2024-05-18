from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from planner.forms import RegisterForm, TransactionForm
from planner.models import Category, Budget, Transaction


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
            return render(request,
                          "registration/register.html",
                          {"form": form})


class CategoryListView(LoginRequiredMixin, generic.ListView):
    model = Category
    context_object_name = "category_list"
    template_name = "planner/category_list.html"
    queryset = Category.objects.select_related("owner")


class CategoryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Category
    fields = ["title"]
    success_url = reverse_lazy("planner:category-list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class BudgetListView(LoginRequiredMixin, generic.ListView):
    model = Budget
    context_object_name = "budget_list"
    template_name = "planner/budget_list.html"
    queryset = Budget.objects.select_related("owner")


class BudgetCreateView(LoginRequiredMixin, generic.CreateView):
    model = Budget
    fields = ["title", "balance"]
    success_url = reverse_lazy("planner:budget-list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TransactionListView(LoginRequiredMixin, generic.ListView):
    model = Transaction
    context_object_name = "transaction_list"
    template_name = "planner/transaction_list.html"
    queryset = Transaction.objects.select_related("budget__owner")


class TransactionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Transaction
    form_class = TransactionForm
    success_url = reverse_lazy("planner:transaction-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
