from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('products', views.ProductView.as_view(), name='products_page'),
    path('products/export', views.ProductView.as_view(), name='export_page'),
]