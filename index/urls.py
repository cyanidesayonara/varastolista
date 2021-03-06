from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("search/", views.search, name="search"),
    path("new/", views.new, name="new"),
    path("plus/", views.plus, name="plus"),
    path("minus/", views.minus, name="minus"),
    path("edit/", views.edit, name="edit"),
    path("delete/", views.delete, name="delete"),
    path("upload/", views.upload, name="upload"),
    path("download/", views.download, name="download"),
    path('language/', include('django.conf.urls.i18n')),
]
