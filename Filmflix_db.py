import sqlite3 as sql

class Filmflix_db:
    def __init__(self):
        self.con = sql.connect('filmflix.db')
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

    def get_films_by_x(self, genre=None, yearReleased=None, rating=None, title=None, duration=None):
        sql = "SELECT * FROM tblFilms WHERE 1=1"
        values = []

        if genre:
            sql += ' AND genre = ?'
            values.append(genre)

        if yearReleased:
            sql += ' AND yearReleased = ?'
            values.append(yearReleased)

        if rating:
            sql += ' AND rating = ?'
            values.append(rating)

        if title:
            sql += ' AND title LIKE ?'
            values.append('%' + title + '%')

        if duration:
            sql += ' AND duration = ?'
            values.append(duration)

        self.cursor.execute(sql, values)
        return self.cursor.fetchall()


    def get_films_by_genre(self, genre):
        return self.get_films_by_x(genre=genre)


    def print_films_by_genre(self, genre):
        films = self.get_films_by_x(genre=genre)
        for film in films:
            print(film)

    def get_films_by_yearReleased(self, yearReleased):
        return self.get_films_by_x(yearReleased=yearReleased)

    def print_films_by_year(self, yearReleased):
        films = self.get_films_by_x(yearReleased=yearReleased)
        for film in films:
            print(film)

    def get_films_by_rating(self, rating):
        return self.get_films_by_x(rating=rating)

    def print_films_by_rating(self, rating):
        films = self.get_films_by_x(rating=rating)
        for film in films:
            print(film)

    def get_films_by_title(self, title):
        return self.get_films_by_x(title=title)

    def print_films_by_title(self, title):
        for film in self.get_films_by_title(title):
            print(film)

    def check_film_exists(self, filmID):
        sql = "SELECT COUNT(*) FROM tblFilms WHERE filmID = ?"
        self.cursor.execute(sql, (filmID,))
        count = self.cursor.fetchone()[0]
        return count > 0

    def exit_db(self):
        self.cursor.close()
        self.con.close()


def get_menu_number(num):
    i = input(num)   
    while not i.isnumeric() or int(i) <= 0 or int(i) >= 7:
        print('Please choose a valid number')
        i = input(num)
    return int(i)    
       
def get_sub_menu_number(num):
    i = input(num)   
    while not i.isnumeric() or int(i) <= 0 or int(i) >= 5:
        print('Please choose a valid number')
        i = input(num)
    return int(i)   


def text_input():
    films = Filmflix_db()
    menu = get_menu_number('Please Enter: \n 1 for Add Film \n 2 for Delete Film 3 for Update Film \n 4 for Show All \n 5 for Reports \n 6 to Exit \n> ')

    while menu != 6 :
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
            sub_menu = get_sub_menu_number('Please Enter: \n 1 for Show by Rating \n 2 for Show by Year \n 3 for Show by Genre \n 4 Show by Title \n > ')
            if sub_menu == 1:
                 rating = input('R or PG?: ')
                 films.print_films_by_rating(rating)
            if sub_menu == 2:
                yearReleased = input('Which Year?: ')
                films.print_films_by_year(yearReleased)
            if sub_menu == 3:
                genre = input('Genre?: ')
                films.print_films_by_genre(genre)
            if sub_menu == 4:
                title = input('Title?: ')
                films.print_films_by_title(title)
            
            menu = get_menu_number('Please Enter: \n 1 for Add Film \n 2 for Delete Film 3 for Update Film \n 4 for Show All \n 5 for Reports \n 6 to Exit \n> ')        
            
    if menu == 6:
        films.exit_db()
        

# if __name__ == '__main__':
#     db = Filmflix_db()
#     print(db.get_all_films())
#
#     text_input()

