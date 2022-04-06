from config.databaseConnect import DatabaseConnect

class UserDAO():
    def __init__(self):
        self.connection = DatabaseConnect().getConnection()

    def existUserEmail(self, email):
        cursor = self.connection.cursor()
        cursor.execute("select exists (Select email from \"User\" where email = %s);", (email,));
        resquery = cursor.fetchone()
        cursor.close()
        return resquery

    def existUserType(self, userType):
        cursor = self.connection.cursor()
        cursor.execute("select exists (Select user_role from roles where user_role = %s);", (userType,));
        resquery = cursor.fetchone()
        cursor.close()
        return resquery

    def registerNewUser(self, role_id, first_name, last_name, user_name, email, password, age, sex, phone_num):
        cursor = self.connection.cursor()
        cursor.execute(
            "insert into \"User\"(role_id, first_name, last_name, user_name, email, password, age, sex, phone_num) values (%s,%s,%s,%s,%s,%s,%s,%s,%s) returning user_id",
            (role_id, first_name, last_name, user_name, email, password, age, sex, phone_num))
        self.connection.commit()
        resquery = cursor.fetchone()[0]
        cursor.close()
        return resquery

    def getRoleID(self, userType):
        cursor = self.connection.cursor()
        cursor.execute("select role_id from roles where user_role = %s;", (userType,));
        resquery = cursor.fetchone()[0]
        cursor.close()
        return resquery

    def isUserAdmin(self,userId):
        cursor = self.connection.cursor()
        cursor.execute("select role_id from roles where user_role = 'Admin';")
        adminRoleId = cursor.fetchone()[0]
        query = "select exists(select user_id from \"User\" where \"User\".role_id =" + str(adminRoleId) + " and user_id =" + str(userId) +");"
        cursor.execute(query)
        resquery = cursor.fetchone()[0]
        cursor.close()
        return resquery

    def isUserCustomer(self,userId):
        cursor = self.connection.cursor()
        cursor.execute("select role_id from roles where user_role = 'Customer';")
        customerRoleId = cursor.fetchone()[0]
        query = "select exists(select user_id from \"User\" where \"User\".role_id =" + str(customerRoleId) + " and user_id =" + str(userId) +");"
        cursor.execute(query)
        resquery = cursor.fetchone()[0]
        cursor.close()
        return resquery

    def getAllUsers(self):
        cursor = self.connection.cursor()
        cursor.execute("select user_id, role_id, first_name, last_name,user_name, email,password,age,sex,phone_num from \"User\";")
        resquery = []
        for row in cursor:
            resquery.append(row)
        cursor.close()
        return resquery

    def getUser(self, userId):
        cursor = self.connection.cursor()
        query = "select user_id, role_id, first_name, last_name, user_name, email, password, age, sex, phone_num from \"User\" where user_id = %s;"
        cursor.execute(query, (userId,))
        result = cursor.fetchone()
        return result

