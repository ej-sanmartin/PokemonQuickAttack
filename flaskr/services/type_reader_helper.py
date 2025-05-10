import pokebase as pb

from ..models.type_relationship import TypeRelationship
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
            # Extract type names from the type objects
            type_names = [type_obj.name for type_obj in types]
            setattr(type_relationship_output, damage_relationship, type_names)

    return type_relationship_output


def get_type_relationship(input_type):
    """Get and format type data from PokeAPI."""

    type = _normalize_string(input_type)
    relationship = _create_type_damage_relationship([type])
    if isinstance(relationship, dict) and relationship.get("error"):
        return {"error": True}
    return {"type": type, "type_relationship": relationship}
