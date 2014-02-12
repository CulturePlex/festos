# Create your views here.
from celery.task.control import revoke
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import SortedDict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response, HttpResponse, redirect
from django.contrib.auth.models import User

from guardian.shortcuts import assign_perm, get_objects_for_user, remove_perm
from guardian.decorators import permission_required_or_403
from haystack.views import SearchView
from haystack.query import SearchQuerySet
from haystack.forms import SearchForm
from models import Document
from forms import DocumentForm, EditDocumentForm, SearchDocumentForm

from django_zotero.forms import get_tag_formset

import simplejson as json
from taggit.models import Tag
from docviewer.models import Annotation
from utils import count_processed_pages, count_total_pages


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
                'q' in self.request.GET:
            results = SearchQuerySet()

        self.vs_query = ""
        if ('q' in self.request.GET):
            self.vs_query += " text:" + self.request.GET.get('q')
        documents_ids = self.get_documents().values_list('id', flat=True)
        results = results.filter(document_id__in=documents_ids)
        return results

    def get_documents(self):
        """ Return the documents accordingly to specific search field """
        documents = Document.objects.all()
        if self.request.user.is_authenticated():
            permited_docs = get_objects_for_user(
                self.request.user,
                'documents.access_document',
                Document,
                use_groups=True).values_list('id', flat=True)
            documents = \
                documents.filter(Q(id__in=permited_docs) | Q(public=True))
        else:
            documents = documents.filter(public=True)
        
        form = SearchDocumentForm(self.request.GET)
        if form.is_valid():
            opts = {}
            for key in form.cleaned_data:
                data = form.cleaned_data[key]
                if data != '':
                    if key == 'annotations':
                        documents = \
                            documents.filter(
                                Q(annotations_set__title__icontains=data) |
                                Q(annotations_set__content__icontains=data)
                            )
                    elif key == 'tags':
                        documents = documents.filter(taggit_tags__name=data)
                    else:
                        opts[key + '__icontains'] = data
                    self.vs_query += " " + key + ":" + data
            documents = documents.filter(**opts)

#        references = self.get_references()
#        if references:
#            documents = documents.filter(reference__in=references)

        return documents

#    def get_references(self):
#        """ Return the references accordingly to specific search fields """
#        form = SearchReferenceForm(self.request.GET)
#        self.refs_fields = {}
#        if form.is_valid():
#            opts = {}
#            for key in form.cleaned_data:
#                if form.cleaned_data[key] != '':
#                    opts[key + '__icontains'] = form.cleaned_data[key]
#                    self.refs_fields[key.capitalize()] =\
#                        form.cleaned_data[key]
#                    self.vs_query += " " + key + ":" +\
#                        form.cleaned_data[key]
#            return Reference.objects.all().filter(**opts)
#        return None

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
                documents[r.document_id] = {
                    'id': r.object.document.id,
                    'document': r.object.document.document,
                    'pages': [r.object]
                }

        paginator = Paginator(documents.items(), 5)
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
        if 'pag' in cp:
            cp.pop('pag')

        return {
            'docs': docs,
            'total': len(documents),
            'vs_query': self.vs_query,
            'refs_fields': None,
            'url_query': cp.urlencode,
            'tags': json.dumps([tag.name for tag in Tag.objects.all()]),
        }


search_document = SearchDocumentView(form_class=SearchForm)


@login_required
def list_documents(request):
    """ List the documents for the current user """
    documents = get_objects_for_user(
        request.user,
        'documents.access_document',
        Document,
        use_groups=True)
#    add running value
    return render_to_response('list_documents.html', {
        'documents': documents,
    }, context_instance=RequestContext(request))


@login_required
@permission_required_or_403('documents.access_document', (Document, 'pk', 'pk'))
def retry_document(request, pk):
    """ Retry to process document when it fails """
    document = Document.objects.get(pk=pk)
    document.status = document.STATUS.waiting
    document.process_file()
    return redirect('list_documents')


@login_required
def add_document(request):
    """ Add a document """
    label_options = {'labels': {'item_type': 'Document type'}}
    dform = DocumentForm(user=request.user)
#    rform = ReferenceForm()
    tag_formset = get_tag_formset(**label_options)
    if request.method == 'POST':
#        rform = ReferenceForm(request.POST)
        dform = DocumentForm(request.POST, request.FILES, user=request.user)
        tag_formset = get_tag_formset(dform.instance, data=request.POST, **label_options)
        #this avoids ignoring the evaluation of the form to show the errors
#        rf_is_valid = rform.is_valid()
        rf_is_valid = True
        df_is_valid = dform.is_valid()
        if rf_is_valid and df_is_valid and tag_formset.is_valid():
#            rform.save()
#            dform.instance.reference = rform.instance
            dform.save()
#            file = dform.cleaned_data['file']
#            dform.instance.seet_file(file=file, filename=file.name)
            assign_perm('documents.access_document', request.user, dform.instance)
            tag_formset.save()
            return HttpResponseRedirect(reverse('documents.views.list_documents'))

    return render_to_response('add_document.html', {
        'dform': dform,
        'rform': None,
        'formset': tag_formset,
    }, context_instance=RequestContext(request))


@login_required
@permission_required_or_403('documents.access_document', (Document, 'pk', 'pk'))
def edit_document(request, pk):
    """ Edit a document """
    label_options = {'labels': {'item_type': 'Document type'}}
    document = Document.objects.get(pk=pk)
    eform = EditDocumentForm(instance=document)
