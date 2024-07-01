from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name")

    def clean_username(self):
        username = self.cleaned_data["username"].lower().strip()
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("A user with that username already exists.")
        return username

    def clean_first_name(self):
        return self.cleaned_data["first_name"].strip()

    def clean_last_name(self):
        return self.cleaned_data["last_name"].strip()
