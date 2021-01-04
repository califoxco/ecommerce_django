from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from .models import Item, OrderItem, Order
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckoutForm

from lazysignup.decorators import allow_lazy_user

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


class OrderSummaryView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        order = OrderItem.objects.filter(user=self.request.user, ordered=False)
        if order:
            context = {
                'object': order
            }
            print(order.first().quantity)
            return render(self.request, 'core/order_summary.html', context)
        else:
            messages.error(self.request, "You do have an active order")
            return render(self.request, 'core/order_summary.html')


class CheckoutView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        order = OrderItem.objects.filter(user=self.request.user, ordered=False)
        order_total = self.get_order_total(self)
        form = CheckoutForm()
        if order:
            context = {
                'object': order,
                'order_total': order_total,
                'form': form,
            }
            return render(self.request, 'core/checkout.html', context)
        else:
            messages.error(self.request, "You do have an active order")
            return render(self.request, 'core/order_summary.html')

    def get_order_total(self, *args, **kwargs):
        order = OrderItem.objects.filter(user=self.request.user, ordered=False)
        order_total = 0
        for order_items in order:
            order_total += order_items.item.price * order_items.quantity
        return order_total

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        order = OrderItem.objects.filter(user=self.request.user, ordered=False)
        order_total = self.get_order_total(self)
        if order:
            context = {
                'object': order,
                'order_total': order_total,
                'form': form,
            }
            print(self.request.POST)
            if form.is_valid():
                print("the form is valid")
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                email = form.cleaned_data.get('email')
                phone_number = form.cleaned_data.get('phone_number')
                address_1 = form.cleaned_data.get('address_1')
                address_2 = form.cleaned_data.get('address_2')
                country = form.cleaned_data.get('country')
                state = form.cleaned_data.get('state')
                zip = form.cleaned_data.get('zip')

                sale_order = Order.objects.filter(user=self.request.user, ordered=False)
                sale_order.update(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_number=phone_number,
                    address_1=address_1,
                    address_2=address_2,
                    country=country,
                    state=state,
                    zip=zip,
                    order_total=order_total,

                )
                return redirect('core:checkout')

            return render(self.request, 'core/checkout.html', context)

        else:
            messages.error(self.request, "You do have an active order")
            return render(self.request, 'core/order_summary.html')


@allow_lazy_user
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            print("it is in")
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
    return redirect("core:item-detail", slug=slug)
