import psycopg2
#Class to connect to a PostgreSQL database
class DatabaseConnect:
    def __init__(self):
        try:
            self.connection =  psycopg2.connect(user="cphcapypqzssdm",
                                          password="815b0599c4c49e37f0e62528386cf2e3e22eb4abe234d8b2c68e74c8c48e8838",
                                          host="ec2-3-231-254-204.compute-1.amazonaws.com", port="5432",
                                          database="d7i8e69i0cdo3j")
            self.cursor = self.connection.cursor()
        except:
            print('DatabaseConnect Error: error connecting to the database.')

    def getConnection(self):
        return self.connection

    def getCursor(self):
        return self.cursor