#    rform = ReferenceForm(instance=document.reference)
    tag_formset = get_tag_formset(document, **label_options)
    if request.method == 'POST':
#        rform = ReferenceForm(request.POST, instance=document.reference)
        eform = EditDocumentForm(request.POST, instance=document)
        tag_formset = get_tag_formset(document, data=request.POST, **label_options)
        #this avoids ignoring the evaluation of the form to show the errors
#        rf_is_valid = rform.is_valid()
        rf_is_valid = True
        ef_is_valid = eform.is_valid()
        if rf_is_valid and ef_is_valid and tag_formset.is_valid():
#            rform.save()
#            eform.instance.reference = rform.instance
            eform.save()
            tag_formset.save()
            return HttpResponseRedirect(reverse('documents.views.list_documents'))

    return render_to_response('edit_document.html', {
        'document': document,
        'rform': None,
        'dform': eform,
        'formset': tag_formset,
    }, context_instance=RequestContext(request))


@login_required
@permission_required_or_403('documents.access_document', (Document, 'pk', 'pk'))
def remove_document(request, pk):
    """ Remove a document """
#    try:
    document = Document.objects.get(pk=pk)
    revoke(document.task_id, terminate=True)
    document.document.delete()
    document.delete()
#    except:
#        pass
    return HttpResponseRedirect(reverse('documents.views.list_documents'))


@login_required
@permission_required_or_403('documents.access_document', (Document, 'pk', 'pk'))
def change_privacy_document(request, pk):
    """ Change the privacy of a document """
    document = Document.objects.get(pk=pk)
    document.public = not document.public
    document.save()
    return HttpResponseRedirect(reverse('documents.views.list_documents'))


@login_required
def add_sharer(request):
    """ Add a user that shares the document """
    doc = Document.objects.get(pk=request.GET['doc_id'])
    if not (request.user.has_perm('access_document', doc)):
                raise PermissionDenied
    usr = User.objects.get(username=request.GET['username'])
    assign_perm('documents.access_document', usr, doc)
    return HttpResponse(
        json.dumps({'status': 'ok'}), content_type="application/json")


@login_required
def remove_sharer(request, pk, username):
    """ Removes a user that shares the document """
    doc = Document.objects.get(pk=pk)
    if not (request.user.has_perm('access_document', doc)):
                raise PermissionDenied
    usr = User.objects.get(username=username)
    remove_perm('documents.access_document', usr, doc)
    return HttpResponseRedirect(reverse('documents.views.list_documents'))


@login_required
def autocomplete_users(request, pk):
    """ Autocomplete for adding sharers """
    document = Document.objects.get(pk=pk)
    users = User.objects.exclude(id__in=document.get_users_with_perms())\
                        .exclude(id=-1).exclude(id = document.owner.id)\
                        .filter(username__contains=request.POST['term'])\
                        .values_list('username', flat=True)

    return HttpResponse(json.dumps(list(users)))


@login_required
def add_taggit_tag(request):
    """ Add a taggit_tag to the document """
    doc = Document.objects.get(pk=request.POST['doc_id'])
    if not (request.user.has_perm('access_document', doc)):
                raise PermissionDenied
    doc.taggit_tags.add(request.POST['tag'])
    return HttpResponse(
        json.dumps({'status': 'ok'}), content_type="application/json")


@login_required
def remove_taggit_tag(request, pk, taggit_tag):
    """ Removes a taggit_tag from the document """
    doc = Document.objects.get(pk=pk)
    if not (request.user.has_perm('access_document', doc)):
                raise PermissionDenied
    doc.taggit_tags.remove(taggit_tag)
    return HttpResponseRedirect(reverse('documents.views.list_documents'))


@login_required
def autocomplete_taggit_tags(request):
    """ Autocomplete for adding taggit_tags """
#    document = Document.objects.get(pk=pk)
#    taggit_tags = Tag.objects.exclude(name__in=document.taggit_tags\
#                        .filter(name__contains=request.POST['term'])\
#                        .values_list('taggit_tags', flat=True)
    taggit_tags = Tag.objects.filter(name__contains=request.POST['term']).values_list('name', flat=True)

    return HttpResponse(json.dumps(list(taggit_tags)))


def progress(request):
    """
    Get the number of progressed pages for this document
    """
    result = {}
    id_list = request.GET.getlist("ids[]")
    for doc_id in id_list:
#        import ipdb; ipdb.set_trace()
        document = Document.objects.get(id=doc_id)
        if document.status == Document.STATUS.starting and \
           not document.page_count:
            num_pages = count_total_pages(document)
            if num_pages > 0:
                document.page_count = num_pages
                document.status = Document.STATUS.running
                document.save()
        if document.status == Document.STATUS.running:
            num_pages = count_processed_pages(document)
            total_pages = document.page_count
        else:
            num_pages = 0
            total_pages = 0
        
        result[doc_id] = {
            'status': document.status,
            'num_pages': num_pages,
            'total_pages': total_pages,
            'error': document.task_error,
            'position': get_position(document),
        }
    
    return HttpResponse(
        json.dumps(result),
        content_type="application/json",
    )


def get_position(document):
    waiting_documents = Document.waiting.all()
    ids = map(lambda x: x.id, waiting_documents)
    if document.id in ids:
        position = ids.index(document.id) + 1
    else:
        position = None
    return position
