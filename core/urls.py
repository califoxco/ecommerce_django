from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    #path('item/<int:pk>/', views.ItemDetailView.as_view(), name='item-detail'),
    path('item/<slug>/', views.ItemDetailView.as_view(), name='item-detail'),
    path('checkout/<slug>/', views.DetailView, name='checkout'),
    path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart'),
]