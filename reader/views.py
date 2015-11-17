from django.shortcuts import render, redirect
from django.middleware.csrf import get_token, rotate_token

from .forms import LoginForm
from .data_base import *

# Create your views here.
def index(request):
    form = LoginForm()
    ren = None
    content = {"form" : form}
    #ren = render(request, 'index.html', {"form": form, "lolel": "error_text"})
    if request.method == "POST":
        if request.POST.get('new_user'):
            curr.execute("select user_email from reader_user where user_email=(%s)", (request.POST.get('your_email'),))
            if curr.rowcount == 0:
                rotate_token(request)
                #curr.execute("insert into reader_user (user_email, password, token) values (%s, %s, %s)", (request.POST.get('your_email', 'FUCK'), request.POST.get('password', 'FUCK'), get_token(request)))
                curr.execute("insert into reader_user (user_email, password) values (%s, %s)", (request.POST.get('your_email', 'FUCK'), request.POST.get('password', 'FUCK')))
                curr.execute("insert into reader_user_token (user_id, last_use, token) values ((select id from reader_user where user_email=(%s)), (select clock_timestamp()), %s)", (request.POST.get('your_email', 'FUCK'), get_token(request)))
                conn.commit()
                #ren = render(request, 'collection.html')
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
                    #curr.execute("update reader_user set token=(%s) where user_email=(%s)", (get_token(request), request.POST.get('your_email', 'FUCK')))
                    curr.execute("insert into reader_user_token (user_id, last_use, token) values ((select id from reader_user where user_email=(%s)), (select clock_timestamp()), %s)", (request.POST.get('your_email', 'FUCK'), get_token(request)))
                    conn.commit()
                    #ren = render(request, 'collection.html')
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
                #ren = render(request, 'collection.html')
                ren = redirect('collection')
    if ren is None:
        ren = render(request, 'index.html', content)
    return ren

def collection(request):
    ren = None
    if request.method == "GET":
        #if request.GET.get('user_id', '') == 'None':
            #print "shiii"
            #rotate_token(request)
            #ren = render(request, 'collection.html')
        #else:
            curr.execute("select user_id from reader_user_token where token=(%s)", (get_token(request),))
            if curr.rowcount == 1:
                curr.execute("update reader_user_token set last_use=(select clock_timestamp()) where token=(%s)", (get_token(request),))
                conn.commit()
                curr.execute("select id from reader_user_token where token=(%s)", (get_token(request),))
                ren = render(request, 'collection.html', {id : curr.fetchone()[0]})
    if ren is None:
        #ren = HttpResponseRedirect('/', {"error": "ups"})
        ren = redirect('index')
    return ren