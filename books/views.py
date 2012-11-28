# Create your views here.

from django.utils.datastructures import SortedDict 
from haystack.views import basic_search, SearchView
from haystack.query import SearchQuerySet
from books.models import Book

class SearchBookView(SearchView):
    def get_results(self):
        """
        Fetches the results via the form.

        Returns an empty list if there's no query to search with.
        """
        results = self.form.search()

        # if there is no 'q' haystack returns an empty results
       # import ipdb; ipdb.set_trace()
        if results.count() == 0 and len(self.request.GET) > 0:
            results = SearchQuerySet()

        self.vs_query = ""
        if (self.request.GET.get('q')):
            self.vs_query += " text:" + self.request.GET.get('q')
        if (self.request.GET.get('author')):
            results = results.filter(author=self.request.GET.get('author'))
            self.vs_query += " author:" + self.request.GET.get('author')
        if (self.request.GET.get('title')):
            results = results.filter(title=self.request.GET.get('title'))
            self.vs_query += " title:" + self.request.GET.get('title')
        if (self.request.GET.get('source')):
            results = results.filter(source=self.request.GET.get('source'))
            self.vs_query += " source:" + self.request.GET.get('source')
        if (self.request.GET.get('description')):
            results = results.filter(description = \
                          self.request.GET.get('description'))
            self.vs_query += " description:" +\
                          self.request.GET.get('description')
        if (self.request.GET.get('notes')):
            results = results.filter(notes=self.request.GET.get('notes'))
            self.vs_query += " notes:" + self.request.GET.get('notes')

        return results

    def extra_context(self):
        """
        Allows the addition of more context variables as needed.

        Must return a dictionary.
        """
        
        titles = set()
        authors = set()
        sources = set()
        for book in Book.objects.all():
            if book.title != '':
                titles.add(book.title)
            if book.author != '':
                authors.add(book.author)
            if book.source != '':
                sources.add(book.source)

        documents = SortedDict()
        for r in self.results:
            if r.document_id in documents:
                documents[r.document_id].append(r)
            else:
                documents[r.document_id]=[r]

        #toolbar
        #import ipdb; ipdb.set_trace()

        return {'titles': titles, 
                'authors': authors, 
                'sources': sources,
                'documents': documents,
                'vs_query': self.vs_query }
