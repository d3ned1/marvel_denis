from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.contrib import auth
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
import requests
import hashlib, datetime, requests, json
from marvel.settings import pri_key, pub_key
from .models import Comic, Variant  # , searchedComic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

limit = 20


def email_check(user):
    return User(is_staff=True)


@login_required(login_url='/login/')
def master(request):
    return render(request, 'marvel_app/comics.html', locals())


@login_required(login_url='/login/')
def comics(request):
    comicsobj = Comic.objects.all()
    return render(request, 'marvel_app/comics.html', locals())


def about(request):
    return render(request, 'marvel_app/about.html', locals())


class Marvel():
    baseURI = "http://gateway.marvel.com/v1/public"

    def query(request):
        if 'q' in request.GET and request.GET['q']:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d%H:%M:%S")
            hash_input = timestamp + pri_key + pub_key
            hashed_string = hashlib.md5(hash_input.encode('utf-8')).hexdigest()
            url_params = {
                'ts': timestamp,
                'apikey': pub_key,
                'hash': hashed_string
            }
            title = request.GET['q']
            if limit is not None:
                url_params['limit'] = limit
                URI = "/comics" + "?title=" + title
                Marvel.fullURI = Marvel.baseURI + URI
                resp = requests.get(Marvel.fullURI, params=url_params)
                print(resp.url)
                list_to_sort = resp.json()['data']['results']
                URI = ''
                return list_to_sort


@user_passes_test(email_check)
@login_required(login_url='/login/')
def marvel(request):
    list_to_model = Marvel.query(request)
    if list_to_model is not None:
        objs = [Comic() for i in range(0, len(list_to_model))]
        comicsid = 0
        if comicsid < len(list_to_model):
            for obj in objs:
                obj.external_id = list_to_model[comicsid]['id']
                obj.title = list_to_model[comicsid]['title']
                obj.date_on_sale = list_to_model[comicsid]['dates'][0]['date']
                obj.ean = list_to_model[comicsid]['ean']
                obj.variant_d = list_to_model[comicsid]['variantDescription']
                obj.variant_d = list_to_model[comicsid]['description']
                # x.image_cover =
                obj.image_ref = (list_to_model[comicsid]['thumbnail']['path'] + '/detail.jpg')

                comicsid += 1

        # paginator = Paginator(objs, 5)
        # page = request.GET.get('page')
        # try:
        #     objj = paginator.page(page)
        # except PageNotAnInteger:
        #     # If page is not an integer, deliver first page.
        #     objj = paginator.page(1)
        # except EmptyPage:
        #     # If page is out of range (e.g. 9999), deliver last page of results.
        #     objj = paginator.page(paginator.num_pages)
        # return render_to_response('marvel_app/marvel.html', {"obj": objj})

        return render(request, 'marvel_app/marvel.html', locals())
    else:
        return render(request, 'marvel_app/marvel.html')


def save_comic(request):
    if request == 'POST' and request.POST['title']:
        x = Comic()
        x.image_cover = request.POST["title"]
        x.save()
        # x.image_cover = request.POST['image_cover']
