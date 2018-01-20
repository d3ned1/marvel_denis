from django.contrib import admin
from marvel_app.models import Comic
from marvel_app.models import searchedComic

admin.site.register(Comic)
admin.site.register(searchedComic)

# Register your models here.
