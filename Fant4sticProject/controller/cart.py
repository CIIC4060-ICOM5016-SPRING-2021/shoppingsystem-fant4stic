from flask import jsonify
from dao.cart import CartDao

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

        #Verify is the book is already in the cart
        bookExists = dao.checkIfBookExists(bookToAdd)

        if(not bookExists):
            #Now add the book to the cart
            dao.addBook(bookToAdd,existingCart,howMuchBooks)
        else:
            wantToAdd = input("The desired book already exists in your cart.\n"
                               "Do you wish to add more copies of the book? (Yes or No): ")

            #Keep asking until input is the desired string
            while(wantToAdd != "Yes" and wantToAdd != "No"):
                wantToAdd = input("Please answer Yes or No (use capital letter for the Y or N)")

            if(wantToAdd == "Yes"):
                howMuchBooks = input("How many copies you want to add: ")
            else:
                return jsonify("Process concluded!")

            if(bookExists and wantToAdd == "Yes"):
                #Get the current copies in cart of the desired book
                currentCopies = dao.getCopies(bookToAdd)

                #Add the desired copies
                dao.addExtraCopies(howMuchBooks, currentCopies, bookToAdd)

                #Verify the desired copies were added
                totalCopies = int(howMuchBooks)+int(currentCopies)

                if(totalCopies == dao.getCopies(bookToAdd)):
                    return jsonify("Copies added successfully")


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
            #Ask if he wants to eliminate a certain amount of copies instead of the book
            wantToDelete = input("The desired book already exists in the car\n"
                                 "Do you wish to eliminate a certain amount of copies instead of the book? (Yes or No): ")

            #Keep asking until input is the desired string
            while(wantToDelete != "Yes" and wantToDelete != "No"):
                wantToDelete = input("Please answer Yes or No (use capital letter for the Y or N)")

            #If the customer desires to not delete copies conclude the process
            if(wantToDelete == "Yes"):
                howMuchBooks = input("How many copies you want to delete: ")

            if(bookExists and wantToDelete == "Yes"):
                #Get the current copies in cart of the desired book
                currentCopies = dao.getCopies(bookToDelete)

                #Delete the desired copies
                dao.deleteCopies(howMuchBooks, currentCopies, bookToDelete)

                #Verify the desired copies were subtracted
                totalCopies = int(currentCopies) - int(howMuchBooks)

                if(totalCopies == dao.getCopies(bookToDelete)):
                    return jsonify("Copies eliminated successfully")

            if(wantToDelete == "No"):
                #Delete the book now
                dao.deleteBook(bookToDelete)

                # Verify the book was deleted
                bookExists = dao.checkIfBookExists(bookToDelete)

                if (not bookExists):
                    return jsonify("Book was deleted from cart!")
                else:
                    return jsonify("Book could not be deleted from cart!")
        else:
            return jsonify("The selected book was not in your cart")

        return jsonify("Could not delete the desired book from your cart")
