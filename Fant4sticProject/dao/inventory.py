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

    def isUserAdmin(self,userId):
        cursor = self.connection.cursor()
        cursor.execute("select role_id from roles where user_role = 'Admin';")
        adminRoleId = cursor.fetchone()[0]
        query = "select exists(select user_id from \"User\" where \"User\".role_id =" + str(adminRoleId) + " and user_id =" + str(userId) +");"
        cursor.execute(query)
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
