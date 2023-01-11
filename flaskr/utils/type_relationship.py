from dataclasses import dataclass
from .type_list import TypeList

@dataclass(frozen=True)
class TypeRelationship:
    '''Type relationships, ex. fire is strong against water.'''

    # The type relationship this type has TOWARDS another type.
    # This type is not very effective against...
    no_damage_to: TypeList
    # This type is not effective against...
    half_damage_to: TypeList
    # This type is super effective against..
    double_damage_to: TypeList

    # The type relationship this type has FROM other types.
    # This type takes no damage from...
    no_damage_from: TypeList
    # This type is not very effected by...
    half_damage_from: TypeList
    # This type takes super effective damage from...
    double_damage_from: TypeList
