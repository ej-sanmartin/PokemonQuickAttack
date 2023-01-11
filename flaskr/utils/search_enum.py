from enum import Enum

class Search(Enum):
    """Specifies the two types of search criteria this site recognizes."""

    #: Search box will accept Pokemon names or Id numbers.
    POKEMON = 1
    #: Search will accept type names. For example, "fire", "water", etc.
    TYPE = 2

    # Helper method to turn enum values to strings.
    @classmethod
    def enum_to_string(cls, _search):
        if _search is cls.POKEMON:
            return 'POKEMON'
        return 'TYPE'
