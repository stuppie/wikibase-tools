#!/usr/bin/env bash

set -e

source config.py

wget -N https://raw.githubusercontent.com/wmde/wikibase-docker/master/docker-compose.yml

./configure_yaml.py docker-compose.yml

# start up image
docker-compose pull
docker-compose up -d

# get the docker id for the wikibase
ID=$(docker-compose ps -q wikibase)

# create a new bot account
sleep 10
docker exec -it $ID php /var/www/html/maintenance/createAndPromote.php ${USER} ${PASS} --bot

./initial_setup.py

./make_entities.py