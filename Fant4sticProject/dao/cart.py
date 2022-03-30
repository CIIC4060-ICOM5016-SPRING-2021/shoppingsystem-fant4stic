from config.databaseConnect import DatabaseConnect
class CartDao:
    def __init__(self):
       self.connection = DatabaseConnect().getConnection()

    def checkIfCartExists(self, customerToAdd):
        cursor = self.connection.cursor()

        cursor.execute("select exists (select cart_id from customer natural inner join cart where customer_id =" + str(customerToAdd) + ")")
        cartExists = cursor.fetchone()[0]

        cursor.close()
        return cartExists
    def returnCustomerCart(self, customerToAdd):
        cursor = self.connection.cursor()

        cursor.execute("select cart_id from customer natural inner join cart where customer_id =" + str(customerToAdd))
        cart = cursor.fetchone()[0]

        cursor.close()
        return cart

    def generateCart(self, customerToAdd):
        cursor = self.connection.cursor()

        cursor.execute("insert into cart(customer_id) values(%s)", (customerToAdd))

        self.connection.commit()
        cursor.close()

    def addBook(self, bookToAdd, existingCart, howMuchBooks):
        cursor = self.connection.cursor()

        cursor.execute("insert into add_to_cart(book_id, cart_id, num_addeditems) values(%s,%s,%s)",
                       (bookToAdd, str(existingCart), howMuchBooks))

        self.connection.commit()
        cursor.close

    def checkIfBookExists(self, bookToAdd):
        cursor = self.connection.cursor()

        cursor.execute("select exists(select book_id from add_to_cart where book_id = " + str(bookToAdd) + ");")

        bookExists = cursor.fetchone()[0]

        cursor.close()
        return bookExists

    def deleteBook(self, bookToDelete):
        cursor = self.connection.cursor()

        query = "delete from add_to_cart where book_id = "
        cursor.execute(query + str(bookToDelete))

        self.connection.commit()
        cursor.close()

    def getCopies(self, bookToAdd):
        cursor = self.connection.cursor()

        query = "select num_addeditems from add_to_cart where book_id = "
        cursor.execute(query + str(bookToAdd))

        result = cursor.fetchone()[0]

        cursor.close()
        return result

    def addExtraCopies(self, howMuchBooks, currentCopies, bookToAdd):
        cursor = self.connection.cursor()

        #Calculate total copies after addition
        totalItems = int(currentCopies) + int(howMuchBooks)

        query = "update add_to_cart set num_addeditems = "
        queryTwo = "where book_id = "

        cursor.execute(query + str(totalItems) + queryTwo + str(bookToAdd))

        self.connection.commit()
        cursor.close()

    def deleteCopies(self, howMuchBooks, currentCopies, bookToDelete):
        cursor = self.connection.cursor()

        #Calculate total copies after substraction
        totalItems = int(currentCopies) - int(howMuchBooks)

        query = "update add_to_cart set num_addeditems = "
        queryTwo = "where book_id = "

        cursor.execute(query + str(totalItems) + queryTwo + str(bookToDelete))

        self.connection.commit()
        cursor.close()
