class Product:
   
    def __init__(self, name, description, price, stock, category, image_url=''): 
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.category = category
        self.image_url = image_url

    def toDBCollection(self):
        return{
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock': self.stock,
            'category': self.category,
            'image_url': self.image_url
        }