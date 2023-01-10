from django.urls import path

from chatapp import views

urlpatterns = [
    path("", views.index, name="index"),
]
