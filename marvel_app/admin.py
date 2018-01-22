from django.contrib import admin
from marvel_app.models import Comic, Comic_variant, ComicImage

# admin.site.register(searchedComic)

admin.site.register(Comic)
admin.site.register(ComicImage)
admin.site.register(Comic_variant)

class ComicImageInline(admin.TabularInline):
    model = ComicImage
    extra = 10


class ComicAdmin(admin.ModelAdmin):
    inlines = [ComicImageInline,]
