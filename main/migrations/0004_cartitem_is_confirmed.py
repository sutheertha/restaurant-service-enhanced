# Generated by Django 5.0.6 on 2024-07-09 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_cart_created_at_cart_is_confirmed_cart_total_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='is_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]