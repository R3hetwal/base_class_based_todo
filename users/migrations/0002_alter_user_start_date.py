# Generated by Django 4.1.6 on 2023-02-13 07:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 13, 7, 10, 12, 856325, tzinfo=datetime.timezone.utc)),
        ),
    ]