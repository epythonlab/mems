# tests/test_models.py

import unittest
from app import create_app, db
from app.models.users import Company, User
from app.models.userlog import UserLog
from app.models.inventory import Category, Product, Batch
from datetime import datetime
import uuid

class TestCompanyModel(unittest.TestCase):
    def setUp(self):
        self.app = create_app('config.TestConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_company_creation(self):
        company = Company(name='Test Company')
        db.session.add(company)
        db.session.commit()

        self.assertIsNotNone(company.id)
        self.assertEqual(company.name, 'Test Company')

class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.app = create_app('config.TestConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation(self):
        user = User(first_name='John', last_name='Doe', email='john@example.com', active=True, fs_uniquifier=str(uuid.uuid4()))
        user.set_password('password')
        db.session.add(user)
        db.session.commit()

        self.assertIsNotNone(user.id)
        self.assertEqual(user.first_name, 'John')
        self.assertTrue(user.check_password('password'))
        
class TestUserLogModel(unittest.TestCase):
    def setUp(self):
        self.app = create_app('config.TestConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_log_creation(self):
        # Create a UserLog entry
        user_log = UserLog(
            user_id=1,
            user_ip='192.168.1.1',
            device_type='Desktop',
            device_os='Windows',
            browser_type='Chrome',
            action='Logged in',
            action_type='login',
            description='User logged in successfully',
            additional_data={'additional_info': 'Any additional data'}
        )
        db.session.add(user_log)
        db.session.commit()

        # Retrieve the UserLog entry from the database
        retrieved_log = UserLog.query.first()

        # Check if the attributes match
        self.assertEqual(retrieved_log.user_id, 1)
        self.assertEqual(retrieved_log.user_ip, '192.168.1.1')
        self.assertEqual(retrieved_log.device_type, 'Desktop')
        self.assertEqual(retrieved_log.device_os, 'Windows')
        self.assertEqual(retrieved_log.browser_type, 'Chrome')
        self.assertEqual(retrieved_log.action, 'Logged in')
        self.assertEqual(retrieved_log.action_type, 'login')
        self.assertEqual(retrieved_log.description, 'User logged in successfully')
        self.assertEqual(retrieved_log.additional_data, {'additional_info': 'Any additional data'})
        self.assertIsInstance(retrieved_log.timestamp, datetime)
        
class TestInventoryModels(unittest.TestCase):
    def setUp(self):
        self.app = create_app('config.TestConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_category_creation(self):
        category = Category(name='Test Category')
        db.session.add(category)
        db.session.commit()
        self.assertEqual(Category.query.count(), 1)
        self.assertEqual(Category.query.first().name, 'Test Category')

    def test_product_creation(self):
        category = Category(name='Test Category')
        db.session.add(category)
        db.session.commit()

        product = Product(name='Test Product', category_id=category.id, company_id=1, vendor='Test Vendor')
        db.session.add(product)
        db.session.commit()
        self.assertEqual(Product.query.count(), 1)
        self.assertEqual(Product.query.first().name, 'Test Product')

    def test_batch_creation(self):
        category = Category(name='Test Category')
        db.session.add(category)
        db.session.commit()

        product = Product(name='Test Product', category_id=category.id, company_id=1, vendor='Test Vendor')
        db.session.add(product)
        db.session.commit()

        batch = Batch(batch_number='123', product_id=product.id, expiration_date=datetime.now().date(), quantity=10)
        db.session.add(batch)
        db.session.commit()
        self.assertEqual(Batch.query.count(), 1)
        self.assertEqual(Batch.query.first().quantity, 10)

    def test_update_stock(self):
        category = Category(name='Test Category')
        db.session.add(category)
        db.session.commit()

        product = Product(name='Test Product', category_id=category.id, company_id=1, vendor='Test Vendor')
        db.session.add(product)
        db.session.commit()

        batch = Batch(batch_number='123', product_id=product.id, expiration_date=datetime.now().date(), quantity=10)
        db.session.add(batch)
        db.session.commit()

        product.update_stock()
        self.assertEqual(product.stock, 10)
   
if __name__ == '__main__':
    unittest.main()
