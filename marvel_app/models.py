from django.db import models
from django.contrib.auth.models import User


class Comic(models.Model):
    class Meta:
        verbose_name_plural = 'Comics'

    external_id = models.IntegerField(blank=True)  # external id of the comic
    title = models.CharField(max_length=100)  # title of the comic
    date_on_sale = models.CharField(max_length=10, blank=True)  # sale start date of the comic
    ean = models.TextField(blank=True)  # comic EAN number
    variant_d = models.TextField(blank=True)  # current comic variant description
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


class Comic_variant(models.Model):
    class Meta:
        verbose_name_plural = 'Comic variants'

    variant = models.ForeignKey(Comic, on_delete=None)
    v_id = models.IntegerField(blank=True)  # external id of the comic
    variant_name = models.CharField(blank=True, max_length=100)


class ComicImage(models.Model):
    class Meta:
        verbose_name_plural = 'Comic images'

    comic = models.ForeignKey(Comic, related_name='images', on_delete=False)
    image = models.ImageField(upload_to='media/')

    def __str__(self):
        return self.comic.title