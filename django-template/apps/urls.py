from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.static import serve
# Un/comment the next two lines to enable or disable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	# Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
	# Serve static
	from django.contrib.staticfiles.urls import staticfiles_urlpatterns
	urlpatterns += staticfiles_urlpatterns()

	# Serve Media
	urlpatterns += patterns('',
		(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
	)