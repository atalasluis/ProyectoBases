from flask import Blueprint, redirect, url_for
import database as dbase

products = dbase.dbConnection()['products']

eliminar_producto_bp = Blueprint('eliminar_producto_bp', __name__)

@eliminar_producto_bp.route('/delete/<string:product_name>')
def delete(product_name):
    products.delete_one({'name': product_name})
    return redirect(url_for('listar'))
