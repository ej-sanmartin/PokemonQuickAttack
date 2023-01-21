from .pokemon import Pokemon
from .type_reader_helper import create_type_damage_relationship


def create_pokemon_data_from_response(response):
    """Takes API response and fills relevant fields in Pokemon dataclass."""

    # Handle getting all the type a pokemon can have.
    pokemon_type = list()
    for type in response.types:
        pokemon_type.append(type.type.name)

    pokemon_damage_type_relationship = create_type_damage_relationship(
        pokemon_type)

    pokemon_artwork = vars(vars(response.sprites.other)["official-artwork"])

    pokemon = Pokemon(
        name = response.name,
        img_url = pokemon_artwork["front_default"],
        types = pokemon_type,
        type_relationship = pokemon_damage_type_relationship,
    )

    return pokemon
