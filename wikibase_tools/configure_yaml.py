#!/usr/bin/env python
"""
Modify docker-compose file to set config options in config.py
Usage: configure_yaml.py `file`
Overwrites `file` in place
"""

import yaml
from wikibase_tools.config import WIKIBASE_PORT, WDQS_FRONTEND_PORT, PROXY_PORT, WIKIBASE_ALIAS
import sys

path = sys.argv[1]

d = yaml.load(open(path))

d['services']['wikibase']['ports'][0] = "{}:80".format(WIKIBASE_PORT)
d['services']['wdqs-frontend']['ports'][0] = "{}:80".format(WDQS_FRONTEND_PORT)
d['services']['wdqs-proxy']['ports'][0] = "{}:80".format(PROXY_PORT)

d['services']['wikibase']['networks']['default']['aliases'][0] = WIKIBASE_ALIAS
d['services']['wdqs-frontend']['environment'] = [
    "WIKIBASE_HOST={}".format(WIKIBASE_ALIAS) if "WIKIBASE_HOST=" in x else x for x in
    d['services']['wdqs-frontend']['environment']]
d['services']['wdqs']['environment'] = [
    "WIKIBASE_HOST={}".format(WIKIBASE_ALIAS) if "WIKIBASE_HOST=" in x else x for x in
    d['services']['wdqs']['environment']]
d['services']['wdqs-updater']['environment'] = [
    "WIKIBASE_HOST={}".format(WIKIBASE_ALIAS) if "WIKIBASE_HOST=" in x else x for x in
    d['services']['wdqs-updater']['environment']]

with open(path, 'w') as f:
    yaml.dump(d, f)
