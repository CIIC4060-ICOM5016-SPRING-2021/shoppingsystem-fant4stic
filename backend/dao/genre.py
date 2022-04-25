from config.databaseConnect import DatabaseConnect
# DAO Class that works for Genre Controller
class GenreDAO:
    def __init__(self):
       self.connection = DatabaseConnect().getConnection()

    def getAllGenres(self):
        cursor = self.connection.cursor()
        cursor.execute("select genre_id,genre_name from genre;")
        resquery = []
        for row in cursor:
            resquery.append(row)
        cursor.close()
        return resquery

    def getAllAuthorGenre(self):
        cursor = self.connection.cursor()
        cursor.execute("select author_id,genre_id from author_genre;")
        resquery = []
        for row in cursor:
            resquery.append(row)
        cursor.close()
        return resquery

    def getAllBookGenre(self):
        cursor = self.connection.cursor()
        cursor.execute("select genre_id, book_id from book_genre;")
        resquery = []
        for row in cursor:
            resquery.append(row)
        cursor.close()
        return resquery

    def existGenre(self, genre):
        cursor = self.connection.cursor()
        cursor.execute("select exists (Select genre_name from genre where genre_name = %s);", (genre,));
        resquery = cursor.fetchone()
        cursor.close()
        return resquery

    def addNewGenre(self, genre):
        cursor = self.connection.cursor()
        cursor.execute("insert into genre(genre_name) values(%s)", (genre,))
        self.connection.commit()
        cursor.close()
        return

    def getGenreId(self, genre):
        cursor = self.connection.cursor()
        cursor.execute("select genre_id from genre where genre_name = %s;", (genre,));
        resquery = cursor.fetchone()[0]
        cursor.close()
        return resquery
