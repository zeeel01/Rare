# Generated by Django 3.2.6 on 2021-12-08 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rare_app', '0011_rename_artist_details_artist_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist_detail',
            name='active_status',
            field=models.BooleanField(default=False),
        ),
    ]