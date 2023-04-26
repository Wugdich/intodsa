from django.urls import path

from dsa import views

urlpatterns = [
        path("", views.index, name="index"),
        ]
