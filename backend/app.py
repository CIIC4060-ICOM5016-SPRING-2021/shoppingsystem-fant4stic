from flask import Flask, jsonify, request, json
from flask_cors import CORS
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

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

# Get All Operation for Tables:
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

@app.route('/fant4stic/writes/get_all', methods = ['GET'])
def getAllWrites():
    if request.method == 'GET':
        return AuthorController().getAllWrites()
    else:
        jsonify("Method not supported"), 405

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

@app.route('/fant4stic/addtowishlist/get_all', methods = ['GET'])
def getAllAddToWishlist():
    if request.method == 'GET':
        return WishlistController().getAllAddToWishlist()
    else:
        jsonify("Method not supported"), 405

@app.route('/fant4stic/genre/get_all', methods = ['GET'])
def getAllGenre():
    if request.method == 'GET':
        return GenreController().getAllGenres()
    else:
        jsonify("Method not supported"), 405

@app.route('/fant4stic/author_genre/get_all', methods = ['GET'])
def getAllAuthorGenre():
    if request.method == 'GET':
        return GenreController().getAllAuthorGenre()
    else:
        jsonify("Method not supported"), 405

@app.route('/fant4stic/book_genre/get_all', methods = ['GET'])
def getAllBookGenre():
    if request.method == 'GET':
        return GenreController().getAllBookGenre()
    else:
        jsonify("Method not supported"), 405

@app.route('/fant4stic/book_order/get_all', methods = ['GET'])
def getAllBookOrder():
    if request.method == 'GET':
        return OrderController().getAllBookOrder()
    else:
        jsonify("Method not supported"), 405

@app.route('/fant4stic/order/get_all', methods = ['GET'])
def getAllOrder():
    if request.method == 'GET':
        return OrderController().getAllOrder()
    else:
        jsonify("Method not supported"), 405

@app.route('/fant4stic/cart/get_all', methods = ['GET'])
def getAllCarts():
    if request.method == 'GET':
        return CartController().getAllCarts()
    else:
        return jsonify("Method not supported"), 405

@app.route('/fant4stic/addtocart/get_all', methods = ['GET'])
def getAllAddToCart():
    if request.method == 'GET':
        return CartController().getAllAddToCart()
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

# Operations for Inventory:
@app.route('/fant4stic/inventory/addproduct', methods = ['POST'])
def inventoryAddBookProduct():
    if request.method == 'POST':
        requestjson = request.json
        BookController().addNewBook(requestjson)
        return InventoryController().addBookProduct(requestjson)
    else:
        return jsonify("Method not supported"),405

@app.route('/fant4stic/inventory/deleteproduct', methods = ['DELETE'])
def inventoryDeleteBookProduct():
    if request.method == 'DELETE':
        return InventoryController().deleteBookProduct(request.json)
    else:
        return jsonify("Method not supported"),405

@app.route('/fant4stic/inventory/updatepriceproduct', methods = ['PUT'])
def inventoryUpdatePriceBookProduct():
    if request.method == 'PUT':
        return InventoryController().updatePriceInventory(request.json)
    else:
        return jsonify("Method not supported"), 405

@app.route('/fant4stic/inventory/updateavailableunitsproduct', methods = ['PUT'])
def inventoryUpdateAvailableUnitBookProduct():
    if request.method == 'PUT':
        return InventoryController().updateAvailableUnitsInventory(request.json)
    else:
        return jsonify("Method not supported"), 405

@app.route('/fant4stic/inventory/get_cheapest_product', methods = ['GET'])
def getCProduct():
    if request.method == 'GET':
        return InventoryController().getCheapestProductG()
    else:
        return jsonify("Method not supported"), 405

@app.route('/fant4stic/inventory/get_most_expensive_product', methods = ['GET'])
def getEProduct():
    if request.method == 'GET':
        return InventoryController().getMostExpensiveProductG()
    else:
        return jsonify("Method not supported"), 405

# Operations for Book:
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

@app.route('/fant4stic/book/crud_operations/<int:bookId>', methods=['GET', 'PUT'])
def bookCRUD(bookId):
    if request.method == 'GET':
        return BookController().getBook(bookId)
    elif request.method == 'PUT':
        return BookController().updateBook(bookId, request.json)
    else:
        return jsonify("Method not supported"), 405

