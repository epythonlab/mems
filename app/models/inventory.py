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
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
     
    vendor = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    # Define one-to-many relationship with Batch
    batches = db.relationship('Batch', backref='product', lazy=True, cascade="all, delete-orphan")
   # Define one-to-many relationship with category
    category = db.relationship('Category', backref=db.backref('products', lazy=True))
    # Define one-to-many relationship with company
    company = db.relationship('Company', backref=db.backref('products', lazy=True))
    
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
    created_at = db.Column(db.DateTime )
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    months_left = db.Column(db.Float, nullable=False, default=0)

    def update_months_left(self):
        if self.expiration_date is not None:
            # Ensure self.expiration_date is a datetime object
            if isinstance(self.expiration_date, str):
                self.expiration_date = datetime.strptime(self.expiration_date, '%Y-%m-%d').date()
            
            # Calculate the difference in months
            today = datetime.today().date()
            months_left = (self.expiration_date.year - today.year) * 12 + self.expiration_date.month - today.month
            
            self.months_left = months_left
        else:
            # If expiration_date is None, set months_left to 0
            self.months_left = 0
            
        db.session.commit()
            

    def __repr__(self):
        return f'<Batch {self.batch_number} of {self.product.name}>'