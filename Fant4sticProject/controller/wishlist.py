from flask import jsonify
from dao.wishlist import WishlistDAO
# Class Controller for Wishlist table
class WishlistController:
    def build_dict_wishlist(self,row):
        result = {}
        result['WishlistId'] = row[0]
        result['CustomerId'] = row[1]
        return result

    def getAllWishlists(self):
        dao = WishlistDAO()
        records = dao.getAllWishlists()
        result = []
        for row in records:
            dict = self.build_dict_wishlist(row)
            result.append(dict)
        return jsonify(result), 200
