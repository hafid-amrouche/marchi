# Generated by Django 4.0.1 on 2022-06-14 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0028_product_has_variant_product_price_and_more'),
        ('order', '0006_remove_orderproduct_variation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='value',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='value',
            field=models.ManyToManyField(blank=True, to='store.Value'),
        ),
    ]
