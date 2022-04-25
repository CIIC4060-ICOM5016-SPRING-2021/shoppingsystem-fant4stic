from flask import jsonify
from dao.genre import GenreDAO
# Class Controller for Genre table
class GenreController:
    def build_dict_genre(self,row):
        result = {}
        result['GenreId'] = row[0]
        result['GenreName'] = row[1]
        return result

    def build_dict_author_genre(self,row):
        result = {}
        result['AuthorId'] = row[0]
        result['GenreId'] = row[1]
        return result

    def build_dict_book_genre(self,row):
        result = {}
        result['GenreId'] = row[0]
        result['BookId'] = row[1]
        return result

    def getAllGenres(self):
        dao = GenreDAO()
        records = dao.getAllGenres()
        result = []
        for row in records:
            dict = self.build_dict_genre(row)
            result.append(dict)
        return jsonify(result), 200

    def getAllAuthorGenre(self):
        dao = GenreDAO()
        records = dao.getAllAuthorGenre()
        result = []
        for row in records:
            dict = self.build_dict_author_genre(row)
            result.append(dict)
        return jsonify(result), 200

    def getAllBookGenre(self):
        dao = GenreDAO()
        records = dao.getAllBookGenre()
        result = []
        for row in records:
            dict = self.build_dict_book_genre(row)
            result.append(dict)
        return jsonify(result), 200

