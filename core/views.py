from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Item


"""
    The code below is already implemented automatically by django
"""
# def item_detail(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, 'item_detail.html', context)

def checkout(request):
    return render(request, 'checkout.html', {})

class HomeView(ListView):
    model = Item
    template_name = "home.html"
    # setting ordering to newest to oldest
    ordering = ['-listed_date']

class ItemDetailView(DetailView):
    model = Item
    # template_name = "item_detail.html"
