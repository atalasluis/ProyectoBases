from flask import Blueprint, request, jsonify, redirect, url_for
from product import Product
import database as dbase

db = dbase.dbConnection()

crear_producto_bp = Blueprint('crear_producto_bp', __name__)

@crear_producto_bp.route('/products', methods=['POST'])
def addProduct():
    products = db['products']
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    stock = request.form['stock']
    category = request.form['category']

    if name and description and price and stock and category:
        product = Product(name, description, price, stock, category)
        products.insert_one(product.toDBCollection())

        return redirect(url_for('home'))
    else:
        response = jsonify({'message': 'Datos incompletos'})
        response.status_code = 400
        return response
