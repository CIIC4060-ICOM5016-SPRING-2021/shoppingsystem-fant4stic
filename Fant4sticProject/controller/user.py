from config.databaseConnect import DatabaseConnect
from dao.user import UserDAO
from flask import jsonify, request

class UserController:
    def __init__(self):
        self.connection = DatabaseConnect().getConnection()

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
                user_id = dao.registerNewUser(role_id, first_name, last_name, user_name, email, password, age, sex, phone_num)
                json['User_id'] = user_id

            elif userType == 'Customer':
                user_id = dao.registerNewUser(role_id, first_name, last_name, user_name, email, password, age, sex, phone_num)
                json['User_id'] = user_id

        else:
            return jsonify("Invalid user type."), 400

        return jsonify(json), 201
