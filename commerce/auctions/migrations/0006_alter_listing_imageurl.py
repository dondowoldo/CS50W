# Generated by Django 4.1.4 on 2023-04-24 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_remove_listing_image_listing_imageurl_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='imageurl',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
