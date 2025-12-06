from pymongo import MongoClient


MONGO_URI ="mongodb+srv://mauriciousseglio:mi_clave_123@clusterlast.4ip2mv0.mongodb.net/?appName=ClusterLast"

MONGO_URI = 'mongodb://localhost:27017/'


def dbConnection():
    try:
        client = MongoClient(MONGO_URI)
        db = client["dbb_products_app"]
        return db
    except Exception as e:
        print("Error de conexión con la bdd:", e)
        return None
    