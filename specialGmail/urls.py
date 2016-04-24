__author__ = 'RishabhBhatia'
from django.conf.urls import url
from specialGmail.views import listen
urlpatterns = [
    # Product Endpoints
    url(r'text/(?P<text>[^/]+)$', listen.hello),
]
