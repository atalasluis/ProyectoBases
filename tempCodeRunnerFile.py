from flask import Flask, render_template, request, Response, jsonify, redirect, url_for
import database as dbase  
from product import Product

db = dbase.dbConnection()

app = Flask(__name__)

#Rutas de la aplicación
@app.route('/')
def home():
    products = db['products']
    productsReceived = products.find()
    return render_template('index.html', products = productsReceived)



#Method Post
@app.route('/products', methods=['POST'])
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
        response = jsonify({
            'name' : name,
            'description' : description,
            'price' : price,
            'stock' : stock,
            'category' : category
        })
        return redirect(url_for('home'))
    else:
        return notFound()

#Method delete
@app.route('/delete/<string:product_name>')
def delete(product_name):
    products = db['products']
    products.delete_one({'name' : product_name})
    return redirect(url_for('home'))

#Method Put
@app.route('/edit/<string:product_name>', methods=['POST'])
def edit(product_name):
    products = db['products']
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    stock = request.form['stock']
    category = request.form['category']

    if name and description and price and stock and category:
        products.update_one({'name' : product_name}, {'$set' : {'name' : name, 'description' : description, 'price' : price, 'stock' : stock,  'category' : category}})
        response = jsonify({'message' : 'Producto ' + product_name + ' actualizado correctamente'})
        return redirect(url_for('home'))
    else:
        return notFound()

@app.errorhandler(404)
def notFound(error=None):
    message ={
        'message': 'No encontrado ' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response

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
    # 1. Obtenemos los parámetros de búsqueda de la URL (request.args)
    category = request.args.get('category')
    name_search = request.args.get('name')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')

    # 2. Inicializamos el diccionario de la query de MongoDB
    query = {}

    # 3. Aplicar Filtro por Categoría
    if category:
        # Usa $regex para una coincidencia flexible (opcional, podrías usar category.lower() si quieres coincidencia exacta)
        # La 'i' hace que la búsqueda sea insensible a mayúsculas/minúsculas
        query['category'] = {'$regex': category, '$options': 'i'}

    # 4. Aplicar Búsqueda por Nombre
    if name_search:
        # Busca el nombre en cualquier parte del campo 'name'
        query['name'] = {'$regex': name_search, '$options': 'i'}

    # 5. Aplicar Filtro por Rango de Precio
    price_range = {}
    
    if min_price and min_price.replace('.', '', 1).isdigit():
        # Convierte a float y usa el operador $gte (mayor o igual que)
        price_range['$gte'] = float(min_price)
    
    if max_price and max_price.replace('.', '', 1).isdigit():
        # Convierte a float y usa el operador $lte (menor o igual que)
        price_range['$lte'] = float(max_price)

    # Si se definió un rango de precio (min o max), lo agregamos a la query
    if price_range:
        query['price'] = price_range

    # 6. Ejecutar la consulta con todos los filtros combinados
    productsReceived = products.find(query)

    # 7. Renderizar la plantilla, pasando los resultados
    return render_template('filtrosbusqueda.html', products = productsReceived)


#-------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=4000)