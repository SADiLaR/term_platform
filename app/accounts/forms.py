from django import forms
from django.contrib.auth.forms import AuthenticationForm as _AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm as _PasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm as _PasswordResetForm
from django.contrib.auth.forms import SetPasswordForm as _SetPasswordForm
from django.contrib.auth.forms import UserCreationForm as _UserCreationForm
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser


class BoostrapFormMixin:
    """Customise form for Bootstrap styling."""

    error_css_class = "alert alert-danger"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class UserCreationForm(BoostrapFormMixin, _UserCreationForm):
    email = forms.EmailField(label=_("E-mail address"), required=True)
    first_name = forms.CharField(label=_("First name"), required=True)
    last_name = forms.CharField(label=_("Last name"), required=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "first_name", "last_name")


class AuthenticationForm(BoostrapFormMixin, _AuthenticationForm):
    pass


class PasswordChangeForm(BoostrapFormMixin, _PasswordChangeForm):
    pass


class PasswordResetForm(BoostrapFormMixin, _PasswordResetForm):
    pass


class SetPasswordForm(BoostrapFormMixin, _SetPasswordForm):
    pass
