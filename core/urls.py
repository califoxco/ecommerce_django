from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('item/<slug>/', views.ItemDetailView.as_view(), name='item'),
    path('checkout/<slug>/', views.DetailView, name='checkout'),
]