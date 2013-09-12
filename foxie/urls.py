from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from foxie.apps.main.views import Home, Login, Logout, Profile, YipView, FollowView, TrendingView, Account
from foxie.apps.registration.views import Register

urlpatterns = patterns('',
    # Examples:
    url(r'^$', Home.as_view(), name='home'),
    url(r'^login/$', Login.as_view(), name="login"),
    url(r'^logout/$', Logout.as_view(), name="logout"),
    url(r'^profile/$', Profile.as_view(), name="profile"),
    url(r'^profile/(?P<username>)/$', Profile.as_view(), name="profile"),
    url(r'^yip/$', YipView.as_view(), name="yip"),
    url(r'^follow/$', FollowView.as_view(), name="follow"),
    url(r'^trending/$', TrendingView.as_view(), name="trending"),
    url(r'^trending/(?P<name>\w+)/$', TrendingView.as_view(), name="trending_query"),
    url(r'^register/$', Register.as_view(), name="register"),
    url(r'^account/$', Account.as_view(), name="account"),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

if not settings.DEBUG:
    urlpatterns += patterns('',
            (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
        )
