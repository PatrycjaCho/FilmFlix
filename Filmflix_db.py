import sqlite3 as sql

class Filmflix_db:
    def __init__(self):
        self.con = sql.connect('C:\\Users\\lisac\\Desktop\\Python Project\\FilmFlix\\filmflix.db')
        self.cursor = self.con.cursor()

    def add_film(self, title, yearReleased, rating, duration, genre):
        sql = "INSERT INTO tblFilms(title, yearReleased, rating, duration, genre) VALUES (?, ?, ?, ?, ?)"
        values = (title, yearReleased, rating, duration, genre)
        self.cursor.execute(sql, values)
        self.con.commit()

    def delete_film(self, filmID):
        sql = "DELETE FROM tblFilms WHERE filmID = ?"
        values = (filmID,)
        self.cursor.execute(sql, values)
        self.con.commit()
        
    def amend_film(self, filmID, column_name, new_value):
        sql = f"UPDATE tblFilms SET {column_name} = ? WHERE filmID = ?"
        values = (new_value, filmID)
        self.cursor.execute(sql, values)
        self.con.commit()

    def get_all_films(self):
        sql = "SELECT * FROM tblFilms"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def print_all_films(self):
        for film in self.get_all_films():
            print(film)
            
    def print_films_by_genre(self, genre):
        sql = "SELECT * FROM tblFilms WHERE genre = ?"
        self.cursor.execute(sql, (genre,))
        films = self.cursor.fetchall()
        for film in films:
            print(film)

    def print_films_by_year(self, year):
        sql = "SELECT * FROM tblFilms WHERE yearReleased = ?"
        self.cursor.execute(sql, (year,))
        films = self.cursor.fetchall()
        for film in films:
            print(film)

    def print_films_by_rating(self, rating):
        sql = "SELECT * FROM tblFilms WHERE rating = ?"
        self.cursor.execute(sql, (rating,))
        films = self.cursor.fetchall()
        for film in films:
            print(film)

    def print_films_by_rating_hugo(self, rating):
        films = self.get_films_by_x(rating=rating)
        for film in films:
            print(film)

    def get_films_by_x(self, genre=None, year=None, rating=None):
        sql = "SELECT * FROM tblFilms"
        filters = ''

        if genre:
            filters += f' AND genre = {genre}'

        if filters:
            sql += ' WHERE '
            sql += filters

        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def exit_db(self):
        self.cursor.close()
        self.con.close()


def get_menu_number(num):
    i = input(num)   
    while not i.isnumeric() or int(i) <= 0 or int(i) >= 7:
        print('Please pick one of the options.')
        i = input(num)
    return int(i)    
       


def text_input():
    films = Filmflix_db()
    menu = get_menu_number('Please Enter: \n 1 for Add Film \n 2 for Delete Film 3 for Update Film \n 4 for Show All \n 5 for Reports \n 6 to Exit \n> ')

    while menu != 6:
        if menu == 1:
            title = input('Title: ')
            yearReleased = input('Year Released: ')
            rating = input('Rating: ')
            duration = input('Duration: ')
            genre = input('Genre: ')
            films.add_film(title, yearReleased, rating, duration, genre)

        if menu == 2:
            filmID = input('Film ID: ')
            films.delete_film(filmID)

        if menu == 3:
            filmID = input('Film ID: ')
            column_name = input('Which would you like to change?: Title, Year, Rating, Duration, Genre')
            new_value = input('What would you like to change it to?')
            films.amend_film(filmID, column_name, new_value)
            
        if menu == 4:            
            films.print_all_films()
    
        if menu == 5:
            sub_menu = get_menu_number('Please Enter: \n 1 for Add Film \n 2 for Delete Film 3 for Update Film \n 4 for Show All \n 5 for Reports \n 6 to Exit \n> ')
            print('Not yet implemented')
            
        menu = get_menu_number('Please Enter: \n 1 for Add Film \n 2 for Delete Film 3 for Update Film \n 4 for Show All \n 5 for Reports \n 6 to Exit \n> ')

if __name__ == '__main__':
    text_input()