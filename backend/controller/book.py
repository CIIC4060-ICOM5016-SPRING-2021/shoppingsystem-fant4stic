from config.databaseConnect import DatabaseConnect
from dao.book import BookDAO
from dao.author import AuthorDAO
from dao.genre import GenreDAO
from dao.inventory import InventoryDAO
from flask import jsonify
from controller.inventory import InventoryController
from dao.user import UserDAO
# Class Controller for Book table
class BookController:
    def __init__(self):
        self.connection = DatabaseConnect().getConnection()

    def getBookByGenre(self, genre_id):
        dao = BookDAO()
        inventoryController = InventoryController()
        if(not dao.existGenre(genre_id)):
            return jsonify("Invalid GenreId."), 404
        records = dao.getBookByGenre(genre_id)
        result = []
        if not records:
            return jsonify("Genre not found"), 404
        else:
            groupRecords = inventoryController.groupBooks(records)
            for row in groupRecords:
                dict = inventoryController.build_dict_showBook(row)
                result.append(dict)
            return jsonify(result), 200

    def orderByTitle(self, order_in):
        cursor = self.connection.cursor()
        dao = BookDAO()
        inventoryController = InventoryController()
        result = []
        if order_in == 'Ascending' or order_in == 'ascending':
            records = dao.getBooksAscendingOrder()
            groupRecords = inventoryController.groupBooks(records)
            for row in groupRecords:
                dict = inventoryController.build_dict_showBook(row)
                result.append(dict)
            return jsonify(result), 200
        elif order_in == 'Descending' or order_in == 'descending':
            records = dao.getBooksDescendingOrder()
            groupRecords = inventoryController.groupBooks(records)
            for row in groupRecords:
                dict = inventoryController.build_dict_showBook(row)
                result.append(dict)
            return jsonify(result), 200
        else:
            return jsonify("Needs to be ascending or descending")

    def orderByPrice(self, order_in):
        cursor = self.connection.cursor()
        dao = BookDAO()
        inventoryController = InventoryController()
        result = []
        if order_in == "lowtohigh" or order_in == 'low to high':
            records = dao.getBooksFromLowToHigh()
            groupRecords = inventoryController.groupBooks(records)
            for row in groupRecords:
                dict = inventoryController.build_dict_showBook(row)
                result.append(dict)
            return jsonify(result), 200
        elif order_in == 'hightolow' or order_in == 'high to low':
            records = dao.getBooksFromHighToLow()
            groupRecords = inventoryController.groupBooks(records)
            for row in groupRecords:
                dict = inventoryController.build_dict_showBook(row)
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

    def addNewBook(self, json):
        book, author, genre = BookDAO(), AuthorDAO(), GenreDAO()
        title = json['Title']
        language = json['Language']
        num_pages = json['NumberOfPages']
        year_publ = json['YearPublished']
        book_genre = json['Genre']
        author_first = json['AuthorFirstName']
        author_last = json['AuthorLastName']
        author_country = json['AuthorCountry']
        userId = json["UserId"]

        is_admin = UserDAO().isUserAdmin(userId)
        if (not is_admin):
            return jsonify("The UserId passed is not an admin. No book was added."), 404

        record = book.existBook(title)
        exist = record[0]
        if exist:
            return jsonify("This book is already registered.")

        record2 = genre.existGenre(book_genre)
        exist2 = record2[0]

        if not exist2:
            genre.addNewGenre(book_genre)

        record3 = author.existAuthor(author_first, author_last)
        exist3 = record3[0]

        if not exist3:
            author.addNewAuthor(author_first, author_last, author_country)

        book_id = book.addNewBook(title, language, num_pages, year_publ)
        genre_id = genre.getGenreId(book_genre)
        author_id = author.getAuthorId(author_first, author_last)
        book.addBookGenre(genre_id, book_id)
        author.addAuthorWrites(author_id, book_id)

        record4 = author.doesAuthorWriteGenre(author_id, genre_id)
        exist4 = record4[0]
        if not exist4:
            author.addAuthorGenre(author_id, genre_id)

        json['Book_id'] = book_id
        return jsonify(json), 201

    def getBook(self, bookId):
        bookDao = BookDAO()
        book = bookDao.getBook(bookId)
        if not book:
            return jsonify("Book Not Found"), 404

        invDao = InventoryDAO()
        book_inv = invDao.getBookPriceAndUnits(bookId)
        if not book_inv:
            book = self.build_dict_book(book)
            return jsonify(book), 200
        else:
            book = self.build_dict_book(book)
            book_inv = InventoryController().build_dict_book_price_availableUnits(book_inv)
            d4 = book.copy()
            d4.update(book_inv)
            return jsonify(d4), 200


    def updateBook(self, bookId, json):
        dao = BookDAO()
        book = dao.getBook(bookId)
        if not book:
            return jsonify("Book Not Found"), 404

        title = json['Title']
        language = json['Language']
        num_pages = json['NumberPages']
        year_publ = json['YearPublished']

        if title and language and num_pages and year_publ:
            dao.updateBook(bookId, title, language, num_pages, year_publ)
            result = self.build_book_attributes(bookId, title, language, num_pages, year_publ)
            return jsonify(result), 200
        else:
            return jsonify("Unexpected attributes in update request"), 400

    def build_book_attributes(self, bookId, title, language, num_pages, year_publ):
        result = {}
        result['BookID'] = bookId
        result['Title'] = title
        result['Language'] = language
        result['NumberPages'] = num_pages
        result['YearPublished'] = year_publ
        return result
