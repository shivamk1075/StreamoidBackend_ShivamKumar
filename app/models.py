from .database import db


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    brand = db.Column(db.String(120), nullable=False)
    color = db.Column(db.String(80))
    size = db.Column(db.String(80))
    mrp = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            "sku": self.sku,
            "name": self.name,
            "brand": self.brand,
            "color": self.color,
            "size": self.size,
            "mrp": self.mrp,
            "price": self.price,
            "quantity": self.quantity,
        }
