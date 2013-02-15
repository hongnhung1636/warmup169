from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^users/login$', 'logincounter.views.login'),
    url(r'^users/add$', 'logincounter.views.add'),
    url(r'^TESTAPI/resetFixture$', 'logincounter.views.reset_fixture'),
    url(r'^TESTAPI/unitTests$', 'logincounter.views.invoke_unittests'),
    
    url(r'(?P<path>client\.\w+$)', 'django.views.static.serve', {"document_root": settings.STATIC_ROOT})
    # url(r'^warmup/', include('warmup.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
