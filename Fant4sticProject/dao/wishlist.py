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

    def getAllAddToWishlist(self):
        cursor = self.connection.cursor()
        query = "select wishlist_id, book_id, "
        query += "extract(year from date_added) as year,extract(mon from date_added) as month, extract(day from date_added) as day "
        query += "from add_to_wish;"
        cursor.execute(query)
        resquery = []
        for row in cursor:
            resquery.append(row)
        cursor.close()
        return resquery
