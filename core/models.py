from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

class Item(models.Model):
    title = models.CharField(max_length= 100, unique=True)
    price = models.FloatField()
    slug = models.SlugField(default='1')
    listed_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:item-detail", kwargs={
            'slug': self.slug
        })

class OrderItem(models.Model):
    pass





