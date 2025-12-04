# filters.py
from flask import request

def build_filter_query():
    """
    Construye el diccionario de consulta de MongoDB a partir de los 
    parámetros de la URL.
    """
    
    # 1. Obtenemos los parámetros
    category = request.args.get('category')
    name_search = request.args.get('name')
    min_price_str = request.args.get('min_price')
    max_price_str = request.args.get('max_price')

    query = {}

    # 2. Aplicar Filtro por Categoría
    # Si la categoría no es None Y no es una cadena vacía (el valor de '-- Todas las Categorías --' es "")
    if category: 
        query['category'] = category

    # 3. Aplicar Búsqueda por Nombre (utilizando $regex)
    if name_search:
        # La 'i' hace la búsqueda insensible a mayúsculas/minúsculas
        query['name'] = {'$regex': name_search, '$options': 'i'}

    # 4. Aplicar Filtro por Rango de Precio
    price_range = {}
    
    # Manejo de precio mínimo
    if min_price_str:
        try:
            min_float = float(min_price_str)
            price_range['$gte'] = min_float
        except ValueError:
            pass 
    
    # Manejo de precio máximo
    if max_price_str:
        try:
            max_float = float(max_price_str)
            price_range['$lte'] = max_float
        except ValueError:
            pass 

    # 5. Si hay condiciones de precio, se añaden a la query principal
    if price_range:
        query['price'] = price_range

    # La query final puede ser {} si no hay filtros, o contener una combinación de ellos.
    return query