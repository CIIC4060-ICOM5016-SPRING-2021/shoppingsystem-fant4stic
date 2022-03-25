from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2

# Activate
app = Flask(__name__)

# Apply CORS to this app
CORS(app)

# Connect to server
connection = psycopg2.connect(user = "cphcapypqzssdm", password = "815b0599c4c49e37f0e62528386cf2e3e22eb4abe234d8b2c68e74c8c48e8838", host = "ec2-3-231-254-204.compute-1.amazonaws.com", port = "5432", database = "d7i8e69i0cdo3j")

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

if __name__ == '__main__':
    app.run()
