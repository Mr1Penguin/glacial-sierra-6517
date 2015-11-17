from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^collection/$', views.collection, name='collection'),
    url(r'^collection/load_site/$', views.load_site, name='load_site')
]
