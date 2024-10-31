from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_password/', views.update_password, name='update_password'),

    path('product/<uuid:uuid>', views.product, name='product'),
    path('categories/', views.categories, name='categories'),

    path('orders/', views.orders, name='orders')
]
