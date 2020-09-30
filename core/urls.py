from django.urls import path
from . import views

urlpatterns = [
    path('', views.item_detail, name='item_detail'),
]