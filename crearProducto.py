from flask import Blueprint, request, jsonify, redirect, url_for, current_app 
from product import Product
import database as dbase
import os
from werkzeug.utils import secure_filename

db = dbase.dbConnection()

crear_producto_bp = Blueprint('crear_producto_bp', __name__)

# Función para verificar extensiones permitidas
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS2']

@crear_producto_bp.route('/products', methods=['POST'])
def addProduct():
    products = db['products']
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    stock = request.form['stock']
    category = request.form['category']

    image_url = ''
    
    # Manejo de imagen
    if 'image' in request.files:
        file = request.files['image']
        
        # Validación de la subida
        if file.filename != '' and allowed_file(file.filename):
            
            filename = secure_filename(file.filename)
            
           #guardar la imagen en la carpeta configurada
            save_path = os.path.join(current_app.config['UPLOAD_FOLDER2'], filename)
            file.save(save_path)
            
           #guarda la ruta relativa para la base de datos
            image_url = os.path.join(current_app.config['UPLOAD_FOLDER2'], filename).replace('\\', '/')


    if name and description and price and stock and category:
        # Pasar imagen_url como nuevo parámetro 
        product = Product(name, description, price, stock, category, image_url)
        products.insert_one(product.toDBCollection())

        return redirect(url_for('home'))
    else:
        response = jsonify({'message': 'Datos incompletos'})
        response.status_code = 400
        return response