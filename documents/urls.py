from django.conf.urls import patterns, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'documents.views.list_documents', name='list_documents'),
    url(r'^add/', 'documents.views.add_document', name='add_document'),
    url(r'^edit/(?P<pk>\d+)/',
        'documents.views.edit_document', name='edit_document'),
    url(r'^remove/(?P<pk>\d+)/',
        'documents.views.remove_document', name='remove_document'),
    url(r'^change/(?P<pk>\d+)/', 'documents.views.change_privacy_document',
        name='change_privacy_document'),
    url(r"autocomplete_users/(?P<pk>\d+)/$",
        'documents.views.autocomplete_users', name="autocomplete_users"),
    url(r"add_sharer/$", 'documents.views.add_sharer', name="add_sharer"),
    url(r"remove_sharer/(?P<pk>\d+)/(?P<username>.+)/$",
        'documents.views.remove_sharer', name="remove_sharer"),
    url(r"autocomplete_taggit_tags/$",
        'documents.views.autocomplete_taggit_tags', name="autocomplete_taggit_tags"),
    url(r"add_taggit_tag/$", 'documents.views.add_taggit_tag', name="add_taggit_tag"),
    url(r"remove_taggit_tag/(?P<pk>\d+)/(?P<taggit_tag>.+)/$",
        'documents.views.remove_taggit_tag', name="remove_taggit_tag"),
)
