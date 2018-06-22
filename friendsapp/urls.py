from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'friendsapp.views.home', name='home'),
    # url(r'^friendsapp/', include('friendsapp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^usermgr/', include('usermgr.urls', namespace="usermgr")),
    url(r'^admin/', include(admin.site.urls)),

)
