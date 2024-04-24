from django.contrib.auth.models import AbstractUser
from django.db import models
from simple_history.models import HistoricalRecords

from general.models import Institution, Language, Subject


class CustomUser(AbstractUser):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, null=True, blank=True)
    languages = models.ManyToManyField(Language, blank=True)
    subject = models.ManyToManyField(Subject, blank=True)

    # added simple historical records to the model
    history = HistoricalRecords()

    def __str__(self):
        return self.username
