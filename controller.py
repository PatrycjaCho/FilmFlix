from flask import Flask, request, render_template, redirect, url_for
import requests
from Filmflix_db import Filmflix_db

app = Flask(__name__)


@app.get('/')
def index_page():
    return render_template("base.html")


@app.get('/films')
def all_films():
    films = Filmflix_db().get_all_films()
    columns = ['filmID', 'title', 'yearReleased', 'rating', 'duration', 'genre']
    data = {'columns': columns, 'films': films}
    return render_template('films.html', data=data)


from flask import render_template

# ...

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


@app.post('/AmendFilm')
def amend_film():
    film_db = Filmflix_db()

    data = request.json
    columns = 'filmID', 'column_name', 'new_value'

    for key in columns:
        if not data.get(key):
            return f'Mandatory field {key} not present in request to "amend_film"'

    film_db.amend_film(data['filmID'], data['column_name'], data['new_value'])
    return 'Success'


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

