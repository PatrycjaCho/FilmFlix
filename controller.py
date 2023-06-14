from flask import Flask, request, render_template, redirect, url_for
import requests
from Filmflix_db import Filmflix_db

app = Flask(__name__)


# @app.route('/hello/')
# def index():
#   return 'Whatever'

# @app.run(host=


# @app.get('/')
# def index_page():
#     return render_template("base.html")
#
#
# @app.post('/films')
# def post_films():
#     films = Filmflix_db().get_all_films()
#     columns = 'title', 'yearReleased', 'rating', 'duration', 'genre'
#     data = {'columns': columns, 'films': films}
#     return render_template('Films.html', data=data)

@app.route('/')
def index_page():
    return render_template("base.html")

@app.route('/films', methods=['POST'])
def post_films():
    films = Filmflix_db().get_all_films()
    columns = ['title', 'yearReleased', 'rating', 'duration', 'genre']
    data = {'columns': columns, 'films': films}
    return render_template('films.html', data=data)


@app.post('/AddFilm')
def add_film():
    film_db = Filmflix_db()

    data = request.json
    columns = 'title', 'yearReleased', 'rating', 'duration', 'genre'

    for key in columns:
        if not data.get(key):
            return {'Success': False, 'Error': f'Mandatory field {key} not present in request to "add_film"'}

    existing_films = film_db.get_films_by_x(title=data['title'], yearReleased=data['yearReleased'], rating=data['rating'], duration=data['duration'], genre=data['genre'])
    if existing_films:
        return {'Success': False, 'Error': 'Film already exists'}

    film_db.add_film(data['title'], data['yearReleased'], data['rating'], data['duration'], data['genre'])
    return {'Success': True}


@app.post('/DeleteFilm')
def delete_film():
    film_db = Filmflix_db()

    data = request.json

    if not data.get('filmID'):
        return 'Mandatory field filmID not present in request to "delete_film"'

    film_db.delete_film(data['filmID'])
    return 'Success'


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


if __name__ == '__main__':
    app.run()

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
