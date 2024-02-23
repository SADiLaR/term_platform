from django.contrib.auth.models import AbstractUser
from django.db import models

from general.models import Institution, Language, Subject


class CustomUser(AbstractUser):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, null=True, blank=True)
    languages = models.ManyToManyField(Language)
    subject = models.ManyToManyField(Subject)

    def __str__(self):
        return self.username
