from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser


class BoostrapFormMixin:
    """Customise form for Bootstrap styling."""

    error_css_class = "alert alert-danger"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


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
