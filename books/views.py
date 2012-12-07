# Create your views here.
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import SortedDict 
from haystack.views import basic_search, SearchView
from haystack.query import SearchQuerySet
from books.models import Book
from books.forms import BookForm, EditBookForm



class SearchBookView(SearchView):
    def get_results(self):
        """
        Fetches the results via the form.

        Returns an empty list if there's no query to search with.
        """
        results = self.form.search()

        # if there is no 'q' haystack returns an empty results
        #import ipdb; ipdb.set_trace()
        if results.count() == 0 and \
                len(self.request.GET) > 0 and not \
                self.request.GET.get('q'):
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

        documents = SortedDict()
        
        for r in self.results:
            if r.document_id in documents:
                documents[r.document_id]['pages'].append(r.object)
            else:
                documents[r.document_id]={'document': r.object.document,
                                          'notes': r.notes,
                                          'source': r.source,
                                          'description': r.description,
                                          'pages': [r.object] }

        #toolbar
        #import ipdb; ipdb.set_trace()

        return {'documents': documents,
                'vs_query': self.vs_query,
                'query_dict': self.request.GET }

def search_books(search_book_view):
  return search_book_view;


@login_required
def list_books(request):
    """ Add a book """

    form = BookForm()
    books = Book.objects.all()

    return render_to_response('list_books.html', {
                                'books': books,
                                'form': form,
                                }, context_instance=RequestContext(request))


@login_required
def add_book(request):
    """ Add a book """
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            file = form.cleaned_data['file']
            form.instance.set_file(file = file, filename=file.name)
            return HttpResponseRedirect(reverse('books.views.list_books'))

    return render_to_response('add_book.html', {
                                'form': form,
                                }, context_instance=RequestContext(request))

@login_required
def edit_book(request, pk):
    """ Edit a book """
    book = Book.objects.get(pk=pk)
    form = EditBookForm(instance = book)
    if request.method == 'POST':
        form = EditBookForm(request.POST, instance = book)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('books.views.list_books'))

    return render_to_response('edit_book.html', {
                                'book': book,
                                'form': form,
                                }, context_instance=RequestContext(request))
                                
@login_required
def remove_book(request, pk):
    """ Remove a book """

    book = Book.objects.get(pk=pk)
    book.delete()
    return HttpResponseRedirect(reverse('books.views.list_books'))
