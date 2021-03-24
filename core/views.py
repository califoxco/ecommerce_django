import stripe
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View, TemplateView
from .models import Item, OrderItem, Order
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckoutForm
from django.conf import settings
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from lazysignup.decorators import allow_lazy_user

"""
    The code below is already implemented automatically by django
"""


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

            if form.is_valid():

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

                '''
                    Form-valid action
                '''
                # return redirect('core:checkout')

                order_items = []
                print(order)
                # composes a list of ordering items
                for order_item in order:
                    order_items.append({
                        'name': order_item.item.title,
                        'quantity': order_item.quantity,
                        'currency': 'usd',
                        'amount': int(order_item.item.price * 100),
                    })

                domain_url = 'http://localhost:8000/'
                stripe.api_key = settings.STRIPE_SECRET_KEY
                try:
                    # Create new Checkout Session for the order
                    # For full details see https://stripe.com/docs/api/checkout/sessions/create
                    checkout_session = stripe.checkout.Session.create(
                        success_url=domain_url + 'checkout_success?session_id={CHECKOUT_SESSION_ID}',
                        cancel_url=domain_url + 'cancelled/',
                        payment_method_types=['card'],
                        mode='payment',
                        line_items=order_items
                    )
                    return HttpResponse("<script src='https://js.stripe.com/v3/'></script><script>const stripe = "
                                        "Stripe('"+settings.STRIPE_PUBLISHABLE_KEY+"');stripe"
                                        ".redirectToCheckout({sessionId: '" +
                                        checkout_session['id'] +
                                        "'})</script>")
                    # return JsonResponse({'sessionId': checkout_session['id']})


                except Exception as e:
                    return JsonResponse({'error': str(e)})

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
            context = {
                'object': order,
                'order_total': order_total,
            }
            return render(self.request, 'core/payment.html', context)
        else:
            return redirect('home')


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    sale_order = Order.objects.filter(user=request.user, ordered=False)
    order_items = []
    # redirects if order does not exist
    if not sale_order:
        return redirect('home')

    # composes a list of ordering items
    else:
        for order_item in sale_order[0].items.all():
            order_items.append({
                'name': order_item.item.title,
                'quantity': order_item.quantity,
                'currency': 'usd',
                'amount': int(order_item.item.price * 100),
            })
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'checkout_success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=order_items
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


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
        print("Payment was successful!!!!!!!!!!!!!!!!!")
        # TODO: run some custom code here

    return HttpResponse(status=200)


class SuccessView(LoginRequiredMixin, View):
    #template_name = 'core/checkout_success.html'

    def get(self, *args, **kwargs):
        order = OrderItem.objects.filter(user=self.request.user, ordered=False)
        if order:
            context = {
                'object': order
            }
            return render(self.request, 'core/checkout_success.html', context)
        else:
            messages.error(self.request, "You do have an active order")
            return render(self.request, 'core/checkout_success.html')


class CancelledView(TemplateView):
    template_name = 'cancelled.html'


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
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
    return redirect("core:item-detail", slug=slug)
