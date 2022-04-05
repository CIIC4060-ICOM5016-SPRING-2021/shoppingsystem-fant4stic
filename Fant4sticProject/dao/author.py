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