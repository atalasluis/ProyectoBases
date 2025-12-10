class Product:
    def __init__(self, name, description, price, stock, category, offer=0, image=''): 
        self.name = name
        self.description = description
        self.price = float(price)
        self.stock = int(stock)
        self.category = category
        self.offer = float(offer)
        self.image = image

    def toDBCollection(self):
        return {
            'name': self.name,
            'description': self.description,
            'price': self.price,       # precio final ya con descuento
            'stock': self.stock,
            'category': self.category,
            'offer': self.offer,       # cuánto se descontó
            'image': self.image
        }
