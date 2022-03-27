from flask import Flask, jsonify, request
from flask_cors import CORS
from databaseConnect import DatabaseConnect
from controller.inventory import InventoryController
import psycopg2

# Activate
app = Flask(__name__)

# Apply CORS to this app
CORS(app)

# Connect to server
connection = DatabaseConnect().getConnection()

# Object to operate the DB
cursor = connection.cursor()

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/fant4stic/book/get all')
def getAllBooks():
    cursor.execute("Select * from book")
    record = cursor.fetchall()
    return jsonify(record)

@app.route('/fant4stic/author/get all')
def getAllAuthors():
    cursor.execute("Select * from author")
    record = cursor.fetchall()
    return jsonify(record)

@app.route('/fant4stic/inventory/addproduct')
def inventoryAddBookProduct():
    return InventoryController().addBookProduct()

# Check if an element is inside a list of records or a single record
def member_of_Record(element, records):
    bool_const = False
    #Check if records is an array of tuples
    if(not(type(records) is tuple)):
        for record in records:
            if(element in record):
                bool_const = True
                break
    else:
        #records is a single tuple
        bool_const = element in records
    return bool_const

if __name__ == '__main__':
    app.run()
