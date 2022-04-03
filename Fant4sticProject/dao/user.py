from config.databaseConnect import DatabaseConnect

class UserDAO():
    def __init__(self):
        self.connection = DatabaseConnect().getConnection()

    def existUser(self, email):
        cursor = self.connection.cursor()
        cursor.execute("select exists (Select email from \"User\" where email = %s);", (email,));
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

