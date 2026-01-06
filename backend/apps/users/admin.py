from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your custom user model
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # This adds your custom fields (Index & WhatsApp) to the Admin edit page
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('index_number', 'whatsapp_number')}),
    )
    # This adds them to the "Add User" page
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('index_number', 'whatsapp_number')}),
    )
    # This shows them in the main list of users
    list_display = ['username', 'email', 'index_number', 'whatsapp_number', 'is_staff']