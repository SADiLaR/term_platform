from django.core.validators import FileExtensionValidator
from django.db import models
from simple_history.models import HistoricalRecords


class Project(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=200, blank=True, verbose_name="URL")
    logo = models.ImageField(upload_to="projects/logos/", blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    institution = models.ForeignKey(
        "Institution", on_delete=models.CASCADE, blank=True, verbose_name="institution"
    )
    subjects = models.ManyToManyField("Subject", blank=True)
    languages = models.ManyToManyField("Language", blank=True)

    # added simple historical records to the model
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=200, unique=True)
    abbreviation = models.CharField(max_length=200)
    url = models.URLField(max_length=200, blank=True, verbose_name="URL")
    email = models.EmailField(max_length=200, blank=True)
    logo = models.ImageField(upload_to="institutions/logos/", blank=True)

    # added simple historical records to the model
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name} ({self.abbreviation})"


class Language(models.Model):
    name = models.CharField(max_length=150, unique=True)
    iso_code = models.CharField(
        max_length=50,
        unique=True,
        help_text="The 2 or 3 letter code from ISO 639.",
        verbose_name="ISO code",
    )

    # added simple historical records to the model
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=150, unique=True)

    # added simple historical records to the model
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class DocumentFile(models.Model):
    file_validators = [FileExtensionValidator(["pdf"])]

    # names and abbreviations based on
    # https://en.wikipedia.org/wiki/Creative_Commons_license#Six_regularly_used_licenses
    license_choices = [
        ("(c)", "All rights reserved"),
        ("CC0", "No rights reserved"),
        ("CC BY", "Creative Commons Attribution"),
        ("CC BY-SA", "Creative Commons Attribution-ShareAlike"),
        ("CC BY-NC", "Creative Commons Attribution-NonCommercial"),
        ("CC BY-NC-SA", "Creative Commons Attribution-NonCommercial-ShareAlike"),
    ]
    license_help_text = """
            <a
              href="https://creativecommons.org/share-your-work/cclicenses/"
              rel="noreferrer"
              target="_blank"
            >
                    More information about Creative Commons licenses.
            </a>'
    """
    document_type_choices = [("Glossary", "Glossary"), ("Policy", "Policy")]

    file_type = "pdf"

    title = models.CharField(max_length=200)
    url = models.URLField(max_length=200, blank=True, verbose_name="URL")
    uploaded_file = models.FileField(
        upload_to="documents/",
        validators=file_validators,
        blank=True,
        help_text="PDF files up to 10MB are allowed.",
    )
    available = models.BooleanField(default=True)
    license = models.CharField(
        max_length=200,
        choices=license_choices,
        default="(c)",
        help_text=license_help_text,
    )
    mime_type = models.CharField(
        max_length=200, blank=True, help_text="This input will auto-populate."
    )
    document_type = models.CharField(max_length=200, choices=document_type_choices)
    document_data = models.TextField(blank=True)
    institution = models.ForeignKey("Institution", on_delete=models.CASCADE)
    subjects = models.ManyToManyField("Subject", blank=True)
    languages = models.ManyToManyField("Language", blank=True)

    # added simple historical records to the model
    history = HistoricalRecords(excluded_fields=["document_data"])

    def __str__(self):
        return self.title
