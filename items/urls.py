# items/urls.py
from django.urls import path
from . import views

app_name = 'items'

urlpatterns = [
    path('', views.ItemListView.as_view(), name='item_list'),
    path('my-items/', views.my_items, name='my_items'),
    path('create/', views.ItemCreateView.as_view(), name='item_create'),
    path('<slug:slug>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('<slug:slug>/edit/', views.ItemUpdateView.as_view(), name='item_update'),
    path('<slug:slug>/delete/', views.ItemDeleteView.as_view(), name='item_delete'),
]