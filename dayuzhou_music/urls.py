from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dayuzhou_music.views.home', name='home'),
    # url(r'^dayuzhou_music/', include('dayuzhou_music.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'search/','dayuzhou_music.search.search'),
    url(r'get_link/','dayuzhou_music.song.get_link'),
)

urlpatterns += staticfiles_urlpatterns()
