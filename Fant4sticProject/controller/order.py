from src.databaseConnect import DatabaseConnect
from flask import jsonify
# Class Controller for Order table
class OrderController:
    def __init__(self):
        self.connection = DatabaseConnect().getConnection()

    def historyOfCustomer(self):
        customerId = input("Enter a customer_id to view its corresponding orders: ")
        cursor = self.connection.cursor()
        cursor.execute("select exists( select customer_id from \"Order\" where customer_id =" + str(customerId) +");")
        cust_record = cursor.fetchone()
        exist = cust_record[0]
        if (not exist):
            print("This customer_id does not have any orders.")
            return jsonify(("This customer_id does not have any orders."))
        query = "select extract(year from order_date) as year, extract(mon from order_date) as month, "
        query += "extract(day from order_date) as day, extract(hour from order_time) as hour_time, "
        query += "extract(min from order_time) as min_time, extract(sec from order_time) as sec_time, "
        query += "o.customer_id, title, num_items, price_unit "
        query += "from \"Order\" as o,book_order as bor,book as b, inventory as i "
        query += "where o.order_id = bor.order_id and b.book_id = bor.book_id and b.book_id = i.book_id and o.customer_id =" +str(customerId)+ " "
        query += "order by order_date, order_time;"
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        self.connection.close()
        ordRecords = self.orderRecords(records)
        print(ordRecords)
        return jsonify(ordRecords)

    def historyAll(self):
        cursor = self.connection.cursor()
        query = "select extract(year from order_date) as year, extract(mon from order_date) as month, "
        query += "extract(day from order_date) as day, extract(hour from order_time) as hour_time, "
        query += "extract(min from order_time) as min_time, extract(sec from order_time) as sec_time, "
        query += "o.customer_id, title, num_items, price_unit "
        query += "from \"Order\" as o,book_order as bor,book as b, inventory as i "
        query += "where o.order_id = bor.order_id and b.book_id = bor.book_id and b.book_id = i.book_id "
        query += "order by customer_id, order_date,order_time;"
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        self.connection.close()
        ordRecords = self.orderRecords(records)
        print(ordRecords)
        return jsonify(ordRecords)

    # Store in a dictionary the date and time as values for each order
    def separateOrders(self,records):
        dict = {}
        for rec in records:
            string = str(int(rec[0])) + "-" + str(int(rec[1])) + "-" + str(int(rec[2])) + "-" + str(
                int(rec[3])) + "-" + str(int(rec[4])) + "-" + str(int(rec[5])) + " | Customer Id:" + str(int(rec[6]))
            value = string
            key = str(rec[7]) + "|" + str(rec[8]) + "|" + str(rec[9])
            dict[key] = value
        return dict

    # Change the values to keys and group orders that have same date and time
    def groupOrders(self,records):
        dict = self.separateOrders(records)
        # Get unique keys
        values = set(dict.values())
        newDict = {}
        for val in values:
            newDict[val] = [k for k in dict.keys() if dict[k] == val]
        return newDict

    # Calculate total order for each record
    def orderRecords(self,records):
        dictRecord = self.groupOrders(records)
        keysRecord = dictRecord.keys()
        valuesRecord = dictRecord.values()
        sum = 0
        for val in valuesRecord:
            sum = 0
            if len(val) > 1:
                for v in val:
                    x = v.split("|")
                    sum += float(x[len(x) - 1]) * float(x[len(x) - 2])  # Get the total price for v
                val.append("Total Price: " + str(sum))
            else:
                x = val[0].split("|")
                sum += float(x[len(x) - 1]) * float(x[len(x) - 2])  # Get the total price for val
                val.append("Total Price: " + str(sum))
        arrRecords = []
        for key in keysRecord:
            arrRecords.append(tuple([key] + dictRecord[key]))
        return arrRecords

