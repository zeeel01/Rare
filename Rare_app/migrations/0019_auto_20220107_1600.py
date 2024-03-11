# Generated by Django 3.2.6 on 2022-01-07 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rare_app', '0018_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='product',
            field=models.ManyToManyField(blank=True, null=True, related_name='cart_products', to='Rare_app.Post'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='total_amt',
            field=models.PositiveIntegerField(default=0),
        ),
    ]