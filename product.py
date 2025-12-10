class Product:
    def __init__(self, name, description, price, stock, category, offer, image=''): 
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.category = category
        self.offer = offer
        self.image = image

    def toDBCollection(self):
        return {
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock': self.stock,
            'category': self.category,
            'offer': self.offer,
            'image': self.image
        }
