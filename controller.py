from flask import Flask, request, render_template

from Filmflix_db import Filmflix_db

app = Flask(__name__, template_folder='templates')


@app.get('/')
def index_page():
    return render_template("base.html")


@app.get('/films')
def all_films():
    films = Filmflix_db().get_all_films()
    columns = ['FILM ID', 'TITLE', 'YEAR RELEASED', 'RATING', 'DURATION', 'GENRE']
    data = {'columns': columns, 'films': films}
    return render_template('films.html', data=data)


@app.route('/AddFilm', methods=['GET', 'POST'])
def add_film():
    film_db = Filmflix_db()

    if request.method == 'POST':
        columns = ['title', 'yearReleased', 'rating', 'duration', 'genre']
        for column in columns:
            if column not in request.form:
                error_message = f'Mandatory field {column} not present in request to "add_film"'
                return render_template("addfilm.html", error=error_message)

        existing_films = film_db.get_films_by_x(title=request.form['title'], yearReleased=request.form['yearReleased'], rating=request.form['rating'], duration=request.form['duration'], genre=request.form['genre'])
        if existing_films:
            error_message = 'Film already exists'
            return render_template("addfilm.html", error=error_message)

        film_db.add_film(request.form['title'], request.form['yearReleased'], request.form['rating'], request.form['duration'], request.form['genre'])
        return render_template("addfilm.html", success=True)

    return render_template("addfilm.html")


@app.route('/DeleteFilm', methods=['GET', 'POST'])
def delete_film():
    film_db = Filmflix_db()

    if request.method == 'POST':
        film_id = request.form.get('filmID')
        if not film_id:
            error_message = 'Mandatory field filmID not present in request to "delete_film"'
            return render_template("deletefilm.html", error=error_message)

        if not film_db.check_film_exists(film_id):
            error_message = 'Invalid film ID'
            return render_template("deletefilm.html", error=error_message)

        film_db.delete_film(film_id)
        return render_template("deletefilm.html", success=True)

    return render_template("deletefilm.html")


@app.route('/AmendFilm', methods=['GET', 'POST'])
def amend_film():
    film_db = Filmflix_db()

    if request.method == 'POST':
        film_id = request.form.get('filmID')
        column_name = request.form.get('column_name')
        new_value = request.form.get('new_value')

        if not film_id or not column_name or not new_value:
            error_message = 'Mandatory fields filmID, column_name, and new_value are required.'
            return render_template('amendfilm.html', error=error_message)

        film_db.amend_film(film_id, column_name, new_value)
        success_message = 'Film updated successfully!'
        return render_template('amendfilm.html', success=True, message=success_message)

    return render_template('amendfilm.html')


@app.route('/reports', methods=['GET', 'POST'])
def display_films_by_x():
    film_db = Filmflix_db()

    if request.method == 'POST':
        column_report = request.form.get('column_report')
        find_values = request.form.get('find_values')

        db_function = getattr(film_db, f'get_films_by_{column_report}')

        columns = ['filmID', 'title', 'yearReleased', 'rating', 'duration', 'genre']
        films = db_function(find_values.strip())
        data = {'columns': columns, 'films': films}

        return render_template('reports.html', data=data)
    return render_template('reports.html', data=None)


# @app.post('/')

# Once Run - in Python Console / Javascript do the equivalent of:

# For all films
# import requests
# r = requests.post('http://127.0.0.1:5000/Films', headers={'Content-type': 'application/json'})
# print(r.json())
#
# res = r.json()  # { columns: [], films: [ [ id, ... ] ] }
#
# title, yearReleased, rating, duration, genre = 'Hello', 2002, '1', 5, 'Testing'
# to_delete = {'title': title, 'yearReleased': yearReleased, 'rating': rating, 'duration': duration, 'genre': genre}
# to_delete_id = None
#
# for film in res['films']:
#     film_id, to_compare = film[0], film[1:]
#     if to_compare == [title, yearReleased, rating, duration, genre]:
#         to_delete_id = film_id
#
# print(to_delete_id)

# To add film
# import requests
# r = requests.post('http://127.0.0.1:5000/AddFilm', json={'title': 'Hello', 'yearReleased': 2002, 'rating': 1, 'duration': 5, 'genre': 'Testing'}, headers={'Content-type': 'application/json'})

# r = requests.post('http://127.0.0.1:5000/DeleteFilm', json={'filmID': to_delete_id}, headers={'Content-type': 'application/json'})
# a = 1

# For reports:

# request: { 'rating': 5, 'genre': 'horror' }
if __name__ == '__main__':
    app.run()
