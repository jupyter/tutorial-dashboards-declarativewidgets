#!/usr/bin/env python

import requests
import json
from os.path import join

# Fetch metadata associated with the VM on which this runs
# No API key required!
resp = requests.get('https://api.service.softlayer.com/rest/v3/SoftLayer_Resource_Metadata/getUserMetadata')
# It's double-enocded because of the way the client works ...
metadata = json.loads(resp.json())
# Key is config file name to write, value is the file content
for key, value in metadata.items():
    with open(join('dashboards_setup', 'docker_deploy', key), 'w') as fh:
        fh.write(value)
