# tips/urls.py
# Responsibility: Dhruv Patel & Dharmik Patel

from django.urls import path
from . import views

app_name = 'tips'

urlpatterns = [
    path('', views.TipListView.as_view(), name='tip_list'),
    path('my-tips/', views.my_tips, name='my_tips'),
    path('favorites/', views.favorite_tips, name='favorite_tips'),
    path('clear-history/', views.clear_tip_history, name='clear_history'),
    path('create/', views.TipCreateView.as_view(), name='tip_create'),
    path('<slug:slug>/', views.TipDetailView.as_view(), name='tip_detail'),
    path('<slug:slug>/edit/', views.TipUpdateView.as_view(), name='tip_update'),
    path('<slug:slug>/delete/', views.TipDeleteView.as_view(), name='tip_delete'),
    path('<slug:slug>/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
]