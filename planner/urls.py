from django.urls import path

from planner.views import index, register,CategoryListView

urlpatterns = [
    path("", index, name="index"),
    path("register/", register, name="register"),
    path("categories/", CategoryListView.as_view(), name="category-list")
]

app_name = "planner"
