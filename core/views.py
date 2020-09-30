from django.shortcuts import render

def index(request):
    return render(request, 'home.html', {})

def item_detail(request):
    return render(request, 'detail.html', {})
