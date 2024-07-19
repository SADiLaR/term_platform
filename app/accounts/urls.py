from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .views import CustomPasswordResetView

app_name = "accounts"
urlpatterns = [
    path("register/", views.register, name="accounts_register"),
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path(
        "password_reset/",
        CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            success_url="/accounts/reset/done/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("activation_sent/", views.activation_sent, name="activation_sent"),
    path("resend_activation/", views.resend_activation, name="resend_activation"),
]
