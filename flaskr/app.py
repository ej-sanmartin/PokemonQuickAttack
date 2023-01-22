from flask import Flask, request, render_template, redirect, url_for

from utils.pokemon_reader_helper import get_pokemon_data
from utils.type_reader_helper import get_type_relationship
from utils.search_enum import Search

app = Flask(__name__)

# By default, set to POKEMON so search works on pokemon name or Id.
search = Search.POKEMON


@app.route("/")
def index():
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
def get_pokemon():
    pass


@app.route("/type", methods=['GET'])
def get_type():
    pass


if __name__ == "__main__":
    app.run()
