from flask import Flask, render_template, request, Response, jsonify, redirect, url_for
import database as dbase  
from product import Product
from crearProducto import crear_producto_bp
from editarProducto import editar_producto_bp
from eliminarProducto import eliminar_producto_bp
import filters
import os


db = dbase.dbConnection()

app = Flask(__name__)

#Creacion de imagen folder si no existe
UPLOAD_FOLDER2 = 'static/uploads'
ALLOWED_EXTENSIONS2 = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER2'] = UPLOAD_FOLDER2
app.config['ALLOWED_EXTENSIONS2'] = ALLOWED_EXTENSIONS2
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB

#asegurar que la carpeta de imagenes exista
if not os.path.exists(UPLOAD_FOLDER2):
    os.makedirs(UPLOAD_FOLDER2)



# metodo post
app.register_blueprint(crear_producto_bp)
app.register_blueprint(editar_producto_bp, url_prefix='/productos')
app.register_blueprint(eliminar_producto_bp, url_prefix='/productos')

#Rutas de la aplicación
@app.route('/')
def home():
    products = db['products']
    productsReceived = products.find()
    return render_template('index.html', products = productsReceived)


# otras rutas de la aplicacion
#----------------------------------
@app.route('/listar')
def listar():
    products = db['products']
    productsReceived = products.find()
    return render_template('listar.html', products = productsReceived)

@app.route('/filtrosbusqueda')
def filtrosbusqueda():
    products = db['products']
    query = filters.build_filter_query() # Llama a la lógica corregida
    all_categories = products.distinct("category")
    productsReceived = list(products.find(query)) 
    return render_template(
        'filtrosbusqueda.html',
        products=productsReceived,
        categories=all_categories
        )



#-------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=4000)