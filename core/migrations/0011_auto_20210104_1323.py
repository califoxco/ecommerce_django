# Generated by Django 3.1.1 on 2021-01-04 21:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20210104_1257'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='billing_email',
        ),
        migrations.RemoveField(
            model_name='order',
            name='billing_phone_number',
        ),
    ]