from django.conf.urls import patterns, include, url
import mojo
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mojodemo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$',include('mojo.urls')),
    url(r'^upload/', mojo.views.upload),
    url(r'^logout/', mojo.views.logout),
    url(r'^admin/', include(admin.site.urls)),
)
