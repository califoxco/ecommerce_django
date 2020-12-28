from django.contrib import admin
from .models import  Item, OrderItem, Order



class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'ordered_date')

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)