from django.shortcuts import render
#from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from bs4 import BeautifulSoup
import requests
import re
from collections import defaultdict
import json, time

CACHE = defaultdict()
@csrf_exempt
def analysis_link(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        if 'link' in req:
            link = req['link'].strip()

            # implementing 24 hr cache
            t = time.time()
            for k, v in list(CACHE.items()):
                if t - v['time'] > 60 * 60 * 24:
                    CACHE.pop(k)

            #result = cache.get(link)
            if link not in CACHE:
                result = do_analysis(link)
                CACHE[link] = {'data':result, 'time':time.time()}
                #cache.set(link, result, timeout= 60 * 60 * 24)
            else:
                result = CACHE[link]['data']


            if 'message' not in result:
                return JsonResponse(result, status=200)
            else:
                return JsonResponse(result, status=400)
        else:
            return JsonResponse({'message':'wrong parameters'}, status=400)
    else:
        return JsonResponse({'message':'wrong method'}, status=400)

# assume link format: http://domain/.../.../ or https://domain/.../...
def do_analysis(link):
    print('not in cache, do analysis')
    # parse domain
    if 'http://' in link:
        domain = link.replace('http://', '').split('/')[0]
    elif 'https://' in link:
        domain = link.replace('https://', '').split('/')[0]
    else:
        return {'message':'unexpected link format'}
    try:
        r = requests.get(link)
        if r.status_code == requests.codes.ok:
            soup = BeautifulSoup(r.text, 'html.parser')

            # find title 
            title = soup.title.string

            # find heading
            headings = soup.findAll(re.compile('^h[1-6]$'))
            heading_dict = {}
            if headings != None:
                for h in headings:
                    if h.name not in heading_dict:
                        heading_dict[h.name] = 0
                    heading_dict[h.name] += 1

            # find links 
            external_links = []
            internal_links = []
            inaccessible = []
            for link in soup.findAll('a', attrs={'href': re.compile("^https*://")}):
                l = link.get('href')

                # simple check if the link has the same domain
                if domain in l:
                    internal_links.append(l)
                else:
                    external_links.append(l)

                # try to connect the link
                temp_r = requests.get(l)
                if r.status_code != requests.codes.ok:
                    inaccessible.append(l)

            num_external_links = len(external_links)
            num_internal_links = len(internal_links)
            num_inaccessible_links = len(inaccessible)

            # check if login form
            login_form = soup.findAll('form', attrs={'id':re.compile("^login^")})
            is_login = (login_form != None)

            # construct result
            res = {
                'title':title,
                'headings':heading_dict,
                'num_internal_links':num_internal_links,
                'num_external_links':num_external_links,
                'num_inaccessible_links':num_inaccessible_links,
                'inaccessible_links':inaccessible,
                'is_login':is_login
            }
            return res
        else:
            return {'message':'unaccessible link'}
    except:
        return {'message':'unaccessible link'}
