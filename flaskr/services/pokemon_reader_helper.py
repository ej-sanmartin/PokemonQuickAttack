import pokebase as pb
import requests

from flaskr.models.pokemon import Pokemon
from flaskr.services.type_reader_helper import _create_type_damage_relationship
from flaskr.utils.util import _normalize_string


def _create_pokemon_dataclass(response):
    """Takes API response and fills relevant fields in Pokemon dataclass."""

    try:
        # Handle getting all the type a pokemon can have.
        pokemon_type = list()
        for type_data in response['types']:
            pokemon_type.append(type_data['type']['name'])

        pokemon_damage_type_relationship = _create_type_damage_relationship(
            pokemon_type)

        # Safely get the artwork URL with a fallback
        try:
            img_url = response['sprites']['other']['official-artwork']['front_default']
        except (KeyError, TypeError):
            img_url = response['sprites']['front_default']

        pokemon = Pokemon(
            name = response['name'],
            img_url = img_url,
            types = pokemon_type,
            type_relationship = pokemon_damage_type_relationship,
        )

        return pokemon
    except Exception as e:
        return {"error": True}


def get_pokemon_data(input_pokemon):
    """Get and format pokemon data from PokeAPI."""

    try:
        pokemon = _normalize_string(input_pokemon)
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon}')
        response.raise_for_status()  # Raise an exception for bad status codes
        api_response = response.json()

        return _create_pokemon_dataclass(api_response)
    except Exception as e:
        return {"error": True}
