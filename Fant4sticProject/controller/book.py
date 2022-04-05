from config.databaseConnect import DatabaseConnect
from dao.book import BookDAO
from flask import jsonify
# Class Controller for Book table
class BookController:
    def __init__(self):
        self.connection = DatabaseConnect().getConnection()

    def getBookByGenre(self, genre_id):
        dao = BookDAO()
        records = dao.getBookByGenre(genre_id)
        result = []
        result.append({"Genre": dao.getGenreName(genre_id)})
        if not records:
            return jsonify("Genre not found"), 404
        else:
            for i in range(len(records)):
                dict = self.build_dict_book(records[i])
                result.append(dict)
            return jsonify(result), 200

    def orderByTitle(self, order_in):
        cursor = self.connection.cursor()
        dao = BookDAO()
        result = []
        result.append(order_in)
        if order_in == 'Ascending' or order_in == 'ascending':
            records = dao.getBooksAscendingOrder()
            for i in range(len(records)):
                dict = self.build_dict_book(records[i])
                result.append(dict)
            return jsonify(result), 200
        elif order_in == 'Descending' or order_in == 'descending':
            records = dao.getBooksDescendingOrder()
            for i in range(len(records)):
                dict = self.build_dict_book(records[i])
                result.append(dict)
            return jsonify(result), 200
        else:
            return jsonify("Needs to be ascending or descending")

    def orderByPrice(self, order_in):
        cursor = self.connection.cursor()
        dao = BookDAO()
        result = []
        result.append(order_in)
        if order_in == "lowtohigh" or order_in == 'low to high':
            records = dao.getBooksFromLowToHigh()
            for i in range(len(records)):
                dict = self.build_dict_bookAndinventory(records[i])
                result.append(dict)
            return jsonify(result), 200
        elif order_in == 'hightolow' or order_in == 'high to low':
            records = dao.getBooksFromHighToLow()
            for i in range(len(records)):
                dict = self.build_dict_bookAndinventory(records[i])
                result.append(dict)
            return jsonify(result), 200
        else:
            return jsonify("Needs to be Low to High or High to Low")


    def getAllBooks(self):
        dao = BookDAO()
        records = dao.getAllBooks()
        result =[]
        for row in records:
            dict = self.build_dict_book(row)
            result.append(dict)
        return jsonify(result) , 200

    def build_dict_book(self,row):
        result = {}
        result['BookId'] = row[0]
        result['BookTitle'] = row[1]
        result['Language'] = row[2]
        result['NumberPages'] = row[3]
        result['YearPublished'] = row[4]
        return result

    def build_dict_bookAndinventory(self, row):
        result = {}
        result['BookId'] = row[0]
        result['BookTitle'] = row[1]
        result['Language'] = row[2]
        result['NumberPages'] = row[3]
        result['YearPublished'] = row[4]
        result['Price'] = row[5]
        return result

