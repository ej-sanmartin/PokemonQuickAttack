#!/usr/bin/env python3

from flask import Flask, request, render_template, redirect, url_for, session, flash
from functools import wraps

from utils.pokemon_reader_helper import get_pokemon_data
from utils.type_reader_helper import get_type_relationship
from utils.search_enum import Search
from utils.type_colors import TYPE_COLORS

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
        
        return render_template("index.html.jinja", 
                             search=Search.enum_to_string(search_type),
                             data=data)
    except ValueError as e:
        flash(str(e), 'error')
        session['search_type'] = Search.enum_to_string(Search.POKEMON)
        return redirect(url_for('index'))

@app.route("/search-type/<search_type>")
def change_search_type(search_type):
    try:
        # Convert the URL parameter to enum to validate it
        search_enum = Search.string_to_enum(search_type)
        # Store the validated string representation in session
        session['search_type'] = Search.enum_to_string(search_enum)
        flash(f'Search mode changed to {search_type.title()}', 'info')
    except ValueError as e:
        flash(str(e), 'error')
        session['search_type'] = Search.enum_to_string(Search.POKEMON)
    
    return redirect(url_for('index'))

@app.route("/pokemon")
@search_type_required
def get_pokemon():
    try:
        requested_pokemon = request.args.get('name', '')
        if not requested_pokemon:
            flash('Please enter a Pokémon name', 'error')
            return redirect(url_for('index'))
        
        flash('Searching for Pokémon...', 'loading')
        pokemon_data = get_pokemon_data(requested_pokemon)
        
        if isinstance(pokemon_data, dict) and pokemon_data.get('error'):
            flash('Pokémon not found', 'error')
            session['search_data'] = {}
        else:
            try:
                # Convert Pokemon dataclass to dictionary for session storage
                type_relationship = pokemon_data.type_relationship
                def zip_types(type_list):
                    return list(zip(type_list, [TYPE_COLORS.get(t.lower(), '#A8A77A') for t in type_list]))
                session['search_data'] = {
                    'name': pokemon_data.name,
                    'img_url': pokemon_data.img_url,
                    'types': pokemon_data.types,
                    'type_colors': [TYPE_COLORS.get(t.lower(), '#A8A77A') for t in pokemon_data.types],
                    'zipped_types': list(zip(pokemon_data.types, [TYPE_COLORS.get(t.lower(), '#A8A77A') for t in pokemon_data.types])),
                    'type_relationship': {
                        'no_damage_to': getattr(type_relationship, 'no_damage_to', []),
                        'half_damage_to': getattr(type_relationship, 'half_damage_to', []),
                        'double_damage_to': getattr(type_relationship, 'double_damage_to', []),
                        'no_damage_from': getattr(type_relationship, 'no_damage_from', []),
                        'half_damage_from': getattr(type_relationship, 'half_damage_from', []),
                        'double_damage_from': getattr(type_relationship, 'double_damage_from', []),
                        'zipped_no_damage_to': zip_types(getattr(type_relationship, 'no_damage_to', [])),
                        'zipped_half_damage_to': zip_types(getattr(type_relationship, 'half_damage_to', [])),
                        'zipped_double_damage_to': zip_types(getattr(type_relationship, 'double_damage_to', [])),
                        'zipped_no_damage_from': zip_types(getattr(type_relationship, 'no_damage_from', [])),
                        'zipped_half_damage_from': zip_types(getattr(type_relationship, 'half_damage_from', [])),
                        'zipped_double_damage_from': zip_types(getattr(type_relationship, 'double_damage_from', [])),
                    }
                }
                # Remove the loading message since we have results
                session.pop('_flashes', None)
            except Exception as e:
                flash('Error processing Pokémon data', 'error')
                session['search_data'] = {}
        
        return redirect(url_for('index'))
    except Exception as e:
        flash('An unexpected error occurred', 'error')
        session['search_data'] = {}
        return redirect(url_for('index'))

@app.route("/type")
@search_type_required
def get_type():
    requested_type = request.args.get('name', '')
    if not requested_type:
        flash('Please enter a type', 'error')
        return redirect(url_for('index'))
    
    flash('Searching for type...', 'loading')
    type_data = get_type_relationship(requested_type)
    
    if type_data.get('error'):
        flash('Type not found', 'error')
        session['search_data'] = {}
    else:
        type_data["type"] = requested_type
        type_name = requested_type.lower()
        # Add color for the type
        type_data["type_color"] = TYPE_COLORS.get(type_name, '#A8A77A')
        session['search_data'] = type_data
        # Remove the loading message since we have results
        session.pop('_flashes', None)
    
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
