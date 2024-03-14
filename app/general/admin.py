from django.contrib import admin

from .models import ContributingCentre, Institution, Language, Subject


class SubjectInline(admin.TabularInline):
    model = Subject.contributing_centre.through


class ContributingCentreAdmin(admin.ModelAdmin):
    inlines = [SubjectInline]


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name", "iso_code")


admin.site.register(ContributingCentre, ContributingCentreAdmin)
admin.site.register(Institution)
admin.site.register(Subject)
