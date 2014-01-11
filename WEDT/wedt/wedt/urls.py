from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wedt.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'wedt.views.main'),
    url(r'^search$', 'wedt.views.search'),
    url(r'^admin/', include(admin.site.urls)),
)