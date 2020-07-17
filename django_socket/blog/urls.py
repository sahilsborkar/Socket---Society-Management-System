from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('soclist', views.soclist, name='blog-soclist'),
    re_path(r'^sochome/(?P<oid>[0-9]+)/$', views.sochome, name='blog-sochome')
]