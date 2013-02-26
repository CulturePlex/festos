from django.core.exceptions import PermissionDenied
from models import Document

class DocumentGuardianMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path.startswith('/viewer/'):
            document = Document.objects.get(pk=view_kwargs['pk'])
            if not (request.user.has_perm('access_document', document)):
                raise PermissionDenied
        return None
