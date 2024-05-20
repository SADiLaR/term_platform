import magic
from django.contrib import admin
from django.forms import HiddenInput, ModelForm
from simple_history.admin import SimpleHistoryAdmin

from .models import DocumentFile, Institution, Language, Project, Subject


class DocumentFileForm(ModelForm):
    class Meta:
        model = DocumentFile
        fields = "__all__"  # noqa: DJ007

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

        if uploaded_file:
            file_type = magic.from_buffer(uploaded_file.read(), mime=True)
            if file_type != "application/pdf":
                self.add_error("uploaded_file", "Only PDF files are allowed.")

            cleaned_data["mime_type"] = file_type

            uploaded_file.seek(0)  # Reset file pointer after read

        if not url and not uploaded_file:
            self.add_error("url", "Either URL or uploaded file must be provided.")
            self.add_error("uploaded_file", "Either URL or uploaded file must be provided.")

        if uploaded_file:
            limit = 10 * 1024 * 1024
            if uploaded_file.size and uploaded_file.size > limit:
                self.add_error("uploaded_file", "File size must not exceed 10MB.")

        return cleaned_data


class DocumentFileAdmin(SimpleHistoryAdmin):
    ordering = ["title"]
    list_display = ["title", "license", "document_type", "available"]
    search_fields = ["title"]
    list_filter = ["institution", "license", "document_type"]
    form = DocumentFileForm
    history_list_display = ["title", "license", "document_type", "available"]


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
    search_fields = ["name"]
    list_display = ["name"]
    inlines = [ProjectAdminInline]
    history_list_display = ["name", "abbreviation"]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(DocumentFile, DocumentFileAdmin)
