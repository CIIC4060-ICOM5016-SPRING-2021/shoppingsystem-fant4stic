from dao.user import UserDAO
from dao.cart import CartDao
from flask import jsonify

class UserController:

    def registerNewUser(self, json):
        dao = UserDAO()
        first_name = json['FirstName']
        last_name = json['LastName']
        user_name = json['Username']
        email = json['Email']

        record = dao.existUser(email)
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

