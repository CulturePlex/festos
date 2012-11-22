from haystack import indexes
from docviewer.search_indexes import PageIndex
from docviewer.models import Page


class BookPageIndex(PageIndex, indexes.Indexable):
    title = indexes.CharField(model_attr='document__title')
    document = indexes.CharField(model_attr='document__description')
    author = indexes.CharField(model_attr='document__book__author')
    notes = indexes.CharField(model_attr='document__book__notes')
