# Generated by Django 4.0.3 on 2022-03-24 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_remove_variation_product_product_variation'),
        ('cart', '0003_remove_cartitem_variation_cartitem_variation_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='variation_value',
            field=models.ManyToManyField(blank=True, to='store.variation'),
        ),
    ]
