from django.conf.urls import patterns, include, url
from django.conf import settings


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^users/login$', 'login.views.login'),
    url(r'^users/add$', 'login.views.add'),
    url(r'^TESTAPI/resetFixture$', 'login.views.resetFixture'),
    url(r'^TESTAPI/unitTests$', 'login.views.unittestControll'),
    url(r'(?P<path>client\.\w+$)', 'django.views.static.serve', {"document_root": settings.STATIC_ROOT})
 
)
