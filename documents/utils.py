import os
import re
from datetime import date
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.template import Context, loader
from docviewer.utils import create_email
from haystack.utils import Highlighter

from documents import fss


class CompleteHighlighter(Highlighter):
    def render_html(self, highlight_locations=None, start_offset=None, end_offset=None):
        highlighted_chunk = self.text_block[start_offset:end_offset]

        for word in self.query_words:
            highlighted_chunk = highlighted_chunk.replace(word, 'Bork!')

        return highlighted_chunk


def _total_pages_a(document):
    version_re = re.compile(r'^.*-([0-9]{20})\.txt$')
    path = document.get_root_path()
    elems = [
        path+'/'+e for e in fss.listdir(path)
            if e[-4:] == '.txt' and
               e != "%s.txt" % document.slug and
               not version_re.match(e)
    ]
    return elems


def _total_pages_b(document):
    try:
        path = document.get_root_path() + '/700x'
        elems = fss.listdir(path)
    except OSError:
        path = document.get_root_path() + '/normal'
        elems = fss.listdir(path)
    except:
        elems = []
    return elems


def _is_processed(f):
#    return os.path.getmtime(f) != os.path.getctime(f)
    return os.path.getsize(f) != 1


def count_total_pages(document):
    elems = _total_pages_b(document)
    return len(elems)


def count_processed_pages(document):
#    elems = [e for e in _total_pages(document) if _is_processed(e)]
    elems = [e for e in _total_pages_a(document) if _is_processed(e)]
    return len(elems)


def send_email(author, collaborator, document):
    email_content = create_email(author, collaborator, document)
    user_target = User.objects.get(username=collaborator)
    emails = [collaborator.email]
    try:
        send_mail(
            settings.PROJECT_NAME + \
                ' - %s has added you as collaborator' % author,
            email_content,
            settings.DEFAULT_FROM_EMAIL,
            emails,
            fail_silently=False
        )
    except Exception as e:
        'email could not be sent.'


def create_email(author, collaborator, document):
    title = document.title
    filename = document.docfile_basename
    doc_url = get_absolute_url(reverse(
        "docviewer_viewer_view",
        kwargs={'pk': document.pk, 'slug': document.slug}
    ))
    template = loader.get_template('email_add_collaborator.html')
    context = Context({
        'username': author,
        'collaborator': collaborator,
        'document': '{} - {}'.format(title, filename),
        'url': doc_url,
    })
    message = template.render(context)
    return message


def get_absolute_url(relative_url):
    SITE = Site.objects.get_current()
    if relative_url and (relative_url[0:7] == 'http://' or relative_url[0:8] == 'https://'):
        return relative_url
    return "http://%s%s" % (SITE.domain, relative_url)
