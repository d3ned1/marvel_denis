# Generated by Django 2.0.1 on 2018-01-22 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marvel_app', '0019_auto_20180122_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='comic_variant',
            name='variant_name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
