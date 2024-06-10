# import unittest
# from app import create_app, db
# from app.models.users import User, Company, Role
# from app.models.userlog import UserLog
# from app.models.inventory import Category, Product, Batch
# from datetime import datetime, timedelta
# import uuid

# class TestModels(unittest.TestCase):

#     @classmethod
#     def setUpClass(cls):
#         cls.app = create_app('config.TestConfig')
#         cls.app_context = cls.app.app_context()
#         cls.app_context.push()
#         db.create_all()

#     @classmethod
#     def tearDownClass(cls):
#         db.session.remove()
#         db.drop_all()
#         cls.app_context.pop()

#     def setUp(self):
#         self.client = self.app.test_client()
#         self.runner = self.app.test_cli_runner()

#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()
#         db.create_all()

#     def test_create_user(self):
#         user = User(email='test@example.com', password='password', fs_uniquifier=str(uuid.uuid4()), active=True)
#         db.session.add(user)
#         db.session.commit()
#         self.assertIsNotNone(user.id)

#     def test_get_user_by_email(self):
#         user = User(email='test@example.com', password='password', fs_uniquifier=str(uuid.uuid4()), active=True)
#         db.session.add(user)
#         db.session.commit()
#         fetched_user = User.query.filter_by(email='test@example.com').first()
#         self.assertIsNotNone(fetched_user)

#     def test_create_company(self):
#         company = Company(name='Test Company')
#         db.session.add(company)
#         db.session.commit()
#         self.assertIsNotNone(company.id)

#     def test_get_company_by_name(self):
#         company = Company(name='Test Company')
#         db.session.add(company)
#         db.session.commit()
#         fetched_company = Company.query.filter_by(name='Test Company').first()
#         self.assertIsNotNone(fetched_company)

#     def test_create_role(self):
#         role = Role(name='Admin', description='Administrator role')
#         db.session.add(role)
#         db.session.commit()
#         self.assertIsNotNone(role.id)

#     def test_get_role_by_name(self):
#         role = Role(name='Admin', description='Administrator role')
#         db.session.add(role)
#         db.session.commit()
#         fetched_role = Role.query.filter_by(name='Admin').first()
#         self.assertIsNotNone(fetched_role)

#     def test_create_user_log(self):
#         user = User(email='log_test@example.com', password='password', fs_uniquifier=str(uuid.uuid4()), active=True)
#         db.session.add(user)
#         db.session.commit()
#         user_log = UserLog(
#             user_id=user.id,
#             user_ip='127.0.0.1',
#             device_type='Desktop',
#             device_os='Linux',
#             browser_type='Chrome',
#             action='Logged in',
#             action_type='login',
#             description='User logged in successfully',
#             additional_data={'additional_info': 'Any additional data'}
#         )
#         db.session.add(user_log)
#         db.session.commit()
#         self.assertIsNotNone(user_log.id)

#     def test_get_user_log_by_action(self):
#         user = User(email='log_test@example.com', password='password', fs_uniquifier=str(uuid.uuid4()), active=True)
#         db.session.add(user)
#         db.session.commit()
#         user_log = UserLog(
#             user_id=user.id,
#             user_ip='127.0.0.1',
#             device_type='Desktop',
#             device_os='Linux',
#             browser_type='Chrome',
#             action='Logged in',
#             action_type='login',
#             description='User logged in successfully',
#             additional_data={'additional_info': 'Any additional data'}
#         )
#         db.session.add(user_log)
#         db.session.commit()
#         fetched_log = UserLog.query.filter_by(action='Logged in').first()
#         self.assertIsNotNone(fetched_log)

#     def test_create_category(self):
#         category = Category(name='Test Category')
#         db.session.add(category)
#         db.session.commit()
#         self.assertIsNotNone(category.id)

#     def test_get_category_by_name(self):
#         category = Category(name='Test Category')
#         db.session.add(category)
#         db.session.commit()
#         fetched_category = Category.query.filter_by(name='Test Category').first()
#         self.assertIsNotNone(fetched_category)

#     def test_create_product(self):
#         category = Category(name='Test Category')
#         company = Company(name='Test Company')
#         db.session.add(category)
#         db.session.add(company)
#         db.session.commit()
#         product = Product(name='Test Product', category_id=category.id, company_id=company.id, vendor='Vendor')
#         db.session.add(product)
#         db.session.commit()
#         self.assertIsNotNone(product.id)

