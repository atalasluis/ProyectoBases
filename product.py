class Product:
    def __init__(self, name, price, description, stock, category):
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.category = category

    def toDBCollection(self):
        return{
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock': self.stock,
            'category': self.category,
        }