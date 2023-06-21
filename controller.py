from flask import Flask, request, render_template

from Filmflix_db import Filmflix_db

app = Flask(__name__, template_folder='templates')


@app.get('/')
def index_page():
    return render_template("base.html")


@app.route('/films')
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


if __name__ == '__main__':
    app.run()
