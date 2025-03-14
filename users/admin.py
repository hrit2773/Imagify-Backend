from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from .forms import CustomUserChangeForm,CustomUserCreationForm
from .models import User

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model=User
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("is_staff", "is_active"),
            },
        ),
    )
    
    list_display = ( "email", "is_staff", "is_active")
    list_filter = ( "email", "is_staff", "is_active")
    ordering=("email","first_name")
    search_fields = ( "email", "is_active")

admin.site.register(User,CustomUserAdmin)