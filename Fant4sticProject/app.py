from flask import Flask, jsonify, request, json
from flask_cors import CORS
from config.databaseConnect import DatabaseConnect
from controller.inventory import InventoryController
from controller.filter import FilterByController
from controller.order import OrderController
from controller.cart import CartController
from controller.user import UserController

import psycopg2

# Activate
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

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

@app.route('/fant4stic/inventory/addproduct', methods = ['POST'])
def inventoryAddBookProduct():
    if request.method == 'POST':
        return InventoryController().addBookProduct(request.json)
    else:
        return jsonify("Method not supported"),405

@app.route('/fant4stic/inventory/deleteproduct', methods = ['DELETE'])
def inventoryDeleteBookProduct():
    if request.method == 'DELETE':
        return InventoryController().deleteBookProduct(request.json)
    else:
        return jsonify("Method not supported"),405

@app.route('/fant4stic/book/desiredgenre')
def getBooksInGenres():
    return FilterByController().filterByGenre()

@app.route('/fant4stic/book/orderInAscOrDes')
def getBooksInOrder():
    return FilterByController().orderByTitle()

@app.route('/fant4stic/book/orderInPrice')
def getBooksByPrice():
    return FilterByController().orderByPrice()

@app.route('/fant4stic/order/get_all', methods = ['GET'])
def getOrderHistoryAll():
    if request.method == 'GET':
        return OrderController().historyAll()
    else:
        return jsonify("Method not supported"), 405

@app.route('/fant4stic/order/historyoforders/<int:customerId>', methods = ['GET'])
def getOrderHistoryCustomer(customerId):
    if request.method == 'GET':
        return OrderController().historyOfCustomer(customerId)
    else:
        return jsonify("Method not supported"), 405

@app.route('/fant4stic/cart/', methods = ['POST', 'DELETE'])
def cartController():
    if request.method == 'POST':
        return CartController().addBook(request.json)
    if request.method == 'DELETE':
        return CartController().deleteBook(request.json)

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

@app.route('/fant4stic/user/register_new_user', methods=['POST'])
def registerNewUser():
    return UserController().registerNewUser(request.json)
    # else:
    #     return jsonify("Not supported"), 405


if __name__ == '__main__':
    app.run()
