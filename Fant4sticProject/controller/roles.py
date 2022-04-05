from flask import jsonify
from dao.roles import RolesDAO
# Class Controller for Roles table
class RolesController:
    def build_dict_roles(self,row):
        result = {}
        result['RoleId'] = row[0]
        result['RoleOfUser'] = row[1]
        return result

    def getAllRoles(self):
        dao = RolesDAO()
        records = dao.getAllRoles()
        result = []
        for row in records:
            dict = self.build_dict_roles(row)
            result.append(dict)
        return jsonify(result), 200
