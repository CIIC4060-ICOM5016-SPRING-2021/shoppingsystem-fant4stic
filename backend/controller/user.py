from dao.user import UserDAO
from dao.cart import CartDao
from dao.wishlist import  WishlistDAO
from dao.order import OrderDAO
from flask import jsonify

class UserController:

    def registerNewUser(self, json):
        dao = UserDAO()
        first_name = json['FirstName']
        last_name = json['LastName']
        user_name = json['Username']
        email = json['Email']

        record = dao.existUserEmail(email)
        exist = record[0]

        if exist:
            return jsonify("This email is already registered.")

        password = json['Password']
        age = json['Age']
        sex = json['Sex']
        phone_num = json['PhoneNumber']
        userType = json['UserType']

        record2 = dao.existUserType(userType)
        exist2 = record2[0]

        if exist2:
            role_id = dao.getRoleID(userType)

            if userType == 'Admin':
                user_id = dao.registerNewUser(role_id, first_name, last_name, user_name, email, password, age, sex,
                                              phone_num)
                json['User_id'] = user_id

            elif userType == 'Customer':
                user_id = dao.registerNewUser(role_id, first_name, last_name, user_name, email, password, age, sex,
                                              phone_num)
                cartDao = CartDao()
                cartDao.createCart(user_id)
                json['User_id'] = user_id

        else:
            return jsonify("Invalid user type."), 400

        return jsonify(json), 201

    def getAllUsers(self):
        dao = UserDAO()
        records = dao.getAllUsers()
        result = []
        for row in records:
            dict = self.build_dict_user(row)
            result.append(dict)
        return jsonify(result),200

    def build_dict_user(self,row):
        result = {}
        result['UserId'] = row[0]
        result['RoleId'] = row[1]
        result['FirstName'] = row[2]
        result['LastName'] = row[3]
        result['UserName'] = row[4]
        result['Email'] = row[5]
        result['Password'] = row[6]
        result['Age'] = row[7]
        result['Sex'] = row[8]
        result['PhoneNumber'] = row[9]
        return result

    def getUser(self, userId):
        dao = UserDAO()
        user = dao.getUser(userId)
        if not user:
            return jsonify("User Not Found"), 404
        else:
            user = self.build_dict_user(user)
            return jsonify(user), 200

    def updateUser(self, userId, json):
        dao = UserDAO()
        user = dao.getUser(userId)
        if not user:
            return jsonify("User Not Found"), 404

        first_name = json['FirstName']
        last_name = json['LastName']
        username = json['Username']
        email = json['Email']
        password = json['Password']
        age = json['Age']
        sex = json['Sex']
        phone_number = json['PhoneNumber']

        if first_name and last_name and username and email and password and age and sex and phone_number:
            dao.updateUser(userId, first_name, last_name, username, email, password, age, sex, phone_number)
            result = self.build_user_attributes(userId, first_name, last_name, username, email, password, age, sex,
                                                phone_number)
            return jsonify(result), 200
        else:
            return jsonify("Unexpected attributes in update request"), 400

    def build_user_attributes(self, user_id, first_name, last_name, username, email, password, age, sex, phone_number):
        result = {}
        result['UserID'] = user_id
        result['FirstName'] = first_name
        result['LastName'] = last_name
        result['Username'] = username
        result['Email'] = email
        result['Password'] = password
        result['Age'] = age
        result['Sex'] = sex
        result['PhoneNumber'] = phone_number
        return result

    def deleteUser(self, userId):
        dao = UserDAO()
        user = dao.getUser(userId)
        if not user:
            return jsonify("User Not Found"), 404

        role = dao.isUserAdmin(userId)
        if role:
            dao.deleteUser(userId)
            return jsonify("User deleted successfully."), 201
        else:
            cart, wishlist, order = CartDao(), WishlistDAO(), OrderDAO()
            cartID = cart.getCartID(userId)
            cart.clearCartContent(cartID)
            cart.deleteCart(cartID)
            wishlistsId = wishlist.getWishlistsID(userId)
            for x in wishlistsId:
                wishlist.clearWishContent(x)
            wishlist.deleteUserWishlists(userId)
            ordersId = order.getOrdersID(userId)
            for x in ordersId:
                order.clearOrderContent(x)
            order.deleteUserOrders(userId)
            dao.deleteUser(userId)
            return jsonify("User deleted successfully."), 201
