from flask import Flask, request, render_template, redirect, url_for
import pokebase as pb

from utils.pokemon_reader_helper import *
from utils.search_enum import Search

app = Flask(__name__)

# By default, set to POKEMON so search works on pokemon name or Id.
search = Search.POKEMON


@app.route("/")
def index():
    charmander = pb.pokemon('charmander')
    print(vars(charmander))
    charmander_object = create_pokemon_data_from_response(charmander)
    print(vars(charmander_object))
    return render_template("index.html.jinja",
                           search=Search.enum_to_string(search))


@app.route("/search-type", methods=['POST'])
def search_type():
    global search
    # Prevents users from sending multiple requests that would cause an unneeded
    # re render. For instance, if the page is expecting a pokemon name, having
    # the user repeatedly press the "pokemon" button will re render the page.
    # The page should only be re rendered if it's changing the search type.
    if (request.form.get('search') == Search.enum_to_string(search)):
        pass

    search = Search.POKEMON if request.form.get('search') == 'pokemon' else Search.TYPE

    return redirect(url_for('index'))


@app.route("/pokemon", methods=['GET'])
def pokemon():
    pass


@app.route("/pokemon-type", methods=['GET'])
def pokemon_type():
    pass


if __name__ == "__main__":
    app.run()
