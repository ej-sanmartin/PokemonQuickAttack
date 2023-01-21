from dataclasses import dataclass

from .type_relationship import TypeRelationship


@dataclass(frozen=True)
class Pokemon:
    '''Pokemon data, relevant to this application.'''

    # Pokemon name.
    name: str

    # URL to image of pokemon.
    img_url: str

    # List of types of this pokemon.
    types: list()

    # List of types this pokemon is strong and weak against.    
    type_relationship: TypeRelationship
