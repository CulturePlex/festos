# Create your views here.
from operator import itemgetter
from haystack.views import basic_search, SearchView
from books.models import Book
from django.utils.datastructures import SortedDict 


def book_home(request):
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

    return basic_search(request, 
              extra_context={ 'titles': titles, 
                              'authors': authors, 
                              'sources': sources})


def book_search(request):

#    import ipdb; ipdb.set_trace()
    return basic_search(request, 
           template = 'search/results.html')


class SearchBookView(SearchView):
    def get_results(self):
        """
        Fetches the results via the form.

        Returns an empty list if there's no query to search with.
        """
        results = self.form.search()

#        filterfields = {}
#        if (self.request.GET.get('author')):
#            filterfields['author'] = self.request.GET.get('author')

        if (self.request.GET.get('author')):
            results = results.filter(author=self.request.GET.get('author'))
        if (self.request.GET.get('title')):
            results = results.filter(title=self.request.GET.get('title'))
        if (self.request.GET.get('source')):
            results = results.filter(source=self.request.GET.get('source'))
        if (self.request.GET.get('description')):
            results = results.filter(description=self.request.GET.get('description'))
        if (self.request.GET.get('notes')):
            results = results.filter(notes=self.request.GET.get('notes'))

        #import ipdb; ipdb.set_trace()

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
                'documents': documents}
