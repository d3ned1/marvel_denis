from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
import requests
import hashlib, datetime, requests, json
from marvel.settings import pri_key, pub_key
from .models import Comic, searchedComic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

limit = 10


# def login(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = auth.authenticate(username=username, password=password)
#     if user is not None and user.is_active:
#         # Правильный пароль и пользователь "активен"
#         auth.login(request, user)
#         # Перенаправление на "правильную" страницу
#         return HttpResponseRedirect("?next=/mypage/")
#     else:
#         # Отображение страницы с ошибкой
#         return HttpResponseRedirect("/ge/q/")


# def logout(request):
#     auth.logout(request)
#     # Перенаправление на страницу.
#     return HttpResponseRedirect("/account/loggedout/")


def master(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)
    else:
        comics_list = Comic.objects.all()
        paginator = Paginator(comics_list, 25)
        return render(request, 'marvel_app/comics.html', locals())


def comics(request):
    comicsobj = Comic.objects.all()
    return render(request, 'marvel_app/comics.html', locals())


def index(request):
    return render(request, 'marvel_app/index.html', locals())


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


def marvel(request):
    list_to_model = Marvel.query(request)
    if list_to_model is not None:
        objs = [searchedComic() for i in range(0, len(list_to_model))]
        comicsid = 0
        if comicsid < len(list_to_model):
            for obj in objs:
                obj.external_id = list_to_model[comicsid]['id']
                obj.title = list_to_model[comicsid]['title']
                obj.date_on_sale = list_to_model[comicsid]['dates'][0]['date']
                obj.ean = list_to_model[comicsid]['ean']
                obj.variant_d = list_to_model[comicsid]['variant']
                # x.image_cover =
                obj.image_ref = (list_to_model[comicsid]['thumbnail']['path'] + '/detail.jpg')

                comicsid += 1
        # for comicsid in range(1, len(list_to_model)):
        #
        #     x = searchedComic()
        #     x.external_id = list_to_model[comicsid]['id']
        #     x.title = list_to_model[comicsid]['title']
        #     x.date_on_sale = list_to_model[comicsid]['dates'][0]['date']
        #     x.ean = list_to_model[comicsid]['ean']
        #     x.variant_d = list_to_model[comicsid]['variantDescription']
        #     # x.image_cover =
        #     x.image_ref = (list_to_model[comicsid]['thumbnail']['path'] + '/detail.jpg')
        return render(request, 'marvel_app/marvel.html', locals())
    else:
        return render(request, 'marvel_app/marvel.html')


def save_comic(request):
    if request.POST and 'obj.external_id' in request.POST:

        x = Comic(request.POST['obj.external_id'])
        x.save()

        # sortedlist.append([
        #     list_to_sort[num]['title'],
        #     list_to_sort[num]['ean'],
        #     list_to_sort[num]['variantDescription'],
        #     list_to_sort[num]['dates'][0]['date'],
        #     (list_to_sort[num]['thumbnail']['path'] + '/detail.jpg')
        # ])

        # Comic.title = [list_to_sort[0]['title']]
        # Comic.ean = [list_to_sort[0]['ean']]
        # Comic.variant_d = [list_to_sort[0]['variantDescription']]
        # Comic.date_on_sale = [list_to_sort[0]['dates'][0]['date']]
        # Comic.image_ref = [(list_to_sort[0]['thumbnail']['path'] + '/detail.jpg')]
        #
        # for num in range(1, len(list_to_sort)):
        #     Comic.title.append(list_to_sort[num]['title'])
        #     Comic.ean.append(list_to_sort[num]['ean'])
        #     Comic.variant_d.append(list_to_sort[num]['variantDescription'])
        #     Comic.date_on_sale.append(list_to_sort[num]['dates'][0]['date'])
        #     Comic.image_ref.append((list_to_sort[num]['thumbnail']['path'] + '/detail.jpg'))
        #
        # results = [Comic.title, Comic.ean, Comic.variant_d, Comic.date_on_sale, Comic.image_ref]
