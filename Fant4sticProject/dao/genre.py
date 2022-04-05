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
