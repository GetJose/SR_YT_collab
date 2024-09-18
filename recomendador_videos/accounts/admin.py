from django.contrib import admin

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)  # Exibe o nome do usuário na lista

