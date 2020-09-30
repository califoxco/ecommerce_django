from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('item/<slug>/', views.item_detail, name='item-detail'),
]