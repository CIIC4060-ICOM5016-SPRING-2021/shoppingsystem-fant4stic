from flask import jsonify
from dao.genre import GenreDAO
# Class Controller for Genre table
class GenreController:
    def build_dict_genre(self,row):
        result = {}
        result['GenreId'] = row[0]
        result['GenreName'] = row[1]
        return result

    def getAllGenres(self):
        dao = GenreDAO()
        records = dao.getAllGenres()
        result = []
        for row in records:
            dict = self.build_dict_genre(row)
            result.append(dict)
        return jsonify(result), 200
