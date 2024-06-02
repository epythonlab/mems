from app import db

"""Inventory model class"""

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    items = db.relationship('InventoryItem', backref='category', lazy=True)

class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    expiration_date = db.Column(db.String(10), nullable=True)
    batch_number = db.Column(db.String(50), nullable=True)
    lot_number = db.Column(db.String(50), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)