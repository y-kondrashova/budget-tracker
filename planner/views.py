from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from planner.forms import (
    RegisterForm,
    TransactionForm,
    TransferForm,
    DateSearchForm,
)
from planner.models import Category, Budget, Transaction, Transfer


class BaseListViewWithDateSearch(LoginRequiredMixin, generic.ListView):

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        form = DateSearchForm(self.request.GET)
        context["search_form"] = form
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = DateSearchForm(self.request.GET)
        if form.is_valid():
            start_date = form.cleaned_data.get("start_date")
            end_date = form.cleaned_data.get("end_date")
            if start_date:
                queryset = queryset.filter(date__gte=start_date)
            if end_date:
                queryset = queryset.filter(date__lte=end_date)
        return queryset


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
            user.save()
            messages.success(request, "You have singed up successfully.")
            login(request, user)
            return redirect("planner:index")
        else:
            return render(request,
                          "registration/register.html",
                          {"form": form})


class ProfileDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    context_object_name = "user"

    def get_object(self, queryset=None):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    fields = ["first_name", "last_name", "username", "email"]
    success_url = reverse_lazy("planner:profile")

    def get_object(self, queryset=None):
        return self.request.user


class CategoryListView(LoginRequiredMixin, generic.ListView):
    model = Category
    context_object_name = "category_list"
    template_name = "planner/category_list.html"
    queryset = Category.objects.select_related("owner")
    paginate_by = 10


class CategoryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Category
    fields = ["title"]
    success_url = reverse_lazy("planner:category-list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Category
    fields = ["title"]
    success_url = reverse_lazy("planner:category-list")


class CategoryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Category
    success_url = reverse_lazy("planner:category-list")


class BudgetListView(LoginRequiredMixin, generic.ListView):
    model = Budget
    context_object_name = "budget_list"
    template_name = "planner/budget_list.html"
    queryset = Budget.objects.select_related("owner")
    paginate_by = 10


class BudgetCreateView(LoginRequiredMixin, generic.CreateView):
    model = Budget
    fields = ["title", "balance"]
    success_url = reverse_lazy("planner:budget-list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class BudgetUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Budget
    fields = ["title", "balance"]
    success_url = reverse_lazy("planner:budget-list")


class BudgetDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Budget
    success_url = reverse_lazy("planner:budget-list")


class TransactionListView(BaseListViewWithDateSearch):
    model = Transaction
    context_object_name = "transaction_list"
    template_name = "planner/transaction_list.html"
    queryset = Transaction.objects.select_related("budget__owner", "category")
    paginate_by = 10


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


class TransactionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Transaction
    form_class = TransactionForm
    success_url = reverse_lazy("planner:transaction-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class TransactionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Transaction
    success_url = reverse_lazy("planner:transaction-list")


class TransferListView(BaseListViewWithDateSearch):
    model = Transfer
    context_object_name = "transfer_list"
    template_name = "planner/transfer_list.html"
    queryset = Transfer.objects.select_related(
        "from_budget__owner",
        "to_budget__owner"
    )
    paginate_by = 10


class TransferCreateView(LoginRequiredMixin, generic.CreateView):
    model = Transfer
    form_class = TransferForm
    success_url = reverse_lazy("planner:transfer-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TransferUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Transfer
    form_class = TransferForm
    success_url = reverse_lazy("planner:transfer-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class TransferDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Transfer
    success_url = reverse_lazy("planner:transfer-list")
