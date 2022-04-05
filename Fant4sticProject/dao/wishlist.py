from config.databaseConnect import DatabaseConnect
# DAO Class that works for Wishlist Controller
class WishlistDAO:
    def __init__(self):
       self.connection = DatabaseConnect().getConnection()

    def getAllWishlists(self):
        cursor = self.connection.cursor()
        cursor.execute("select wishlist_id, user_id from wishlist;")
        resquery = []
        for row in cursor:
            resquery.append(row)
        cursor.close()
        return resquery
