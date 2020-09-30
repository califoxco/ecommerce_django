from django.shortcuts import render
from .models import Item


def index(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'home.html', context)

def item_detail(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'detail.html', context)
