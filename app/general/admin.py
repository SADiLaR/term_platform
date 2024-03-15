from django.contrib import admin

from .models import Institution, Language, Project, Subject

# class SubjectInline(admin.TabularInline):
#     # model = Subject.projects.through
#     pass
#
#
# class ProjectsAdmin(admin.ModelAdmin):
#     inlines = [SubjectInline]


# admin.site.register(Projects, ProjectsAdmin)
admin.site.register(Project)
admin.site.register(Institution)
admin.site.register(Language)
admin.site.register(Subject)
