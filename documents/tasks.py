from documents.utils import dup_dirs_and_files
from celery.task import task
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage

@task(default_retry_delay=10, max_retries=5)
def task_clone_document(orig, new, options):
    from docviewer.helpers import generate_document
    try:
        clone_document(orig, new, options)
    except ObjectDoesNotExist, e:
        task_clone_document.retry(exc=e)

def clone_document(orig, new, options):
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
        edits = orig.editions_set.all()
        for edit in edits:
            new.editions_set.create(
                date=edit.date,
                date_string=edit.date_string,
                modified_pages=edit.modified_pages,
                comment=edit.comment,
                author=edit.author,
            )
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
    # Duplicate directories and files
    fs = FileSystemStorage()
    orig_dir_path = orig.get_root_path()
    dest_dir_path = new.get_root_path()
    orig_slug = orig.slug
    dest_slug = new.slug
    dup_dirs_and_files(
        fs,
        orig_dir_path,
        dest_dir_path,
        orig_slug,
        dest_slug
    )
