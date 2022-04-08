from config.databaseConnect import DatabaseConnect
# DAO Class that works for Book Controller
class BookDAO:
    def __init__(self):
        self.connection = DatabaseConnect().getConnection()

    def getAllBooks(self):
        cursor = self.connection.cursor()
        cursor.execute("select book_id,title,language,num_pages,year_publ from book order by book_id;")
        resquery =[]
        for row in cursor:
            resquery.append(row)
        cursor.close()
        return resquery

    def getBookByGenre(self, genre_id):
        cursor = self.connection.cursor()
        cursor.execute("Select book_id, title, language, num_pages, year_publ from book natural inner join book_genre where genre_id = " + str(genre_id) + ";")
        resquery = []
        for row in cursor:
            resquery.append(row)
        cursor.close()
        return resquery

    def getGenreName(self, genre_id):
        cursor = self.connection.cursor()
        cursor.execute("Select genre_name from genre where genre_id = " + str(genre_id) + ";")
        genre_name = cursor.fetchall()
        return genre_name

    def getBooksAscendingOrder(self):
        cursor = self.connection.cursor()
        cursor.execute("Select book_id, title, language, num_pages, year_publ from book order by title")
        resquery = cursor.fetchall()
        cursor.close()
        return resquery

    def getBooksDescendingOrder(self):
        cursor = self.connection.cursor()
        cursor.execute("Select book_id, title, language, num_pages, year_publ from book order by title desc")
        resquery = cursor.fetchall()
        cursor.close()
        return resquery

    def getBooksFromLowToHigh(self):
        cursor = self.connection.cursor()
        cursor.execute("Select book_id, title, language, num_pages, year_publ, price_unit from book natural inner join inventory order by price_unit")
        resquery = cursor.fetchall()
        cursor.close()
        return resquery

    def getBooksFromHighToLow(self):
        cursor = self.connection.cursor()
        cursor.execute("Select book_id, title, language, num_pages, year_publ, price_unit from book natural inner join inventory order by price_unit desc")
        resquery = cursor.fetchall()
        cursor.close()
        return resquery

    def existBook(self, title):
        cursor = self.connection.cursor()
        cursor.execute("select exists (Select title from book where title = %s);", (title,))
        resquery = cursor.fetchone()
        cursor.close()
        return resquery

    def addNewBook(self, title, language, num_pages, year_publ):
        cursor = self.connection.cursor()
        cursor.execute("insert into book(title, language, num_pages, year_publ) values(%s, %s, %s, %s) returning book_id", (title, language, num_pages, year_publ,))
        self.connection.commit()
        resquery = cursor.fetchone()[0]
        cursor.close()
        return resquery

    def addBookGenre(self, genreId, bookId):
        cursor = self.connection.cursor()
        cursor.execute("insert into book_genre(genre_id, book_id) values(%s, %s)", (genreId, bookId,))
        self.connection.commit()
        cursor.close()
        return

    def getBook(self, bookId):
        cursor = self.connection.cursor()
        query = "select book_id, title, language, num_pages, year_publ from book where book_id = %s;"
        cursor.execute(query, (bookId,))
        result = cursor.fetchone()
        return result
