from store.models import Product

class Cart():
	def __init__(self, request):
		self.session = request.session
		cart = self.session.get('session_key')

		if 'session_key' not in request.session:
			cart = self.session['session_key'] = {}

		self.cart = cart

	def clear(self):
		self.session['session_key'] = {}
		self.session.modified = True
	
	def add(self, product, qty):
		product_uuid = str(product.uuid)
		qty = str(qty)

		if product_uuid in self.cart:
			self.cart[product_uuid] += int(qty)
		else:
			self.cart[product_uuid] = int(qty)

		self.session.modified = True

	def __len__(self):
		product_uuids = self.cart.keys()
		count = Product.objects.filter(uuid__in=product_uuids).count()
		return count
	
	def get(self):
		product_uuids = self.cart.keys()
		products = Product.objects.filter(uuid__in=product_uuids)

		cart_items = []
		for product in products:
			cart_items.append({
				'product': product,
				'qty': self.cart[str(product.uuid)],
				'total': (product.sale_price if product.is_sale else product.price) * self.cart[str(product.uuid)]
			})
		return cart_items
	
	def update(self, product_uuid, qty):
		if str(product_uuid) in self.cart:
			self.cart[str(product_uuid)] = int(qty)
			self.session.modified = True

		return int(qty)
	
	def delete(self, product_uuid):
		if str(product_uuid) in self.cart:
			del self.cart[str(product_uuid)]
			self.session.modified = True

	def get_total_price(self):
		product_uuids = self.cart.keys()
		products = Product.objects.filter(uuid__in=product_uuids)
		
		return sum(
			(product.sale_price if product.is_sale else product.price) * self.cart[str(product.uuid)]
			for product in products
		)