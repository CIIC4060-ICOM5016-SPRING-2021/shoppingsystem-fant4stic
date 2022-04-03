from dao.order import OrderDAO
from flask import jsonify
# Class Controller for Order table
class OrderController:

    def historyOfCustomer(self,customerId):
        dao = OrderDAO()
        exist = dao.existCustomerOrder(customerId)
        if (not exist):
            print("This CustomerId does not have any orders.")
            return jsonify("This CustomerId does not have any orders.") , 404
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

    def build_dict_order(self,row):
        result ={}
        result['OrderId'] = row[0]
        result['UserId'] = row[1]
        result['OrderDate'] = row[2]
        result['OrderTime'] = row[3]
        result['ListOfProductsBought'] = row[4]
        result['TotalPrice'] = row[5]
        return result

    def build_dict_book(self, row):
        result = {}
        result['BookTitle'] = row[8]
        result['NumberOfQuantities'] = row[9]
        result['BookPrice'] = row[10]/row[9] # Unit Price of Book
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
                    ordIdChanged = False
                    newOrderRow.append(time) #Add order_time
                if ordId == orders[i][0]:
                    dict = self.build_dict_book(orders[i])
                    totalPrice += orders[i][10]
                    listProducts.append(dict)
            newOrderRow.append(listProducts) #Add listProducts
            newOrderRow.append(totalPrice) #Add totalprice
            resultOrders.append(newOrderRow)
        return resultOrders
