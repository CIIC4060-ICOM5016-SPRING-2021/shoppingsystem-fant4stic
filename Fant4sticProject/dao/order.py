from config.databaseConnect import DatabaseConnect
# DAO Class that works for Order Controller
class OrderDAO:
    def __init__(self):
        self.connection = DatabaseConnect().getConnection()

    def existCustomerOrder(self,customerId):
        cursor = self.connection.cursor()
        cursor.execute("select exists( select user_id from \"Order\" where user_id =" + str(customerId) + ");")
        resquery = cursor.fetchone()[0]
        cursor.close()
        return resquery

    def getOrderHistoryOf(self,customerId):
        cursor = self.connection.cursor()
        query = "select o.order_id, user_id, "
        query += "extract(year from order_date) as year,extract(mon from order_date) as month, extract(day from order_date) as day, "
        query += "extract(hour from order_time) as hour_time, extract(min from order_time) as min_time, extract(sec from order_time) as sec_time, "
        query += "title, num_items, order_payment "
        query += "from \"Order\" as o, book_order as bor,book as b "
        query += "where o.order_id = bor.order_id and bor.book_id = b.book_id and user_id = " +str(customerId) + ";"
        cursor.execute(query)
        resquery = []
        for row in cursor:
            resquery.append(row)
        cursor.close()
        return resquery

    def getOrderHistoryOfAllCustomers(self):
        cursor = self.connection.cursor()
        query = "select o.order_id, user_id, "
        query += "extract(year from order_date) as year,extract(mon from order_date) as month, extract(day from order_date) as day, "
        query += "extract(hour from order_time) as hour_time, extract(min from order_time) as min_time, extract(sec from order_time) as sec_time, "
        query += "title, num_items, order_payment "
        query += "from \"Order\" as o, book_order as bor,book as b "
        query += "where o.order_id = bor.order_id and bor.book_id = b.book_id;"
        cursor.execute(query)
        resquery = []
        for row in cursor:
            resquery.append(row)
        cursor.close()
        return resquery

    # Group orders of customer by category and sum the number of times bought
    def getCustomerMostBoughtCategories(self,customerId):
        cursor = self.connection.cursor()
        query = "select genre_name , sum(num_items) as times_bought "
        query += "from \"Order\" as o, book_order as bor,book as b, book_genre as bog, genre as g "
        query += "where o.order_id = bor.order_id and bor.book_id = b.book_id "
        query += "and b.book_id = bog.book_id and bog.genre_id = g.genre_id "
        query += "and user_id =" + str(customerId) + " "
        query += "group by genre_name order by times_bought DESC;"
        cursor.execute(query)
        resquery = []
        for row in cursor:
            resquery.append(row)
        cursor.close()
        return resquery

    # Group products and sum all the copies of the same book
    def getCustomerMostBoughtProducts(self,customerId):
        cursor = self.connection.cursor()
        query = "select title , sum(num_items) as times_bought "
        query +="from \"Order\" as o, book_order as bor,book as b "
        query +="where o.order_id = bor.order_id and bor.book_id = b.book_id "
        query += "and user_id =" +str(customerId) +" "
        query += "group by title order by times_bought DESC;"
        cursor.execute(query)
        resquery = []
        for row in cursor:
            resquery.append(row)
        cursor.close()
        return resquery

    def getCustomerCheapestBoughtProd(self,customerId):
        cursor = self.connection.cursor()
        # Get cheapest price customer has bought
        query = "select min(order_payment/num_items) as price_unit "
        query += "from \"Order\" as o, book_order as bor,book as b "
        query += "where o.order_id = bor.order_id and bor.book_id = b.book_id "
        query += "and user_id = "+str(customerId)+ ";"
        cursor.execute(query)
        cheapestPrice = cursor.fetchone()[0]
        # Get Products that its price are equal to cheapest one
        queryTwo = "select title, order_payment/num_items as price_unit "
        queryTwo += "from \"Order\" as o, book_order as bor,book as b "
        queryTwo += "where o.order_id = bor.order_id and bor.book_id = b.book_id "
        queryTwo += "and user_id ="+str(customerId)+ " and order_payment/num_items = "+str(cheapestPrice)+ " "
        queryTwo += "group by title, order_payment/num_items;"
        cursor.execute(queryTwo)
        resquery = cursor.fetchall()
        cursor.close()
        return resquery

    def getCustomerMostExpensiveBoughtProd(self,customerId):
        cursor = self.connection.cursor()
        # Get most expensive price customer has bought
        query = "select max(order_payment/num_items) as price_unit "
        query += "from \"Order\" as o, book_order as bor,book as b "
        query += "where o.order_id = bor.order_id and bor.book_id = b.book_id "
        query += "and user_id = " + str(customerId) + ";"
        cursor.execute(query)
        mostExpensivePrice = cursor.fetchone()[0]
        # Get Products that its price are equal to most expensive one
        queryTwo = "select title, order_payment/num_items as price_unit "
        queryTwo += "from \"Order\" as o, book_order as bor,book as b "
        queryTwo += "where o.order_id = bor.order_id and bor.book_id = b.book_id "
        queryTwo += "and user_id =" + str(customerId) + " and order_payment/num_items = " + str(mostExpensivePrice) + " "
        queryTwo += "group by title, order_payment/num_items;"
        cursor.execute(queryTwo)
        resquery = cursor.fetchall()
        cursor.close()
        return resquery
