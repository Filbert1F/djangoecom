from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal
from .models import Category, Profile, Product, Order, OrderProduct
import uuid

class UserJourneyTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.category = Category.objects.create(name="Electronics")
        self.image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',
            content_type='image/jpeg'
        )
        self.product = Product.objects.create(
            name="Test Laptop",
            price=Decimal('999.99'),
            category=self.category,
            description="Amazing test laptop",
            image=self.image,
            is_sale=True,
            sale_price=Decimal('899.99')
        )
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }

    def test_complete_user_journey(self):
        response = self.client.post('/register/', self.user_data)
        self.assertEqual(response.status_code, 302)
        
        user = User.objects.get(username=self.user_data['username'])
        self.assertTrue(user)
        self.assertTrue(Profile.objects.filter(user=user).exists())
        
        login_successful = self.client.login(
            username=self.user_data['username'],
            password=self.user_data['password1']
        )
        self.assertTrue(login_successful)
        
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Laptop")
        
        response = self.client.get('/product/'+str(self.product.uuid))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Laptop")
        self.assertContains(response, "899.99")
        
        cart_data = {
            'product_uuid': str(self.product.uuid),
            'qty': 1
        }
        response = self.client.post('/cart/add/', cart_data)
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Laptop")
        self.assertContains(response, "899.99")
        
        checkout_data = {
            'address': '123 Test Street',
            'phone': '012345678900'
        }
        response = self.client.post('/cart/', checkout_data)
        self.assertEqual(response.status_code, 302)
        
        order = Order.objects.filter(user=user).latest('created_at')
        self.assertTrue(order)
        self.assertEqual(order.total_price, Decimal('899.99'))
        self.assertEqual(order.status, "IN DELIVERY")
        self.assertEqual(order.address, '123 Test Street')
        
        order_product = OrderProduct.objects.get(order=order)
        self.assertEqual(order_product.name, "Test Laptop")
        self.assertEqual(order_product.price, Decimal('899.99'))
        self.assertEqual(order_product.quantity, 1)
        
        response = self.client.get('/orders/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(order.uuid))

    def test_order_with_multiple_products(self):
        product2 = Product.objects.create(
            name="Test Mouse",
            price=Decimal('49.99'),
            category=self.category,
            description="Gaming mouse",
            image=self.image,
            is_sale=False
        )
        
        self.client.post('/register/', self.user_data)
        self.client.login(
            username=self.user_data['username'],
            password=self.user_data['password1']
        )
        
        self.client.post('/cart/add/', {
            'product_uuid': str(self.product.uuid),
            'qty': 1
        })
        self.client.post('/cart/add/', {
            'product_uuid': str(product2.uuid),
            'qty': 2
        })
        
        response = self.client.post('/cart/', {
            'address': '123 Test Street',
            'phone': '012345678900'
        })
        self.assertEqual(response.status_code, 302)
        
        user = User.objects.get(username=self.user_data['username'])
        order = Order.objects.filter(user=user).latest('created_at')
        self.assertEqual(
            order.total_price,
            Decimal('899.99') + (Decimal('49.99') * 2)
        )
        
        order_products = OrderProduct.objects.filter(order=order)
        self.assertEqual(order_products.count(), 2)
        self.assertTrue(
            order_products.filter(name="Test Mouse", quantity=2).exists()
        )

    def test_invalid_order_scenarios(self):
        self.client.post('/register/', self.user_data)
        self.client.login(
            username=self.user_data['username'],
            password=self.user_data['password1']
        )
        
        response = self.client.post('/cart/', {
            'address': '123 Test Street',
            'phone': '012345678900'
        })
        self.assertEqual(response.status_code, 422)
        
        response = self.client.post('/cart/add/', {
            'product_uuid': str(uuid.uuid4()),
            'qty': 1
        })
        self.assertEqual(response.status_code, 404)
        
        response = self.client.post('/cart/add/', {
            'product_uuid': str(self.product.uuid),
            'qty': -1
        })
        self.assertEqual(response.status_code, 422)
        
        self.client.post('/cart/add/', {
            'product_uuid': str(self.product.uuid),
            'qty': 1
        })
        response = self.client.post('/cart/', {
            'phone': '012345678900'
        })
        self.assertEqual(response.status_code, 422)