from copy import deepcopy
from datetime import datetime
#from documents.utils import dup_dirs_and_files
from documents import fss
from celery.task import task
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import utc
from django_zotero.models import Tag
from guardian.shortcuts import assign_perm

@task(default_retry_delay=10, max_retries=5)
def task_clone_document(orig_id, new_id, options):
    from documents.models import Document
    try:
        new = Document.objects.get(id=new_id)
        new.task_start = datetime.utcnow().replace(tzinfo=utc)
        clone_document(orig_id, new_id, options)
        new.status = new.STATUS.copied
        new.task_end = datetime.utcnow().replace(tzinfo=utc)
        new.save()
    except ObjectDoesNotExist, e:
        task_clone_document.retry(exc=e)

def clone_document(orig, new, options):
    # Duplicate directories and files
    orig = Document.objects.get(id=orig_id)
    new = Document.objects.get(id=new_id)
    
    orig_docfile_name = orig.docfile_basename
    orig_docfile_path = orig.docfile.name
    orig_dir_path = orig.get_root_path()
    dest_dir_path = new.get_root_path()
    orig_slug = orig.slug
    dest_slug = new.slug
    fss.clone_tree(
        orig_docfile_name,
        orig_docfile_path,
        orig_dir_path,
        dest_dir_path,
        orig_slug,
        dest_slug
    )
    # Clone pages
    pages = orig.pages_set.all()
    for page in pages:
        new.pages_set.create(
            page=page.page,
            modified=page.modified,
        )
    # Clone annotations
    if options['annotations']:
        anns = orig.annotations_set.all()
        for ann in anns:
            new.annotations_set.create(
                title=ann.title,
                location=ann.location,
                page=ann.page,
                content=ann.content,
                author=ann.author,
            )
    # Clone editions
    if options['editions']:
        clone_all_editions(orig, new)
    else:
        clone_only_primitive_editions(orig, new)
    # Clone zotero tags
    if options['zotero']:
        z_tags = Tag.get_tags(orig)
        for tag in z_tags:
            new_t = deepcopy(tag)
            new_t.id = None
            new_t.pk = None
            new_t.set_object(new)
#                new_t.save() Not necessary - set_object saves the object
    # Copy collaborators
    if options['collaborators']:
        collabs = orig.get_users_with_perms()
        for collab in collabs:
            assign_perm('documents.access_document', collab, new)
    # Copy taggit tags
    if options['tags']:
        t_tags = orig.taggit_tags.all()
        for tag in t_tags:
            new.taggit_tags.add(tag.name)


def clone_all_editions(orig, new):
    edits = orig.editions_set.all()
    for edit in edits:
        new.editions_set.create(
            date=edit.date,
            date_string=edit.date_string,
            modified_pages=clone_modified_pages(
                edit.modified_pages,
                orig,
                new,
            ),
            comment=edit.comment,
            author=edit.author,
        )


def clone_only_primitive_editions(orig, new):
    original = '0'*20
    current = '9'*20
    sql = "date_string='" + original + "' OR date_string='" + current + "'"
    edits = orig.editions_set.extra(where=[sql])
    for edit in edits:
        new.editions_set.create(
            date=edit.date,
            date_string=edit.date_string,
            modified_pages=clone_modified_pages(
                edit.modified_pages,
                orig,
                new,
            ),
            comment=edit.comment,
            author=edit.author,
        )


def clone_modified_pages(modified_pages, orig, new):
    new_pages = {}
    for k in modified_pages:
        orig_url = modified_pages[k]
        new_url = orig_url.replace(
            '/' + str(orig.id) + '/', '/' + str(new.id) + '/'
        )
        new_pages[k] = new_url
    return new_pages
