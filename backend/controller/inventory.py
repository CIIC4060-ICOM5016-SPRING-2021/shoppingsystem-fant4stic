from dao.inventory import InventoryDAO
from dao.user import UserDAO
from dao.book import BookDAO
from flask import jsonify
# Class Controller for Inventory table
class InventoryController:

    def build_dict(self,row):
        result = {}
        result['InventoryId'] = row[0]
        result['BookId'] = row[1]
        result['UserId'] = row[2]
        result['BookPrice'] = row[3]
        result['BookNumberUnits'] = row[4]
        return result

    def build_dict_inventory(self,row):
        result = {}
        result['InventoryId'] = row[0]
        result['BookId'] = row[1]
        result['UnitPrice'] = row[2]
        result['AvailableUnits'] = row[3]
        return result

    def build_dict_update_price(self,row):
        result = {}
        result['InventoryId'] = row[0]
        result['BookId'] = row[1]
        result['UnitPrice'] = row[2]
        result['UserId'] = row[3]
        return result

    def build_dict_update_available(self,row):
        result = {}
        result['InventoryId'] = row[0]
        result['BookId'] = row[1]
        result['AvailableUnits'] = row[2]
        result['UserId'] = row[3]
        return result

    def build_dict_book_price_availableUnits(self,row):
        result = {}
        result['UnitPrice'] = row[0]
        result['AvailableUnits'] = row[1]
        return result

    def addBookProduct(self,json):
        bookName = json['Title']
        userId = json['UserId']
        price = json['BookPrice']
        num_units = json['BookNumberUnits']
        dao = InventoryDAO()
        bdao = BookDAO()
        is_admin = UserDAO().isUserAdmin(userId)
        if (not is_admin):
            return jsonify("The UserId passed is not an admin. No book was added to the inventory."), 404
        # Check if the book does not exist, if not add it
        if(not bdao.existBookName(bookName)):
            return jsonify("Not a valid Book Name."), 409
        bookId = bdao.getBookId(bookName)
        existInInv = dao.existBookInv(bookId)
        if (existInInv):
            return jsonify("Product is already added to Inventory. No need to add it again."), 409
        # Get the id of the inventory created
        invId = dao.addBookInv(bookId,price,num_units)
        row = [invId,bookId,userId,price,num_units]
        resultdict = self.build_dict(row)
        return jsonify(resultdict), 201

    def deleteBookProduct(self, json):
        bookId = json['BookId']
        userId = json['UserId']
        dao = InventoryDAO()
        exist = dao.existBookInv(bookId)
        if(not exist):
            return jsonify("Book is not in Inventory. No book was deleted."), 409
        # Get the inventoryId of the BookId specified in the input
        is_admin = UserDAO().isUserAdmin(userId)
        if(not is_admin):
            return jsonify("The UserId passed is not an admin. No book was deleted."), 404
        dao.deleteBookInv(bookId)
        return jsonify("Product was successfully deleted.") , 202

    def getAllInventories(self):
        dao = InventoryDAO()
        records = dao.getAllInventories()
        result = []
        for row in records:
            dict = self.build_dict_inventory(row)
            result.append(dict)
        return jsonify(result), 200

    def updatePriceInventory(self, json):
        bookId = json['BookId']
        priceUnit = json['PriceUnit']
        userId = json['UserId']
        dao = InventoryDAO()
        exist = dao.existBookInv(bookId)
        if not exist:
            return jsonify("Book is not in Inventory. No book was updated."), 409

        is_admin = UserDAO().isUserAdmin(userId)
        if not is_admin:
            return jsonify("The UserId passed is not an admin. No book was updated."), 404

        invId = dao.getInventory(bookId)
        dao.updatePriceInventoryDAO(bookId, priceUnit)
        row = [invId, bookId, priceUnit, userId]
        result = self.build_dict_update_price(row)
        return jsonify(result), 200


    def updateAvailableUnitsInventory(self, json):
        dao = InventoryDAO()
        bookId = json['BookId']
        availableUnits = json['AvailableUnits']
        userId = json['UserId']
        exist = dao.existBookInv(bookId)

        if not exist:
            return jsonify("Book is not in Inventory. No book was updated."), 409

        is_admin = UserDAO().isUserAdmin(userId)
        if not is_admin:
            return jsonify("The UserId passed is not an admin. No book was updated."), 404

        invId = dao.getInventory(bookId)
        dao.updateAvailableUnitsInventory(bookId, availableUnits)
        row = [invId, bookId, availableUnits, userId]
        result = self.build_dict_update_available(row)
        return jsonify(result), 200

    def build_dict_G(self, row, title):
        dictionary = {}
        dictionary ['Book_ID'] = row[0]
        dictionary ['Book_price'] = row[1]
        dictionary ['Book_title'] = title
        return dictionary

    def getCheapestProductG(self):

        #Create a dao instance to run the queries
        dao = InventoryDAO()

        #Get the record with the cheapest products
        result = dao.getCheapestProductGlobally()

        #Create a variable to store the result
        cheapestBook = []

        #Now build the dictionary for display
        for row in result:
            #Get the title of the book
            title = dao.getBookTitle(row[0])

            dictionary = self.build_dict_G(row, title)
            cheapestBook.append(dictionary)

        return jsonify(cheapestBook)

    def getMostExpensiveProductG(self):

        #Create a dao instance to run the queries
        dao = InventoryDAO()

        #Get the record with the most expensive products
        result = dao.getMostExpensiveProductGlobally()

        # Create a variable to store the result
        mostExpensiveBook = []

        # Now build the dictionary for display
        for row in result:
            # Get the title of the book
            title = dao.getBookTitle(row[0])

            dictionary = self.build_dict_G(row, title)
            mostExpensiveBook.append(dictionary)

        return jsonify(mostExpensiveBook)