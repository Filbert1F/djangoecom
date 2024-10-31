from django.db import models
import uuid
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Category(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name
	
	class Meta:
		verbose_name_plural = 'categories'

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	uuid = models.UUIDField(default=uuid.uuid4, unique=True)
	phone = models.CharField(max_length=13, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.user.username
	
def create_profile(sender, instance, created, **kwargs):
	if created:
		user_profile = Profile(user=instance)
		user_profile.save()

post_save.connect(create_profile, sender=User)



class Product(models.Model):
	id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
	uuid = models.UUIDField(default=uuid.uuid4, unique=True)
	name = models.CharField(max_length=100)
	price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
	description = models.TextField(default='', blank=True, null=True)
	image = models.ImageField(upload_to='uploads/product/')
	is_sale = models.BooleanField(default=False)
	sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

class Order(models.Model):
	id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
	uuid = models.UUIDField(default=uuid.uuid4, unique=True)

	user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
	address = models.CharField(max_length=255, default='', blank=True)
	phone = models.CharField(max_length=13, default='', blank=True)
	total_price = models.DecimalField(decimal_places=2, max_digits=6, default=0)
	STATUS_CHOICES = (
    	("IN DELIVERY", 'In delivery'),
    	("DONE", 'Done'),
    )
	status = models.CharField(max_length=11, default="IN DELIVERY", choices=STATUS_CHOICES)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.uuid)
	
class OrderProduct(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	product_uuid = models.UUIDField(blank=False)

	name = models.CharField(max_length=100)
	price = models.DecimalField(decimal_places=2, max_digits=6)

	category_id = models.PositiveBigIntegerField(blank=False)
	category_name = models.CharField(max_length=100)

	description = models.TextField(default='', blank=True, null=True)
	image = models.ImageField(upload_to='uploads/order_product/')
	quantity = models.PositiveIntegerField(blank=False)

	def __str__(self):
		return self.name