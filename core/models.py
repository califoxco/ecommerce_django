from django.db import models
from django.shortcuts import reverse

class Item(models.Model):
    title = models.CharField(max_length= 100)
    price = models.FloatField()
    slug = models.SlugField()
    listed_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:item", kwargs={
            'slug': self.slug
        })

class OrderItem(models.Model):
    pass





