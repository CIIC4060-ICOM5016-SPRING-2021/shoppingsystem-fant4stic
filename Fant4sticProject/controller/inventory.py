from src.databaseConnect import DatabaseConnect
from flask import jsonify
# Class Controller for Inventory table
class InventoryController:
    def __init__(self):
        self.connection = DatabaseConnect().getConnection()

    def addBookProduct(self):
        bookId = input("BookId to add in Inventory: ")
        cursor = self.connection.cursor()
        cursor.execute("select exists (Select inventory_id from inventory where book_id =" + str(bookId) + ");")
        record = cursor.fetchone()
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
                cursor.execute("select exists (Select admin_id from admin where admin_id =" + str(adminId) + ");")
                ad_record = cursor.fetchone()
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
            cursor.execute(
                "insert into inventory(book_id, price_unit, available_units) values (%s,%s,%s) returning inventory_id",
                (bookId, price, num_units))
            # Get the id of the inventory created
            invId = cursor.fetchone()[0]
            self.connection.commit()
            cursor.execute("insert into manages(admin_id, inventory_id) values (%s,%s)", (adminId, invId))
            self.connection.commit()
            cursor.close()
            self.connection.close()
            print("Product was successfully added.")
            return jsonify(("Product was successfully added."))
        print("Product was already added to the Inventory. No need to add it again.")
        return jsonify(("Product was already added to the Inventory. No need to add it again."))

    def deleteBookProduct(self):
        bookId = input("BookId to delete in Inventory: ")
        cursor = self.connection.cursor()
        cursor.execute("select exists (Select inventory_id from inventory where book_id =" + str(bookId) + ");")
        record = cursor.fetchone()
        exist = record[0]
        if(not exist):
            print("Book is not in Inventory. Failed to delete.")
            return jsonify(("Book is not in Inventory. Failed to delete."))
        # Get the inventoryId of the BookId specified in the input
        cursor.execute("Select inventory_id from inventory where book_id =" + str(bookId) + ";")
        invId = cursor.fetchone()[0]
        print("Valid BookId. The inventory_id that holds this product is: " +str(invId))
        repeat = True
        tries = 0
        # Loop until admin input is valid
        while (repeat):
            tries += 1
            adminId = input("Provide an existing admin_id that manages inventory_id = " + str(invId) + ": ")
            cursor.execute("select exists (select admin_id from manages where inventory_id =" + str(invId) + " and admin_id =" + str(adminId) +");")
            ad_exist= cursor.fetchone()[0]
            if (ad_exist):
                repeat = False
            if (tries == 3):
                break
        if (repeat == True):
            print("No valid admin_id was provided. No book was deleted.")
            return jsonify(("No valid admin_id was provided. No book was deleted."))
        print("admin_id valid.\nWill proceed to delete BookId from inventory_id.")
        cursor.execute("delete from manages where inventory_id = " + str(invId) +";")
        self.connection.commit()
        cursor.execute("delete from inventory where book_id =" + str(bookId)+";")
        self.connection.commit()
        print("Product was successfully deleted.")
        return jsonify(("Product was successfully deleted."))
