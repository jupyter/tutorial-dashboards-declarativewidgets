#!/usr/bin/env python

import json
from urllib import urlopen

# Fetch metadata associated with the VM on which this runs
# No API key required!

resp = urlopen('https://api.service.softlayer.com/rest/v3/SoftLayer_Resource_Metadata/getUserMetadata')
# It's double-enocded because of the way the client works ...
metadata = json.loads(json.loads(resp.read()))
# Key is config file name to write, value is the file content
for key, value in metadata.items():
    # Write to the current working dir
    with open(key, 'w') as fh:
        fh.write(value)
    print('Wrote {} to disk'.format(key))
