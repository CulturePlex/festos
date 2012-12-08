from haystack import indexes
from docviewer.search_indexes import PageIndex
from docviewer.models import Page


class BookPageIndex(PageIndex, indexes.Indexable):
    title = indexes.CharField(model_attr='document__title')
    description = indexes.CharField(model_attr='document__description')
    source = indexes.CharField(model_attr='document__book__source')
    author = indexes.CharField(model_attr='document__book__author')
    notes = indexes.CharField(model_attr='document__book__notes')
    public = indexes.BooleanField(model_attr='document__book__public')
    owner_id = indexes.IntegerField(model_attr='document__book__owner__id')
