#!/usr/bin/env python3

from flask import Flask, request, render_template, redirect, url_for, session, flash
from functools import wraps
import os

from constants.search_enum import Search
from cache.main import (
    init_cache, get_cached_pokemon_data, get_cached_type_data,
    process_pokemon_data, process_type_data, get_all_pokemon_names
)
from utils.rate_limiter import init_rate_limiter

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-placeholder')
init_cache(app)
init_rate_limiter(app)

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
        
        template_data = {
            'search': Search.enum_to_string(search_type),
            'data': data
        }
        
        # Add pokemon names for autocomplete when in pokemon search mode
        if search_type == Search.POKEMON:
            template_data['pokemon_names'] = get_all_pokemon_names()
        
        return render_template("index.html.jinja", **template_data)
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
        # Clear any existing search data when switching modes
        session.pop('search_data', None)
    except ValueError as e:
        flash(str(e), 'error')
        session['search_type'] = Search.enum_to_string(Search.POKEMON)
        session.pop('search_data', None)
    
    return redirect(url_for('index'))

@app.route("/pokemon")
@search_type_required
@app.limiter.limit("10 per minute")
def get_pokemon():
    try:
        requested_pokemon = request.args.get('name', '')
        if not requested_pokemon:
            session['search_data'] = {'error': 'Please enter a Pokémon name'}
            return redirect(url_for('index'))
        
        flash('Searching for Pokémon...', 'loading')
        pokemon_data = get_cached_pokemon_data(requested_pokemon)
        session['search_data'] = process_pokemon_data(pokemon_data)
        
        # Remove the loading message since we have results
        session.pop('_flashes', None)
        return redirect(url_for('index'))
    except Exception as e:
        session['search_data'] = {'error': 'An unexpected error occurred'}
        return redirect(url_for('index'))

@app.route("/type")
@search_type_required
@app.limiter.limit("10 per minute")
def get_type():
    requested_type = request.args.get('name', '')
    if not requested_type:
        session['search_data'] = {'error': 'Please enter a type'}
        return redirect(url_for('index'))
    
    flash('Searching for type...', 'loading')
    type_data = get_cached_type_data(requested_type)
    session['search_data'] = process_type_data(requested_type, type_data)
    
    # Remove the loading message since we have results
    session.pop('_flashes', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
