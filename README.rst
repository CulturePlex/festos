Festos
======

Festos is an infrastructure for scanning, OCR'ing and make searchable texts.


                                             
Installation of system dependencies:
------------------------------------

1) Install all the packages (the next line has been tried only in Ubuntu 12.04 64b and 12.10 64b)::

    $ sudo apt-get install rabbitmq-server rubygems graphicsmagick poppler-utils pdftk ghostscript tesseract-ocr yui-compressor git python-pip python-dev build-essential npm openjdk-7-jre -y

2) You need to install docsplit. Then the docsplit:

    a) Install::

        $ sudo gem install docsplit

    b) Try it::

        $ docsplit

    c) This is part of the django-docviewer configuration::

        $ sudo ln -s /usr/local/bin/docsplit /usr/bin/docsplit
        $ sudo ln -s /usr/bin/yui-compressor /usr/local/bin/yuicompressor

3) Install yuglify::

    npm install yuglify

4) Install the elasticsearch::
  
    $ cd ~
    $ wget https://github.com/downloads/elasticsearch/elasticsearch/elasticsearch-0.19.11.deb
    $ sudo dpkg -i elasticsearch-0.19.11.deb

Deploy the project:
-------------------

1) Install the virtual environment:

    a) Install the packages::

        $ sudo pip install --upgrade pip 
        $ sudo pip install --upgrade virtualenv 
        $ sudo pip install virtualenvwrapper
        
    b) Create your .venv directory::

        $ mkdir -p ~/.venvs

    c) You need to configure the environment::

        $ export WORKON_HOME=~/.venvs
        $ source /usr/local/bin/virtualenvwrapper.sh
    
    d) Add the lines to your .bashrc file so the next time your environment is ready::

      i) Opent the .bashrc::

            $ pico .bashrc

      ii) Opent the .bashrc::

            export WORKON_HOME=~/.venvs
            source /usr/local/bin/virtualenvwrapper.sh

    e) Create a virtualenv for the project::

        $ mkvirtualenv festos --no-site-packages

    f) Try it::

        $ workon festos
        $ deactivate

2) Install the project:

    a) Download it::

        $ cd $HOME
        $ git clone https://github.com/CulturePlex/festos.git git/festos

    b) Enter in the new location and update the virtual environment previously created::

        $ cd git/festos/

    c) Set the .gitignore_global to ignore unnecessary files and extensions::

        $ git config --global core.excludesfile .gitignore_global

    d) Install the requierements of the project::

        $ workon festos
        $ pip install -U -r requirements.txt

3) Create database and launch:

    a) You must create a database, user and configure the site. If your are in developing stage, you can use the start_all.sh script::

        $ ./start-all.sh

    b) If you want to launch your site again, just use the following one:

        $ python manage.py runserver localhost:8000

    c) Access the site in the URL http://localhost:8000/

                                             
Testing the installation:
-------------------------

1) Go to the following address (login with user "festos" and password "festos" or if you didn't use the ./start-all.sh then use the one you created)::

    localhost:8000/admin/sites/site/1/

2) Check the domain name is correct ("localhost:8000" if you are developing). Change it to whatever you need. You will need to restart the server to reflex the changes::

    $ python manage.py runserver localhost:8000

3) In another terminal run the celery service::

    $ python manage.py celery worker

4) Add a scanned pdf (for convenience, there is one in ~/git/festos/test.pdf) document in the admin interface::

    localhost:8000/admin/document/

5) You will need to wait a few seconds while docsplit splits the document and elasticsearch index it. You can see the status in the admin interface. When the status is 'ready', you can search in the following URL (make sure you search with an appropiate term that is insider your pdf)::

    localhost:8000/search/

6) You can also try accessing the document directly::

    Access the document : http://localhost:8000/viewer/1/demo.html
