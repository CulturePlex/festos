from django.core.management.base import BaseCommand, CommandError
from django.core.files.uploadedfile import SimpleUploadedFile
from os.path import join
from os import listdir
from books.forms import BookForm



class Command(BaseCommand):
    args = '<path path ...>'
    help = 'Closes the specified poll for voting'

    
    def handle(self, *args, **options):
        for path in args:
          for fname in listdir(path):
              upload_file = open(join(path,fname), 'rb')
              post_dict = {'title': fname, 'author': "Auto Test" }
              file_dict = {'file': SimpleUploadedFile(upload_file.name,
                                  upload_file.read())}
              form = BookForm(post_dict, file_dict)
              if form.is_valid():
                  form.save()
                  file = form.cleaned_data['file']
                  form.instance.set_file(file=file, filename=file.name)

