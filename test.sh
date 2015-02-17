#!/bin/sh
sudo service elasticsearch stop
rm -r /tmp/elasticsearch-0.20.5
if [ ! -f /tmp/elasticsearch-0.20.5.tar.gz ]; then
  wget -P /tmp https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-0.20.5.tar.gz
fi
tar xvfz /tmp/elasticsearch-0.20.5.tar.gz -C /tmp
/tmp/elasticsearch-0.20.5/bin/elasticsearch -f & ESP=$!
python manage.py test --settings=festos.test_settings --verbosity=2
kill -9 $ESP
rm -r /tmp/elasticsearch-0.20.5
sudo service elasticsearch start
