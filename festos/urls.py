from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from documents.views import search_document

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^viewer/', include('docviewer.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^documents/', include('documents.urls')),
    #url(r'^search/', include('haystack.urls')),
    url(r'^about/', TemplateView.as_view(template_name="about.html"),
        name='about'),
    url(r'^$', search_document, name='index'),
    #url(r'^$', include('haystack.urls')),
)

urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^docs/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.DOCVIEWER_DOCUMENT_ROOT,
            }),
    )
    urlpatterns += patterns(
        '',
        url(
            r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, }),
    )
