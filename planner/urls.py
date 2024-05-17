from django.urls import path

from planner.views import (
    index,
    register,
    BudgetCreateView,
    BudgetListView,
    CategoryListView,
    CategoryCreateView,
    TransactionListView
)

urlpatterns = [
    path("", index, name="index"),
    path("register/", register, name="register"),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("budgets/", BudgetListView.as_view(), name="budget-list"),
    path("budgets/create", BudgetCreateView.as_view(), name="budget-create"),
    path(
        "transactions/",
        TransactionListView.as_view(),
        name="transaction-list"
    ),
    path(
        "categories/create/",
        CategoryCreateView.as_view(),
        name="category-create"
    ),
]

app_name = "planner"
