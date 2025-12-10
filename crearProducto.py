from flask import Blueprint, request, jsonify, redirect, url_for, current_app 
from product import Product
import database as dbase
import os
from werkzeug.utils import secure_filename

db = dbase.dbConnection()

crear_producto_bp = Blueprint('crear_producto_bp', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS2']

@crear_producto_bp.route('/products', methods=['POST'])
def addProduct():
    products = db['products']

    # Captura de datos del formulario
    name = request.form.get('name')
    description = request.form.get('description')
    price = request.form.get('price')
    stock = request.form.get('stock')
    category = request.form.get('category')
    offer = request.form.get('offer')

    # Conversión de tipos (si vienen como string)
    try:
        price = float(price) if price else 0.0
        stock = int(stock) if stock else 0
    except ValueError:
        return jsonify({'message': 'Precio o stock inválido'}), 400

    image = ''
    
    # Manejo de imagen
    if 'image' in request.files:
        file = request.files['image']
        
        if file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            # Guardar la imagen físicamente
            save_path = os.path.join(current_app.config['UPLOAD_FOLDER2'], filename)
            file.save(save_path)
            
            # Guardar SOLO el nombre de la imagen en la base de datos
            image = filename

    # Validación de datos
    if name and description and price and stock and category and offer:
        product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            category=category,
            offer=offer,
            image=image
        )
        products.insert_one(product.toDBCollection())

        return redirect(url_for('home'))
    
    return jsonify({'message': 'Datos incompletos'}), 400
