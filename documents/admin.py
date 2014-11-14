from django.contrib import admin
from docviewer.admin import DocumentAdmin as Docviewer_DocumentAdmin

from forms import DocumentAdminForm
from models import Document
from django_zotero.admin import TagInlineAdmin


class DocumentInline(admin.StackedInline):
    """
    Inline admin for the document
    """
    model = Document
    max_num = 1

    form = DocumentAdminForm
    readonly_fields = (
        'status', 'page_count', 'filename', 'task_id', 'task_error',
        'task_start', 'task_end')
    fieldsets = [
        ('Document details', {'fields': [
            'docfile', 'language', 'title', 'author', 'source',
            'description', 'notes', 'owner']
        }),
    ]
    fieldsets.insert(1, Docviewer_DocumentAdmin.fieldsets[1])


class DocumentAdmin(Docviewer_DocumentAdmin):
    """
    Admin for the document
    """
    form = DocumentAdminForm
    inlines = (TagInlineAdmin,)
    list_display = ['title', 'status', 'task_start', 'task_end', 'task_error']
    fieldsets = [
        ('Document details', {'fields': [
            'docfile', 'language', 'public', 'source', 'notes']}),
    ]
    fieldsets.insert(1, Docviewer_DocumentAdmin.fieldsets[1])

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()

admin.site.register(Document, DocumentAdmin)
