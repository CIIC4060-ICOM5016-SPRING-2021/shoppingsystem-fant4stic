from config.databaseConnect import DatabaseConnect
# DAO Class that works for Inventory Controller
class InventoryDAO:
    def __init__(self):
        self.connection = DatabaseConnect().getConnection()

    def existBookInv(self,bookId):
        cursor = self.connection.cursor()
        cursor.execute("select exists (Select inventory_id from inventory where book_id =" + str(bookId) + ");")
        resquery = cursor.fetchone()[0]
        cursor.close()
        return resquery

    def existBook(self, bookId):
        cursor = self.connection.cursor()
        cursor.execute("select exists (Select title from book where book_id = %s);", (bookId,))
        resquery = cursor.fetchone()[0]
        cursor.close()
        return resquery

    # Add book and return the inventory's id
    def addBookInv(self,bookId,price,num_units):
        cursor = self.connection.cursor()
        cursor.execute("insert into inventory(book_id, price_unit, available_units) values (%s,%s,%s) returning inventory_id",
            (bookId, price, num_units))
        self.connection.commit()
        resquery = cursor.fetchone()[0]
        cursor.close()
        return resquery

    def getInventory(self,bookId):
        cursor = self.connection.cursor()
        cursor.execute("Select inventory_id from inventory where book_id =" + str(bookId) + ";")
        resquery = cursor.fetchone()[0]
        cursor.close()
        return resquery

    def deleteBookInv(self,bookId):
        cursor = self.connection.cursor()
        cursor.execute("delete from inventory where book_id =" + str(bookId) + ";")
        self.connection.commit()
        cursor.close()

    def getAllInventories(self):
        cursor = self.connection.cursor()
        cursor.execute("select inventory_id, book_id, price_unit, available_units from inventory;")
        resquery = []
        for row in cursor:
            resquery.append(row)
        cursor.close()
        return resquery

    def updatePriceInventoryDAO(self, bookId, priceUnit):
        cursor = self.connection.cursor()
        cursor.execute("update inventory set price_unit = %s where book_id = %s;", (priceUnit, bookId,))
        self.connection.commit()
        cursor.close()

    def updateAvailableUnitsInventory(self, bookId, available_units):
        cursor = self.connection.cursor()
        cursor.execute("update inventory set available_units = %s  where book_id = %s;", (available_units, bookId))
        self.connection.commit()
        cursor.close()

    def getCheapestProductGlobally(self):
        cursor = self.connection.cursor()

        query = "select book_id, price_unit from inventory where price_unit = (select min(price_unit) from inventory)"

        cursor.execute(query)
        result = cursor.fetchall()

        cursor.close()
        return result

    def getMostExpensiveProductGlobally(self):
        cursor = self.connection.cursor()

        query = "select book_id, price_unit from inventory where price_unit = (select max(price_unit) from inventory)"

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
