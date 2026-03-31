import random
import requests
from django.core.cache import cache

POKEAPI_BASE = "https://pokeapi.co/api/v2"

# Types we want to expose (excluding stellar/unknown)
AVAILABLE_TYPES = [
    'normal', 'fighting', 'flying', 'poison', 'ground',
    'rock', 'bug', 'ghost', 'steel', 'fire', 'water',
    'grass', 'electric', 'psychic', 'ice', 'dragon',
    'dark', 'fairy',
]

TYPE_EMOJIS = {
    'normal': '⚪', 'fighting': '🥊', 'flying': '🦅', 'poison': '☠️',
    'ground': '🌎', 'rock': '🪨', 'bug': '🐛', 'ghost': '👻',
    'steel': '⚙️', 'fire': '🔥', 'water': '💧', 'grass': '🌿',
    'electric': '⚡', 'psychic': '🔮', 'ice': '❄️', 'dragon': '🐉',
    'dark': '🌑', 'fairy': '✨',
}

TYPE_COLORS = {
    'normal': '#A8A878', 'fighting': '#C03028', 'flying': '#A890F0',
    'poison': '#A040A0', 'ground': '#E0C068', 'rock': '#B8A038',
    'bug': '#A8B820', 'ghost': '#705898', 'steel': '#B8B8D0',
    'fire': '#F08030', 'water': '#6890F0', 'grass': '#78C850',
    'electric': '#F8D030', 'psychic': '#F85888', 'ice': '#98D8D8',
    'dragon': '#7038F8', 'dark': '#705848', 'fairy': '#EE99AC',
}


def get_type_pokemon_list(type_name: str) -> list:
    """Get list of Pokémon for a given type, with caching."""
    cache_key = f"type_pokemon_{type_name}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    try:
        resp = requests.get(f"{POKEAPI_BASE}/type/{type_name}/", timeout=10)
        resp.raise_for_status()
        data = resp.json()
        # Filter to only include normal Pokémon (id < 10000 to exclude mega forms etc)
        pokemon_list = [
            p['pokemon'] for p in data.get('pokemon', [])
            if _extract_id_from_url(p['pokemon']['url']) < 10000
        ]
        cache.set(cache_key, pokemon_list, 3600)  # Cache 1hr
        return pokemon_list
    except requests.RequestException:
        return []


def get_random_pokemon_of_type(type_name: str, excluded_ids: list = None) -> dict | None:
    """Pick a random Pokémon of a type and fetch its full data."""
    pokemon_list = get_type_pokemon_list(type_name)
    if not pokemon_list:
        return None

    excluded_ids = excluded_ids or []
    # Filter out already captured
    available = [p for p in pokemon_list if _extract_id_from_url(p['url']) not in excluded_ids]
    if not available:
        available = pokemon_list  # fallback: allow duplicates

    chosen = random.choice(available)
    return fetch_pokemon_data(chosen['name'])


def fetch_pokemon_data(identifier) -> dict | None:
    """Fetch full Pokémon data from PokeAPI."""
    cache_key = f"pokemon_data_{identifier}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    try:
        resp = requests.get(f"{POKEAPI_BASE}/pokemon/{identifier}/", timeout=10)
        resp.raise_for_status()
        data = resp.json()

        stats_map = {s['stat']['name']: s['base_stat'] for s in data['stats']}
        types = [t['type']['name'] for t in data['types']]

        result = {
            'pokeapi_id': data['id'],
            'name': data['name'],
            'image_url': (
                data['sprites'].get('other', {}).get('official-artwork', {}).get('front_default')
                or data['sprites'].get('front_default')
                or ''
            ),
            'types': types,
            'hp': stats_map.get('hp', 0),
            'attack': stats_map.get('attack', 0),
            'defense': stats_map.get('defense', 0),
            'special_attack': stats_map.get('special-attack', 0),
            'special_defense': stats_map.get('special-defense', 0),
            'speed': stats_map.get('speed', 0),
        }
        cache.set(cache_key, result, 3600)
        return result
    except requests.RequestException:
        return None


def _extract_id_from_url(url: str) -> int:
    try:
        return int(url.rstrip('/').split('/')[-1])
    except (ValueError, IndexError):
        return 0
