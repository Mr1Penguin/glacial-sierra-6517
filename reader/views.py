from django.shortcuts import render

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
                curr.execute("insert into reader_user (user_email, password) values (%s, %s)", (request.POST.get('your_email', 'FUCK'), request.POST.get('password', 'FUCK')))
                conn.commit()
            else:
                content.update({"error": "User with this e-mail already exist!", "lastmail": request.POST.get('your_email')})
        else:
            # if correct load collection. else index with error
            curr.execute("select password from reader_user where user_email=(%s)", (request.POST.get('your_email'),))
            if curr.rowcount == 1:
                passwd = curr.fetchone()[0]
                if passwd == request.POST.get('password'):
                    ren = render(request, 'collection.html')
                else:
                    content.update({"error": "Wrong password!", "lastmail":request.POST.get('your_email')})
            else:
                content.update({"error": "User with this e-mail doesn't exist!", "lastmail":request.POST.get('your_email')})
    if ren is None:
        ren = render(request, 'index.html', content)
    return ren
