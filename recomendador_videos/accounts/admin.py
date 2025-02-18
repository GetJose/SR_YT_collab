from django.contrib import admin
from .models import Interest, UserProfile

admin.site.register(Interest)
admin.site.register(UserProfile)

# @admin.register(UserProfile)
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'role', 'duracao_faixa')
#     list_filter = ('role',)
#     search_fields = ('user__username',)