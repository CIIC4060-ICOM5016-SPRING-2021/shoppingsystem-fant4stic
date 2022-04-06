from flask import jsonify
from dao.wishlist import WishlistDAO
# Class Controller for Wishlist table
class WishlistController:
    def build_dict_wishlist(self,row):
        result = {}
        result['WishlistId'] = row[0]
        result['CustomerId'] = row[1]
        return result

    def build_dict_addtowishlist(self,row):
        result = {}
        result['WishlistId'] = row[0]
        result['BookId'] = row[1]
        result['DateAdded'] = str(int(row[2])) + "-" + str(int(row[3])) + "-" + str(int(row[4]))
        return result

    def getAllWishlists(self):
        dao = WishlistDAO()
        records = dao.getAllWishlists()
        result = []
        for row in records:
            dict = self.build_dict_wishlist(row)
            result.append(dict)
        return jsonify(result), 200

    def getAllAddToWishlist(self):
        dao = WishlistDAO()
        records = dao.getAllAddToWishlist()
        result = []
        for row in records:
            dict = self.build_dict_addtowishlist(row)
            result.append(dict)
        return jsonify(result), 200
