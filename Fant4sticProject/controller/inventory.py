from dao.inventory import InventoryDAO
from flask import jsonify
# Class Controller for Inventory table
class InventoryController:

    def build_dict(self,row):
        result = {}
        result['InventoryId'] = row[0]
        result['BookId'] = row[1]
        result['AdminId'] = row[2]
        result['BookPrice'] = row[3]
        result['BookNumberUnits'] = row[4]
        return result

    def addBookProduct(self,json):
        bookId = json['BookId']
        adminId = json['AdminId']
        price = json['BookPrice']
        num_units = json['BookNumberUnits']
        dao = InventoryDAO()
        exist = dao.existBookInv(bookId)
        if (exist):
            return jsonify("Product is already added to Inventory. No need to add it again."), 409
        ad_exist = dao.existAdmin(adminId)
        if(not ad_exist):
            return jsonify("Not a valid adminId. No book was added."), 404
        # Get the id of the inventory created
        invId = dao.addBookInv(bookId,price,num_units)
        dao.addManages(adminId,invId)
        row = [invId,bookId,adminId,price,num_units]
        resultdict = self.build_dict(row)
        return jsonify(resultdict), 201

    def deleteBookProduct(self, json):
        bookId = json['BookId']
        adminId = json['AdminId']
        dao = InventoryDAO()
        exist = dao.existBookInv(bookId)
        if(not exist):
            return jsonify("Book is not in Inventory. No book was deleted.") ,409
        # Get the inventoryId of the BookId specified in the input
        invId = dao.getInventory(bookId)
        ad_exist = dao.existAdminManages(adminId, invId)
        if(not ad_exist):
            return jsonify("No valid admin_id was provided. No book was deleted."),409
        dao.deleteInvManages(invId)
        dao.deleteBookInv(bookId)
        return jsonify("Product was successfully deleted.") , 202
