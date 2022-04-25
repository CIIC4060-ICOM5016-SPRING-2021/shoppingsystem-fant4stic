from dao.author import AuthorDAO
from flask import jsonify
# Class Controller for Author table
class AuthorController:

    def build_dict_author(self,row):
        result = {}
        result['AuthorId'] = row[0]
        result['AuthorName'] = row[1]
        result['Country'] = row[2]
        return result

    def build_dict_writes(self,row):
        result = {}
        result['AuthorId'] = row[0]
        result['BookId'] = row[1]
        return result

    def getAllAuthors(self):
        dao = AuthorDAO()
        records = dao.getAllAuthors()
        result = []
        for row in records:
            dict = self.build_dict_author(row)
            result.append(dict)
        return jsonify(result) , 200

    def getAllWrites(self):
        dao = AuthorDAO()
        records = dao.getAllWrites()
        result = []
        for row in records:
            dict = self.build_dict_writes(row)
            result.append(dict)
        return jsonify(result), 200
