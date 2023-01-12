import pokebase as pb

from .type_relationship import TypeRelationship


def create_type_damage_relationship(target_types):
    """Given type(s), format the damage relationship into TypeRelationship"""

    types_api_response = list()

    for type in target_types:
        types_api_response.append(pb.type(type).damage_relations)

    type_relationship_output = TypeRelationship()

    for type_relationship in types_api_response:
        for damage_relationship in type_relationship:
            for key in damage_relationship.keys():
                if key == "name":
                    type_relationship_output.key += damage_relationship.key
    
    return type_relationship_output
