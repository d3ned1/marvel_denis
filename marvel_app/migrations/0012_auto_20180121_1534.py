# Generated by Django 2.0.1 on 2018-01-21 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marvel_app', '0011_auto_20180121_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comic',
            name='date_on_sale',
            field=models.CharField(blank=True, max_length=1),
        ),
    ]
