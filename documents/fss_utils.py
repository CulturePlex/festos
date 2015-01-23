import os
import shutil

from django.core.files.storage import get_storage_class


fs = get_storage_class()
opened_files = {}


def open_file(path, mode='rb'):
    if opened_files.get(path) == None:
        f = fs.open(path, mode)
        opened_files[path] = f
    else:
        f = opened_files[path]
    return f


def close_file(path):
    f = opened_files[path]
    f.close()


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


def listdir(path):
    return fs.listdir(path)
