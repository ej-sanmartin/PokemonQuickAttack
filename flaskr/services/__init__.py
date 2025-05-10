"""Business logic and API handling services.
This module contains all the service layer code that handles API calls,
data processing, and business logic for the application."""
from flaskr.services.pokemon_reader_helper import get_pokemon_data
from flaskr.services.type_reader_helper import get_type_relationship

__all__ = ['get_pokemon_data', 'get_type_relationship']
