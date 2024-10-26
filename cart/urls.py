from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
  	path('', views.get, name='get'),
  	path('add/', views.add, name='add'),
  	path('update/', views.update, name='update'),
  	path('delete', views.delete, name='delete'),
]
