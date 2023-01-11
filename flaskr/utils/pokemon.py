from dataclasses import dataclass
from .type_relationship import TypeRelationship

@dataclass(frozen=True)
class Pokemon:
    '''Pokemon data, relevant to this application.'''

    name: str
    img_url: str
    type_relationship: TypeRelationship
