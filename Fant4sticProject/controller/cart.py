from flask import jsonify
from dao.cart import CartDao
from dao.user import UserDAO

class CartController:
    def build_dict(self, row):
        result = {}
        result['Title'] = row[0]
        result['Customer_id'] = row[1]
        result['Copies'] = row[2]
        result['Book_id'] = row[3]
        result['Cart_id'] = row[4]
        return result

    def build_dict_cart(self,row):
        result = {}
        result['CartId'] = row[0]
        result['Customer_id'] = row[1]
        return result

    def getAllCarts(self):
        dao = CartDao()
        records = dao.getAllCarts()
        result = []
        for row in records:
            dict = self.build_dict_cart(row)
            result.append(dict)
        return jsonify(result), 200


    def addBook(self, json):
        bookTitle = json['Title']
        userAddingTheBook = json['Customer_id']
        howMuchBooks = json['Copies']

        dao = CartDao()

        #First verify if a book with the title provided exists
        existsTitle = dao.checkifTitleExists(bookTitle)

        if(not existsTitle):
            return jsonify("The provided title does not match any of our book records"), 404


        #Now get the book id
        bookToAdd = dao.getBookID(bookTitle)

        #Now verify the book is on inventory
        existsOnInventory = dao.checkIfBookIsAvailable(bookToAdd)

        if(not existsOnInventory):
            return jsonify("The book is not currently available :("), 404

        #Now verify the user is a customer
        userRole = dao.getUserRole(userAddingTheBook)

        if(userRole != "Customer"):
            return jsonify("User is unavailable to add items to a cart, because he/she is not a customer"), 405

        #Now verify that the amount of copies the customer wants to add does not exceed inventory capacity
        exceeds = dao.getInventoryUnits(bookToAdd)

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
            #Get how many units were available before addition
            unitsAvailableBefore = dao.getInventoryUnits(bookToAdd)

            #Now update inventory
            dao.updateInventoryAfterAddition(bookToAdd,howMuchBooks,unitsAvailableBefore)

            #Build json for output
            row = [bookTitle, userAddingTheBook, howMuchBooks, bookToAdd, existingCart]
            dictionary = self.build_dict(row)

            return jsonify("Book added to cart!",
                           dictionary), 200
        else:
            return jsonify("Book could not be added to cart!"), 500

    def deleteBook(self, json):
        bookTitle = json['Title']
        userDeletingTheBook = json['Customer_id']

        dao = CartDao()

        #First verify if a book with the title provided exists
        existsTitle = dao.checkifTitleExists(bookTitle)

        if(not existsTitle):
            return jsonify("The provided title does not match any of our book records"), 404


        #Now get the book id
        bookToDelete = dao.getBookID(bookTitle)

        #Now verify the user is a customer
        userRole = dao.getUserRole(userDeletingTheBook)

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

            # Get units available in inventory
            inventoryUnits = dao.getInventoryUnits(bookToDelete)

            # Update the inventory now
            dao.updateInventoryAfterDeletion(bookToDelete,copiesStored, inventoryUnits)
        else:
            return jsonify("The desired book could not be deleted, because it was not present in your cart"), 404

        # Verify the book was deleted
        bookExists = dao.checkIfBookExists(bookToDelete, userDeletingTheBook)

        if(not bookExists):
            # Build the Json for output
            row = [bookTitle, userDeletingTheBook, copiesStored, bookToDelete, customerCart]
            dictionary = self.build_dict(row)

            return jsonify("The following book and copies were deleted from your cart:", dictionary), 200
        else:
            return jsonify("Book could not be deleted from cart"), 500

    def clearCartContent(self, userId):
        cartDao, userDao = CartDao(), UserDAO()
        if not userDao.isUserCustomer(userId):
            return jsonify('This user is not a customer.'), 404
        cartID = cartDao.getCartID(userId)
        cartDao.clearCartContent(cartID)
        return jsonify("Cart cleared successfully"), 201
