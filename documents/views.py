# Create your views here.
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import SortedDict 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from haystack.views import basic_search, SearchView
from haystack.query import SearchQuerySet
from haystack.forms import SearchForm
from models import Document
from forms import DocumentForm, EditDocumentForm, SearchDocumentForm



class SearchDocumentView(SearchView):
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
                self.request.GET.has_key('q'):
            results = SearchQuerySet()

        url_query = ""
        self.vs_query = ""

        documents = Document.objects.all()
        if self.request.user.is_authenticated():
            documents = documents.filter(Q(owner_id = self.request.user.id) | 
                                 Q(public = True))
        else:
            documents = documents.filter(public = True)


        if (self.request.GET.has_key('q')):
            self.vs_query += " text:" + self.request.GET.get('q')


        form=SearchDocumentForm(self.request.GET)        
        if form.is_valid():
            opts = {}
            for key in form.cleaned_data:
                if form.cleaned_data[key] != '':
                    opts[key+'__icontains'] = form.cleaned_data[key]
                    self.vs_query += " " + key + ":" + form.cleaned_data[key]
            documents = documents.filter(**opts)


        results = results.filter(document_id__in = \
            documents.values_list('id', flat=True))

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
                documents[r.document_id]={'id': r.object.document.id,
                                          'document': r.object.document.document,
                                          'pages': [r.object] }


        paginator =  Paginator(documents.items(), 5)
        try:
            page = self.request.GET.get('pag')
            docs = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            docs = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), 
            # deliver last page of   results.
            docs = paginator.page(paginator.num_pages)

        cp = self.request.GET.copy()
        if cp.has_key('pag'):
            cp.pop('pag')

        return {'docs': docs,
                'total': len(documents),
                'vs_query': self.vs_query,
                'url_query': cp.urlencode }

#def search_documents(search_document_view):
#  return search_document_view;

search_document = SearchDocumentView(form_class=SearchForm)

@login_required
def list_documents(request):
    """ Add a document """

    documents = Document.objects.filter(owner=request.user)

    return render_to_response('list_documents.html', {
                                'documents': documents,
                                }, context_instance=RequestContext(request))


@login_required
def add_document(request):
    """ Add a document """
    form = DocumentForm(user=request.user)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            file = form.cleaned_data['file']
            form.instance.set_file(file = file, filename=file.name)
            return HttpResponseRedirect(reverse('documents.views.list_documents'))

    return render_to_response('add_document.html', {
                                'form': form,
                                }, context_instance=RequestContext(request))

@login_required
def edit_document(request, pk):
    """ Edit a document """
    document = Document.objects.get(pk=pk)
    form = EditDocumentForm(instance = document)
    if request.method == 'POST':
        form = EditDocumentForm(request.POST, instance = document)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('documents.views.list_documents'))

    return render_to_response('edit_document.html', {
                                'document': document,
                                'form': form,
                                }, context_instance=RequestContext(request))
                                
@login_required
def remove_document(request, pk):
    """ Remove a document """

    document = Document.objects.get(pk=pk)
    document.delete()
    return HttpResponseRedirect(reverse('documents.views.list_documents'))

@login_required
def change_privacy_document(request, pk):
    """ Remove a document """

    document = Document.objects.get(pk=pk)
    document.public = not document.public
    document.save()
    return HttpResponseRedirect(reverse('documents.views.list_documents'))
