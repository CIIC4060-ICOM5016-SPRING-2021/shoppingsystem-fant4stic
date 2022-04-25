from dao.order import OrderDAO
from dao.user import UserDAO
from flask import jsonify
# Class Controller for Order table
class OrderController:

    def historyOfCustomer(self,customerId):
        dao = OrderDAO()
        if(not UserDAO().isUserCustomer(customerId)):
            return jsonify('The value passed is not a valid customerId.'), 404
        exist = dao.existCustomerOrder(customerId)
        if (not exist):
            return jsonify('This customer does not have any orders yet.') , 404
        records = dao.getOrderHistoryOf(customerId)
        groupRecords = self.groupOrders(records)
        result = []
        for row in groupRecords:
            dict = self.build_dict_order(row)
            result.append(dict)
        return jsonify(result)

    def historyAll(self):
        dao = OrderDAO()
        records = dao.getOrderHistoryOfAllCustomers()
        groupRecords = self.groupOrders(records)
        result = []
        for row in groupRecords:
            dict = self.build_dict_order(row)
            result.append(dict)
        return jsonify(result)

    def getAllOrder(self):
        dao = OrderDAO()
        records = dao.getAllOrder()
        result = []
        for row in records:
            dict = self.build_dict_allorder(row)
            result.append(dict)
        print(result)
        return jsonify(result), 200

    def customerMostBoughtCat(self,customerId):
        orderdao , userdao = OrderDAO() , UserDAO()
        if(not userdao.isUserCustomer(customerId)):
            return jsonify('The value passed is not a valid customerId.'), 404
        if (not orderdao.existCustomerOrder(customerId)):
            return jsonify('This customer does not have any orders yet.') , 404
        records = orderdao.getCustomerMostBoughtCategories(customerId)
        result =[]
        for i in range(len(records)):
            dict = self.build_dict_category(records[i],i+1)
            result.append(dict)
        return jsonify(result)

    def customerMostBoughtProd(self,customerId):
        orderdao, userdao = OrderDAO(), UserDAO()
        if (not userdao.isUserCustomer(customerId)):
            return jsonify('The value passed is not a valid customerId.'), 404
        if (not orderdao.existCustomerOrder(customerId)):
            return jsonify('This customer does not have any orders yet.'), 404
        records = orderdao.getCustomerMostBoughtProducts(customerId)
        result = []
        for i in range(len(records)):
            dict = self.build_dict_product(records[i], i + 1)
            result.append(dict)
        return jsonify(result)

    def customerCheapestProductBought(self,customerId):
        orderdao, userdao = OrderDAO(), UserDAO()
        if (not userdao.isUserCustomer(customerId)):
            return jsonify('The value passed is not a valid customerId.'), 404
        if (not orderdao.existCustomerOrder(customerId)):
            return jsonify('This customer does not have any orders yet.'), 404
        record = orderdao.getCustomerCheapestBoughtProd(customerId)
        result = []
        for row in record:
            dict = self.build_dict_cheapestProduct(row)
            result.append(dict)
        return jsonify(result)

    def customerMostExpensiveProductBought(self,customerId):
        orderdao, userdao = OrderDAO(), UserDAO()
        if (not userdao.isUserCustomer(customerId)):
            return jsonify('The value passed is not a valid customerId.'), 404
        if (not orderdao.existCustomerOrder(customerId)):
            return jsonify('This customer does not have any orders yet.'), 404
        record = orderdao.getCustomerMostExpensiveBoughtProd(customerId)
        result = []
        for row in record:
            dict = self.build_dict_mostExpensiveProduct(row)
            result.append(dict)
        return jsonify(result)

    def getAllBookOrder(self):
        dao = OrderDAO()
        records = dao.getAllBookOrder()
        result = []
        for row in records:
            dict = self.build_dict_bookorder(row)
            result.append(dict)
        return jsonify(result), 200

    def build_dict_order(self,row):
        result ={}
        result['OrderId'] = row[0]
        result['UserId'] = row[1]
        result['OrderDate'] = row[2]
        result['OrderTime'] = row[3]
        result['ListOfProductsBought'] = row[4]
        result['TotalPrice'] = row[5]
        return result

    def build_dict_one_order(self,row):
        result ={}
        result['OrderId'] = row[0]
        result['UserId'] = row[1]
        result['OrderDate'] = str(int(row[2])) + "-" + str(int(row[3])) + "-" + str(int(row[4]))
        result['OrderTime'] = str(int(row[5])) + "-" + str(int(row[6])) + "-" + str(int(row[7]))
        return result

    def build_dict_book(self, row):
        result = {}
        result['BookTitle'] = row[8]
        result['NumberOfQuantities'] = row[9]
        result['BookPrice'] = row[10]/row[9] # Unit Price of Book
        return result

    def build_dict_category(self,row,i):
        result = {}
        result['#' + str(i) + '_Genre'] = row[0]
        result['AmountBoughtFromCategory'] = row[1]
        return result

    def build_dict_product(self,row,i):
        result = {}
        result['#' + str(i) + '_ProductID'] = row[0]
        result['Title'] = row[1]
        result['AmountOfCopiesBought'] = row[2]
        return result

    def build_dict_cheapestProduct(self,row):
        result ={}
        result['CheapestProductID'] = row[0]
        result['Title'] = row[1]
        result['Price'] = round(row[2],2)
        return result

    def build_dict_mostExpensiveProduct(self,row):
        result = {}
        result['MostExpensiveProductID'] = row[0]
        result['Title'] = row[1]
        result['Price'] = round(row[2], 2)
        return result

    def build_dict_bookorder(self,row):
        result = {}
        result['OrderId'] = row[0]
        result['BookId'] = row[1]
        result['NUmberOfCopies'] = row[2]
        result['PaymentForCopies'] = row[3]
        return result

    def build_dict_allorder(self,row):
        result = {}
        result['OrderId'] = row[0]
        result['UserId'] = row[1]
        result['OrderDate'] = str(int(row[2])) + "-" + str(int(row[3])) + "-" + str(int(row[4]))
        result['OrderTime'] = str(int(row[5])) + "-" + str(int(row[6])) + "-" + str(int(row[7]))
        return result

    def create_newRow(self,orderId):
        newRow = []
        newRow.append(orderId)
        return newRow

    # Group orders with same order_id
    def groupOrders(self,orders):
        difOrderId = []
        # Generate list of distinct order_id
        for row in orders:
            if difOrderId.count(row[0]) == 0:
                difOrderId.append(row[0])
        resultOrders = []
        #Group books together that have the same order_id
        for ordId in difOrderId:
            newOrderRow = self.create_newRow(ordId) #Add order_id
            totalPrice = 0
            listProducts = []
            ordIdChanged = True
            for i in range(len(orders)):
                if ordIdChanged == True and ordId == orders[i][0]:
                    newOrderRow.append(orders[i][1]) #Add user_id
                    date = str(int(orders[i][2])) +"-"+ str(int(orders[i][3])) +"-"+ str(int(orders[i][4]))
                    newOrderRow.append(date) #Add order_date
                    time = str(int(orders[i][5])) + "-" + str(int(orders[i][6])) + "-" + str(int(orders[i][7]))
                    newOrderRow.append(time) #Add order_time
                    ordIdChanged = False
                if ordId == orders[i][0]:
                    dict = self.build_dict_book(orders[i])
                    totalPrice += orders[i][10]
                    listProducts.append(dict)
            newOrderRow.append(listProducts) #Add listProducts
            newOrderRow.append(totalPrice) #Add totalprice
            resultOrders.append(newOrderRow)
        return resultOrders

    def getMCategoryGlobally(self):

        #Create an instance of the dao to run the queries
        dao = OrderDAO()

        #Simply get the value and return them in a dictionary
        result = dao.getMostBoughtCategoryGlobally()

        #Initialize a count variable to rank the genres
        count = 1

        #Initialize a variable to store the result
        rankedGenres = []

        for row in result:
            dictionary = self.build_dict_category(row, count)
            rankedGenres.append(dictionary)
            count = count + 1

        #Now return the jsonified result
        return jsonify(rankedGenres)

    def getMProductGlobally(self):

        #Create an instance of the dao to run the queries
        dao = OrderDAO()

        #Simply get the value and return them in a dictionary
        result = dao.getMostBoughtProductGlobally()

        #Initialize a count variable to rank the products
        count = 1

        #Initialize a variable to store the result
        rankedProducts = []

        for row in result:
            #For every book get the title to provide it as an output
            dictionary = self.build_dict_product(row, count)
            rankedProducts.append(dictionary)
            count = count + 1

        #Now return the jsonified result
        return jsonify(rankedProducts)

    def getOrder(self, orderId):
        dao = OrderDAO()
        order = dao.getOrder(orderId)
        if not order:
            return jsonify("Order Not Found"), 404
        else:
            order = self.build_dict_one_order(order)
            return jsonify(order), 200

    def deleteOrder(self, orderId):
        dao = OrderDAO()
        order = dao.getOrder(orderId)
        if not order:
            return jsonify("Order Not Found"), 404
        dao.deleteFromBook_Order(orderId)
        dao.deleteFromOrder(orderId)
        return jsonify("Order deleted successfully."), 201
