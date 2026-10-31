from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path

from todos.views import CustomLoginView, register_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", CustomLoginView.as_view(), name="home"),
    path("accounts/login/", CustomLoginView.as_view(), name="login"),
    path("accounts/signup/", register_view, name="register"),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),
    path("todos/", include("todos.urls")),
]
