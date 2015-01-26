import os
import shutil
from datetime import date

from django.core.files.storage import get_storage_class


fs = get_storage_class()()
opened_files = {}


def open_file(path, mode='rb'):
    if not opened_files.get(path):
        f = fs.open(path, mode)
        opened_files[path] = f
    else:
        f = opened_files[path]
    return f


def close_file(path):
    f = opened_files[path]
    f.close()
    del opened_files[path]


def read_file(path):
    f = open_file(path)
    content = f.read()
    close_file(path)
    return content


def write_file(src, dst):
    f1 = open_file(src)
    f2 = open_file(dst, 'w')
    f2.write(f1.read())
    close_file(src)


def write_content(src, dst):
    f = open_file(dst, 'w')
    f.write(src)


def copy_file(src, dst):
    f = open_file(src)
    fs.save(dst, f)
    close_file(src)


def delete_file(path):
    fs.delete(path)


def listdir(path):
    return fs.listdir(path)


def exists(path):
    return fs.exists(path)


def clone_tree(
        src_docfile_name,
        src_docfile_path,
        src_path,
        dst_path,
        src_slug,
        dst_slug):
    
    def clone_pdf_tree(src_docfile_name, src_docfile_path, src_slug, dst_slug):
        today = date.today()
        year = today.year
        month = today.month
        day = today.day
        dst_docfile_name = src_docfile_name.replace(src_slug, dst_slug)
        dst_docfile_path = os.path.join(
            settings.MEDIA_ROOT,
            'pdf',
            year,
            month,
            day,
            dst_docfile_name
        )
        copy_file(src_docfile_path, dst_docfile_path)
    
    def clone_doc_tree(src_path, dst_path, src_slug, dst_slug):
        list_dir = listdir(src_path)
        
        dir_list = list_dir[0]
        for d in dir_list:
            next_src_path = os.path.join(src_path, d)
            next_dst_path = os.path.join(dst_path, d)
            clone_doc_tree(next_src_path, next_dst_path, src_slug, dst_slug)
        
        file_list = list_dir[1]
        for f in file_list:
            src_name = f
            dst_name = f.replace(src_slug, dst_slug)
            src_file_path = os.path.join(src_path, src_name)
            dst_file_path = os.path.join(dst_path, dst_name)
            copy_file(src_file_path, dst_file_path)
    
    clone_pdf_tree(src_docfile_name, src_docfile_path, src_slug, dst_slug)
    clone_doc_tree(src_path, dst_path, src_slug, dst_slug)


def remove_tree(path):
    def remove_tree_aux(path):
        if exists(path):
            list_dir = listdir(path)
            
            dir_list = list_dir[0]
            for d in dir_list:
                next_path = os.path.join(path, d)
                remove_tree_aux(next_path)
            
            file_list = list_dir[1]
            for f in file_list:
                file_path = os.path.join(path, f)
                delete_file(file_path)
    
    remove_tree_aux(path)
    shutil.rmtree(path, ignore_errors=True)
