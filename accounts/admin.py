from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class FarmUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    fieldsets = UserAdmin.fieldsets + (('Farm', {'fields': ('role', 'phone')}),)
    add_fieldsets = UserAdmin.add_fieldsets + (('Farm', {'fields': ('role', 'phone')}),)