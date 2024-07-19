from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    UserCreationForm,
)
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text=_("Required. Add a valid email address."),
    )
    username = forms.CharField(
        required=True,
        help_text=_("Required. Add a valid username."),
    )
    first_name = forms.CharField(
        required=True,
        help_text=_("Required. Add a valid first name."),
    )
    last_name = forms.CharField(
        required=True,
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label=_("Username"), help_text=_("Required. Enter your username."))
    password = forms.CharField(label=_("Password"), help_text=_("Required. Enter your password."))

    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        """

        Cleaning an Email

        This method is used to clean an email address provided by the user. It performs the following operations:

        1. Retrieves the user model using the "get_user_model()" function.
        2. Fetches the email from the "cleaned_data" dictionary.
        3. Queries the user model to find all users with the same email address.
        4. Checks if any users exist with the given email address. If not, it raises a "forms.ValidationError" with a specific error message.
        5. Iterates through each user found with the given email address.
        6. Checks if the user is both active and a staff member. If not, it raises a "forms.ValidationError" with a specific error message.
        7. Finally, the cleaned email address is returned.

        Please note that this method assumes the presence of the "forms.ValidationError" class and the "get_user_model()" function. If any of these are missing, this method will not work properly.

        Reason for the Override:
        The "clean_email" method is overridden to ensure that only active staff members can reset their passwords. This is done to prevent unauthorized users from resetting their passwords and gaining access to the system.
        and prevent users getting an email to reset their password if they are not active or staff members.
        """
        User = get_user_model()
        email = self.cleaned_data["email"]
        users = User.objects.filter(email=email)
        if not users.exists():
            raise forms.ValidationError("There is a error please contact the administrator.")

        for user in users:
            if not user.is_active or not user.is_staff:
                raise forms.ValidationError("There is a error please contact the administrator.")

        return email
