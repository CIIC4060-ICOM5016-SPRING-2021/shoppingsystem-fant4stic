from config.databaseConnect import DatabaseConnect
from datetime import date
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

    def checkifTitleExists(self, bookTitle):
        cursor = self.connection.cursor()

        query = "select exists(select book_id from book where title = %s);"

        cursor.execute(query, (bookTitle,))

        result = cursor.fetchone()[0]

        cursor.close()
        return result

    def getBookID(self, bookTitle):
        cursor = self.connection.cursor()

        query = "select book_id from book where title = %s;"

        cursor.execute(query, (bookTitle,))

        bookID = cursor.fetchone()[0]

        cursor.close()
        return bookID

    def checkIfUserExists(self, userAddingTheBook):
        cursor = self.connection.cursor()

        query = "select exists(select user_id from" + """  "User"  """ + "where user_id = %s);"

        cursor.execute(query, (userAddingTheBook,))
        result = cursor.fetchone()[0]

        cursor.close()
        return result

    def getUserRole(self, userAddingTheBook):
        cursor = self.connection.cursor()

        query = "Select user_role from" + """ "User" """ + "natural inner join roles where user_id = %s;"

        cursor.execute(query, (userAddingTheBook,))
        result = cursor.fetchone()[0]

        cursor.close()
        return result

    def checkIfWishlistExists(self, userAddingTheBook, wishlistID):
        cursor = self.connection.cursor()

        query = "select exists(select wishlist_id from wishlist where user_id = %s and wishlist_id = %s);"

        cursor.execute(query, (userAddingTheBook, wishlistID,))
        result = cursor.fetchone()[0]

        cursor.close()
        return result

    def checkIfBookExists(self, bookToAdd, wishlistID):
        cursor = self.connection.cursor()

        query = "select exists(select book_id from add_to_wish where book_id = %s and wishlist_id = %s);"

        cursor.execute(query, (bookToAdd, wishlistID,))

        bookExists = cursor.fetchone()[0]

        cursor.close()
        return bookExists

    def addBook(self, bookToAdd, wishlistID, todayDate):
        cursor = self.connection.cursor()

        query = "insert into add_to_wish(wishlist_id, book_id, date_added) values (%s,%s,%s);"

        cursor.execute(query, (wishlistID, bookToAdd, todayDate,))

        self.connection.commit()
        cursor.close()

    def deleteBook(self, wishlistID, bookToDelete):
        cursor = self.connection.cursor()

        query = "delete from add_to_wish where wishlist_id = %s and book_id = %s;"

        cursor.execute(query, (wishlistID, bookToDelete,))

        self.connection.commit()
        cursor.close()

    def getMostLikedProductGlobally(self):
        cursor = self.connection.cursor()

        query = "select book_id, amountLiked from (select book_id, count(*) as amountLiked from add_to_wish group by book_id order by count(*) desc) as tableII where amountLiked = (select max(amountLiked) from (select book_id, count(*) as amountLiked from add_to_wish group by book_id order by count(*) desc) as tableIII)"

        cursor.execute(query)
        result = cursor.fetchall()

        cursor.close()
        return result

    def getBookTitle(self, bookID):
        cursor = self.connection.cursor()

        query = "select title from book where book_id = %s;"

        cursor.execute(query, (bookID,))
        result = cursor.fetchone()[0]

        cursor.close()
        return result

    def getWishlistsID(self, userId):
        cursor = self.connection.cursor()
        cursor.execute("select wishlist_id from wishlist where user_id = %s;", (userId,));
        resquery = cursor.fetchall()
        cursor.close()
        return resquery

    def clearWishContent(self, wish_id):
        cursor = self.connection.cursor()
        query = "delete from add_to_wish where wishlist_id = %s;"
        cursor.execute(query, (wish_id,))
        self.connection.commit()
        cursor.close()

    def deleteUserWishlists(self, userId):
        cursor = self.connection.cursor()
        query = "delete from wishlist where user_id = %s;"
        cursor.execute(query, (userId,))
        self.connection.commit()
        cursor.close()

    def createWishlist(self, userID):
        cursor = self.connection.cursor()

        query = "insert into wishlist(user_id) values(%s) returning wishlist_id"

        cursor.execute(query, (userID,))

        wishlist_id = cursor.fetchone()[0]

        self.connection.commit()
        cursor.close()

        return wishlist_id

    def deleteWishList(self, userID, wishlistID):
        cursor = self.connection.cursor()

        query = "delete from wishlist where user_id = %s and wishlist_id = %s;"

        cursor.execute(query, (userID,wishlistID))

        self.connection.commit()
        cursor.close()

    def deleteWishListProducts(self, wishlistID):
        cursor = self.connection.cursor()

        query = "delete from add_to_wish where wishlist_id = %s;"

        cursor.execute(query, (wishlistID,))

        self.connection.commit()
        cursor.close()

    def getUserWishlist(self,userId):
        cursor = self.connection.cursor()
        query = "select wishlist_id, title,  extract(year from date_added) as year,extract(mon from date_added) as month, "
        query += "extract(day from date_added) as day from book natural inner join add_to_wish natural inner join wishlist where user_id =" + str(userId) + " "
        query += "order by wishlist_id;"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
