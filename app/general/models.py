from django.core.validators import FileExtensionValidator
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=200)
    logo = models.FileField(upload_to="logos/", blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    institution = models.ForeignKey(
        "Institution", on_delete=models.CASCADE, blank=True, verbose_name="institution"
    )
    subjects = models.ManyToManyField("Subject", blank=True)
    languages = models.ManyToManyField("Language", blank=True)

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=200, unique=True)
    abbreviation = models.CharField(max_length=200)
    url = models.URLField(max_length=200, blank=True)
    email = models.EmailField(max_length=200, blank=True)
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


class DocumentFile(models.Model):
    file_validators = [FileExtensionValidator(["pdf"])]

    license_choices = [("MIT", "MIT"), ("GNU", "GNU"), ("Apache", "Apache")]
    document_type_choices = [("Glossary", "Glossary"), ("Translation", "Translation")]

    file_type = "pdf"

    title = models.CharField(max_length=200)
    url = models.URLField(max_length=200, blank=True)
    uploaded_file = models.FileField(
        upload_to="documents/",
        validators=file_validators,
        blank=True,
        help_text="Only PDF files are allowed.",
    )
    available = models.BooleanField(default=True)
    license = models.CharField(max_length=200, choices=license_choices)
    mime_type = models.CharField(
        max_length=200, blank=True, help_text="This input will auto-populate."
    )
    document_type = models.CharField(max_length=200, choices=document_type_choices)
    Institution = models.ForeignKey("Institution", on_delete=models.CASCADE)
    subjects = models.ManyToManyField("Subject", blank=True)
    languages = models.ManyToManyField("Language", blank=True)

    def __str__(self):
        return self.title
