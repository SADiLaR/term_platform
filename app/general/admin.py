from django.contrib import admin

from .models import Institution, Language, Project, Subject

admin.site.register(Project)
admin.site.register(Institution)
admin.site.register(Language)
admin.site.register(Subject)