# Operations for Order:
@app.route('/fant4stic/order/historyofallorders', methods = ['GET'])
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

@app.route('/fant4stic/order/most_bought_category', methods = ['GET'])
def getMostBoughtCategoryG():
    if request.method == 'GET':
        return OrderController().getMCategoryGlobally()
    else:
        return jsonify("Method not supported"), 405

@app.route('/fant4stic/order/most_bought_product', methods = ['GET'])
def getMostBoughtProductG():
    if request.method == 'GET':
        return OrderController().getMProductGlobally()
    else:
        return jsonify("Method not supported"), 405

@app.route('/fant4stic/order/crud_operations/<int:orderId>', methods=['GET', 'DELETE'])
def orderCRUD(orderId):
    if request.method == 'GET':
        return OrderController().getOrder(orderId)
    elif request.method == 'DELETE':
        return OrderController().deleteOrder(orderId)
    else:
        return jsonify("Method not supported"), 405

# Operations for Cart:
@app.route('/fant4stic/cart', methods = ['POST', 'DELETE'])
def cartController():
    if request.method == 'POST':
        return CartController().addBook(request.json)

    if request.method == 'DELETE':
        return CartController().deleteBook(request.json)

    return jsonify("Method not supported"), 405

# Operations for User:
@app.route('/fant4stic/user/register_new_user', methods=['POST'])
def registerNewUser():
    if request.method == 'POST':
        return UserController().registerNewUser(request.json)
    else:
        return jsonify("Method not supported"), 405

@app.route('/fant4stic/user/getUserCart/<int:userId>', methods=['GET'])
def getProductsInCart(userId):
    if request.method == 'GET':
        return CartController().getProdsInCart(userId)
    else:
        return jsonify("Method not supported"), 405

@app.route('/fant4stic/user/getWishlist/<int:userId>', methods=['GET'])
def getProductsInWishlist(userId):
    if request.method == 'GET':
        return WishlistController().getProdsInWishlist(userId)
    else:
        return jsonify("Method not supported"), 405

@app.route('/fant4stic/user/clear_cart_content/<int:userId>', methods=['DELETE'])
def clearCartContent(userId):
    if request.method == 'DELETE':
        return CartController().clearCartContent(userId)
    else:
        return jsonify("Method not supported"), 405

@app.route('/fant4stic/user/buy_all/<int:userId>', methods=['POST'])
def buyAllInCart(userId):
    if request.method == 'POST':
        return CartController().buyAllBooks(userId)
    else:
        return jsonify("Method not supported"), 405

@app.route('/fant4stic/user/crud_operations/<int:userId>', methods=['GET', 'PUT', 'DELETE'])
def userCrud(userId):
    if request.method == 'GET':
        return UserController().getUser(userId)
    elif request.method == 'PUT':
        return UserController().updateUser(userId, request.json)
    elif request.method == 'DELETE':
        return UserController().deleteUser(userId)
    else:
        return jsonify("Method not supported"), 405

# Operations for Wishlist:
@app.route('/fant4stic/wishlist', methods = ['POST', 'DELETE'])
def wishlistController():
    if request.method == 'POST':
        return WishlistController().addBook(request.json)

    if request.method == 'DELETE':
        return WishlistController().deleteBook(request.json)

    return jsonify("Method not supported"), 405

@app.route('/fant4stic/wishlist/get_most_liked_product', methods = ['GET'])
def getLProduct():
    if request.method == 'GET':
        return WishlistController().getMostLikedProductG()
    else:
        return jsonify("Method not supported"), 405

@app.route('/fant4stic/wishlist/create', methods = ['POST'])
def createWishlist():
    if request.method == 'POST':
        return WishlistController().createWish(request.json)
    else:
        return jsonify("Method not supported"), 405

@app.route('/fant4stic/wishlist/delete', methods = ['DELETE'])
def deleteWishlist():
    if request.method == 'DELETE':
        return WishlistController().deleteWish(request.json)

if __name__ == '__main__':
    app.run()
