# Generated by Django 3.1.1 on 2020-12-26 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20201226_0015'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.CharField(default='Here is a bunch of product description that keeps talking about how great and how awesome the product is please buy buy buy', max_length=500),
        ),
    ]
