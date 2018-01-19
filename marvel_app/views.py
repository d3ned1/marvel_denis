from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
import requests
import hashlib, datetime, requests, json
from marvel.settings import pri_key, pub_key
from .models import Comic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

limit = 10


def master(request):
    comics_list = Comic.objects.all()
    paginator = Paginator(comics_list, 25)
    return render(request, 'marvel_app/master.html', locals())


def comics(request):
    comicsobj = Comic.objects.all()

    return render(request, 'marvel_app/comics.html', locals())


def index(request):
    return render(request, 'marvel_app/index.html', locals())


def about(request):
    return render(request, 'marvel_app/about.html', locals())


class Marvel():
    global list_to_sort
    baseURI = "http://gateway.marvel.com/v1/public"

    def query(request):
        global list_to_sort

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
    list_to_sort = Marvel.query(request)
    if list_to_sort is not None:
        Comic.title = [list_to_sort[0]['title']]
        Comic.ean = [list_to_sort[0]['ean']]
        Comic.variant_d = [list_to_sort[0]['variantDescription']]
        Comic.date_on_sale = [list_to_sort[0]['dates'][0]['date']]
        Comic.image_ref = [(list_to_sort[0]['thumbnail']['path'] + '/detail.jpg')]

        for num in range(1, len(list_to_sort)):
            Comic.title.append(list_to_sort[num]['title'])
            Comic.ean.append(list_to_sort[num]['ean'])
            Comic.variant_d.append(list_to_sort[num]['variantDescription'])
            Comic.date_on_sale.append(list_to_sort[num]['dates'][0]['date'])
            Comic.image_ref.append((list_to_sort[num]['thumbnail']['path'] + '/detail.jpg'))

        results = [Comic.title, Comic.ean, Comic.variant_d, Comic.date_on_sale, Comic.image_ref]

        return render(request, 'marvel_app/marvel.html', {'res': results})
    else:
        return render(request, 'marvel_app/marvel.html')
# {'title': results[0]}, {'ean': results[1]}




# sortedlist.append([
#     list_to_sort[num]['title'],
#     list_to_sort[num]['ean'],
#     list_to_sort[num]['variantDescription'],
#     list_to_sort[num]['dates'][0]['date'],
#     (list_to_sort[num]['thumbnail']['path'] + '/detail.jpg')
# ])