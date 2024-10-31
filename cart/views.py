from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages
from .forms import PayForm
from store.models import OrderProduct
from django.db import transaction

def get(request):
	cart = Cart(request)
	cart_items = cart.get()

	if request.method == "POST":
		form = PayForm(data=request.POST, request=request)

		if not request.user.is_authenticated:
			messages.error(request, 'You have to be logged in to checkout')
			return render(request, "get.html", {'cart_items': cart_items, 'total': cart.get_total_price(), 'form': form}, status=401)
		
		if cart.__len__() == 0:
			messages.error(request, 'Empty cart')
			return render(request, "get.html", {'cart_items': cart_items, 'total': cart.get_total_price(), 'form': form}, status=422)
		
		if form.is_valid():
			with transaction.atomic():
				order = form.save()

				to_be_added = []
				for item in cart_items:
					to_be_added.append(
						OrderProduct(
							order=order,
							product_uuid=item['product'].uuid,
							name=item['product'].name,
							price=item['product'].price if not item['product'].is_sale else item['product'].sale_price,
							category_id=item['product'].category.id,
							category_name=item['product'].category.name,
							description=item['product'].description,
							image=item['product'].image,
							quantity=item['qty']
						)
					)
				OrderProduct.objects.bulk_create(to_be_added)
				cart.clear()
				return redirect('orders')
		return render(request, "get.html", {'cart_items': cart_items, 'total': cart.get_total_price(), 'form': form}, status=422)
	else:
		form = PayForm(request=request)
		
	return render(request, "get.html", {'cart_items': cart_items, 'total': cart.get_total_price(), 'form': form})

def add(request):
	cart = Cart(request)

	product_uuid = request.POST.get('product_uuid')
	qty = int(request.POST.get('qty'))
	if qty < 1:
		messages.error(request, 'quantity cannot be less than 1')
		return JsonResponse({'error': 'quantity cannot be less than 1'}, status=422)
	
	product = get_object_or_404(Product, uuid=product_uuid)

	cart.add(product=product, qty=qty)
	cart_qty = cart.__len__()

	messages.success(request, product.name + ' added to cart')

	return JsonResponse({'cart_qty': cart_qty})

def update(request):
	cart = Cart(request)

	product_uuid = request.POST.get('product_uuid')
	qty = int(request.POST.get('qty'))

	new_qty = cart.update(product_uuid=product_uuid, qty=qty)
	print(new_qty)

	return JsonResponse({'new_qty': new_qty})

def delete(request):
	cart = Cart(request)
	product_uuid = request.POST.get('product_uuid')
	cart.delete(product_uuid=product_uuid)

	return JsonResponse({'message': "delete successful"})