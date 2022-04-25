from config.databaseConnect import DatabaseConnect
# DAO Class that works for Roles Controller
class RolesDAO:
    def __init__(self):
       self.connection = DatabaseConnect().getConnection()

    def getAllRoles(self):
        cursor = self.connection.cursor()
        cursor.execute("select role_id,user_role from roles;")
        resquery = []
        for row in cursor:
            resquery.append(row)
        cursor.close()
        return resquery
