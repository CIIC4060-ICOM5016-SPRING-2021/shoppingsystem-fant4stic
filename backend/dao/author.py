from config.databaseConnect import DatabaseConnect
# DAO Class that works for Author Controller
class AuthorDAO:
    def __init__(self):
        self.connection = DatabaseConnect().getConnection()

    def getAllAuthors(self):
        cursor = self.connection.cursor()
        cursor.execute("select author_id, concat(first_name, ' ' ,last_name) as AuthorName,country from author order by author_id;")
        resquery = []
        for row in cursor:
            resquery.append(row)
        cursor.close()
        return resquery

    def getAllWrites(self):
        cursor = self.connection.cursor()
        cursor.execute("select author_id, book_id from writes;")
        resquery = []
        for row in cursor:
            resquery.append(row)
        cursor.close()
        return resquery

    def existAuthor(self, first_name, last_name):
        cursor = self.connection.cursor()
        cursor.execute("select exists (Select first_name, last_name from author where first_name = %s and last_name = %s);", (first_name, last_name,))
        resquery = cursor.fetchone()
        cursor.close()
        return resquery

    def getAuthorId(self, first_name, last_name):
        cursor = self.connection.cursor()
        cursor.execute("select author_id from author where first_name = %s and last_name = %s;", (first_name, last_name))
        resquery = cursor.fetchone()
        cursor.close()
        return resquery

    def addNewAuthor(self, first_name, last_name, country):
        cursor = self.connection.cursor()
        cursor.execute(
            "insert into author(first_name, last_name, country) values (%s,%s,%s)",
            (first_name, last_name, country))
        self.connection.commit()
        cursor.close()
        return

    def addAuthorGenre(self, authorId, genreId):
        cursor = self.connection.cursor()
        cursor.execute("insert into author_genre(author_id, genre_id) values(%s, %s)", (authorId, genreId,))
        self.connection.commit()
        cursor.close()
        return

    def addAuthorWrites(self, authorId, bookId):
        cursor = self.connection.cursor()
        cursor.execute("insert into writes(author_id, book_id) values(%s, %s)", (authorId, bookId,))
        self.connection.commit()
        cursor.close()
        return

    def doesAuthorWriteGenre(self, authorId, genreId):
        cursor = self.connection.cursor()
        cursor.execute("select exists (Select author_id from author_genre where author_id = %s and genre_id = %s);", (authorId, genreId))
        resquery = cursor.fetchone()
        cursor.close()
        return resquery