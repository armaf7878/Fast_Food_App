from django.urls import path
from . import views


urlpatterns = [
    # Ví dụ endpoint test tạm
    path('test/', views.test_api, name='test_api'),
]