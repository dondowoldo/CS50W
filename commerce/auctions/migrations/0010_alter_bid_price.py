# Generated by Django 4.2 on 2023-04-27 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_listing_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='price',
            field=models.PositiveIntegerField(blank=True),
        ),
    ]
