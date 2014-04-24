from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
	#url(r'^$', LandingPageView.as_view(), name='landing_page'),
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
