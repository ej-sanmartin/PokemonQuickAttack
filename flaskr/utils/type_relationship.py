from dataclasses import dataclass
from .type_list import TypeList

@dataclass(frozen=True)
class TypeRelationship:
    '''Type relationships, ex. fire is strong against water.'''

    # The type relationship this type has TOWARDS another type.
    no_damage_to: TypeList
    half_damage_to: TypeList
    double_damage_to: TypeList

    # The type relationship this type has FROM other types.
    no_damage_from: TypeList
    half_damage_from: TypeList
    duble_damage_from: TypeList
