from django.urls import path
from . import views


urlpatterns = [
    # Ví dụ endpoint test tạm
    path('register/', views.test_api, name='test_api'),
    path('login/', views.test_api, name='test_api'),
]