# Generated by Django 3.2.6 on 2022-01-14 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rare_app', '0023_customercontact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customercontact',
            name='address',
            field=models.TextField(max_length=300),
        ),
    ]
