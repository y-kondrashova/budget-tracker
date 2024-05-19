from django.urls import path

from planner.views import (
    index,
    register,
    BudgetCreateView,
    BudgetListView,
    BudgetUpdateView,
    BudgetDeleteView,
    CategoryListView,
    CategoryCreateView,
    CategoryDeleteView,
    CategoryUpdateView,
    TransactionCreateView,
    TransactionListView,
    TransactionUpdateView,
    TransactionDeleteView,
    TransferListView,
    TransferCreateView,
    ProfileDetailView,
    ProfileUpdateView,
)

urlpatterns = [
    path("", index, name="index"),
    path("register/", register, name="register"),
    path("profile/", ProfileDetailView.as_view(), name="profile"),
    path("profile/update/", ProfileUpdateView.as_view(), name="profile-update"),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path(
        "categories/create/",
        CategoryCreateView.as_view(),
        name="category-create"
    ),
    path(
        "categories/<int:pk>/update/",
        CategoryUpdateView.as_view(),
        name="category-update"
    ),
    path(
        "categories/<int:pk>/delete/",
        CategoryDeleteView.as_view(),
        name="category-delete"
    ),
    path("budgets/", BudgetListView.as_view(), name="budget-list"),
    path("budgets/create/", BudgetCreateView.as_view(), name="budget-create"),
    path(
        "budgets/<int:pk>/update/",
        BudgetUpdateView.as_view(),
        name="budget-update"
    ),
    path(
        "budgets/<int:pk>/delete/",
        BudgetDeleteView.as_view(),
        name="budget-delete"
    ),
    path(
        "transactions/",
        TransactionListView.as_view(),
        name="transaction-list"
    ),
    path(
        "transactions/create/",
        TransactionCreateView.as_view(),
        name="transaction-create"
    ),
    path(
        "transactions/<int:pk>/update/",
        TransactionUpdateView.as_view(),
        name="transaction-update"
    ),
    path(
        "transactions/<int:pk>/delete/",
        TransactionDeleteView.as_view(),
        name="transaction-delete"
    ),
    path("transfers/", TransferListView.as_view(), name="transfer-list"),
    path(
        "transfers/create/",
        TransferCreateView.as_view(),
        name="transfer-create"
    ),
]

app_name = "planner"
