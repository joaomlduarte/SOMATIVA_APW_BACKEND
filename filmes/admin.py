from django.contrib import admin

from .models import Favorito, Filme


@admin.register(Filme)
class FilmeAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'genero', 'ano_lancamento']
    list_filter = ['genero']
    search_fields = ['titulo']


@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'filme', 'data_favoritado']
    list_filter = ['usuario']
