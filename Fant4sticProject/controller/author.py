from dao.author import AuthorDAO
from flask import jsonify
# Class Controller for Author table
class AuthorController:

    def getAllAuthors(self):
        dao = AuthorDAO()
        records = dao.getAllAuthors()
        result = []
        for row in records:
            dict = self.build_dict_author(row)
            result.append(dict)
        return jsonify(result) , 200

    def build_dict_author(self,row):
        result = {}
        result['AuthorId'] = row[0]
        result['AuthorName'] = row[1]
        result['Country'] = row[2]
        return result
