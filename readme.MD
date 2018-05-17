# wikibase-docker tools

See: https://github.com/wmde/wikibase-docker

Wikibase-docker instructions: https://github.com/wmde/wikibase-docker/blob/master/README-compose.md

## Usage

### Set config options
See config.py for example

### Run
`./run.sh`

## Details

The steps taken by run.sh:
- Download fresh copy of docker-compose.yml
- Configure YAML: edits the docker-compose.yml file using the settings in config.py
- Start up docker images (docker-compose)
- Create a new bot account (using `USER` and `PASS` in settings)
- Create "equivalent property" and "equivalent class" properties
- Recreate all of the properties in Wikidata, along with equivalent
property statements back to wikidata (i.e. `equivalent property -> http://www.wikidata.org/entity/P3840`)

