from django.urls import path

from planner.views import index, register

urlpatterns = [
    path("", index, name="index"),
    path("register/", register, name="register")
]

app_name = "planner"
