from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.register, name="accounts_signup"),
]
