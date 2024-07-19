from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from simple_history.admin import SimpleHistoryAdmin

from accounts.service.active_email import SendActiveEmailService

from .models import CustomUser


class CustomUserAdmin(UserAdmin, SimpleHistoryAdmin):
    model = CustomUser
    ordering = ["username"]
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

    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("email",)}),)

    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("institution", "languages", "subject")}),)
    history_list_display = ["username", "email", "first_name", "last_name", "is_staff", "is_active"]

    def save_model(self, request, obj, form, change):
        if not change:  # Only send the email when a new user is created
            obj.is_active = False  # Deactivate account until it is confirmed
            obj.save()

            SendActiveEmailService.send_activation_email(request, obj)

        else:
            obj.save()


admin.site.register(CustomUser, CustomUserAdmin)
