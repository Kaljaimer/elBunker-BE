from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, CheckIn

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_superuser', 'is_staff', 'is_active']
    list_filter = ['is_superuser', 'is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_superuser', 'is_active', 'is_staff')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

class CheckInAdmin(admin.ModelAdmin):
    list_display = ['user__email', 'user__name', 'user__lastname', 'check_in_time']
    list_filter = ['check_in_time']
    search_fields = ['user__email','user__lastname', 'user__name', 'user__lastname']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CheckIn, CheckInAdmin)
