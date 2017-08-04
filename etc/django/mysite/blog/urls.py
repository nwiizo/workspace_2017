from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.post_list),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^year', views.school, name='school'),
    url(r'^school/(?P<s_year>[0-9]+)/$', views.post_school, name='post_school'),    
    url(r'^edit/', views.edit, name='edit'),
    url(r'^fin/', views.fin, name = 'fin'),
    ]
