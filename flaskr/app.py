from flask import Flask, request, render_template, redirect, url_for

from util.search_enum import Search

app = Flask(__name__)

# By default, set to POKEMON so search works on pokemon name or Id.
search = Search.POKEMON

@app.route("/")
def index():
    return render_template("index.html.jinja",
                           search=Search.enum_to_string(search))

@app.route("/search_type", methods=['POST'])
def change_search_type():
    global search
    # Prevents users from sending multiple requests that would cause an unneeded
    # re render. For instance, if the page is expecting a pokemon name, having
    # the user repeatedly press the "pokemon" button will re render the page.
    # The page should only be re rendered if its changing the search type.
    if (request.form.get('search') == Search.enum_to_string(search)):
        pass

    if request.form.get('search') == 'pokemon':
        search = Search.POKEMON
    elif request.form.get('search') == 'type': 
        search = Search.TYPE

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
