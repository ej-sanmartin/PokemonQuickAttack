"""Cache implementation for Pokemon Quick Guide application."""
from flask import current_app
import pokebase as pb
import requests
from services.pokemon_reader_helper import get_pokemon_data
from services.type_reader_helper import get_type_relationship
from constants.type_colors import TYPE_COLORS
from flask_caching import Cache

cache = Cache()

def init_cache(app):
    """Initialize cache with the Flask app."""
    cache.init_app(app, config={
        'CACHE_TYPE': 'SimpleCache',
        'CACHE_DEFAULT_TIMEOUT': 300  # 5 minutes cache timeout
    })
    with app.app_context():
        _init_pokemon_names_cache()

def _init_pokemon_names_cache():
    """Initialize the cache with all Pokémon names."""
    try:
        # Get all Pokémon from the API using requests
        response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=1026')
        response.raise_for_status()  # Raise an exception for bad status codes
        pokemon_data = response.json()
        pokemon_names = [pokemon['name'] for pokemon in pokemon_data['results']]
        cache.set('pokemon_names', pokemon_names)
        current_app.logger.info(f"Successfully cached {len(pokemon_names)} Pokémon names")
    except Exception as e:
        current_app.logger.error(f"Error initializing pokemon names cache: {e}")
        cache.set('pokemon_names', [])

@cache.memoize(timeout=300)
def get_all_pokemon_names():
    """Get all cached Pokémon names."""
    return cache.get('pokemon_names') or []

def zip_types(type_list):
    """Helper function to zip types with their colors."""
    return list(zip(type_list, [TYPE_COLORS.get(t.lower(), '#A8A77A') for t in type_list]))

@cache.memoize(timeout=300)
def get_cached_pokemon_data(pokemon_name):
    """Get cached Pokemon data."""
    return get_pokemon_data(pokemon_name)

@cache.memoize(timeout=300)
def get_cached_type_data(type_name):
    """Get cached type data."""
    return get_type_relationship(type_name)

def process_pokemon_data(pokemon_data):
    """Process Pokemon data for display."""
    if isinstance(pokemon_data, dict) and pokemon_data.get('error'):
        return {'error': 'Pokémon not found'}
    
    try:
        type_relationship = pokemon_data.type_relationship
        return {
            'name': pokemon_data.name,
            'img_url': pokemon_data.img_url,
            'types': pokemon_data.types,
            'type_colors': [TYPE_COLORS.get(t.lower(), '#A8A77A') 
                          for t in pokemon_data.types],
            'zipped_types': zip_types(pokemon_data.types),
            'type_relationship': {
                'no_damage_to': getattr(type_relationship, 'no_damage_to', []),
                'half_damage_to': getattr(type_relationship, 'half_damage_to', []),
                'double_damage_to': getattr(type_relationship, 'double_damage_to', []),
                'no_damage_from': getattr(type_relationship, 'no_damage_from', []),
                'half_damage_from': getattr(type_relationship, 'half_damage_from', []),
                'double_damage_from': getattr(type_relationship, 'double_damage_from', []),
                'zipped_no_damage_to': zip_types(getattr(type_relationship, 'no_damage_to', [])),
                'zipped_half_damage_to': zip_types(getattr(type_relationship, 'half_damage_to', [])),
                'zipped_double_damage_to': zip_types(getattr(type_relationship, 'double_damage_to', [])),
                'zipped_no_damage_from': zip_types(getattr(type_relationship, 'no_damage_from', [])),
                'zipped_half_damage_from': zip_types(getattr(type_relationship, 'half_damage_from', [])),
                'zipped_double_damage_from': zip_types(getattr(type_relationship, 'double_damage_from', [])),
            }
        }
    except Exception:
        return {'error': 'Error processing Pokémon data'}

def process_type_data(type_name, type_data):
    """Process type data for display."""
    if type_data.get('error'):
        return {'error': 'No Results Found :('}
    
    type_data["type"] = type_name
    type_name_lower = type_name.lower()
    type_data["type_color"] = TYPE_COLORS.get(type_name_lower, '#A8A77A')
    
    tr = type_data["type_relationship"]
    type_data["type_relationship"] = {
        'no_damage_to': getattr(tr, 'no_damage_to', []),
        'half_damage_to': getattr(tr, 'half_damage_to', []),
        'double_damage_to': getattr(tr, 'double_damage_to', []),
        'no_damage_from': getattr(tr, 'no_damage_from', []),
        'half_damage_from': getattr(tr, 'half_damage_from', []),
        'double_damage_from': getattr(tr, 'double_damage_from', []),
        'zipped_no_damage_to': zip_types(getattr(tr, 'no_damage_to', [])),
        'zipped_half_damage_to': zip_types(getattr(tr, 'half_damage_to', [])),
        'zipped_double_damage_to': zip_types(getattr(tr, 'double_damage_to', [])),
        'zipped_no_damage_from': zip_types(getattr(tr, 'no_damage_from', [])),
        'zipped_half_damage_from': zip_types(getattr(tr, 'half_damage_from', [])),
        'zipped_double_damage_from': zip_types(getattr(tr, 'double_damage_from', [])),
    }
    return type_data 