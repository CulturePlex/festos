from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.template import RequestContext
from books.views import SearchBookView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'books.views.home', name='home'),
    # url(r'^books/', include('books.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^viewer/', include('docviewer.urls')),
    url(r'^accounts/', include('userena.urls')),
    url(r'^books/', include('books.urls')),
    #url(r'^search/', include('haystack.urls')),
    url(r'^$', SearchBookView(), name='book_search'),
    #url(r'^$', include('haystack.urls')),
)

urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^docs/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.DOCVIEWER_DOCUMENT_ROOT,
        }),
   )
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, }),
    )
