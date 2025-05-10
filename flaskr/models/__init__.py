"""Data models and class definitions for the application.
This module contains all the data structures and classes that represent
the core entities of the application (Pokemon, Types, etc.)."""
from flaskr.models.pokemon import Pokemon
from flaskr.models.type_relationship import TypeRelationship

__all__ = ['Pokemon', 'TypeRelationship']
