from django.utils.html import format_html
from django.contrib import admin
from authentication.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "country",
        "phone_number",
        "otp",
        "city",
        "gender",
        "date_of_birth",
        "profile_pic",
    )
    search_fields = ("user__username", "phone_number", "email")
    readonly_fields = ("uid",)

    def profile_pic(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius: 50%;" />',
                obj.profile_picture.url,
            )
        return "No image"

    profile_pic.short_description = "Profile Picture"
