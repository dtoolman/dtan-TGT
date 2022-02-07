import os
import sys
import requests

from flask import g, Flask, request, redirect, render_template, url_for, jsonify, Blueprint, abort
from flask_pymongo import PyMongo
from flask_bootstrap import Bootstrap

from urllib.parse import urljoin, urlparse, quote_plus, unquote_plus

# initialize flask_wtf
from flask_wtf import FlaskForm

# initialize flask_nav
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup

# # initialize Redis
# from redis import ConnectionPool, Redis

# relative module pathing
sys.path.append("..")
# from lib.Utils import *
# from lib.Jira import *
# from lib.Grafana import *

# init Flask app
app = Flask(__name__, template_folder="templates")

# init PyMongo app
app.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']
mongo = PyMongo(app)
db = mongo.db

# init Bootstrap
Bootstrap(app)


@app.route('/')
def index():
    # return render_template('index.html')

    return jsonify(
        status=True,
        payload='Welcome to the Flask MongoDB app!'
    )

# @app.route('/products/', methods=['GET'])
@app.route('/products/<prodid>', methods=['GET', 'PUT'])
def products_get(prodid):

    # _products = db.products.find()

    item = {}
    data = []

    if request.method == 'GET':

        # _products = db.products.find({"id": prodid})
        _products = db.products.find_one({"id": prodid})

        # print(str(prodid))
        # print(_products)

        # for product in _products:
        #     item = {
        #         # "_id": product['_id'],
        #         "id": product['id'],
        #         "name": product['name'],
        #         "current_price": product['current_price'],
        #         "currency_code": product['currency_code']
        #     }
        #     data.append(item)

        item = {
            # "_id": product['_id'], # ObjectId code unicode FYI
            "id": _products['id'],
            "name": _products['name'],
            "current_price": _products['current_price'],
            "currency_code": _products['currency_code']
        }
        data.append(item)

    elif request.method == 'PUT':

        data = request.get_json(force=True)

        # _products = db.products.find_one_and_update({"id":prodid}, { '$set': { "Branch" : 'CSE'} }. return_document = ReturnDocument.AFTER)
        _products = db.products.find_one_and_update({"id": prodid}, {'$set': data})

        # item = {
        #     # "_id": product['_id'], # ObjectId code unicode FYI
        #     "id": _products['id'],
        #     "name": _products['name'],
        #     "current_price": _products['current_price'],
        #     "currency_code": _products['currency_code']
        # }
        # data.append(item)

    return jsonify(
        status=True,
        payload=data
    )


@app.route('/productspost', methods=['POST'])
def createProduct():
    data = request.get_json(force=True)
    item = {
        "id": data['id'],
        "name": data['name'],
        "current_price": data['current_price']['value'],
        "currency_code": data['current_price']['currency_code']
    }
    db.products.insert_one(item)

    # loses old record fields, if same fields are not in the new record
    # db.products.replace_one(item)
    # can update specific fields, must be named
    # db.products.update_one(item)

    return jsonify(
        status=True,
        payload='Product saved successfully!'
    ), 201


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    app.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
