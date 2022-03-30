from flask import Flask, jsonify, request, json
from flask_cors import CORS
from config.databaseConnect import DatabaseConnect
from controller.inventory import InventoryController
from controller.filter import FilterByController
from controller.order import OrderController
from controller.cart import CartController

import psycopg2

# Activate
app = Flask(__name__)

# Apply CORS to this app
CORS(app)

# Connect to server
connection = DatabaseConnect().getConnection()

# Object to operate the DB
cursor = connection.cursor()

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/fant4stic/book/get_all')
def getAllBooks():
    cursor.execute("Select * from book")
    record = cursor.fetchall()
    return jsonify(record)

@app.route('/fant4stic/author/get_all')
def getAllAuthors():
    cursor.execute("Select * from author")
    record = cursor.fetchall()
    return jsonify(record)

@app.route('/fant4stic/inventory/addproduct')
def inventoryAddBookProduct():
    return InventoryController().addBookProduct()

@app.route('/fant4stic/inventory/deleteproduct')
def inventoryDeleteBookProduct():
    return InventoryController().deleteBookProduct()

@app.route('/fant4stic/book/desiredgenre')
def getBooksInGenres():
    return FilterByController().filterByGenre()

@app.route('/fant4stic/book/orderInAscOrDes')
def getBooksInOrder():
    return FilterByController().orderByTitle()

@app.route('/fant4stic/book/orderInPrice')
def getBooksByPrice():
    return FilterByController().orderByPrice()

@app.route('/fant4stic/order/get_all')
def getOrderHistoryAll():
    return OrderController().historyAll()

@app.route('/fant4stic/order/historyoforders')
def getOrderHistoryCustomer():
    return OrderController().historyOfCustomer()

@app.route('/fant4stic/cart/addproduct')
def addBookToCart():
    return CartController().addBook()

@app.route('/fant4stic/cart/deleteproduct')
def deleteBookFromCart():
    return CartController().deleteBook()


# Check if an element is inside a list of records or a single record
def member_of_Record(element, records):
    bool_const = False
    #Check if records is an array of tuples
    if(not(type(records) is tuple)):
        for record in records:
            if(element in record):
                bool_const = True
                break
    else:
        #records is a single tuple
        bool_const = element in records
    return bool_const

if __name__ == '__main__':
    app.run()
