from enum import Enum

class Search(Enum):
    """Specifies the two types of search criteria this site recognizes."""

    #: Search box will accept Pokemon names or Id numbers.
    POKEMON = 1
    #: Search will accept type names. For example, "fire", "water", etc.
    TYPE = 2

    @classmethod
    def enum_to_string(enum, _search):
        if _search is enum.POKEMON:
            return 'POKEMON'
        return 'TYPE'
