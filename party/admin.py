from django.contrib import admin
from .models import Pokemon


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display = ['name', 'pokeapi_id', 'location', 'total_power', 'hp', 'attack', 'defense', 'speed', 'captured_at']
    list_filter = ['location']
    search_fields = ['name']
    readonly_fields = ['total_power', 'captured_at']
    ordering = ['-total_power']
