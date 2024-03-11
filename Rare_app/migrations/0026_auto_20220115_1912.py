# Generated by Django 3.2.6 on 2022-01-15 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rare_app', '0025_alter_customercontact_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customercontact',
            name='city',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='customercontact',
            name='state',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='customercontact',
            name='totalamt',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='customercontact',
            name='zip',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
