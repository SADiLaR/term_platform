from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from simple_history.admin import SimpleHistoryAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin, SimpleHistoryAdmin):
    model = CustomUser
    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    ]

    list_filter = [
        "username",
        "email",
    ]

    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("institution", "languages", "subject")}),)
    add_fieldsets = UserAdmin.add_fieldsets
    history_list_display = ["username", "email", "first_name", "last_name", "is_staff", "is_active"]


admin.site.register(CustomUser, CustomUserAdmin)
