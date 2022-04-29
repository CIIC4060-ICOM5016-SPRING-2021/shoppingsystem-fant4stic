from flask import jsonify
from dao.cart import CartDao
from dao.user import UserDAO
from dao.inventory import InventoryDAO

class CartController:
    def build_dict(self, row):
        result = {}
        result['Title'] = row[0]
        result['Book_id'] = row[1]
        result['Copies'] = row[2]
        return result

    def build_dict_getProds(self, row):
        result = {}
        result['Title'] = row[0]
        result['Copies'] = row[1]
        result['BookPrice'] = row[2]
        return result


    def build_dict_cart(self,row):
        result = {}
        result['CartId'] = row[0]
        result['Customer_id'] = row[1]
        return result

    def build_dict_addtocart(self,row):
        result = {}
        result['BookId'] = row[0]
        result['CartId'] = row[1]
        result['NumberOfCopies'] = row[2]
        return result

    def build_dict_buyAllInCart(self,row):
        result = {}
        result['UserId'] = row[0]
        result['OrderDate'] = row[1]
        result['OrderTime'] = row[2]
        return result

    def getAllCarts(self):
        dao = CartDao()
        records = dao.getAllCarts()
        result = []
        for row in records:
            dict = self.build_dict_cart(row)
            result.append(dict)
        return jsonify(result), 200

    def getAllAddToCart(self):
        dao = CartDao()
        records = dao.getAllAddToCart()
        result = []
        for row in records:
            dict = self.build_dict_addtocart(row)
            result.append(dict)
        return jsonify(result), 200

    def addBook(self, json):
        bookTitle = json['Title']
        userAddingTheBook = json['Customer_id']
        howMuchBooks = json['Copies']

        dao = CartDao()

        #First verify if a book with the title provided exists
        if(bookTitle):
            existsTitle = dao.checkifTitleExists(bookTitle)
        else:
            return jsonify("A book title was not provided"), 400

        if(not existsTitle):
            return jsonify("The provided title does not match any of our book records"), 404


        #Now get the book id
        bookToAdd = dao.getBookID(bookTitle)

        #Now verify the book is on inventory
        existsOnInventory = dao.checkIfBookIsAvailable(bookToAdd)

        if(not existsOnInventory):
            return jsonify("The book is not currently available :("), 404

        #Now verify the user exists
        if(userAddingTheBook):
            userExists = dao.checkIfUserExists(userAddingTheBook)
        else:
            return jsonify("A user ID was not provided"), 400

        if(userExists):
            #Now verify the user is a customer
            userRole = dao.getUserRole(userAddingTheBook)
        else:
            return jsonify("Your user ID does not belong to a registered user"), 404

        if(userRole != "Customer"):
            return jsonify("User is unavailable to add items to a cart, because he/she is not a customer"), 405

        #Now verify that the amount of copies the customer wants to add does not exceed inventory capacity
        if(howMuchBooks):
            exceeds = dao.getInventoryUnits(bookToAdd)
        else:
            return jsonify("The quantity of copies wanted was not provided"), 400

        if(howMuchBooks > exceeds):
            return jsonify("The amount of units requested exceeds our capacity of " + str(exceeds) + " available units"), 409


        exists = dao.checkIfCartExists(userAddingTheBook) #Only one cart per customer

        if(exists):
            cart = dao.returnCustomerCart(userAddingTheBook)
            print("Cart ID obtained: " + str(cart))
        else:
            #create a new cart
            dao.generateCart(userAddingTheBook)

            #get the new cart
            cartAdded = dao.returnCustomerCart(userAddingTheBook)

            print("Cart: " + str(cartAdded) + " generated")

        #get the customer cart
        existingCart = dao.returnCustomerCart(userAddingTheBook)

        #Verify if the book is already in the cart
        bookExists = dao.checkIfBookExists(bookToAdd,userAddingTheBook)

        if(not bookExists):
            #Now add the book to the cart
            dao.addBook(bookToAdd,existingCart,howMuchBooks)
        else:
            return jsonify("Book was not added, because it already existed in your cart"), 409

        #Verify the book was added
        bookExists = dao.checkIfBookExists(bookToAdd, userAddingTheBook)

        if(bookExists):
            #Build json for output
            row = [bookTitle, bookToAdd, howMuchBooks]
            dictionary = self.build_dict(row)

            return jsonify(dictionary), 200
        else:
            return jsonify("Book could not be added to cart!"), 500

    def deleteBook(self, json):
        bookTitle = json['Title']
        userDeletingTheBook = json['Customer_id']

        dao = CartDao()

        #First verify if a book with the title provided exists
        if(bookTitle):
            existsTitle = dao.checkifTitleExists(bookTitle)
        else:
            return jsonify("A book title was not provided"), 400

        if(not existsTitle):
            return jsonify("The provided title does not match any of our book records"), 404


        #Now get the book id
        bookToDelete = dao.getBookID(bookTitle)

        #Now verify the user exists
        if(userDeletingTheBook):
            userExists = dao.checkIfUserExists(userDeletingTheBook)
        else:
            return jsonify("A user ID was not provided"), 400

        if(userExists):
            #Now verify the user is a customer
            userRole = dao.getUserRole(userDeletingTheBook)
        else:
            return jsonify("Your user ID does not belong to a registered user"), 404

        if(userRole != "Customer"):
            return jsonify("User is unavailable to delete items from a cart, because he/she is not a customer"), 405

        #Check if a cart associated with the customer exists
        cartExist = dao.checkIfCartExists(userDeletingTheBook)

        if(not cartExist):
            return jsonify("You have no existing cart"), 404

        #Verify the book is in the cart
        bookExists = dao.checkIfBookExists(bookToDelete,userDeletingTheBook)

        if (bookExists):
            # Get the customer cart
            customerCart = dao.returnCustomerCart(userDeletingTheBook)

            # Get the copies stored in the cart
            copiesStored = dao.getCartUnits(bookToDelete, customerCart)

            # Delete the book now
            dao.deleteBook(bookToDelete)
        else:
            return jsonify("The desired book could not be deleted, because it was not present in your cart"), 404

        # Verify the book was deleted
        bookExists = dao.checkIfBookExists(bookToDelete, userDeletingTheBook)

        if(not bookExists):
            # Build the Json for output
            row = [bookTitle, bookToDelete, copiesStored]
            dictionary = self.build_dict(row)

            return jsonify(dictionary), 200
        else:
            return jsonify("Book could not be deleted from cart"), 500

    def getProdsInCart(self, userId):
        cartDao, userDao = CartDao(), UserDAO()
        listOfBooks = []
        if not userDao.isUserCustomer(userId):
            return jsonify('This user is not a customer.'), 404
        cartID = cartDao.getCartID(userId)[0]
        cartContent = cartDao.getProdsCart(userId)
        for row in cartContent:
            dict = self.build_dict_getProds(row)
            listOfBooks.append(dict)
        result = {"UserID": userId, "CartID": cartID, "BooksInCart": listOfBooks}
        return jsonify(result)

    def clearCartContent(self, userId):
        cartDao, userDao = CartDao(), UserDAO()
        if not userDao.isUserCustomer(userId):
            return jsonify('This user is not a customer.'), 404
        cartID = cartDao.getCartID(userId)
        cartDao.clearCartContent(cartID)
        return jsonify("Cart cleared successfully"), 201

    def buyAllBooks(self, userId):
        cartDao, userDao, invDao = CartDao(), UserDAO(), InventoryDAO()

        if not userDao.isUserCustomer(userId):
            return jsonify('This user is not a customer.'), 404

        cart_books = cartDao.getAllBooksInCart(userId)
        cart_id = cartDao.getCartID(userId)
        order_id = ""
        firstBookToAdd = True
        for i in range(len(cart_books)):
            if cart_books[i][1] <= cartDao.getInventoryUnits(cart_books[i][0]):
                if firstBookToAdd:
                    order_id = cartDao.createAOrder(userId)
                    firstBookToAdd = False
                book_price = cartDao.getPriceUnitOfBook(cart_books[i][0])
                cartDao.buyBookInCart(order_id, cart_books[i], book_price)
                cartDao.deleteBookFromCart(cart_books[i][0], cart_id)
                cartDao.updateBookInInventory(cart_books[i][0], cart_books[i][1])

            elif cartDao.getInventoryUnits(cart_books[i][0]) != 0 and cart_books[i][1] > cartDao.getInventoryUnits(cart_books[i][0]):
                if firstBookToAdd:
                    order_id = cartDao.createAOrder(userId)
                    firstBookToAdd = False
                remainingUnits = cart_books[i][1] - cartDao.getInventoryUnits(cart_books[i][0])
                # Settings the units that can be bought
                book_row = (cart_books[i][0], cartDao.getInventoryUnits(cart_books[i][0]))
                book_price = cartDao.getPriceUnitOfBook(book_row[0])
                cartDao.buyBookInCart(order_id, book_row, book_price)
                cartDao.updateCartUnits(remainingUnits, cart_id)
                cartDao.updateBookInInventory(book_row[0], book_row[1])

        if not firstBookToAdd:
            return jsonify("Purchase was successful."), 200
        else:
            return jsonify("No purchase was made."), 409
