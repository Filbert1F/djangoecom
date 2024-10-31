from django.contrib import admin
from .models import Category, Product, Order, Profile, OrderProduct
from django.contrib.auth.models import User
from django.utils.html import format_html

admin.site.register(Category)

class PriceFilter(admin.SimpleListFilter):
	title = 'Price Filter'
	parameter_name = 'price'

	def lookups(self, request, model_admin):
		return (
			("0-49", '$0-$49'),
			("50-99", '$50-$99'),
			(">=100", '$100 and over'),
		)

	def queryset(self, request, queryset):
		if self.value() == '0-49':
			return queryset.filter(price__range=(0, 49))
		if self.value() == '50-99':
			return queryset.filter(price__range=(50, 99))
		if self.value() == '>=100':
			return queryset.filter(price__gte=100)

class SalePriceFilter(admin.SimpleListFilter):
	title = 'Sale Price Filter'
	parameter_name = 'sale_price'

	def lookups(self, request, model_admin):
		return (
			("0-49", '$0-$49'),
			("50-99", '$50-$99'),
			(">=100", '$100 and over'),
		)

	def queryset(self, request, queryset):
		if self.value() == '0-49':
			return queryset.filter(sale_price__range=(0, 49))
		if self.value() == '50-99':
			return queryset.filter(sale_price__range=(50, 99))
		if self.value() == '>=100':
			return queryset.filter(sale_price__gte=100)

class ProductAdmin(admin.ModelAdmin):
	model = Order
	list_display = ['uuid', 'image_tag', 'name', 'price', 'category', 'is_sale', 'sale_price', 'created_at', 'updated_at']
	list_filter = [PriceFilter, 'category', 'is_sale', SalePriceFilter, 'created_at', 'updated_at']
	search_fields = ['uuid', 'name', 'category__name']
	fields = ['uuid', 'name', 'price', 'category', 'description', 'image', 'image_tag', 'is_sale', 'sale_price']
	readonly_fields = ['image_tag']
	
	def image_tag(self, obj):
		return format_html('<img src="{}" style="max-width:100px; max-height:100px"/>'.format(obj.image.url))

admin.site.register(Product, ProductAdmin)

class OrderProductInline(admin.TabularInline):
	model = OrderProduct
	extra = 0
	readonly_fields = ['product_uuid', 'name', 'price', 'category_id', 'category_name', 'description', 'image', 'image_tag', 'quantity']
	
	def image_tag(self, obj):
		return format_html('<img src="{}" style="max-width:100px; max-height:100px"/>'.format(obj.image.url))
	def has_add_permission(self, request, obj=None):
		return False
	def has_delete_permission(self, request, obj=None):
		return False
	
class OrderAdmin(admin.ModelAdmin):
	model = Order
	inlines = [OrderProductInline]
	list_display = ['uuid', 'user_email', 'total_price', 'status', 'created_at']
	list_filter = ['status', 'created_at']
	search_fields = ['uuid', 'user__email', 'address']
	readonly_fields = ['uuid', 'user', 'address', 'phone', 'total_price', 'created_at']

	def user_email(self, obj):
		return obj.user.email

admin.site.register(Order, OrderAdmin)

class ProfileInline(admin.StackedInline):
	model = Profile

class UserAdmin(admin.ModelAdmin):
	model = User
	list_display = ['username', 'profile_uuid', 'email', 'first_name', 'last_name', 'is_active', 'last_login']
	search_fields = ['username', 'profile__uuid', 'email', 'first_name', 'last_name']
	list_filter = ['is_active', 'last_login']
	inlines = [ProfileInline]

	def profile_uuid(self, obj):
		return obj.profile.uuid

admin.site.unregister(User)
admin.site.register(User, UserAdmin)