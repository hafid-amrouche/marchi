# Generated by Django 4.0.1 on 2022-06-25 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0034_reviewrating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reviewrating',
            old_name='Account',
            new_name='user',
        ),
    ]
