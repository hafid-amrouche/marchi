# Generated by Django 4.0.1 on 2022-03-26 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0023_rename_category_variation_name_variation_value_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='variation',
            name='image',
            field=models.ImageField(null=True, upload_to='photos/values'),
        ),
    ]
