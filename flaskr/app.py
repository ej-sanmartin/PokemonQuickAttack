#!/usr/bin/env python3

from flask import Flask, request, render_template, redirect, url_for, session, flash
from functools import wraps

from utils.pokemon_reader_helper import get_pokemon_data
from utils.type_reader_helper import get_type_relationship
from utils.search_enum import Search

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for sessions and flash messages

def search_type_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'search_type' not in session:
            session['search_type'] = Search.enum_to_string(Search.POKEMON)
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
@search_type_required
def index():
    try:
        search_type = Search.string_to_enum(session.get('search_type', 'POKEMON'))
        data = session.get('search_data', {})
        print(f"Data being passed to template: {data}")  # Debug log
        
        return render_template("index.html.jinja", 
                             search=Search.enum_to_string(search_type),
                             data=data)
    except ValueError as e:
        flash(str(e))
        session['search_type'] = Search.enum_to_string(Search.POKEMON)
        return redirect(url_for('index'))

@app.route("/search-type/<search_type>")
def change_search_type(search_type):
    try:
        # Convert the URL parameter to enum to validate it
        search_enum = Search.string_to_enum(search_type)
        # Store the validated string representation in session
        session['search_type'] = Search.enum_to_string(search_enum)
        flash(f'Search mode changed to {search_type.title()}')
    except ValueError as e:
        flash(str(e))
        session['search_type'] = Search.enum_to_string(Search.POKEMON)
    
    return redirect(url_for('index'))

@app.route("/pokemon")
@search_type_required
def get_pokemon():
    try:
        requested_pokemon = request.args.get('name', '')
        if not requested_pokemon:
            flash('Please enter a Pokémon name')
            return redirect(url_for('index'))
        
        flash('Searching for Pokémon...')
        print(f"Searching for Pokémon: {requested_pokemon}")  # Debug log
        
        pokemon_data = get_pokemon_data(requested_pokemon)
        print(f"Pokemon data type: {type(pokemon_data)}")  # Debug log
        
        if isinstance(pokemon_data, dict) and pokemon_data.get('error'):
            flash('Pokémon not found')
            session['search_data'] = {}
        else:
            try:
                # Convert Pokemon dataclass to dictionary for session storage
                type_relationship = pokemon_data.type_relationship
                session['search_data'] = {
                    'name': pokemon_data.name,
                    'img_url': pokemon_data.img_url,
                    'types': pokemon_data.types,
                    'type_relationship': {
                        'no_damage_to': getattr(type_relationship, 'no_damage_to', []),
                        'half_damage_to': getattr(type_relationship, 'half_damage_to', []),
                        'double_damage_to': getattr(type_relationship, 'double_damage_to', []),
                        'no_damage_from': getattr(type_relationship, 'no_damage_from', []),
                        'half_damage_from': getattr(type_relationship, 'half_damage_from', []),
                        'double_damage_from': getattr(type_relationship, 'double_damage_from', [])
                    }
                }
                print(f"Session data: {session['search_data']}")  # Debug log
                flash('Pokémon found!')
            except Exception as e:
                print(f"Error processing Pokemon data: {str(e)}")  # Debug log
                flash('Error processing Pokémon data')
                session['search_data'] = {}
        
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Unexpected error in get_pokemon: {str(e)}")  # Debug log
        flash('An unexpected error occurred')
        session['search_data'] = {}
        return redirect(url_for('index'))

@app.route("/type")
@search_type_required
def get_type():
    requested_type = request.args.get('name', '')
    if not requested_type:
        flash('Please enter a type')
        return redirect(url_for('index'))
    
    flash('Searching for type...')
    type_data = get_type_relationship(requested_type)
    
    if type_data.get('error'):
        flash('Type not found')
        session['search_data'] = {}
    else:
        type_data["type"] = requested_type
        session['search_data'] = type_data
        flash('Type found!')
    
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
