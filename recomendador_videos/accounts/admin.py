from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Interest
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Perfil do Usuário"
    filter_horizontal = ('interests',)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['role']  # Somente administradores podem editar o campo
        return []

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

