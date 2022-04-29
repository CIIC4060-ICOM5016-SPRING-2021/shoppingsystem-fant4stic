from flask import jsonify
from dao.wishlist import WishlistDAO
from dao.user import UserDAO
from datetime import date
# Class Controller for Wishlist table
class WishlistController:
    def build_dict_wishlist(self,row):
        result = {}
        result['WishlistId'] = row[0]
        result['CustomerId'] = row[1]
        return result

    def build_dict_addtowishlist(self,row):
        result = {}
        result['WishlistId'] = row[0]
        result['BookId'] = row[1]
        result['DateAdded'] = str(int(row[2])) + "-" + str(int(row[3])) + "-" + str(int(row[4]))
        return result

    def build_dict_addingBook(self, row):
        result = {}
        result['Title'] = row[0]
        result['Book_id'] = row[1]
        result['Wishlist_id'] = row[2]
        result['Date_added'] = row[3]
        return result

    def build_dict_deletingBook(self, row):
        result = {}
        result['Title'] = row[0]
        result['Book_id'] = row[1]
        result['Wishlist_id'] = row[2]
        return result

    def getAllWishlists(self):
        dao = WishlistDAO()
        records = dao.getAllWishlists()
        result = []
        for row in records:
            dict = self.build_dict_wishlist(row)
            result.append(dict)
        return jsonify(result), 200

    def getAllAddToWishlist(self):
        dao = WishlistDAO()
        records = dao.getAllAddToWishlist()
        result = []
        for row in records:
            dict = self.build_dict_addtowishlist(row)
            result.append(dict)
        return jsonify(result), 200

    def addBook(self, json):
        bookTitle = json['Title']
        userAddingTheBook = json['Customer_id']
        wishlistID = json['Wishlist_id']

        #Create dao instance
        dao = WishlistDAO()

        #First verify if a book with the title provided exists
        if(bookTitle):
            existsTitle = dao.checkifTitleExists(bookTitle)
        else:
            return jsonify("A book title was not provided"), 400

        if(not existsTitle):
            return jsonify("The provided title does not match any of our book records"), 404

        #Now get the book id
        bookToAdd = dao.getBookID(bookTitle)

        #Now verify the user exists
        if(userAddingTheBook):
            userExists = dao.checkIfUserExists(userAddingTheBook)
        else:
            return jsonify("A customer ID was not provided"), 400

        if(userExists):
            #Now verify the user is a customer
            userRole = dao.getUserRole(userAddingTheBook)
        else:
            return jsonify("Your user ID does not belong to a registered user"), 404

        if(userRole != "Customer"):
            return jsonify("User is unavailable to add items to a wishlist, because he/she is not a customer"), 405

    #Check if the indicated wishlist exists and is associated with the user
        if(wishlistID):
            exists = dao.checkIfWishlistExists(userAddingTheBook, wishlistID)
        else:
            return jsonify("A wishlist ID was not provided"), 400

        if(exists):
            #Verify if the book is already in the wishlist
            bookExists = dao.checkIfBookExists(bookToAdd,wishlistID)
        else:
            return jsonify("The indicated wishlist is not associated to the user ID provided or does not exist"), 404

        if(not bookExists):
            #Calculate time externally to be able to use the same variable use for adding the book for the output
            todayDate = date.today()

            #Now add the book to the wishlist
            dao.addBook(bookToAdd,wishlistID, todayDate)
        else:
            return jsonify("Book was not added, because it already existed in your wishlist"), 409

        #Verify the book was added
        bookExists = dao.checkIfBookExists(bookToAdd, wishlistID)

        if(bookExists):
            #Build json for output
            row = [bookTitle, bookToAdd, wishlistID, todayDate]
            dictionary = self.build_dict_addingBook(row)

            return jsonify(dictionary), 200
        else:
            return jsonify("The book could not be added to you wishlist :("), 500

    def deleteBook(self, json):
        bookTitle = json['Title']
        userDeletingTheBook = json['Customer_id']
        wishlistID = json['Wishlist_id']

        # Create dao instance
        dao = WishlistDAO()

        # First verify if a book with the title provided exists
        if (bookTitle):
            existsTitle = dao.checkifTitleExists(bookTitle)
        else:
            return jsonify("A book title was not provided"), 400

        if (not existsTitle):
            return jsonify("The provided title does not match any of our book records"), 404

        # Now get the book id
        bookToDelete = dao.getBookID(bookTitle)

        # Now verify the user exists
        if (userDeletingTheBook):
            userExists = dao.checkIfUserExists(userDeletingTheBook)
        else:
            return jsonify("A customer ID was not provided"), 400

        if (userExists):
            # Now verify the user is a customer
            userRole = dao.getUserRole(userDeletingTheBook)
        else:
            return jsonify("Your user ID does not belong to a registered user"), 404

        if (userRole != "Customer"):
            return jsonify("User is unavailable to delete items from a wishlist, because he/she is not a customer"), 405

        # Check if the indicated wishlist exists and is associated with the user
        if (wishlistID):
            exists = dao.checkIfWishlistExists(userDeletingTheBook, wishlistID)
        else:
            return jsonify("A wishlist ID was not provided"), 400

        if(exists):
            #Verify if the book is already in the wishlist
            bookExists = dao.checkIfBookExists(bookToDelete, wishlistID)
        else:
            return jsonify("The indicated wishlist is not associated to the user ID provided or does not exist"), 404

        if(bookExists):
            #Now delete the book
            dao.deleteBook(wishlistID, bookToDelete)
        else:
            return jsonify("Book was not deleted, because it was not present in your wishlist"), 404

        #Verify the book was deleted
        bookExists = dao.checkIfBookExists(bookToDelete, wishlistID)

        if(not bookExists):
            #Build json for output
            row = [bookTitle, bookToDelete, wishlistID]
            dictionary = self.build_dict_deletingBook(row)

            return jsonify(dictionary), 200
        else:
            return jsonify("The book could not be deleted from your wishlist"), 500

    def build_dict_G(self, row, title):
        result = {}
        result ['Book_ID'] = row[0]
        result ['Book_likes'] = row[1]
        result ['Book_title'] = title

        return result

    def getMostLikedProductG(self):

        #Create a dao instance to run the queries
        dao = WishlistDAO()

        #Get the tuple with the most expensive product
        result = dao.getMostLikedProductGlobally()

        #Build a variable to store the result
        mostLikedProduct = []

        #Now build the dictionary for display
        for row in result:
            #Get the title of the book for display
            title = dao.getBookTitle(row[0])

            dictionary = self.build_dict_G(row, title)
            mostLikedProduct.append(dictionary)

        return jsonify(mostLikedProduct)

    def createWish(self, json):
        userID = json ['User_id']

        #Create a dao instance to run queries
        dao = WishlistDAO()

        #Now verify the user exists
        if(userID):
            userExists = dao.checkIfUserExists(userID)
        else:
            return jsonify("A user ID was not provided"), 400

        if(userExists):
            #Now verify the user is a customer
            userRole = dao.getUserRole(userID)
        else:
            return jsonify("Your user ID does not belong to a registered user"), 404

        if(userRole != "Customer"):
            return jsonify("User is unavailable to add items to a cart, because he/she is not a customer"), 405

        #Now Proceed to create the wishlist
        wishlistID = dao.createWishlist(userID)

        #Verify if a wishlist associated with the customer exists (indicated wishlist was created)
        wishlistExists = dao.checkIfWishlistExists(userID, wishlistID)

        if(wishlistExists):
            #Build Json for output
            result = {}
            result ["User_id"] = userID
            result ["Wishlist_id"] = wishlistID

            return jsonify(result), 200
        else:
            return jsonify("Wishlist was not created due to an internal error"), 500

    def deleteWish(self, json):
        userID = json ['User_id']
        wishlistID = json ['Wishlist_id']

        #Create a dao instance to run queries
        dao = WishlistDAO()

        #Now verify the user exists
        if(userID):
            userExists = dao.checkIfUserExists(userID)
        else:
            return jsonify("A user ID was not provided"), 400

        if(userExists):
            #Now verify the user is a customer
            userRole = dao.getUserRole(userID)
        else:
            return jsonify("Your user ID does not belong to a registered user"), 404

        if(userRole != "Customer"):
            return jsonify("User is unavailable to add items to a cart, because he/she is not a customer"), 405

        #First we need to delete all items associated to this wishlist
        dao.deleteWishListProducts(wishlistID)

        #Now Proceed to delete the wishlist
        dao.deleteWishList(userID, wishlistID)

        #Verify if a wishlist associated with the customer exists (indicated wishlist was created)
        wishlistExists = dao.checkIfWishlistExists(userID, wishlistID)

        if(not wishlistExists):
            #Build Json for output
            result = {}
            result ["User_id"] = userID
            result ["Wishlist_id"] = wishlistID

            return jsonify(result), 200
        else:
            return jsonify("Wishlist was not created due to an internal error"), 500

    def build_dict_CustomerWishlist(self,row):
        result = {}
        result['WishlistId'] = row[0]
        result['CustomerId'] = row[1]
        result['ListOfProducts'] = row[2]
        return result

    def getProdsInWishlist(self,userId):
        dao = WishlistDAO()
        if (not UserDAO().isUserCustomer(userId)):
            return jsonify('The value passed is not a valid customerId.'), 404
        wishlists = dao.getUserWishlist(userId)
        groupedWishList = self.groupWishlist(wishlists,userId)
        result = []
        for wishlist in groupedWishList:
            dict =  self.build_dict_CustomerWishlist(wishlist)
            result.append(dict)
        return jsonify(result), 200

    def create_newRow(self,wishlistID):
        newRow = []
        newRow.append(wishlistID)
        return newRow

    def build_dict_WishListBook(self,row):
        result = {}
        result['BookTitle'] = row[1]
        result['DateAdded'] = str(int(row[2])) +"-"+ str(int(row[3])) +"-"+ str(int(row[4]))
        return result

    def groupWishlist(self,wishlists,userId):
        difWishlistId = []
        # Generate list of distinct wishlist_id
        for row in wishlists:
            if difWishlistId.count(row[0]) == 0:
                difWishlistId.append(row[0])
        resultWishlists = []

        for wishlistId in difWishlistId:
            newWishlistRow = self.create_newRow(wishlistId)  # Add wishlist_id
            newWishlistRow.append(userId) # Add CustomerID
            listProducts = []
            for i in range(len(wishlists)):
                if(wishlistId == wishlists[i][0]):
                    dict = self.build_dict_WishListBook(wishlists[i])
                    listProducts.append(dict)
            newWishlistRow.append(listProducts)  # Add listProducts
            resultWishlists.append(newWishlistRow)
        return resultWishlists
