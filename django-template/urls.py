from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()]

urlpatterns = patterns('',
    url(r'', include('apps.urls')),

    # url(r'^fashionstop/', include('fashionstop.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
	from django.contrib.staticfiles.urls import staticfiles_urlpatterns
	urlpatterns += staticfiles_urlpatterns()