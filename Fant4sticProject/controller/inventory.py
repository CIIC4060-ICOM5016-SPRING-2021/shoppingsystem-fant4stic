from dao.inventory import InventoryDAO
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

    def addBookProduct(self,json):
        bookId = json['BookId']
        userId = json['UserId']
        price = json['BookPrice']
        num_units = json['BookNumberUnits']
        dao = InventoryDAO()
        exist = dao.existBookInv(bookId)
        if (exist):
            return jsonify("Product is already added to Inventory. No need to add it again."), 409
        is_admin = dao.isUserAdmin(userId)
        if(not is_admin):
            return jsonify("The UserId passed is not an admin. No book was added."), 404
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
            return jsonify("Book is not in Inventory. No book was deleted.") ,409
        # Get the inventoryId of the BookId specified in the input
        invId = dao.getInventory(bookId)
        is_admin = dao.isUserAdmin(userId)
        if(not is_admin):
            return jsonify("The UserId passed is not an admin. No book was deleted."),409
        dao.deleteBookInv(bookId)
        return jsonify("Product was successfully deleted.") , 202
