from flask import jsonify
from Fant4sticProject.dao.cart import CartDao

class CartController:
    #def getAllBooks(self):


    def addBook(self):
        bookToAdd = input("Book ID to add to the cart: ")
        customerToAdd = input("ID of the customer adding the book: ")

        dao = CartDao()
        exists = dao.checkIfCartExists(customerToAdd) #Only one cart per customer

        if(exists):
            cart = dao.returnCustomerCart(customerToAdd)
            print("Cart ID obtained: " + str(cart))
        else:
            #create a new cart
            dao.generateCart(customerToAdd)

            #get the new cart
            cartAdded = dao.returnCustomerCart(customerToAdd)

            print("Cart: " + str(cartAdded) + " generated")

        howMuchBooks = input("How many copies to add: ")

        #get the customer cart
        existingCart = dao.returnCustomerCart(customerToAdd)

        #Now add the book to the cart
        dao.addBook(bookToAdd,existingCart,howMuchBooks)

        #Verify the book was added
        bookExists = dao.checkIfBookExists(bookToAdd)

        if(bookExists):
            return jsonify("Book added to cart!")
        else:
            return jsonify("Book could not be added to cart!")

    def deleteBook(self):

        dao = CartDao()

        customerDeleting = input("Please provide your customer ID: ")
        bookToDelete = input("Please provide the book ID of the book you wish to delete: ")

        #Check if a cart associated with the customer exists
        cartExist = dao.checkIfCartExists(customerDeleting)

        if(not cartExist):
            return jsonify("You have no existing cart")

        #Verify the book is in the cart
        bookExists = dao.checkIfBookExists(bookToDelete)

        if(bookExists):
            #Delete the book now
            dao.deleteBook(bookToDelete)
        else:
            return jsonify("The selected book was not in your cart")

        #Verify the book was deleted
        bookExists = dao.checkIfBookExists(bookToDelete)

        if(not bookExists):
            return jsonify("Book was deleted from cart!")
        else:
            return jsonify("Book could not be deleted from cart!")
