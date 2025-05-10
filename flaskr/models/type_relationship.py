from dataclasses import dataclass, field


@dataclass
class TypeRelationship():
    '''Type relationships, ex. fire is strong against water.'''

    # The type relationship this type has TOWARDS another type.
    # This type is not very effective against...
    no_damage_to: list() = field(default_factory=list, repr=False,
                                    init=False)
    # This type is not effective against...
    half_damage_to: list() = field(default_factory=list, repr=False,
                                      init=False)
    # This type is super effective against..
    double_damage_to: list() = field(default_factory=list, repr=False,
                                        init=False)

    # The type relationship this type has FROM other types.
    # This type takes no damage from...
    no_damage_from: list() = field(default_factory=list, repr=False,
                                      init=False)
    # This type is not very effected by...
    half_damage_from: list() = field(default_factory=list, repr=False,
                                        init=False)
    # This type takes super effective damage from...
    double_damage_from: list() = field(default_factory=list, repr=False,
                                          init=False)
