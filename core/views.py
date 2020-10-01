from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Item


def item_detail(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'detail.html', context)

def checkout(request):
    return render(request, 'checkout.html', {})

class HomeView(ListView):
    model = Item
    template_name = "home.html"

class ItemDetailView(DetailView):
    model = Item
    template_name = "detail.html"
