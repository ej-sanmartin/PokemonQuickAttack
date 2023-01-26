#!/usr/bin/env python3

from flask import Flask, request, render_template, redirect, url_for

from utils.pokemon_reader_helper import get_pokemon_data
from utils.type_reader_helper import get_type_relationship
from utils.search_enum import Search

app = Flask(__name__)

# Global. By default, set to POKEMON so search works on pokemon name or Id.
search = Search.POKEMON

poke_data = {}
type_data = {}


@app.route("/")
def index():
    if search is Search.POKEMON:
        return render_template("index.html.jinja",
                            search=Search.enum_to_string(search),
                            data = poke_data)
    
    return render_template("index.html.jinja",
                            search=Search.enum_to_string(search),
                            data = type_data)


@app.route("/search-type", methods=['POST'])
def search_type():
    global search
    # Prevents users from sending multiple requests that would cause an unneeded
    # re render. For instance, if the page is expecting a pokemon name, having
    # the user repeatedly press the "pokemon" button will re render the page.
    # The page should only be re rendered if it's changing the search type.
    if (request.form.get('search') == Search.enum_to_string(search)):
        pass

    # TODO: Refactor to make this statement not go over the 80 char line limit.
    search = Search.POKEMON if request.form.get('search') == 'pokemon' else Search.TYPE

    return redirect(url_for('index'))


@app.route("/pokemon", methods=['POST'])
def get_pokemon():
    global poke_data
    poke_data = {}

    requested_pokemon = request.form.get('pokemon')
    poke_data = get_pokemon_data(requested_pokemon)

    return redirect(url_for('index'))


@app.route("/type", methods=['POST'])
def get_type():
    global type_data
    type_data = {}

    requested_type = request.form.get('type')
    type_data = get_type_relationship(requested_type)

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run()
