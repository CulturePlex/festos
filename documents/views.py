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
from models import Document, Reference
from forms import DocumentForm, EditDocumentForm, SearchDocumentForm, \
                  SearchReferenceForm, ReferenceForm



class SearchDocumentView(SearchView):
    def get_results(self):
        """
        Fetches the results via the form.

        Returns an empty list if there's no query to search with.
        """

        results = self.form.search()

        # if there is no 'q' haystack returns an empty results
        if results.count() == 0 and \
                len(self.request.GET) > 0 and not \
                self.request.GET.has_key('q'):
            results = SearchQuerySet()

        self.vs_query = ""
        if (self.request.GET.has_key('q')):
            self.vs_query += " text:" + self.request.GET.get('q')

        documents_ids = self.get_documents().values_list('id', flat=True)
        results = results.filter(document_id__in = documents_ids)

        return results


    def get_documents(self):
        """ Return the documents accordingly to specific search field """
        documents = Document.objects.all()
        if self.request.user.is_authenticated():
            documents = documents.filter(Q(owner_id = self.request.user.id) | 
                                 Q(public = True))
        else:
            documents = documents.filter(public = True)

        form=SearchDocumentForm(self.request.GET)
        if form.is_valid():
            opts = {}
            for key in form.cleaned_data:
                if form.cleaned_data[key] != '':
                    opts[key+'__icontains'] = form.cleaned_data[key]
                    self.vs_query += " " + key + ":" + form.cleaned_data[key]
            documents = documents.filter(**opts)

        references = self.get_references()
        if references:
            documents = documents.filter(reference__in = references )

        return documents


    def get_references(self):
        """ Return the references accordingly to specific search fields """

        form=SearchReferenceForm(self.request.GET)
        self.refs_fields = {}
        if form.is_valid():
            opts = {}
            for key in form.cleaned_data:
                if form.cleaned_data[key] != '':
                    opts[key+'__icontains'] = form.cleaned_data[key]
                    self.refs_fields[key.capitalize()] = form.cleaned_data[key]
                    self.vs_query += " " + key + ":" + form.cleaned_data[key]
            return Reference.objects.all().filter(**opts)
        return None



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
                'refs_fields': self.refs_fields,
                'url_query': cp.urlencode }


search_document = SearchDocumentView(form_class=SearchForm)

@login_required
def list_documents(request):
    """ List the documents for the current user """

    documents = Document.objects.filter(owner=request.user)

    return render_to_response('list_documents.html', {
                                'documents': documents,
                                }, context_instance=RequestContext(request))


@login_required
def add_document(request):
    """ Add a document """
    dform = DocumentForm(user=request.user)
    rform = ReferenceForm()
    if request.method == 'POST':
        rform = ReferenceForm(request.POST)
        dform = DocumentForm(request.POST, request.FILES, user=request.user)
        #this avoids ignoring the evaluation of the form to show the errors
        rf_is_valid = rform.is_valid()
        df_is_valid = dform.is_valid()
        if rf_is_valid and df_is_valid:
            rform.save()
            dform.instance.reference = rform.instance
            dform.save()
            file = dform.cleaned_data['file']
            dform.instance.set_file(file = file, filename=file.name)
            return HttpResponseRedirect(reverse('documents.views.list_documents'))

    return render_to_response('add_document.html', {
                                'dform': dform,
                                'rform': rform,
                                }, context_instance=RequestContext(request))


@login_required
def edit_document(request, pk):
    """ Edit a document """
    document = Document.objects.get(pk=pk)
    eform = EditDocumentForm(instance = document)
    rform = ReferenceForm(instance = document.reference)
    if request.method == 'POST':
        rform = ReferenceForm(request.POST, instance = document.reference)
        eform = EditDocumentForm(request.POST, instance=document)
        #this avoids ignoring the evaluation of the form to show the errors
        rf_is_valid = rform.is_valid()
        ef_is_valid = eform.is_valid()
        if rf_is_valid and ef_is_valid:
            rform.save()
            eform.instance.reference = rform.instance
            eform.save()
            return HttpResponseRedirect(reverse('documents.views.list_documents'))

    return render_to_response('edit_document.html', {
                                'document': document,
                                'rform': rform,
                                'eform': eform,
                                }, context_instance=RequestContext(request))


@login_required
def remove_document(request, pk):
    """ Remove a document """

    document = Document.objects.get(pk=pk)
    # Delete the dependant document first
    document.reference.delete()
    return HttpResponseRedirect(reverse('documents.views.list_documents'))



@login_required
def change_privacy_document(request, pk):
    """ Change the privacy of a document """

    document = Document.objects.get(pk=pk)
    document.public = not document.public
    document.save()
    return HttpResponseRedirect(reverse('documents.views.list_documents'))
