from app import db
from datetime import datetime

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f'<Category {self.name}>'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('products', lazy=True))
    vendor = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    # Define one-to-many relationship with Batch
    batches = db.relationship('Batch', backref='product', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Product {self.name}>'

    def update_stock(self):
        self.stock = sum(int(batch.quantity) for batch in self.batches)
        db.session.commit()

class Batch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    batch_number = db.Column(db.String(50), nullable=False, unique=True)  # Ensure uniqueness
    expiration_date = db.Column(db.Date, nullable=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Batch {self.batch_number} of {self.product.name}>'
