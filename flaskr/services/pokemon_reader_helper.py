import pokebase as pb

from ..models.pokemon import Pokemon
from .type_reader_helper import _create_type_damage_relationship
from .util import _normalize_string


def _create_pokemon_dataclass(response):
    """Takes API response and fills relevant fields in Pokemon dataclass."""

    try:
        # Handle getting all the type a pokemon can have.
        pokemon_type = list()
        for type in response.types:
            pokemon_type.append(type.type.name)

        pokemon_damage_type_relationship = _create_type_damage_relationship(
            pokemon_type)

        # Safely get the artwork URL with a fallback
        try:
            pokemon_artwork = vars(vars(response.sprites.other)["official-artwork"])
            img_url = pokemon_artwork["front_default"]
        except (AttributeError, KeyError):
            img_url = response.sprites.front_default

        pokemon = Pokemon(
            name = response.name,
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
        api_response = pb.pokemon(pokemon)

        # Handles if pokemon does not exist in the API.
        if vars(api_response)["id_"] is None:
            return {"error": True}

        return _create_pokemon_dataclass(api_response)
    except Exception as e:
        return {"error": True}
