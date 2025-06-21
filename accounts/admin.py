from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import UserForm, UserCreateForm

User = get_user_model()

class CustomUserAdmin(UserAdmin):
    add_form = UserCreateForm
    form = UserForm
    model = User
    list_display = [
        'username', 'email', 'first_name', 'last_name', 'role',
        'is_active', 'is_staff', 'is_superuser'
    ]
    list_filter = ['role', 'is_active', 'is_staff', 'is_superuser']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': (
            'first_name', 'last_name', 'email', 'profile_picture'
        )}),
        ('Professional Info', {'fields': (
            'role', 'phone_number', 'license_number',
            'specialization', 'department'
        )}),
        ('Permissions', {'fields': (
            'is_active', 'is_staff', 'is_superuser',
            'groups', 'user_permissions'
        )}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'first_name', 'last_name', 'role',
                'phone_number', 'license_number', 'specialization',
                'department', 'profile_picture', 'password1', 'password2'
            ),
        }),
    )
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['last_name', 'first_name']

admin.site.register(User, CustomUserAdmin)