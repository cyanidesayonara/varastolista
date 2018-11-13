from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("list/", views.list_view, name="list"),
    path("search/", views.search, name="search"),
    path("new/", views.new, name="new"),
    path("plus/", views.plus, name="plus"),
    path("minus/", views.minus, name="minus"),
    path("edit/", views.edit, name="edit"),
    path("delete/", views.delete, name="delete"),
]
