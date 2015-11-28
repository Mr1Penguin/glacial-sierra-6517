from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^collection/$', views.collection, name='collection'),
    url(r'^collection/load_site/$', views.load_site, name='load_site'),
    url(r'^collection/add_site/$', views.add_site, name='add_site'),
    url(r'^collection/delete_site/$', views.delete_site, name='delete_site'),
    url(r'^restore/$', views.restore, name='restore')
]
