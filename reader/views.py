import json
import collections

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.middleware.csrf import get_token, rotate_token

from .forms import LoginForm
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
                #curr.execute("""select user_token.token_id, user_email from reader_user right outer join 
                                #(select id as token_id, user_id from reader_user_token where token=(%s)) 
                                #as user_token on reader_user.id = user_token.user_id""", (get_token(request),))
                #inform = curr.fetchone()
                #content = {"id" : inform[0], "email" : inform[1]}
                curr.execute("""select user_email from reader_user where id = 
                                (select user_id from reader_user_token where token=(%s))""", (get_token(request),))
                content = {"email" : curr.fetchone()[0]}
                curr.execute("select id, title from reader_site where user_id = (select user_id from reader_user_token where token=(%s))", (get_token(request),))
                rows = curr.fetchall()
                rowarray = []
                for row in rows:
                    d = collections.OrderedDict()
                    d['id'] = row[0]
                    d['title'] = row[1]
                    rowarray.append(d)
                content.update({"sites" : rowarray})
                ren = render(request, 'collection.html', content)
    if ren is None:
        ren = redirect('index')
    return ren

def load_site(request):
    ren = None
    if request.method == "GET":
        curr.execute("select url, width from reader_image where site_id=(%s)", (request.GET.get('site_id')))
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
    return HttpResponse("lol")
