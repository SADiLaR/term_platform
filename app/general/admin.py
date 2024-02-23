from django.contrib import admin

from .models import ContributingCentre, Institution, Language, Subject


class SubjectInline(admin.TabularInline):
    model = Subject.contributing_centre.through


class ContributingCentreAdmin(admin.ModelAdmin):
    inlines = [SubjectInline]


admin.site.register(ContributingCentre, ContributingCentreAdmin)
admin.site.register(Institution)
admin.site.register(Language)
admin.site.register(Subject)
