import magic
from django.contrib import admin
from django.forms import HiddenInput, ModelForm
from django.utils.translation import gettext as _
from simple_history.admin import SimpleHistoryAdmin

from general.service.extract_text import GetTextError, pdf_to_text

from .models import Document, Institution, Language, Project, Subject


class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = "__all__"  # noqa: DJ007
        # Hide if the user doesn't have the permission - if they do, they get a DocumentFormWithFulltext instead
        widgets = {"document_data": HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # If the instance has a mime_type, the field should be disabled
        if not self.instance.mime_type:
            self.fields["mime_type"].widget = HiddenInput()
        else:
            self.fields["mime_type"].widget.attrs["disabled"] = True

    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.get("url", "")
        uploaded_file = cleaned_data.get("uploaded_file", "")

        # We don't unconditionally re-extract PDF text, as the fulltext (`document_data` field) can be edited manually
        # We only want to re-extract the PDF text if the file has changed _and_ the fulltext has not changed. This is to
        # support the use-case of a user editing both the PDF and the fulltext at the same time. It would be confusing if
        # the PDF just overrode the text that they explicitly pasted into that field on the same form page!
        override_existing_fulltext = (
            "uploaded_file" in self.changed_data and "document_data" not in self.changed_data
        )
        if uploaded_file and override_existing_fulltext:
            file_type = magic.from_buffer(uploaded_file.read(), mime=True)
            if file_type != "application/pdf":
                self.add_error("uploaded_file", _("Only PDF files are allowed."))
            cleaned_data["mime_type"] = file_type

            limit = 10 * 1024 * 1024
            if uploaded_file.size and uploaded_file.size > limit:
                self.add_error("uploaded_file", _("File size must not exceed 10MB."))
            if len(self.errors) == 0:
                # Don't parse if validation above failed, or if there are any other errors
                # We want to delay doing the PDF -> text conversion until there are no other errors with the form,
                # because it is quite costly. This is compounded by the fact that Django has included a hard-coded
                # `novalidate` attribute on admin forms for editing (for at least 8 years
                # https://code.djangoproject.com/ticket/26982). Therefore, the fast clientside validation simply does
                # not run, which means we need to optimise the server-side validation as much as we can to get a good
                # experience.

                try:
                    cleaned_data["document_data"] = pdf_to_text(uploaded_file)
                except GetTextError:
                    return self.add_error(
                        "uploaded_file",
                        _("The uploaded file is corrupted or not fully downloaded."),
                    )
                uploaded_file.seek(0)  # Reset file pointer after read

        if not url and not uploaded_file:
            self.add_error("url", _("Either URL or uploaded file must be provided."))
            self.add_error("uploaded_file", _("Either URL or uploaded file must be provided."))

        return cleaned_data


class DocumentFormWithFulltext(DocumentForm):
    class Meta:
        model = Document
        fields = "__all__"  # noqa: DJ007


class DocumentAdmin(SimpleHistoryAdmin):
    ordering = ["title"]
    list_display = ["title", "license", "document_type", "available"]
    search_fields = ["title"]
    list_filter = ["institution", "license", "document_type"]
    form = DocumentForm
    history_list_display = ["title", "license", "document_type", "available"]

    def get_form(self, request, *args, **kwargs):
        # Show the fulltext field if the user has the requisite permission
        if request.user.has_perm("general.can_edit_fulltext"):
            kwargs["form"] = DocumentFormWithFulltext
        return super(DocumentAdmin, self).get_form(request, *args, **kwargs)


class SubjectAdmin(SimpleHistoryAdmin):
    ordering = ["name"]
    search_fields = ["name"]
    list_display = ["name"]
    history_list_display = ["name"]


class LanguageAdmin(SimpleHistoryAdmin):
    ordering = ["name"]
    history_list_display = ["name", "iso_code"]
    list_display = ["name", "iso_code"]


class ProjectAdminInline(admin.TabularInline):
    model = Project
    extra = 0


class ProjectAdmin(SimpleHistoryAdmin):
    ordering = ["name"]
    search_fields = ["name"]
    list_display = ["name"]
    history_list_display = ["name"]


class InstitutionAdmin(SimpleHistoryAdmin):
    ordering = ["name"]
    search_fields = ["name", "abbreviation"]
    list_display = ["name"]
    history_list_display = ["name", "abbreviation"]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Document, DocumentAdmin)
