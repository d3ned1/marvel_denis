from django.db import models
from django.contrib.auth.models import User


class Comic(models.Model):
    class Meta:
        verbose_name_plural = 'Comics'

    external_id = models.IntegerField(blank=True, verbose_name='External ID')  # external id of the comic
    title = models.CharField(max_length=100, verbose_name='Title')  # title of the comic
    date_on_sale = models.CharField(max_length=10, blank=True, verbose_name='Date of sales start')  # sale start date of the comic
    ean = models.CharField(blank=True, max_length=100, verbose_name='EAN')  # comic EAN number
    variant_d = models.CharField(blank=True, max_length=100, verbose_name='Current variant description')  # current comic variant description
    image_ref = models.URLField(blank=True, verbose_name='Cover source link')  # link to the cover image
    image_cover = models.ImageField(blank=True, upload_to='media/', verbose_name='Cover image field')  # storage field and place for the image cover
    com_descr = models.TextField(blank=True, verbose_name='Comic short description')  # current comic short description
    hidden = models.BooleanField(default=False, verbose_name='Should comic be hidden or not')  # object is hidden or not
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
    image = models.ImageField()

    def __str__(self):
        return self.comic.title
