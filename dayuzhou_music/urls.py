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
    url(r'^$','dayuzhou_music.views.index'),
    url(r'^bound/xiami/taobao/$','dayuzhou_music.bounder.bound_xiami_taobao'),
    url(r'^bound/xiami/$','dayuzhou_music.bounder.bound_xiami'),
    #TOTEST
    url(r'^bound/netease/$','dayuzhou_music.bounder.bound_netease'),
    #TODO
    url(r'^login/$','dayuzhou_music.user.login'),
    url(r'^register/$','dayuzhou_music.user.register'),
    url(r'^findpasswd/$','dayuzhou_music.user.findpasswd'),

    url(r'^home/setting/$','dayuzhou_music.user.user_setting'),
    url(r'^home/$','dayuzhou_music.user.user_home'),
)

urlpatterns += staticfiles_urlpatterns()
