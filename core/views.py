import stripe
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, View
from .models import Item, OrderItem, Order
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckoutForm
from JSJ import settings

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

                billing_first_name = form.cleaned_data.get('billing_first_name')
                billing_last_name = form.cleaned_data.get('billing_last_name')
                billing_address_1 = form.cleaned_data.get('billing_address_1')
                billing_address_2 = form.cleaned_data.get('billing_address_2')
                billing_country = form.cleaned_data.get('billing_country')
                billing_state = form.cleaned_data.get('billing_state')
                billing_zip = form.cleaned_data.get('billing_zip')

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

                    billing_first_name=billing_first_name,
                    billing_last_name=billing_last_name,
                    billing_address_1=billing_address_1,
                    billing_address_2=billing_address_2,
                    billing_country=billing_country,
                    billing_state=billing_state,
                    billing_zip=billing_zip,
                )
                return redirect('core:checkout')

            return render(self.request, 'core/checkout.html', context)

        else:
            messages.error(self.request, "You do have an active order")
            return render(self.request, 'core/order_summary.html')


class PaymentView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        sale_order = Order.objects.filter(user=self.request.user, ordered=False)
        if sale_order:
            order_total = sale_order[0].order_total
            order = sale_order[0].items.all()
            print(f'this order consists of {order}')
            context = {
                'object': order,
                'order_total': order_total,
            }
            return render(self.request, 'core/payment.html', context)
        else:
            return redirect('home')


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


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        # TODO: run some custom code here

    return HttpResponse(status=200)
