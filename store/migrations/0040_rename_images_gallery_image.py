# Generated by Django 4.0.1 on 2022-07-16 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0039_alter_gallery_options_alter_gallery_images'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gallery',
            old_name='images',
            new_name='image',
        ),
    ]