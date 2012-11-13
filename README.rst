Festos
======

Festos is an infrastructure for scanning, OCR'ing and make searchable texts.


                                             
Installation:
-------------

You need to install docsplit. First the dependences::

  $ sudo apt-get install rabbitmq-server rubygems graphicsmagick poppler-utils pdftk ghostscript tesseract-ocr yui-compressor git python-pip python-dev build-essential npm openjdk-7-jre -y

Then the docsplit::

  $ sudo gem install docsplit

Try it running::

  $ docsplit

This is part of the django-docviewer configuration::

  $ sudo ln -s /usr/local/bin/docsplit /usr/bin/docsplit
  $ sudo ln -s /usr/bin/yui-compressor /usr/local/bin/yuicompressor

Install yuglify::

  npm install yuglify

Now, the elasticsearch::
  
  $ cd ~
  $ wget https://github.com/downloads/elasticsearch/elasticsearch/elasticsearch-0.19.11.deb
  $ sudo dpkg -i elasticsearch-0.19.11.deb


You need is to have installed pip_ and virtualenv_ in your machine::

  $ sudo pip install --upgrade pip 
  $ sudo pip install --upgrade virtualenv 


Then, it's a good option to use virtualenvwrapper_::

  $ sudo pip install virtualenvwrapper

In the instructions given on virtualenvwrapper_, you should to set the working
directory for your virtual environments. First, create your .venv directory::

  mkdir -p ~/.venvs

So, you could add it in the end of your .bashrc file::

  export WORKON_HOME=~/.venvs
  source /usr/local/bin/virtualenvwrapper.sh

Reopen the console. And finally, create a virtualenv for the project::

  $ mkvirtualenv festos --no-site-packages

After you setup your virtual environment, you should be able to enable and
disable it. The system propmt must change where you have it enable::

  $ workon festos
  $ deactivate

Now, if you didn't get the project yet, clone it in your desired location::

  $ cd $HOME
  $ git clone https://github.com/CulturePlex/festos.git git/festos

Enter in the new location and update the virtual environment previously created::

  $ cd git/festos/
  $ workon festos
  $ pip install -U -r requirements.txt

Now you have installed the Django_ project and almost ready to run it. Before that, you must create a database. In developing stage, we use SQLite::

  $ python manage.py syncdb
  
And that is. If you run the project using the standalone development server of
Django_, you could be able to access to the URL http://localhost:8000/::

  $ python manage.py runserver localhost:8000

                                             
Testing the installation:
------------------------

To use it, first you have to go to the followin address (login with the password you introduce in the syncdb step)::

  localhost:8000/admin/sites/site/1/

And change the name and default name domain of the site (usually example.com) to 'localhost:8000'. You will need to restart the server to reflex the changes::

  $ python manage.py runserver localhost:8000

Then, add a scanned pdf (for convenience, there is one in ~/git/festos/test.pdf) document in the admin interface::

  localhost:8000/admin/document/

Generate the document images and 'ocr'ed text with the following command::

  $ python manage.py generate_document $INDEX

$INDEX is the index of the document you just added in the interface. Then, you have to index the processed document::

  $ python manage.py rebuild_index

Now you can search in the following URL::

  localhost:8000/search/