#     def test_get_product_by_name(self):
#         category = Category(name='Test Category')
#         company = Company(name='Test Company')
#         db.session.add(category)
#         db.session.add(company)
#         db.session.commit()
#         product = Product(name='Test Product', category_id=category.id, company_id=company.id, vendor='Vendor')
#         db.session.add(product)
#         db.session.commit()
#         fetched_product = Product.query.filter_by(name='Test Product').first()
#         self.assertIsNotNone(fetched_product)

#     def test_create_batch(self):
#         category = Category(name='Test Category')
#         company = Company(name='Test Company')
#         db.session.add(category)
#         db.session.add(company)
#         db.session.commit()
#         product = Product(name='Test Product', category_id=category.id, company_id=company.id, vendor='Vendor')
#         db.session.add(product)
#         db.session.commit()
#         batch = Batch(product_id=product.id, batch_number='12345', quantity=100)
#         db.session.add(batch)
#         db.session.commit()
#         self.assertIsNotNone(batch.id)

#     def test_get_batch_by_batch_number(self):
#         category = Category(name='Test Category')
#         company = Company(name='Test Company')
#         db.session.add(category)
#         db.session.add(company)
#         db.session.commit()
#         product = Product(name='Test Product', category_id=category.id, company_id=company.id, vendor='Vendor')
#         db.session.add(product)
#         db.session.commit()
#         batch = Batch(product_id=product.id, batch_number='12345', quantity=100)
#         db.session.add(batch)
#         db.session.commit()
#         fetched_batch = Batch.query.filter_by(batch_number='12345').first()
#         self.assertIsNotNone(fetched_batch)

#     def test_update_stock(self):
#         category = Category(name='Test Category')
#         company = Company(name='Test Company')
#         db.session.add(category)
#         db.session.add(company)
#         db.session.commit()
#         product = Product(name='Test Product', category_id=category.id, company_id=company.id, vendor='Vendor')
#         db.session.add(product)
#         db.session.commit()
#         # Create mock batches with different quantities
#         batches = [
#             Batch(batch_number='12', product_id=product.id, quantity=10),
#             Batch(batch_number='23', product_id=product.id, quantity=20),
#             Batch(batch_number='55', product_id=product.id, quantity=5),
#         ]
#         db.session.add_all(batches)
#         db.session.commit()
#         # Update the stock
#         product.update_stock()
#         db.session.commit()
#         self.assertEqual(product.stock, 35)  # Sum of quantities from mock batches

#     def test_update_months_left_with_future_expiration_date(self):
#         category = Category(name='Test Category')
#         company = Company(name='Test Company')
#         db.session.add(category)
#         db.session.add(company)
#         db.session.commit()
#         product = Product(name='Test Product', category_id=category.id, company_id=company.id, vendor='Vendor')
#         db.session.add(product)
#         db.session.commit()
#         # Create a Batch with a future expiration date
#         future_date = datetime.today().date() + timedelta(days=30)
#         batch = Batch(product_id=product.id, batch_number='12345', expiration_date=future_date)
#         db.session.add(batch)
#         db.session.commit()
#         # Update months left
#         batch.update_months_left()
#         self.assertEqual(batch.months_left, 1)  # Expected 1 month left until expiration

#     def test_update_months_left_with_past_expiration_date(self):
#         category = Category(name='Test Category')
#         company = Company(name='Test Company')
#         db.session.add(category)
#         db.session.add(company)
#         db.session.commit()
#         product = Product(name='Test Product', category_id=category.id, company_id=company.id, vendor='Vendor')
#         db.session.add(product)
#         db.session.commit()
#         # Create a Batch with a past expiration date
#         past_date = datetime.today().date() - timedelta(days=30)
#         batch = Batch(product_id=product.id, batch_number='12345', expiration_date=past_date)
#         db.session.add(batch)
#         db.session.commit()
#         # Update months left
#         batch.update_months_left()
#         db.session.commit()
#         # If expiration date is in the past
#         self.assertEqual(batch.months_left, 0)
def test_sample(self):
    self.assertEqual(1+1+1, 3)