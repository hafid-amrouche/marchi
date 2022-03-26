# Generated by Django 4.0.3 on 2022-03-24 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_variation_has_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='value',
            name='variation',
        ),
        migrations.AddField(
            model_name='variation',
            name='value',
            field=models.ManyToManyField(related_name='values', to='store.value'),
        ),
    ]
