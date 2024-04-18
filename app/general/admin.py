import mimetypes

from django.contrib import admin
from django.forms import ModelForm, fields_for_model

from .models import DocumentFile, Institution, Language, Project, Subject


class ProjectAdminInline(admin.TabularInline):
    model = Project
    extra = 0


class DocumentFileForm(ModelForm):
    class Meta:
        model = DocumentFile
        fields = fields_for_model(DocumentFile)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["mime_type"].widget.attrs["disabled"] = True

    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.get("url", "")
        uploaded_file = cleaned_data.get("uploaded_file", "")

        if cleaned_data["mime_type"] is not None:
            cleaned_data["mime_type"] = (
                mimetypes.guess_type(uploaded_file.name)[0] if uploaded_file else ""
            )

        if not url and not uploaded_file:
            self.add_error("url", "Either URL or uploaded file must be provided.")
            self.add_error("uploaded_file", "Either URL or uploaded file must be provided.")

        if uploaded_file:
            limit = 10 * 1024 * 1024
            if uploaded_file.size and uploaded_file.size > limit:
                self.add_error("uploaded_file", "File size must not exceed 10MB.")

        return cleaned_data


class DocumentFileAdmin(admin.ModelAdmin):
    list_display = ["title", "license", "document_type", "available"]
    ordering = [
        "license",
    ]
    search_fields = ["title", "license", "document_type"]

    form = DocumentFileForm


class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectAdminInline]


admin.site.register(Project)
admin.site.register(Institution, ProjectAdmin)
admin.site.register(Language)
admin.site.register(Subject)
admin.site.register(DocumentFile, DocumentFileAdmin)
