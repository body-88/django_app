from django.contrib import admin
from django.utils.translation import gettext_lazy as _
# to avoid name conflict with UserAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile

# Register your models here.


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    # specified whether the inline object can be deleted through the other
    # object or not. Still not that important, but it is preferable not to.
    can_delete = False


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
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
    # class defines an Inline object for the admin panel. That is, an object
    # that it is displayed as part of another object “inline”
    inlines = (UserProfileInline,)
