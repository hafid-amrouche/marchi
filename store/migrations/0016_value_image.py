# Generated by Django 4.0.1 on 2022-03-22 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_remove_variation_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='value',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='photos/values'),
        ),
    ]