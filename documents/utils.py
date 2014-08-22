import os
import re
from haystack.utils import Highlighter


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
        path+'/'+e for e in os.listdir(path)
            if e[-4:] == '.txt' and
               e != "%s.txt" % document.slug and
               not version_re.match(e)
    ]
    return elems


def _total_pages_b(document):
    try:
        path = document.get_root_path() + '/700x'
        elems = os.listdir(path)
    except OSError:
        path = document.get_root_path() + '/normal'
        elems = os.listdir(path)
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
