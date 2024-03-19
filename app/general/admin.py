from django.contrib import admin

from .models import Institution, Language, Project, Subject


class ProjectAdminInline(admin.TabularInline):
    model = Project
    extra = 0


class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectAdminInline]


admin.site.register(Project)
admin.site.register(Institution, ProjectAdmin)
admin.site.register(Language)
admin.site.register(Subject)
