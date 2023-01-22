import pokebase as pb

from .pokemon import Pokemon
from .type_reader_helper import _create_type_damage_relationship
from .util import _normalize_string


def _create_pokemon_dataclass(response):
    """Takes API response and fills relevant fields in Pokemon dataclass."""

    # Handle getting all the type a pokemon can have.
    pokemon_type = list()
    for type in response.types:
        pokemon_type.append(type.type.name)

    pokemon_damage_type_relationship = _create_type_damage_relationship(
        pokemon_type)

    pokemon_artwork = vars(vars(response.sprites.other)["official-artwork"])

    pokemon = Pokemon(
        name = response.name,
        img_url = pokemon_artwork["front_default"],
        types = pokemon_type,
        type_relationship = pokemon_damage_type_relationship,
    )

    return pokemon


def get_pokemon_data(input_pokemon):
    """Get and format pokemon data from PokeAPI."""

    pokemon = _normalize_string(input_pokemon)
    api_response = pb.pokemon(pokemon)
    return _create_pokemon_dataclass(api_response)
