from django.contrib import admin
from docviewer.admin import DocumentAdmin as Docviewer_DocumentAdmin

from forms import DocumentAdminForm
from models import Document, Reference


class DocumentInline(admin.StackedInline):
    """
    Inline admin for the document
    """
    model = Document
    max_num = 1

    form = DocumentAdminForm
    readonly_fields = (
        'status', 'page_count', 'filename', 'task_id', 'task_error',
        'task_start')
    fieldsets = [
        ('Document details', {'fields': [
            'file', 'title', 'author', 'source', 'description', 'notes',
            'owner']
        }),
    ]
    fieldsets.insert(1, Docviewer_DocumentAdmin.fieldsets[1])


class DocumentAdmin(Docviewer_DocumentAdmin):
    """
    Admin for the document
    """
    form = DocumentAdminForm
    fieldsets = [
        ('Document details', {'fields': [
            'file', 'title', 'author', 'source', 'description', 'notes']}),
    ]
    fieldsets.insert(1, Docviewer_DocumentAdmin.fieldsets[1])

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()
        file = form.cleaned_data['file']
        obj.set_file(file=file, filename=file.name)


class ReferenceAdmin(admin.ModelAdmin):
    """
    Inline admin for the reference
    """
    inlines = (DocumentInline,)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()

    def save_formset(self, request, form, formset, change):

        if formset.model != Document:
            return super(ReferenceAdmin, self).\
                save_formset(request, form, formset, change)

        instances = formset.save(commit=False)
        for (counter, instance) in enumerate(instances):
            instance.save()
            file = formset.cleaned_data[counter]['file']
            instance.set_file(file=file, filename=file.name)

        formset.save_m2m()


#admin.site.register(Document, DocumentAdmin)
admin.site.register(Reference, ReferenceAdmin)
