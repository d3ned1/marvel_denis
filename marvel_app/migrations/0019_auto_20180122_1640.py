# Generated by Django 2.0.1 on 2018-01-22 16:40

from django.db import migrations, models
import marvel_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('marvel_app', '0018_comicimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comic_variant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('v_id', models.IntegerField(blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='comic',
            name='variants',
        ),
        migrations.AlterField(
            model_name='comicimage',
            name='comic',
            field=models.ForeignKey(on_delete=False, related_name='images', to='marvel_app.Comic'),
        ),
        migrations.AlterField(
            model_name='comicimage',
            name='image',
            field=models.ImageField(upload_to='media/', verbose_name=marvel_app.models.Comic),
        ),
        migrations.DeleteModel(
            name='Variant',
        ),
        migrations.AddField(
            model_name='comic_variant',
            name='variant',
            field=models.ForeignKey(blank=True, max_length=50, on_delete=True, to='marvel_app.Comic'),
        ),
    ]