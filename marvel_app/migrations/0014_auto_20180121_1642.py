# Generated by Django 2.0.1 on 2018-01-21 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marvel_app', '0013_auto_20180121_1535'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comic',
            name='variants',
        ),
        migrations.AddField(
            model_name='comic',
            name='variants',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='marvel_app.Variant'),
        ),
    ]