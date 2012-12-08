from django.conf import settings
from django.conf.urls import patterns, include, url
from books.views import SearchBookView, add_book


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
    url(r'^$', 'books.views.list_books', name='list_books'),
    url(r'^add/', 'books.views.add_book', name='add_book'),
    url(r'^edit/(?P<pk>\d+)/', 'books.views.edit_book', name='edit_book'),
    url(r'^remove/(?P<pk>\d+)/', 'books.views.remove_book', name='remove_book'),

)
