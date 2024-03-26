from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=200)
    logo = models.FileField(upload_to="logos/", blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    Institution = models.ForeignKey(
        "Institution", on_delete=models.CASCADE, blank=True, verbose_name=("institution")
    )
    subject = models.ManyToManyField("Subject", blank=True, verbose_name=("subjects"))

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=200, unique=True)
    abbreviation = models.CharField(max_length=200)
    url = models.URLField(max_length=200)
    email = models.EmailField(max_length=200)
    logo = models.FileField(upload_to="logos/", blank=True)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=150, unique=True)
    iso_code = models.CharField(
        max_length=50, unique=True, help_text="Enter the ISO code for the language"
    )

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name
