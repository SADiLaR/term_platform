from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView as _LoginView
from django.contrib.auth.views import PasswordChangeView as _PasswordChangeView
from django.contrib.auth.views import (
    PasswordResetConfirmView as _PasswordResetConfirmView,
)
from django.contrib.auth.views import PasswordResetView as _PasswordResetView
from django.shortcuts import redirect, render

from .forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            auth_login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


# We subclass the builtin views where we want to supply our own forms. We
# (mostly) stick to the expected template names, and they are therefore
# automatically picked up, even in views where we don't subclass the builtin
# views.
class LoginView(_LoginView):
    form_class = AuthenticationForm


class PasswordChangeView(_PasswordChangeView):
    form_class = PasswordChangeForm
    # The builtin view expects password_change_form.html, but so does the admin
    # interface, and we don't want to replace that one as well, so we use a
    # custom name.
    template_name = "registration/password_change_form2.html"


class PasswordResetView(_PasswordResetView):
    form_class = PasswordResetForm


class PasswordResetConfirmView(_PasswordResetConfirmView):
    form_class = SetPasswordForm
