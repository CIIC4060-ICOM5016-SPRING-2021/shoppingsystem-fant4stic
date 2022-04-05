from config.databaseConnect import DatabaseConnect
from dao.book import BookDAO
from flask import jsonify
# Class Controller for Book table
class BookController:
    def __init__(self):
        self.connection = DatabaseConnect().getConnection()

    def filterByGenre(self):
        cursor = self.connection.cursor()
        genre_input = input("Enter your genre: ")
        cursor.execute("Select * from book natural inner join book_genre where genre_id = " + genre_input)
        record = cursor.fetchall()
        return jsonify(record)

    def orderByTitle(self):
        cursor = self.connection.cursor()
        # Write the ordering desired
        order_in = input("Ascending or Descending?: ")

        if order_in == 'Ascending':
            # Order books by title in ascending order
            cursor.execute("Select * from book order by title")
        else:
            # Order books by title in descending order
            cursor.execute("Select * from book order by title desc")

        record = cursor.fetchall()
        return jsonify(record)

    def orderByPrice(self):
        cursor = self.connection.cursor()
        # Write if prices goes from low to high or vice versa
        order_in = input("Low to High or High to Low?: ")

        if order_in == "Low to High":
            # Order books from cheaper to expensive
            cursor.execute("Select * from book natural inner join inventory order by price_unit")
        else:
            # Order books from expensive to cheaper
            cursor.execute("Select * from book natural inner join inventory order by price_unit desc")

        record = cursor.fetchall()
        return jsonify(record)

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


