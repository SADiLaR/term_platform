from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector, SearchVectorField
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords


class Project(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("name"))
    description = models.TextField(blank=True, verbose_name=_("description"))
    url = models.URLField(max_length=200, blank=True, verbose_name=_("URL"))
    logo = models.ImageField(upload_to="projects/logos/", blank=True, verbose_name=_("logo"))
    start_date = models.DateField(blank=True, null=True, verbose_name=_("start date"))
    end_date = models.DateField(blank=True, null=True, verbose_name=_("end date"))
    institution = models.ForeignKey(
        "Institution", on_delete=models.CASCADE, blank=False, verbose_name=_("institution")
    )
    subjects = models.ManyToManyField("Subject", blank=True, verbose_name=_("subjects"))
    languages = models.ManyToManyField("Language", blank=True, verbose_name=_("languages"))

    # added simple historical records to the model
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name=_("name"))
    abbreviation = models.CharField(max_length=200, verbose_name=_("abbreviation"))
    url = models.URLField(max_length=200, blank=True, verbose_name=_("URL"))
    email = models.EmailField(max_length=200, blank=True, verbose_name=_("email"))
    logo = models.ImageField(upload_to="institutions/logos/", blank=True, verbose_name=_("logo"))

    # added simple historical records to the model
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Institution")
        verbose_name_plural = _("Institutions")

    def __str__(self):
        return f"{self.name} ({self.abbreviation})"


class Language(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name=_("name"))
    iso_code = models.CharField(
        max_length=50,
        unique=True,
        help_text=_("The 2 or 3 letter code from ISO 639."),
        verbose_name=_("ISO code"),
    )

    # added simple historical records to the model
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")

    def __str__(self):
        return self.name


class SubjectManager(models.Manager):
    def get_used_subjects(self):
        """Returns only the subjects that have documents or projects associated with them"""
        return self.filter(Q(document__isnull=False) | Q(project__isnull=False)).distinct()


class Subject(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name=_("name"))

    # added simple historical records to the model
    history = HistoricalRecords()
    objects = SubjectManager()

    class Meta:
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")

    def __str__(self):
        return self.name


class Document(models.Model):
    file_validators = [FileExtensionValidator(["pdf"])]

    # names and abbreviations based on
    # https://en.wikipedia.org/wiki/Creative_Commons_license#Six_regularly_used_licenses
    license_choices = [
        ("(c)", _("All rights reserved")),
        ("CC0", _("No rights reserved")),
        ("CC BY", _("Creative Commons Attribution")),
        ("CC BY-SA", _("Creative Commons Attribution-ShareAlike")),
        ("CC BY-NC", _("Creative Commons Attribution-NonCommercial")),
        ("CC BY-NC-SA", _("Creative Commons Attribution-NonCommercial-ShareAlike")),
    ]
    license_help_text = _(
        """<a
              href="https://creativecommons.org/share-your-work/cclicenses/"
              rel="noreferrer"
              target="_blank"
          >
          More information about Creative Commons licenses.
        </a>"""
    )
    document_type_choices = [
        ("Glossary", _("Glossary")),
        ("Policy", _("Policy")),
        ("Term list", _("Term list")),
    ]

    file_type = "pdf"

    title = models.CharField(max_length=200, verbose_name=_("title"))
    description = models.TextField(blank=True, verbose_name=_("description"))
    url = models.URLField(max_length=200, blank=True, verbose_name=_("URL"))
    uploaded_file = models.FileField(
        upload_to="documents/",
        validators=file_validators,
        blank=True,
        help_text=_("PDF files up to 10MB are allowed."),
        verbose_name=_("uploaded file"),
    )
    verified = models.BooleanField(default=False, verbose_name=_("verified"))
    standardised = models.BooleanField(
        default=False, verbose_name=_("authenticated and standardised")
    )
    available = models.BooleanField(default=True, verbose_name=_("available"))
    license = models.CharField(
        max_length=200,
        choices=license_choices,
        default="(c)",
        help_text=license_help_text,
        verbose_name=_("license"),
    )
    mime_type = models.CharField(
        max_length=200,
        blank=True,
        help_text=_("This input will auto-populate."),
        verbose_name=_("MIME type"),
    )
    document_type = models.CharField(
        max_length=200, choices=document_type_choices, verbose_name=_("document category")
    )
    document_data = models.TextField(
        blank=True,
        verbose_name=_("Searchable content"),
        help_text=_(
            "The searchable text extracted from the document where possible, but it can also be edited."
        ),
    )
    institution = models.ForeignKey(
        "Institution", on_delete=models.CASCADE, verbose_name=_("institution")
    )
    subjects = models.ManyToManyField("Subject", blank=True, verbose_name=_("subjects"))
    languages = models.ManyToManyField("Language", blank=True, verbose_name=_("languages"))

    # `config="english"` is required to ensure that the `expression` is
    # immutable, otherwise the migration to the GeneratedField fails.
    search_vector = models.GeneratedField(
        expression=(
            SearchVector("title", config="english", weight="A")
            + SearchVector("description", config="english", weight="B")
            + SearchVector("document_data", config="english", weight="C")
        ),
        output_field=SearchVectorField(),
        db_persist=True,
        null=True,
        blank=True,
    )

    # added simple historical records to the model
    history = HistoricalRecords(excluded_fields=["document_data", "search_vector"])

    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")

        indexes = [
            GinIndex(fields=["search_vector"]),
        ]

        permissions = [("can_edit_fulltext", "Can edit document fulltext (used for search)")]

    def __str__(self):
        return self.title
