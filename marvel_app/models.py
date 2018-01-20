# from .views import Marvel
from django.db import models
from django.contrib.auth.models import User
from django.conf.urls.static import static
# from marvel.settings import pri_key, pub_key


class Comic(models.Model):
    external_id = models.IntegerField(blank=True)
    title = models.CharField(max_length=200)
    date_on_sale = models.TextField(blank=True)
    ean = models.TextField(blank=True)
    variant_d = models.TextField(blank=True)
    image_ref = models.URLField(blank=True)
    image_cover = models.ImageField(upload_to='media/')
    user = models.ForeignKey(
        User,
        models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title

class searchedComic(models.Model):
    external_id = models.IntegerField(blank=True)
    title = models.CharField(max_length=200)
    date_on_sale = models.TextField(blank=True)
    ean = models.TextField(blank=True)
    variant_d = models.TextField(blank=True)
    image_ref = models.URLField(blank=True)
    image_cover = models.ImageField(upload_to='media/')
    user = models.ForeignKey(
        User,
        models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title
