from config.databaseConnect import DatabaseConnect
# DAO Class that works for Order Controller
class OrderDAO:
    def __init__(self):
        self.connection = DatabaseConnect().getConnection()

    def existCustomerOrder(self,customerId):
        cursor = self.connection.cursor()
        cursor.execute("select exists( select customer_id from \"Order\" where customer_id =" + str(customerId) + ");")
        resquery = cursor.fetchone()[0]
        cursor.close()
        return resquery

    def getOrderHistoryOf(self,customerId):
        cursor = self.connection.cursor()
        query = "select extract(year from order_date) as year, extract(mon from order_date) as month, "
        query += "extract(day from order_date) as day, extract(hour from order_time) as hour_time, "
        query += "extract(min from order_time) as min_time, extract(sec from order_time) as sec_time, "
        query += "o.customer_id, title, num_items, price_unit "
        query += "from \"Order\" as o,book_order as bor,book as b, inventory as i "
        query += "where o.order_id = bor.order_id and b.book_id = bor.book_id and b.book_id = i.book_id and o.customer_id =" + str(customerId) + " "
        query += "order by order_date, order_time;"
        cursor.execute(query)
        resquery = cursor.fetchall()
        cursor.close()
        return resquery

    def getOrderHistoryOfAllCustomers(self):
        cursor = self.connection.cursor()
        query = "select extract(year from order_date) as year, extract(mon from order_date) as month, "
        query += "extract(day from order_date) as day, extract(hour from order_time) as hour_time, "
        query += "extract(min from order_time) as min_time, extract(sec from order_time) as sec_time, "
        query += "o.customer_id, title, num_items, price_unit "
        query += "from \"Order\" as o,book_order as bor,book as b, inventory as i "
        query += "where o.order_id = bor.order_id and b.book_id = bor.book_id and b.book_id = i.book_id "
        query += "order by customer_id, order_date,order_time;"
        cursor.execute(query)
        resquery = cursor.fetchall()
        cursor.close()
        return resquery
