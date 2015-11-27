from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'liberte_music.views.home', name='home'),
    # url(r'^liberte_music/', include('liberte_music.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^search/','liberte_music.search.search'),
    url(r'^get_link/','liberte_music.song.get_link'),
    url(r'^get_playlist_links/','liberte_music.song.get_playlist_links'),
    url(r'^add_to_playlist/','liberte_music.song.add_to_playlist'),
    url(r'^more/$','liberte_music.views.index'),
    url(r'^more/playlist/$','liberte_music.views.index_playlist'),
    url(r'^bound/xiami/taobao/$','liberte_music.bounder.bound_xiami_taobao'),
    url(r'^bound/xiami/$','liberte_music.bounder.bound_xiami'),
    url(r'^unbound/xiami/$','liberte_music.bounder.unbound_xiami'),
    url(r'^unbound/netease/$','liberte_music.bounder.unbound_netease'),
    url(r'^login/$','liberte_music.user.login'),
    url(r'^logout/$','liberte_music.user.logout'),
    url(r'^register/$','liberte_music.user.register'),
    #TODO
    url(r'^findpasswd/$','liberte_music.user.findpasswd'),
    url(r'^setting/$','liberte_music.user.user_setting'),
    url(r'^$','liberte_music.user.main'),
    url(r'^home/$','liberte_music.user.user_home'),
    url(r'^home/xiami/(?P<page>\d+)/$','liberte_music.user.user_home_xiami'),
    url(r'^home/xiami/$','liberte_music.user.user_home_xiami'),
    url(r'^home/netease/$','liberte_music.user.user_home_netease'),

    url(r'^bound/netease/$','liberte_music.bounder.bound_netease'),

    url(r'^netease/playlist/(?P<id_>\d+)/$','liberte_music.detail.netease_playlist'),
    url(r'^xiami/playlist/(?P<id_>\d+)/$','liberte_music.detail.xiami_playlist'),
    url(r'^xiami/album/(?P<id_>\d+)/$','liberte_music.detail.xiami_album'),
    url(r'^netease/album/(?P<id_>\d+)/$','liberte_music.detail.netease_album'),
   
    #test
   #url(r'^test_put/$','liberte_music.song.test_put'),
    #url(r'^test_get/$','liberte_music.song.test_get'),
    #url(r'^test_open/$','liberte_music.song.test_open'),
    #url(r'^add_song/$','liberte_music.song.add_song'),
)

urlpatterns += staticfiles_urlpatterns()
