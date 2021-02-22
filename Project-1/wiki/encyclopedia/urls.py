from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.article, name="article"),
    path("search", views.search, name="search"),
    path("add", views.add, name="add"),
    path("wiki/edit/<str:title>", views.edit, name="edit"),
    path("random_page", views.random_page, name="random_page")
]
