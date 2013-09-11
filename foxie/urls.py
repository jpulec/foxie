from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from foxie.apps.main.views import Home, Login, Logout, Profile, YipView, FollowView, TrendingView

urlpatterns = patterns('',
    # Examples:
    url(r'^$', Home.as_view(), name='home'),
    url(r'^login/$', Login.as_view(), name="login"),
    url(r'^logout/$', Logout.as_view(), name="logout"),
    url(r'^profile/$', Profile.as_view(), name="profile"),
    url(r'^yip/$', YipView.as_view(), name="yip"),
    url(r'^follow/$', FollowView.as_view(), name="follow"),
    url(r'^trending/$', TrendingView.as_view(), name="trending"),
    url(r'^trending/(?P<name>)/$', TrendingView.as_view(), name="trending_query"),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
