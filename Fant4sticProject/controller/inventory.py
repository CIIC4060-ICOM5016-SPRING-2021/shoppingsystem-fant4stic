from config.databaseConnect import DatabaseConnect
from dao.inventory import InventoryDAO
from flask import jsonify
# Class Controller for Inventory table
class InventoryController:
    def __init__(self):
        self.connection = DatabaseConnect().getConnection()

    def addBookProduct(self):
        bookId = input("BookId to add in Inventory: ")
        dao = InventoryDAO()
        record = dao.existBook(bookId)
        exist = record[0]
        # Add it if the book does not exist
        if (not exist):
            print("Book is not in Inventory. Proceed.")
            repeat = True
            tries = 0
            # Loop until admin input is valid
            while (repeat):
                tries += 1
                adminId = input("Provide an existing AdminId:")
                ad_record = dao.existAdminInv(adminId)
                ad_exist = ad_record[0]
                if (ad_exist):
                    repeat = False
                if (tries == 3):
                    break
            if (repeat == True):
                print("No valid adminId was provided. No book was added.")
                return jsonify(("No valid adminId was provided. No book was added."))
            print("Valid AdminId. Proceed")
            price = input("Price of book:")
            num_units = input("Number of copies:")
            # Get the id of the inventory created
            invId = dao.addBook(bookId,price,num_units)
            dao.addManages(adminId,invId)
            self.connection.close()
            print("Product was successfully added.")
            return jsonify(("Product was successfully added."))
        print("Product was already added to the Inventory. No need to add it again.")
        return jsonify(("Product was already added to the Inventory. No need to add it again."))

    def deleteBookProduct(self):
        bookId = input("BookId to delete in Inventory: ")
        dao = InventoryDAO()
        record = dao.existBook(bookId)
        exist = record[0]
        if(not exist):
            print("Book is not in Inventory. Failed to delete.")
            return jsonify(("Book is not in Inventory. Failed to delete."))
        # Get the inventoryId of the BookId specified in the input
        invId = dao.getInventory(bookId)
        print("Valid BookId. The inventory_id that holds this product is: " +str(invId))
        repeat = True
        tries = 0
        # Loop until admin input is valid
        while (repeat):
            tries += 1
            adminId = input("Provide an existing admin_id that manages inventory_id = " + str(invId) + ": ")
            ad_exist= dao.existAdminManages(adminId,invId)
            if (ad_exist):
                repeat = False
            if (tries == 3):
                break
        if (repeat == True):
            print("No valid admin_id was provided. No book was deleted.")
            return jsonify(("No valid admin_id was provided. No book was deleted."))
        print("admin_id valid.\nWill proceed to delete BookId from inventory_id.")
        dao.deleteInvManages(invId)
        dao.deleteBookInv(bookId)
        self.connection.close()
        print("Product was successfully deleted.")
        return jsonify(("Product was successfully deleted."))
