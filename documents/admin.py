from django.contrib import admin
from docviewer.admin import DocumentAdmin as Docviewer_DocumentAdmin

from forms import DocumentAdminForm
from models import Document, Reference


class DocumentAdmin(Docviewer_DocumentAdmin):

    form = DocumentAdminForm
    fieldsets = [
             ('Document details', {'fields': ['file','title','author','source',
                                          'description','notes','reference',
                                          'owner']}),
    ]
    fieldsets.insert(1, Docviewer_DocumentAdmin.fieldsets[1])

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


admin.site.register(Document, DocumentAdmin)
admin.site.register(Reference)
