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

    # Exist Admin
    def existAdmin(self,adminId):
        cursor = self.connection.cursor()
        cursor.execute("select exists (Select admin_id from admin where admin_id =" + str(adminId) + ");")
        resquery = cursor.fetchone()[0]
        cursor.close()
        return resquery

    # Exist Admin in Manages
    def existAdminManages(self, adminId,inventoryId):
        cursor = self.connection.cursor()
        cursor.execute("select exists (select admin_id from manages where inventory_id =" + str(inventoryId) + " and admin_id =" + str(adminId) +");")
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

    def addManages(self,adminId,inventoryId):
        cursor = self.connection.cursor()
        cursor.execute("insert into manages(admin_id, inventory_id) values (%s,%s)", (adminId, inventoryId))
        self.connection.commit()
        cursor.close()

    def getInventory(self,bookId):
        cursor = self.connection.cursor()
        cursor.execute("Select inventory_id from inventory where book_id =" + str(bookId) + ";")
        resquery = cursor.fetchone()[0]
        cursor.close()
        return resquery

    def deleteInvManages(self,inventoryId):
        cursor = self.connection.cursor()
        cursor.execute("delete from manages where inventory_id = " + str(inventoryId) + ";")
        self.connection.commit()
        cursor.close()

    def deleteBookInv(self,bookId):
        cursor = self.connection.cursor()
        cursor.execute("delete from inventory where book_id =" + str(bookId) + ";")
        self.connection.commit()
        cursor.close()
