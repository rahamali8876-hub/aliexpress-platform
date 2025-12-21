class Product:
    def __init__(self, product_id, seller_id, title):
        self.id = product_id
        self.seller_id = seller_id
        self.title = title

    @classmethod
    def create(cls, product_id, seller_id, title):
        return cls(product_id, seller_id, title)
