from django.urls import path

from planner.views import index, register,CategoryListView
from planner.views import (
    index,
    register,
    BudgetListView,
    CategoryListView,
)

urlpatterns = [
    path("", index, name="index"),
    path("register/", register, name="register"),
    path("categories/", CategoryListView.as_view(), name="category-list")
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("budgets/", BudgetListView.as_view(), name="budget-list"),
]

app_name = "planner"
