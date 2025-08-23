from django.contrib import admin
from django.urls import path
from . import views

app_name = 'milk_data'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('supplier/<int:pk>/', views.supplier_detail, name='supplier_detail'),
    path('cow/<int:pk>/', views.cow_detail, name='cow_detail'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('add_supplier',views.add_supplier, name='add_supplier'),
    path('api/classify_milk/', views.classify_milk, name='classify_milk'),
    path("suppliers/", views.suppliers_page, name="supplier_page"),
    ]   