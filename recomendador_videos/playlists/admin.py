from django.contrib import admin
from .models import Playlist, PlaylistVideo, PlaylistRecomendacao

admin.site.register(Playlist)
admin.site.register(PlaylistVideo)
admin.site.register(PlaylistRecomendacao)