# Generated by Django 4.0.3 on 2022-03-17 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_remove_product_off_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='off_sale_price',
            field=models.FloatField(null=True),
        ),
    ]
