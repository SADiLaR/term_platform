from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect, render
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from accounts.service.active_email import SendActiveEmailService

from .forms import CustomAuthenticationForm, CustomUserCreationForm
from .tokens import account_activation_token


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False
            user.is_active = False
            user.save()

            SendActiveEmailService.send_activation_email(request, user)

            return redirect("accounts:activation_sent")

    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect("home")
    else:
        form = CustomAuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})


def activate(request, uidb64, token):
    User = get_user_model()  # Get the custom user model
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request, user)
        return render(request, "accounts/activate.html")
    else:
        return render(request, "accounts/activation_invalid.html")


def activation_sent(request):
    return render(request, "accounts/activation_sent.html")


def resend_activation(request):
    User = get_user_model()  #
    if request.method == "POST":
        user_email = request.POST["email"]
        try:
            user = User.objects.get(email=user_email)
            if not user.is_active:
                SendActiveEmailService.send_activation_email(request, user)

                return redirect("accounts:activation_sent")

            else:
                return render(
                    request, "accounts/resend_activation.html", {"error": "Email address active."}
                )

        except User.DoesNotExist:
            # Handle the case where the email does not exist
            return render(
                request, "accounts/resend_activation.html", {"error": "Email address not found."}
            )
    return render(request, "accounts/resend_activation.html")
