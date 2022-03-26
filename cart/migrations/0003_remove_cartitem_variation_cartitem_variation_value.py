# Generated by Django 4.0.3 on 2022-03-24 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_remove_variation_product_product_variation'),
        ('cart', '0002_cartitem_variation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='variation',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='variation_value',
            field=models.ManyToManyField(blank=True, to='store.value'),
        ),
    ]
