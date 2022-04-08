from config.databaseConnect import DatabaseConnect
class CartDao:
    def __init__(self):
       self.connection = DatabaseConnect().getConnection()

    def getAllCarts(self):
        cursor = self.connection.cursor()
        cursor.execute("select cart_id,user_id from cart;")
        resquery = []
        for row in cursor:
            resquery.append(row)
        cursor.close()
        return resquery

    def getAllAddToCart(self):
        cursor = self.connection.cursor()
        cursor.execute("select book_id,cart_id,num_addeditems from add_to_cart;")
        resquery = []
        for row in cursor:
            resquery.append(row)
        cursor.close()
        return resquery

    def checkIfCartExists(self, userAddingTheBook):
        cursor = self.connection.cursor()

        cursor.execute("select exists (select cart_id from" + """ "User" """ + "natural inner join cart where user_id = %s);", (userAddingTheBook,))
        cartExists = cursor.fetchone()[0]

        cursor.close()
        return cartExists
    def returnCustomerCart(self, userAddingTheBook):
        cursor = self.connection.cursor()

        cursor.execute("select cart_id from" + """ "User" """ + "natural inner join cart where user_id = %s;", (userAddingTheBook,))
        cart = cursor.fetchone()[0]

        cursor.close()
        return cart

    def generateCart(self, userAddingTheBook):
        cursor = self.connection.cursor()

        cursor.execute("insert into cart(user_id) values(%s)", (userAddingTheBook,))

        self.connection.commit()
        cursor.close()

    def addBook(self, bookToAdd, existingCart, howMuchBooks):
        cursor = self.connection.cursor()

        cursor.execute("insert into add_to_cart(book_id, cart_id, num_addeditems) values(%s,%s,%s)",
                       (bookToAdd, str(existingCart), howMuchBooks))

        self.connection.commit()
        cursor.close

    def checkIfBookExists(self, bookToAdd, user):
        cursor = self.connection.cursor()

        cursor.execute("select exists(select book_id from cart natural inner join add_to_cart where book_id = %s and user_id = %s);", (bookToAdd, user,))

        bookExists = cursor.fetchone()[0]

        cursor.close()
        return bookExists

    def deleteBook(self, bookToDelete):
        cursor = self.connection.cursor()

        query = "delete from add_to_cart where book_id = "
        cursor.execute(query + str(bookToDelete))

        self.connection.commit()
        cursor.close()

    def getBookID(self, bookTitle):
        cursor = self.connection.cursor()

        query = "select book_id from book where title = %s;"

        cursor.execute(query, (bookTitle,))

        bookID = cursor.fetchone()[0]

        cursor.close()
        return bookID

    def checkIfBookIsAvailable(self, bookToAdd):
        cursor = self.connection.cursor()

        query = "select exists(select book_id from inventory where book_id = %s);"

        cursor.execute(query, (bookToAdd,))

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

    def checkifTitleExists(self, bookTitle):
        cursor = self.connection.cursor()

        query = "select exists(select book_id from book where title = %s);"

        cursor.execute(query, (bookTitle,))

        result = cursor.fetchone()[0]

        cursor.close()
        return result

    def updateInventoryAfterAddition(self, bookToAdd, howMuchBooks, unitsAvailableBefore):
        cursor = self.connection.cursor()

        #Calculate how many units will be left on inventory
        totalUnits = unitsAvailableBefore - howMuchBooks

        query = "update inventory set available_units = %s where book_id = %s;"

        cursor.execute(query, (totalUnits, bookToAdd,))

        self.connection.commit()
        cursor.close()

    def getInventoryUnits(self, bookToAdd):
        cursor = self.connection.cursor()

        query = "select available_units from inventory where book_id = %s;"

        cursor.execute(query, (bookToAdd,))
        result = cursor.fetchone()[0]

        cursor.close()
        return result

    def getCartUnits(self, bookToDelete, customerCart):
        cursor = self.connection.cursor()

        query = "select num_addeditems from add_to_cart where cart_id = %s and book_id = %s;"

        cursor.execute(query, (customerCart, bookToDelete,))
        result = cursor.fetchone()[0]

        cursor.close()
        return result

    def updateInventoryAfterDeletion(self, bookToDelete, copiesStored, inventoryUnits):
        cursor = self.connection.cursor()

        # Calculate how many units would be available after deletion
        totalUnits = inventoryUnits + copiesStored

        query = "update inventory set available_units = %s where book_id = %s;"

        cursor.execute(query, (totalUnits, bookToDelete,))

        self.connection.commit()
        cursor.close()

    def checkIfUserExists(self, userAddingTheBook):
        cursor = self.connection.cursor()

        query = "select exists(select user_id from" + """  "User"  """ + "where user_id = %s);"

        cursor.execute(query, (userAddingTheBook,))
        result = cursor.fetchone()[0]

        cursor.close()
        return result

    def createCart(self,userId):
        cursor = self.connection.cursor()
        cursor.execute("insert into cart(user_id) values(%s)", (userId,))
        self.connection.commit()
        cursor.close()
        return

    def getCartID(self, userId):
        cursor = self.connection.cursor()
        cursor.execute("select cart_id from cart where user_id = %s;", (userId,))
        resquery = cursor.fetchone()
        cursor.close()
        return resquery

    def clearCartContent(self, cartId):
        cursor = self.connection.cursor()
        query = "delete from add_to_cart where cart_id = %s;"
        cursor.execute(query, (cartId,))
        self.connection.commit()
        cursor.close()
        return

    def deleteCart(self, cartId):
        cursor = self.connection.cursor()
        query = "delete from cart where cart_id = %s;"
        cursor.execute(query, (cartId,))
        self.connection.commit()
        cursor.close()
        return
