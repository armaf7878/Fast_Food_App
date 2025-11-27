from django.urls import path
from . import views

urlpatterns = [
    path('pending/', views.pending, name='pendingOrder'),
    path('create/', views.create, name='createOrder'),
    path('assign-staff/<str:order_id>/', views.assign_staff, name='assignOrder'),
    path('ready/<str:order_id>/', views.ready, name='readyOrder'),
    path('waiting-deliver/', views.waiting_Deliver, name='waiting-deliveryOrder'),
    path('finish/<str:order_id>/', views.finish_order, name='finishOrder'),
]