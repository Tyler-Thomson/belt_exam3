from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),

    url(r'^createUser$', views.createUser),
    url(r'^success$', views.success),

    url(r'^login$', views.login),
    url(r'^logout$', views.logout),

    url(r'^addFriend/(?P<id>\d+)$', views.addFriend),
    url(r'^removeFriend/(?P<id>\d+)$', views.removeFriend),
    url(r'^viewUser/(?P<id>\d+)$', views.viewUser),

]
