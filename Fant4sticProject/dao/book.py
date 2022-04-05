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