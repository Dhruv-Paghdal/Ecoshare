# centers/urls.py
# Responsibility: Sakshi Patel

from django.urls import path
from . import views

app_name = 'centers'

urlpatterns = [
    path('', views.RecyclingCenterListView.as_view(), name='center_list'),
    path('search/', views.center_search, name='center_search'),
    path('<slug:slug>/', views.RecyclingCenterDetailView.as_view(), name='center_detail'),
]