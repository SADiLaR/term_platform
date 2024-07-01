from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, BaseUserManager
from django.db import models
from simple_history.models import HistoricalRecords

from general.models import Institution, Language, Subject


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, null=True, blank=True)
    languages = models.ManyToManyField(Language, blank=True)
    subject = models.ManyToManyField(Subject, blank=True)

    # added simple historical records to the model
    history = HistoricalRecords()

    # objects = CustomUserManager()

    def __str__(self):
        return self.username
