from flask import Flask, request, render_template, redirect, url_for
import requests
from Filmflix_db import Filmflix_db

app = Flask(__name__)


@app.get('/')
def index_page():
    return '''<!doctype html>
<title>Hello from Flask</title>'''
    render_template("base.html")

@app.get('/Films')
@app.post('/Films')
def post_films():
    films = Filmflix_db().get_all_films()
    columns = 'title', 'yearReleased', 'rating', 'duration', 'genre'
    return {'columns': columns, 'films': films}


@app.post('/AddFilm')
def add_film():
    film_db = Filmflix_db()

    data = request.json
    columns = 'title', 'yearReleased', 'rating', 'duration', 'genre'

    for key in columns:
        if not data.get(key):
            return f'Mandatory field {key} not present in request to "add_film"'

    # TODO: what if record already exists??

    film_db.add_film(data['title'], data['yearReleased'], data['rating'], data['duration'], data['genre'])
    return 'Success'

if __name__ == '__main__':
    app.run()

    # Once Run - in Python Console / Javascript do the equivalent of:

    # For all films
    # import requests
    # r = requests.post('http://127.0.0.1:5000/Films', headers={'Content-type': 'application/json'})
    # r.json()


    # To add film
    # import requests
    # r = requests.post('http://127.0.0.1:5000/AddFilm', json={'title': 'Hello', 'yearReleased': 2002, 'rating': 1, 'duration': 5, 'genre': 'Testing'}, headers={'Content-type': 'application/json'})


    # For reports:

    # request: { 'rating': 5, 'genre': 'horror' }
