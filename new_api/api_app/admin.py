from django.contrib import admin
from django.db.models import fields
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin # to avoid name conflict with UserAdmin
from .models import User, UserProfile

# Register your models here.
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False # specified whether the inline object can be deleted through the other object or not. Still not that important, but it is preferable not to.


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',) 
    inlines = (UserProfileInline,)   # class defines an Inline object for the admin panel. That is, an object that it is displayed as part of another object “inline”