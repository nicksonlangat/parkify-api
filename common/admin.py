# -*- coding: utf-8 -*-
from django.apps import apps
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()

UserAdmin.ordering = ("email",)

UserAdmin.add_fieldsets = (
    (
        None,
        {
            "classes": ("wide",),
            "fields": (
                "first_name",
                "last_name",
                "email",
                "is_superuser",
                "is_staff",
                "password1",
                "password2",
            ),
        },
    ),
)

for model in apps.get_models():
    model_name = model._meta.model_name
    model_admin = type(model_name + "Admin", (admin.ModelAdmin,), {})
    if model == User:
        model_admin = UserAdmin
    model_admin.list_display = (
        model.admin_list_display
        if hasattr(model, "admin_list_display")
        else tuple(
            field.name for field in model._meta.fields if field.name != "password"
        )
    )
    model_admin.list_display_links = (
        model.admin_list_display_links
        if hasattr(model, "admin_list_display_links")
        else ()
    )

    model_admin.list_editable = (
        model.admin_list_editable if hasattr(model, "admin_list_editable") else ()
    )
    model_admin.search_fields = (
        model.admin_search_fields if hasattr(model, "admin_search_fields") else ()
    )
    try:
        admin.site.register(model, model_admin)
    except Exception:
        pass
