from django.contrib import admin
from django.urls import path
from . import views

app_name = 'milk_data'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('supplier/<int:pk>/', views.supplier_detail, name='supplier_detail'),
    path('cow/<int:pk>/', views.cow_detail, name='cow_detail'),
]   