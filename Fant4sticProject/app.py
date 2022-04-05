from flask import Flask, jsonify, request, json
from flask_cors import CORS
from config.databaseConnect import DatabaseConnect
from controller.inventory import InventoryController
from controller.book import BookController
from controller.author import AuthorController
from controller.order import OrderController
from controller.cart import CartController
from controller.roles import RolesController
from controller.user import UserController
from controller.genre import GenreController
from controller.wishlist import WishlistController

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

@app.route('/fant4stic/book/get_all', methods = ['GET'])
def getAllBooks():
    if request.method == 'GET':
        return BookController().getAllBooks()
    else:
        jsonify("Method not supported"),405

@app.route('/fant4stic/author/get_all', methods = ['GET'])
def getAllAuthors():
    if request.method == 'GET':
        return AuthorController().getAllAuthors()
    else:
        jsonify("Method not supported"), 405

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

@app.route('/fant4stic/inventory/get_all', methods = ['GET'])
def getAllInventories():
    if request.method == 'GET':
        return InventoryController().getAllInventories()
    else:
        jsonify("Method not supported"), 405

@app.route('/fant4stic/wishlist/get_all', methods = ['GET'])
def getAllWishlists():
    if request.method == 'GET':
        return WishlistController().getAllWishlists()
    else:
        jsonify("Method not supported"), 405

@app.route('/fant4stic/genre/get_all', methods = ['GET'])
def getAllGenre():
    if request.method == 'GET':
        return GenreController().getAllGenres()
    else:
        jsonify("Method not supported"), 405

@app.route('/fant4stic/book/desiredgenre/<int:genre_id>', methods = ['GET'])
def getBooksInGenres(genre_id):
    if request.method == 'GET':
        return BookController().getBookByGenre(genre_id)
    else:
        return jsonify("Method not supported"), 405

@app.route('/fant4stic/book/orderInAscOrDes/<string:order_in>', methods = ['GET'])
def getBooksInOrder(order_in):
    if request.method == 'GET':
        return BookController().orderByTitle(order_in)
    else:
        return jsonify("Method not supported"), 405

@app.route('/fant4stic/book/orderInPrice/<string:order_in>', methods = ['GET'])
def getBooksByPrice(order_in):
    if request.method == 'GET':
        return BookController().orderByPrice(order_in)
    else:
        return jsonify("Method not supported"), 405

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

@app.route('/fant4stic/order/rankcustomercategoriesbought/<int:customerId>', methods = ['GET'])
def getCustomerMostBoughtCategories(customerId):
    if request.method == 'GET':
        return OrderController().customerMostBoughtCat(customerId)
    else:
        return jsonify("Method not supported"), 405

@app.route('/fant4stic/order/rankcustomerproductsbought/<int:customerId>', methods = ['GET'])
def getCustomerMostBoughtProduct(customerId):
    if request.method == 'GET':
        return OrderController().customerMostBoughtProd(customerId)
    else:
        return jsonify("Method not supported"), 405

@app.route('/fant4stic/order/cheapestproduct/<int:customerId>', methods = ['GET'])
def getCustomerCheapestProduct(customerId):
    if request.method == 'GET':
        return OrderController().customerCheapestProductBought(customerId)
    else:
        return jsonify("Method not supported"), 405

@app.route('/fant4stic/order/mostexpensiveproduct/<int:customerId>', methods = ['GET'])
def getCustomerMostExpensiceProduct(customerId):
    if request.method == 'GET':
        return OrderController().customerMostExpensiveProductBought(customerId)
    else:
        return jsonify("Method not supported"), 405

@app.route('/fant4stic/cart/', methods = ['POST', 'DELETE'])
def cartController():
    if request.method == 'POST':
        return CartController().addBook(request.json)
    if request.method == 'DELETE':
        return CartController().deleteBook(request.json)

@app.route('/fant4stic/cart/get_all', methods = ['GET'])
def getAllCarts():
    if request.method == 'GET':
        return CartController().getAllCarts()
    else:
        return jsonify("Method not supported"), 405

@app.route('/fant4stic/user/register_new_user', methods=['POST'])
def registerNewUser():
    if request.method == 'POST':
        return UserController().registerNewUser(request.json)
    else:
        return jsonify("Method not supported"), 405

@app.route('/fant4stic/user/clear_cart_content/<int:userId>', methods=['DELETE'])
def clearCartContent(userId):
    if request.method == 'DELETE':
        return CartController().clearCartContent(userId)
    else:
        return jsonify("Method not supported"), 405

@app.route('/fant4stic/user/get_all', methods=['GET'])
def getAllUsers():
    if request.method == 'GET':
        return UserController().getAllUsers()
    else:
        return jsonify("Method not supported"), 405

@app.route('/fant4stic/roles/get_all', methods=['GET'])
def getAllRoless():
    if request.method == 'GET':
        return RolesController().getAllRoles()
    else:
        return jsonify("Method not supported"), 405

if __name__ == '__main__':
    app.run()
