#!/bin/sh
mkdir certs

docker run --rm --user 0 -v /vagrant/certs/certs/:/certs docker.elastic.co/elasticsearch/elasticsearch:8.5.3 bash -c 'bin/elasticsearch-certutil ca --days 3650 --pem -out /certs/ca.zip && unzip /certs/ca.zip -d /certs'
docker run --rm --user 0 -v /vagrant/certs/certs/:/certs -v /vagrant/certs/instances.yml:/instances.yml docker.elastic.co/elasticsearch/elasticsearch:8.5.3 bash -c 'bin/elasticsearch-certutil cert --days 3650 --pem -out /certs/certs.zip --in /instances.yml --ca-cert /certs/ca/ca.crt --ca-key /certs/ca/ca.key && unzip /certs/certs.zip -d /certs'

docker config create ca.crt certs/ca/ca.crt 
docker config create es-multicert.crt certs/es-multicert/es-multicert.crt 
docker config create es-multicert.key certs/es-multicert/es-multicert.key
