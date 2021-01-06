from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    #path('item/<int:pk>/', views.ItemDetailView.as_view(), name='item-detail'),
    path('item/<slug>/', views.ItemDetailView.as_view(), name='item-detail'),
    path('checkout/<slug>/', views.DetailView, name='checkout'),
    path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart'),
    path('order-summary/', views.OrderSummaryView.as_view(), name='order-summary'),
    path('checkout', views.CheckoutView.as_view(), name='checkout'),
    path('payment', views.PaymentView.as_view(), name='payment'),
    # path('accept-checkout', views.accept_checkout, name='accept-checkout'),
]