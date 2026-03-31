import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import F

from .models import Pokemon
from .services import (
    get_random_pokemon_of_type, AVAILABLE_TYPES,
    TYPE_EMOJIS, TYPE_COLORS
)

MAX_PARTY_SIZE = 6


def _get_type_display_info():
    return [
        {
            'name': t,
            'label': t.capitalize(),
            'emoji': TYPE_EMOJIS.get(t, '❓'),
            'color': TYPE_COLORS.get(t, '#888'),
        }
        for t in AVAILABLE_TYPES
    ]


def _get_party_and_box():
    party = list(Pokemon.objects.filter(location=Pokemon.LOCATION_PARTY).order_by('order', 'captured_at'))
    box = list(Pokemon.objects.filter(location=Pokemon.LOCATION_PC).order_by('order', 'captured_at'))
    return party, box


def index(request):
    party, box = _get_party_and_box()
    context = {
        'party': party,
        'box': box,
        'types': _get_type_display_info(),
        'type_colors': json.dumps(TYPE_COLORS),
        'type_emojis': json.dumps(TYPE_EMOJIS),
        'max_party': MAX_PARTY_SIZE,
        'party_count': len(party),
        'box_count': len(box),
        'total_count': len(party) + len(box),
    }
    return render(request, 'party/index.html', context)


@require_POST
def capture_pokemon(request):
    selected_type = request.POST.get('pokemon_type', 'fire')
    if selected_type not in AVAILABLE_TYPES:
        selected_type = 'fire'

    existing_ids = list(Pokemon.objects.values_list('pokeapi_id', flat=True))
    pokemon_data = get_random_pokemon_of_type(selected_type, excluded_ids=existing_ids)

    if not pokemon_data:
        messages.error(request, f"No se pudo obtener un Pokémon de tipo {selected_type}. Intenta de nuevo.")
        return redirect('party:index')

    # Avoid duplicates
    if Pokemon.objects.filter(pokeapi_id=pokemon_data['pokeapi_id']).exists():
        messages.warning(request, f"¡{pokemon_data['name'].capitalize()} ya está en tu colección!")
        return redirect('party:index')

    party_count = Pokemon.objects.filter(location=Pokemon.LOCATION_PARTY).count()

    if party_count < MAX_PARTY_SIZE:
        location = Pokemon.LOCATION_PARTY
        order = party_count
    else:
        location = Pokemon.LOCATION_PC
        order = Pokemon.objects.filter(location=Pokemon.LOCATION_PC).count()

    pokemon = Pokemon.objects.create(
        location=location,
        order=order,
        **pokemon_data
    )

    location_label = "Party 🎉" if location == Pokemon.LOCATION_PARTY else "PC Box 📦"
    messages.success(request, f"¡{pokemon.name.capitalize()} capturado y enviado a {location_label}!")
    return redirect('party:index')


@require_POST
def optimize_party(request):
    """Select the 6 Pokémon with the highest total_power for the party."""
    all_pokemon = list(Pokemon.objects.all().order_by('-total_power'))

    for i, poke in enumerate(all_pokemon):
        if i < MAX_PARTY_SIZE:
            poke.location = Pokemon.LOCATION_PARTY
            poke.order = i
        else:
            poke.location = Pokemon.LOCATION_PC
            poke.order = i - MAX_PARTY_SIZE
        poke.save()

    messages.success(request, "✨ ¡Equipo optimizado! Los 6 Pokémon más poderosos están en tu Party.")
    return redirect('party:index')


@require_POST
def sort_party(request):
    """Sort party by a given stat."""
    stat = request.POST.get('stat', 'total_power')
    valid_stats = ['hp', 'attack', 'defense', 'special_attack', 'special_defense', 'speed', 'total_power']
    if stat not in valid_stats:
        stat = 'total_power'

    party = list(Pokemon.objects.filter(location=Pokemon.LOCATION_PARTY).order_by(f'-{stat}'))
    for i, poke in enumerate(party):
        poke.order = i
        poke.save(update_fields=['order'])

    stat_labels = {
        'hp': 'HP', 'attack': 'Ataque', 'defense': 'Defensa',
        'special_attack': 'Ataque Esp.', 'special_defense': 'Defensa Esp.',
        'speed': 'Velocidad', 'total_power': 'Poder Total'
    }
    messages.info(request, f"Party ordenada por {stat_labels.get(stat, stat)}.")
    return redirect('party:index')


@require_POST
def move_to_party(request, pk):
    """Move a Pokémon from PC Box to Party (if space available)."""
    pokemon = get_object_or_404(Pokemon, pk=pk)
    party_count = Pokemon.objects.filter(location=Pokemon.LOCATION_PARTY).count()

    if party_count >= MAX_PARTY_SIZE:
        messages.error(request, "¡Tu Party está llena! Mueve un Pokémon al PC primero.")
    else:
        pokemon.location = Pokemon.LOCATION_PARTY
        pokemon.order = party_count
        pokemon.save()
        messages.success(request, f"¡{pokemon.name.capitalize()} se unió a la Party!")

    return redirect('party:index')


@require_POST
def move_to_pc(request, pk):
    """Move a Pokémon from Party to PC Box."""
    pokemon = get_object_or_404(Pokemon, pk=pk)
    pc_count = Pokemon.objects.filter(location=Pokemon.LOCATION_PC).count()
    pokemon.location = Pokemon.LOCATION_PC
    pokemon.order = pc_count
    pokemon.save()
    messages.info(request, f"{pokemon.name.capitalize()} fue enviado al PC Box.")
    return redirect('party:index')


@require_POST
def release_pokemon(request, pk):
    """Release (delete) a Pokémon."""
    pokemon = get_object_or_404(Pokemon, pk=pk)
    name = pokemon.name.capitalize()
    pokemon.delete()
    messages.warning(request, f"¡{name} fue liberado! 👋")
    return redirect('party:index')


def pokemon_stats_api(request, pk):
    """JSON endpoint for chart data."""
    pokemon = get_object_or_404(Pokemon, pk=pk)
    return JsonResponse({
        'name': pokemon.name,
        'stats': {
            'HP': pokemon.hp,
            'Ataque': pokemon.attack,
            'Defensa': pokemon.defense,
            'Atq. Esp.': pokemon.special_attack,
            'Def. Esp.': pokemon.special_defense,
            'Velocidad': pokemon.speed,
        },
        'total': pokemon.total_power,
        'types': pokemon.types,
    })
