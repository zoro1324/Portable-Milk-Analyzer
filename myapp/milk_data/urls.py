from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.submission_dashboard, name='submission-dashboard'),
    path('supplier/<int:pk>/', views.supplier_detail, name='supplier-detail'),
]