from flask import request
import re

def build_filter_query():
    """Construye el diccionario de consulta de MongoDB a partir de los parámetros de la URL."""
    
    # 1. Obtenemos los parámetros de búsqueda de la URL (request.args)
    category = request.args.get('category')
    name_search = request.args.get('name')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')

    query = {}

    # 2. Aplicar Filtro por Categoría (Revisa tu HTML para ver si usas el campo 'category')
    if category: 
        # Búsqueda insensible a mayúsculas/minúsculas y que coincida exactamente
        query['category'] = category

    # 3. Aplicar Búsqueda por Nombre (Utilizando regex para buscar el nombre parcial)
    if name_search:
        # La 'i' hace la búsqueda insensible a mayúsculas/minúsculas
        query['name'] = {'$regex': name_search, '$options': 'i'}

    # 4. Aplicar Filtro por Rango de Precio (CORRECCIÓN CRÍTICA)
    price_range = {}
    
    # Manejo de precio mínimo
    if min_price:
        try:
            min_float = float(min_price)
            if min_float >= 0:
                price_range['$gte'] = min_float
        except ValueError:
            pass # Ignorar si no es un número válido
    
    # Manejo de precio máximo
    if max_price:
        try:
            max_float = float(max_price)
            if max_float >= 0:
                price_range['$lte'] = max_float
        except ValueError:
            pass # Ignorar si no es un número válido

    # Si hay condiciones de precio, se añaden a la query principal
    if price_range:
        query['price'] = price_range

    return query