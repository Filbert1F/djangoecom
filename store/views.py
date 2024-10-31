from django.shortcuts import render, redirect
from .models import Product, Category, Profile, Order, OrderProduct
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, LoginForm, UpdateUserForm, UpdatePasswordForm, UpdateProfileForm
from django.db.models import Case, When, F, Count
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def login_user(request):
	if request.method == "POST":
		form = LoginForm(data=request.POST)
		if form.is_valid():
			username = form.cleaned_data["username"]
			password = form.cleaned_data["password"]
			user = authenticate(request, username=username, password=password)
			if user:
				login(request, user)
				messages.success(request, 'Logged in')
				return redirect('home')
			else:
				messages.error(request, 'Invalid username or password.', status=422)
		else:
			messages.error(request, 'Invalid username or password.', status=422)
	else:
		form = LoginForm()
		
	return render(request, 'login.html', {'form': form})

def logout_user(request):
	logout(request)
	messages.success(request, 'Logged out')
	return redirect('home')

def register_user(request):
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data["username"]
			password = form.cleaned_data["password1"]
			user = authenticate(request, username=username, password=password)
			login(request, user)
			messages.success(request, 'Registered and logged in')
			return redirect('home')
		else:
			return render(request, 'register.html', {'form': form}, status=422)
	else:
		form = SignUpForm()
		
	return render(request, 'register.html', {'form': form})

@login_required
def update_user(request):
	if request.user.is_authenticated:
		curr_user = User.objects.get(id=request.user.id)
		user_form = UpdateUserForm(request.POST or None, instance=curr_user)

		curr_profile = Profile.objects.get(user__id=request.user.id)
		profile_form = UpdateProfileForm(request.POST or None, instance=curr_profile)

		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, 'User updated')
			return redirect('home')
		
		return render(request, 'update_user.html', {'user_form': user_form, 'profile_form': profile_form}, status=422)
	
	else:
		return redirect('home')
	
@login_required
def update_password(request):
	if request.user.is_authenticated:
		curr_user = User.objects.get(id=request.user.id)
		if request.method == 'POST':
			form = UpdatePasswordForm(curr_user, request.POST)
			if form.is_valid():
				form.save()
				login(request, curr_user)
				messages.success(request, 'Password updated')
				return redirect('update_user')
			return render(request, 'update_password.html', {'form': form}, status=422)
		else:
			form = UpdatePasswordForm(curr_user)
			return render(request, 'update_password.html', {'form': form})
	
	else:
		return redirect('home')



def home(request):
	products = Product.objects.all()
	categories = Category.objects.all()

	category_name = request.GET.get('category_name')
	if category_name:
		try:
			category = Category.objects.get(name=category_name)
			products = products.filter(category=category)
		except:
			messages.error(request, 'Category does not exist')
			return redirect('home')

	search = request.GET.get('search')
	if search:
		products = products.filter(name__icontains=search)

	sort_by = request.GET.get('sort_by')
	if sort_by:
		if sort_by == 'newest':
			products = products.order_by('-created_at')
		elif sort_by == 'low-to-high':
			products = products.annotate(
				effective_price=Case(
					When(is_sale=True, then=F('sale_price')),
					default=F('price'),
				)
			).order_by('effective_price')
		elif sort_by == 'high-to-low':
			products = products.annotate(
				effective_price=Case(
					When(is_sale=True, then=F('sale_price')),
					default=F('price'),
				)
			).order_by('-effective_price')

	is_sale = request.GET.get('is_sale')
	if is_sale and is_sale == '1':
		products = products.filter(is_sale=True)

	return render(request, 'home.html', {'products': products, 'categories': categories})

def product(request, uuid):
	product = Product.objects.get(uuid=uuid)
	return render(request, 'product.html', {'product': product})

def categories(request):
	categories = Category.objects.annotate(
		product_count = Count('product')
	).all()

	sort_by = request.GET.get('sort_by')
	if sort_by:
		if sort_by == 'a-z':
			categories = categories.order_by('name')
		elif sort_by == 'z-a':
			categories = categories.order_by('-name')
		elif sort_by == 'most-items':
			categories = categories.order_by('-product_count')

	return render(request, 'categories.html', {'categories': categories})

@login_required
def orders(request):
	orders = Order.objects.filter(user=request.user).order_by('-created_at')

	return render(request, "orders.html", {"orders": orders})
