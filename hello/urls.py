from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.new, name="new"),
    path("plus/", views.plus, name="plus"),
    path("minus/", views.minus, name="minus"),
    path("edit/", views.edit, name="edit"),
    path("delete/", views.delete, name="delete"),
]
