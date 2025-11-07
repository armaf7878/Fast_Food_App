from django.urls import path
from . import views
urlpatterns= [
    path('showall/', views.showall, name="restaurantShowall"),
    path('create/', views.create, name="restaurantCreate"),
    path('update/<str:restaurant_id>/', views.update, name="restaurantUpdate"),
    path('delete/<str:restaurant_id>/', views.delete, name="restaurantDelete")
]