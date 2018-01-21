# from .views import Marvel
from django.db import models
from django.contrib.auth.models import User
from django.conf.urls.static import static
from django import forms
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


# from marvel.settings import pri_key, pub_key



class Variant(models.Model):
    variant = models.CharField(blank=True, max_length=50)
    v_id = models.IntegerField(blank=True)  # external id of the comic


class Comic(models.Model):
    external_id = models.IntegerField(blank=True)  # external id of the comic
    title = models.CharField(max_length=100)  # title of the comic
    date_on_sale = models.CharField(max_length=10, blank=True)  # sale start date of the comic
    ean = models.TextField(blank=True)  # comic EAN number
    variant_d = models.TextField(blank=True)  # current comic variant description
    variants = models.ForeignKey(
        Variant,
        models.SET_NULL,
        blank=True,
        null=True,
    )
    # current comic available variants
    image_ref = models.URLField(blank=True)  # link to the cover image
    image_cover = models.ImageField(blank=True, upload_to='media/')  # storage field and place for the image cover
    com_descr = models.TextField(blank=True)  # current comic description
    hidden = models.BooleanField(default=False)  # object is hidden or not
    user = models.ForeignKey(  # User model
        User,
        models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title

# class searchedComic(models.Model):
#     external_id = models.IntegerField(blank=True)
#     title = models.CharField(max_length=200)
#     date_on_sale = models.TextField(blank=True)
#     ean = models.TextField(blank=True)
#     variant_d = models.TextField(blank=True)
#     image_ref = models.URLField(blank=True)
#     image_cover = models.ImageField(upload_to='media/')
#     user = models.ForeignKey(
#         User,
#         models.SET_NULL,
#         blank=True,
#         null=True,
#     )
#
#     def __str__(self):
#         return self.title
