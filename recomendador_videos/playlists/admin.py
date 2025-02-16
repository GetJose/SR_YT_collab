from django.contrib import admin
from .models import Playlist, PlaylistVideo

admin.site.register(Playlist)
admin.site.register(PlaylistVideo)