from enum import Enum


class Search(Enum):
    """Specifies the two types of search criteria this site recognizes."""

    #: Search box will accept Pokemon names or Id numbers.
    POKEMON = 1
    #: Search will accept type names. For example, "fire", "water", etc.
    TYPE = 2

    @classmethod
    def enum_to_string(cls, search_enum):
        """Convert enum value to string representation.
        
        Args:
            search_enum: Search enum value to convert
            
        Returns:
            str: String representation of the enum value
        """
        if not isinstance(search_enum, cls):
            raise ValueError(f"Expected Search enum, got {type(search_enum)}")
        return search_enum.name

    @classmethod
    def string_to_enum(cls, search_string):
        """Convert string to enum value.
        
        Args:
            search_string: String to convert to enum
            
        Returns:
            Search: Enum value corresponding to the string
            
        Raises:
            ValueError: If string doesn't match any enum value
        """
        try:
            return cls[search_string.upper()]
        except KeyError:
            raise ValueError(f"Invalid search type: {search_string}")
