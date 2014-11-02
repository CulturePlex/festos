import os
import re
#from django.core.files.storage import FileSystemStorage
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

def rename_files_recursively(directory, old, new):
#    import ipdb;ipdb.set_trace()
    for elem in os.listdir(directory):
        path = os.path.join(directory, elem)
        if os.path.isfile(path):
#            import ipdb;ipdb.set_trace()
            old_name = path
            new_name = old_name.replace(old, new)
            os.rename(old_name, new_name)
        elif os.path.isdir(path) and not elem.startswith('.'):
            subdir = path
            rename_files_recursively(subdir, old, new)

def dup_dirs_and_files(fs, orig_dir_path, dest_dir_path, orig_slug, dest_slug):
#    os.makedirs(dest_dir_path)
    listdir = fs.listdir(orig_dir_path)
    
    dir_list = listdir[0]
    for d in dir_list:
        next_orig_dir_path = os.path.join(orig_dir_path, d)
        next_dest_dir_path = os.path.join(dest_dir_path, d)
        dup_dirs_and_files(
            fs,
            next_orig_dir_path,
            next_dest_dir_path,
            orig_slug,
            dest_slug
        )
    
    file_list = listdir[1]
    for f in file_list:
        orig_name = f
        dest_name = f.replace(orig_slug, dest_slug)
        orig_file_path = os.path.join(orig_dir_path, orig_name)
        dest_file_path = os.path.join(dest_dir_path, dest_name)
        orig = fs.open(orig_file_path, 'r')
#        dest = fs.open(dest_file_path, 'w')
#        dest.write(orig.read())
        fs.save(dest_file_path, orig)
