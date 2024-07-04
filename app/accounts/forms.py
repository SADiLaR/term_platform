from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Add a valid email address.")
    username = forms.CharField(required=True, help_text="Required. Add a valid username.")
    first_name = forms.CharField(required=True, help_text="Required. Add a valid first name.")
    last_name = forms.CharField(required=True, help_text="Required. Add a valid last name.")

    class Meta:
        model = CustomUser
        fields = ("username", "email", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields["email"].required = True
        self.fields["username"].required = True
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
