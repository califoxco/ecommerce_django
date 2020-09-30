from django.db import models

class Item(models.Model):
    title = models.CharField(max_length= 100)
    price = models.FloatField()

    listed_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    pass





