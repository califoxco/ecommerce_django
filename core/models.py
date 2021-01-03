from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django.conf import settings

class Item(models.Model):
    title = models.CharField(max_length= 100, unique=True)
    price = models.FloatField()
    slug = models.SlugField(default='1')
    listed_date = models.DateTimeField(auto_now_add=True)
    item_picture = models.ImageField(default='default.jpg', upload_to='item_pics')
    description =  models.CharField(max_length= 500, default="Here is a bunch of product description that keeps talking about how great and how awesome the product is please buy buy buy")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:item-detail", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity =models.IntegerField(default=1)

    def __str__(self):
        return f"{self.item.title}, quantity: {self.quantity}"

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    # Shipping Address
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=100)
    address_1 = models.CharField(max_length=200)
    address_2 = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    order_total = models.FloatField(default=0)

    def __str__(self):
        return self.user.username







