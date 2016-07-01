#!/usr/bin/env python

import json
from urllib import urlopen

# Fetch metadata associated with the VM on which this runs
# No API key required!
resp = urlopen('https://api.service.softlayer.com/rest/v3/SoftLayer_Resource_Metadata/getUserMetadata')
# It's double-enocded because of the way the client works ...
metadata = json.loads(json.loads(resp.read()))

# Write the docker-compose env_file for the dashboard server
with open('db_secrets.env', 'w') as fh:
    fh.write('''USERNAME={db_username}
PASSWORD={db_password}
AUTH_TOKEN={api_token}
PUBLIC_LINK_PATTERN=http://{db_fqdn}:3000'''.format(**metadata))

print('Wrote db_secrets.env')

# Write the docker-compose env_file for the notebook server
with open('nb_secrets.env', 'w') as fh:
    fh.write('''PASSWORD={nb_password}
DASHBOARD_SERVER_AUTH_TOKEN={api_token}'''.format(**metadata))

print('Wrote nb_secrets.env')
