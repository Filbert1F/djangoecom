from django.contrib import admin
from .models import Category, Product, Order, Profile, OrderProduct
from django.contrib.auth.models import User

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
	list_display = ['uuid', 'name', 'price', 'category', 'is_sale', 'sale_price', 'created_at', 'updated_at']
	list_filter = [PriceFilter, 'category', 'is_sale', SalePriceFilter, 'created_at', 'updated_at']
	search_fields = ['uuid', 'name', 'category__name']

	@admin.display()
	def user_email(self, obj):
		return obj.user.email

admin.site.register(Product, ProductAdmin)

class OrderProductInline(admin.TabularInline):
	model = OrderProduct
	extra = 1
class OrderAdmin(admin.ModelAdmin):
	model = Order
	inlines = [OrderProductInline]
	list_display = ['uuid', 'user_email', 'total_price', 'status', 'created_at']
	list_filter = ['status', 'created_at']
	search_fields = ['uuid', 'user__email', 'address']

	@admin.display()
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

	@admin.display()
	def profile_uuid(self, obj):
		return obj.profile.uuid

admin.site.unregister(User)
admin.site.register(User, UserAdmin)