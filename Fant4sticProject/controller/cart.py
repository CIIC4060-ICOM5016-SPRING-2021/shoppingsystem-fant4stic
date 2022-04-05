from flask import jsonify
from dao.cart import CartDao
from dao.user import UserDAO

class CartController:
    #def getAllBooks(self):


    def addBook(self, json):
        bookTitle = json[0]['title']
        userAddingTheBook = json[0]['user_id']
        howMuchBooks = json[0]['num_addeditems']

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
        """
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
        """

        #Verify the book was added
        bookExists = dao.checkIfBookExists(bookToAdd, userAddingTheBook)

        if(bookExists):
            #Get how many units were available before addition
            unitsAvailableBefore = dao.getInventoryUnits(bookToAdd)

            #Now update inventory
            dao.updateInventoryAfterAddition(bookToAdd,howMuchBooks,unitsAvailableBefore)

            return jsonify("Book added to cart!"), 200
        else:
            return jsonify("Book could not be added to cart!"), 500

    def deleteBook(self, json):
        bookTitle = json[0]['title']
        userDeletingTheBook = json[0]['user_id']

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
            return jsonify("User is unavailable to add items to a cart, because he/she is not a customer"), 405


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

        # Verify the book was deleted
        bookExists = dao.checkIfBookExists(bookToDelete,userDeletingTheBook)

        if(not bookExists):
            return jsonify("Book was deleted from your cart"), 200
        else:
            return jsonify("Book could not be deleted from cart"), 500

        """
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
        """

    def clearCartContent(self, userId):
        cartDao, userDao = CartDao(), UserDAO()
        if not userDao.isUserCustomer(userId):
            return jsonify('This user is not a customer.'), 404
        cartID = cartDao.getCartID(userId)
        cartDao.clearCartContent(cartID)
        return jsonify("Cart cleared successfully"), 201
