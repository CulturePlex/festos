Festos
======

Festos is an infrastructure for scanning, OCR'ing and make searchable texts.


                                             
Installation of system dependencies:
------------------------------------

1) Install all the packages (the next line has been tried only in Ubuntu 12.04 64b and 12.10 64b)::

    sudo apt-get install rabbitmq-server rubygems graphicsmagick poppler-utils pdftk ghostscript tesseract-ocr tesseract-ocr-eng tesseract-ocr-spa-old tesseract-ocr-spa yui-compressor git python-pip python-dev build-essential npm openjdk-7-jre -y

2) You need to install docsplit. Then the docsplit:

   a) Install::

        sudo gem install docsplit

   b) Try it::

       docsplit

   c) This is part of the django-docviewer configuration::

        sudo ln -s /usr/local/bin/docsplit /usr/bin/docsplit
        sudo ln -s /usr/bin/yui-compressor /usr/local/bin/yuicompressor

3) Install yuglify::

    npm config set registry http://registry.npmjs.org/
    npm -g install yuglify

4) Install the elasticsearch::
  
    cd ~
    wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-0.20.5.deb
    sudo dpkg -i elasticsearch-0.20.5.deb

Deploy the project:
-------------------

1) Install the virtual environment:

   a) Install the packages::

        sudo pip install --upgrade pip 
        sudo pip install --upgrade virtualenv 
        sudo pip install virtualenvwrapper
        
   b) Create your .venv directory::

        mkdir -p ~/.venvs

   c) You need to configure the environment::

       export WORKON_HOME=~/.venvs
        source /usr/local/bin/virtualenvwrapper.sh
    
   d) Add the lines to your .bashrc file so the next time your environment is ready::

      i) Open the .bashrc::

            pico .bashrc

      ii) Copy and paste the next lines to the end of the .bashr file::

           export WORKON_HOME=~/.venvs
            source /usr/local/bin/virtualenvwrapper.sh

   e) Create a virtualenv for the project::

        mkvirtualenv festos --no-site-packages

   f) Try it::

        workon festos
       deactivate

2) Install the project:

   a) Download it::

       cd $HOME
       git clone https://github.com/CulturePlex/festos.git git/festos

   b) Enter in the new location and update the virtual environment previously created::

       cd git/festos/

   c) Set the .gitignore_global to ignore unnecessary files and extensions::

       git config --global core.excludesfile .gitignore_global

   d) Install the requierements of the project::

        workon festos
        pip install -U -r requirements.txt

3) Create database and launch:

   a) You must create a database, user and configure the site. If your are in developing stage, you can use the start_all.sh script::

        ./start-all.sh

   b) If you want to launch your site again, just use the following one::

        python manage.py runserver localhost:8000

   c) Access the site in the URL http://localhost:8000/

                                             
Testing the installation:
-------------------------

1) Go to the following address (login with user "festos" and password "festos" or if you didn't use the ./start-all.sh then use the one you created)::

    localhost:8000/admin/sites/site/1/

2) Check the domain name is correct ("localhost:8000" if you are developing). Change it to whatever you need. You will need to restart the server to reflex the changes::

    python manage.py runserver localhost:8000

3) In another terminal run the celery service::

    python manage.py celery worker

4) Add a scanned pdf (for convenience, there is one in ~/git/festos/test.pdf) document in the admin interface::

    localhost:8000/admin/document/

5) You will need to wait a few seconds while docsplit splits the document and elasticsearch index it. You can see the status in the admin interface. When the status is 'ready', you can search in the following URL (make sure you search with an appropiate term that is insider your pdf)::

    localhost:8000/search/

6) You can also try accessing the document directly::

   access the document : http://localhost:8000/viewer/1/demo.html


Disabling stop words:
---------------------

1) Open the elasticsearch.yml::

    $ sudo nano /etc/elasticsearch/elasticsearch.yml

2) Add the following to the configuration file (in the Index section)::

    index:
       analysis:
           analyzer:
            # set standard analyzer with no stop words as the default for both indexing and searching
           default:
                type: standard
                stopwords: _none_

3) Delete the haystack index (Warning, this is going to delete all the index)::

    curl -XDELETE 'http://localhost:9200/haystack/'

4) Restart the elasticsearch service::

    sudo service elasticsearch restart


PostgreSQL installation and configuration:
------------------------------------------

1) Install and configure Postgresql Database:

   a) Install Postgresql::

       sudo apt-get install postgresql

   b) Set the password::

       sudo passwd postgres

   c) Create a django user named "festos"::

        sudo -u postgres createuser -P festos

   d) Switch user::

        su postgres

   e) Enter the Postgres shell::

        psql template1

   f) Create db and owner::

       CREATE DATABASE festos_db OWNER festos ENCODING 'UTF8';

   e) Quit the shell::

         \q

   f) Edit the Postgres permissions::

         nano  /etc/postgresql/9.1/main/pg_hba.conf

   g) Adding the following line::

        local     django_db   django_login   md5

   h) Leave user postgresl, go back to your user account::

       exit

   i) Restart the server::

        sudo service postgresql restart


2) Configure the environment:

   a) Install the system libraries::

         sudo apt-get build-dep python-psycopg2

   b) Activate your virtual environment::

        workon festos

   c) Install the python library inside the virtual environment::

        pip install psycopg2

   d) Open the the production settings::

        nano festos/prod_settings.py

   e) Add the configuration::

       DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'festos',
                'USER': 'festos',
                'PASSWORD': 'FESTOS_PASSWORD',
                'HOST': '',
                'PORT': '',
            }
        }

   f) Set the variable::

       export DJANGO_SETTINGS_MODULE=festos.prod_settings

   g) Run the start_all.sh script::

        ./start_all.sh

   h) Restart your servers

