from django.contrib import admin
from docviewer.admin import DocumentAdmin as Docviewer_DocumentAdmin

from forms import DocumentAdminForm
from models import Document

class DocumentAdmin(Docviewer_DocumentAdmin):

    form = DocumentAdminForm
    fieldsets = [
             ('Document details', {'fields': ['file','title','author','source',
                                          'description','notes',]}),
    ]
    fieldsets.insert(1, Docviewer_DocumentAdmin.fieldsets[1])

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()

admin.site.register(Document, DocumentAdmin)
