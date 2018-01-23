from django.shortcuts import render
import hashlib, datetime, requests, json
from marvel.settings import pri_key, pub_key
from .models import Comic, Comic_variant, ComicImage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User

limit = 20


def email_check(user):
    return User(is_staff=True)


@login_required(login_url='/login/')
def comics(request):
    comicsobj = Comic.objects.all()
    variant = Comic_variant.objects.all()
    return render(request, 'marvel_app/comics.html', locals())


def about(request):
    return render(request, 'marvel_app/about.html', locals())


class Marvel():
    baseURI = "http://gateway.marvel.com/v1/public"

    def query(request): # make proper link, send GET request (search btn), return json
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
        # variants =[]
        if comicsid < len(list_to_model):
            for obj in objs:
                obj.external_id = list_to_model[comicsid]['id']
                obj.title = list_to_model[comicsid]['title']
                obj.date_on_sale = list_to_model[comicsid]['dates'][0]['date'][:10]
                obj.ean = list_to_model[comicsid]['ean']
                obj.variant_d = list_to_model[comicsid]['variantDescription']
                obj.image_ref = (list_to_model[comicsid]['thumbnail']['path'] + '/detail.jpg')
                if list_to_model[comicsid]['description'] is not None:
                    obj.com_descr = list_to_model[comicsid]['description']
                # obj.stories = list_to_model[comicsid]['stories']['items'][1]
                if len(list_to_model[comicsid]['variants']) is not 0:
                    var = Comic_variant()
                    var = get_variants(list_to_model, comicsid)
                if len(list_to_model[comicsid]['images']) > 0:
                    img = ComicImage()
                    img = get_images(list_to_model, comicsid)
                comicsid += 1

        if request.method == 'POST':
            save_comic(request)

        return render(request, 'marvel_app/marvel.html', locals())
    else:
        return render(request, 'marvel_app/marvel.html')


def save_comic(request):  # save comic using POST request
    x = Comic()
    x.title = request.POST["title"]
    x.external_id = request.POST['external_id']
    x.image_ref = request.POST['image_ref']
    x.date_on_sale = request.POST['date_on_sale']
    x.ean = request.POST['en']
    x.com_descr = request.POST['com_descr']
    x.variant_d = request.POST['variant_d']

    x.save()


def get_variants(list, comicsid):
    unsorted_list = list
    comics_id = comicsid
    variants = Comic_variant()
    for var_id in range(0, len(unsorted_list[comics_id]['variants'])):
        variants.variant_name = unsorted_list[comics_id]['variants'][var_id]['name']
        variants.v_id = unsorted_list[comics_id]['id']
    return variants


def get_images(list, comicsid):
    unsorted_list = list
    comics_id = comicsid
    images = ComicImage()
    for var_id in range(0, len(unsorted_list[comics_id]['images'])):
        images.image = (unsorted_list[comics_id]['images'][var_id]['path'] + '.jpg')
        images.v_id = unsorted_list[comics_id]['id']
    return images


    # variantss = [Variant() for i in range(0, len(list_to_model))]
    #         comicsid = 0
    #         if comicsid < len(list_to_model):
    #             for var in variantss:
    #                 if len(list_to_model[comicsid]['variants']) is not 0:
    #                     for var_id in range(0, len(list_to_model[comicsid]['variants'])):
    #                         var.variant = list_to_model[comicsid]['variants'][var_id]['name']
    #                         var.v_id = list_to_model[comicsid]['id']
    #                 comicsid = comicsid + 1
