import pokebase as pb

from .type_relationship import TypeRelationship
from .util import _normalize_string


def _create_type_damage_relationship(target_types):
    """Given type(s), format the damage relationship into TypeRelationship."""

    types_api_response = list()

    for type in target_types:
        type_response = pb.type_(type)

        if vars(type_response)["id_"] is None:
            return {"error": True}

        types_api_response.append(type_response.damage_relations)

    type_relationship_output = TypeRelationship()

    for type_relationships in types_api_response:
        type_relationships = vars(type_relationships)
        for damage_relationship, types in type_relationships.items():
            setattr(type_relationship_output, damage_relationship, types)

    return type_relationship_output


def get_type_relationship(input_type):
    """Get and format type data from PokeAPI."""

    type = _normalize_string(input_type)
    return {"type_relationship": _create_type_damage_relationship([type])}
