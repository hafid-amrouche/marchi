# Generated by Django 4.0.1 on 2022-03-22 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_variation_product_variation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='variation',
        ),
    ]
