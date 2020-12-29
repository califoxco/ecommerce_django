from django import template
from core.models import Order

register = template.Library()

@register.filter()
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        total_qty = 0
        if qs.exists():
            for order_item in qs[0].items.all():
                total_qty += order_item.quantity
    return total_qty
