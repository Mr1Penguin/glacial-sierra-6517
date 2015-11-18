import json
import collections
import urllib2

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.middleware.csrf import get_token, rotate_token

from .forms import LoginForm
from .parser import *
from .data_base import *

# Create your views here.
def index(request):
    form = LoginForm()
    ren = None
    content = {"form" : form}
    if request.method == "POST":
        if request.POST.get('new_user'):
            curr.execute("select user_email from reader_user where user_email=(%s)", (request.POST.get('your_email'),))
            if curr.rowcount == 0:
                rotate_token(request)
                curr.execute("insert into reader_user (user_email, password) values (%s, %s)", (request.POST.get('your_email', 'FUCK'), request.POST.get('password', 'FUCK')))
                curr.execute("insert into reader_user_token (user_id, last_use, token) values ((select id from reader_user where user_email=(%s)), (select clock_timestamp()), %s)", (request.POST.get('your_email', 'FUCK'), get_token(request)))
                conn.commit()
                ren = redirect('collection')
            else:
                content.update({"error": "User with this e-mail already exist!", "lastmail": request.POST.get('your_email'), "checkbox" : True})
        else:
            # if correct load collection. else index with error
            curr.execute("select password from reader_user where user_email=(%s)", (request.POST.get('your_email'),))
            if curr.rowcount == 1:
                passwd = curr.fetchone()[0]
                if passwd == request.POST.get('password'):
                    rotate_token(request)
                    curr.execute("insert into reader_user_token (user_id, last_use, token) values ((select id from reader_user where user_email=(%s)), (select clock_timestamp()), %s)", (request.POST.get('your_email', 'FUCK'), get_token(request)))
                    conn.commit()
                    ren = redirect('collection')
                else:
                    content.update({"error": "Wrong password!", "lastmail":request.POST.get('your_email')})
            else:
                content.update({"error": "User with this e-mail doesn't exist!", "lastmail":request.POST.get('your_email')})
    else:
        if request.method == "GET":
            curr.execute("select user_id from reader_user_token where token=(%s)", (get_token(request),))
            if curr.rowcount == 1:
                curr.execute("update reader_user_token set last_use=(select clock_timestamp()) where token=(%s)", (get_token(request),))
                conn.commit()
                ren = redirect('collection')
    if ren is None:
        ren = render(request, 'index.html', content)
    return ren

def collection(request):
    ren = None
    if request.method == "POST":
        curr.execute("delete from reader_user_token where token=(%s)", (get_token(request),))
        conn.commit()
        rotate_token(request)
    else:
        if request.method == "GET":
            curr.execute("select user_id from reader_user_token where token=(%s)", (get_token(request),))
            if curr.rowcount == 1:
                curr.execute("update reader_user_token set last_use=(select clock_timestamp()) where token=(%s)", (get_token(request),))
                conn.commit()
                curr.execute("""select user_email from reader_user where id = 
                                (select user_id from reader_user_token where token=(%s))""", (get_token(request),))
                content = {"email" : curr.fetchone()[0]}
                curr.execute("select id, title, url, favicon from reader_site where user_id = (select user_id from reader_user_token where token=(%s)) order by id", (get_token(request),))
                rows = curr.fetchall()
                rowarray = []
                for row in rows:
                    d = collections.OrderedDict()
                    d['id'] = row[0]
                    d['title'] = row[1]
                    dd = row[2].split('/')
                    d['favicon'] = row[3] or (('http://' + dd[0] if dd[0] != 'http:' else dd[0] + '//' +  dd[2]) + '/favicon.ico')
                    rowarray.append(d)
                content.update({"sites" : rowarray})
                ren = render(request, 'collection.html', content)
    if ren is None:
        ren = redirect('index')
    return ren

def load_site(request):
    if request.method == "GET":
        curr.execute("select url, width from reader_image where site_id=(%s)", (request.GET.get('site_id'),))
        rows = curr.fetchall()
        sites = []
        for row in rows:
            t = collections.OrderedDict()
            t['url'] = row[0]
            t['width'] = row[1]
            sites.append(t)
        sites_j = json.dumps(sites)
        return HttpResponse(sites_j, content_type="application/json")

def add_site(request):
    if request.method == "POST":
        def create_json(toSend, isError):
            content = collections.OrderedDict()
            if isError:
                content['error'] = toSend[0]
                if toSend[0] >= 1000:
                    content['site_id'] = toSend[1]
            else:
                content['site_id'] = toSend[0]
                content['title'] = toSend[1]
                curr.execute("""select favicon from reader_site where id = (%s)""", [site_id])
                if curr.rowcount != 0:
                    content['custom_favicon'] = curr.fetchone()[0]
            return json.dumps(content)
        url = request.POST.get('url')
        curr.execute("""select id from reader_site where url = (%s)
                        and user_id = (select user_id from reader_user_token where token = (%s))""", (url, get_token(request)))
        if curr.rowcount != 0:
            return HttpResponse(create_json([9001, curr.fetchone()[0]], True), content_type="application/json")
        try:
            #req = urllib2.Request(url)
            #response = urllib2.urlopen(req)
            response = urllib2.urlopen(url)
        except urllib2.HTTPError as e:
            return HttpResponse(create_json([e.code], True), content_type="application/json")
        except Exception as e:
            #print e.reason
            return HttpResponse(create_json([901], True), content_type="application/json")
        html = response.read()
        if not isinstance(html, unicode):
            try: 
                unihtml = unicode(html, 'utf-8')
            except UnicodeError:
                unihtml = html.decode('cp1251').encode('utf8')
        else:
            unihtml = html
        curr.execute("""insert into reader_site (url, add_date, user_id) 
                        values ((%s), (select clock_timestamp()), 
                        (select user_id from reader_user_token where token = (%s)))
                        returning id""", (url, get_token(request)))
        site_id = curr.fetchone()[0]
        parser = HTMLImgParser(curr, site_id)
        parser.feed(unihtml)
        curr.execute("""select title from reader_site where id = (%s)""", (site_id,))
        conn.commit()
        return HttpResponse(create_json([site_id, curr.fetchone()[0]], False), content_type="application/json")
    return HttpResponse("Not available")

def delete_site(request):
    if request.method == "POST":
        site_id = request.POST.get('site_id', 0)
        curr.execute("""delete from reader_image where site_id = (%s)""", [site_id])
        curr.execute("""delete from reader_site where id = (%s) and user_id = (
                        select user_id from reader_user_token where token = (%s))""", [site_id, get_token(request)])
        conn.commit()
        content = collections.OrderedDict()
        content['ok'] = True
        return HttpResponse(json.dumps(content), content_type="application/json")
    return HttpResponse("Not available")
