#!/usr/bin/env python

import sys
import SoftLayer
import click
import requests
import json
import string
import random
from prettytable import PrettyTable
from requests import ConnectionError, Timeout

_client = SoftLayer.Client()

# Default virtual machine settings
VM_SETTINGS = {
    'cpus': 1,
    'memory': 4096,
    'hourly': True,
    'os_code': 'UBUNTU_LATEST_64',
    'nic_speed': 100,
    'datacenter': 'wdc01',
    'post_uri': 'https://raw.githubusercontent.com/ibm-et/pydata2016/master/setup/post-install.sh',
}

@click.group()
@click.option('--tags',
              default='pydata2016',
              show_default=True,
              help='''Comma-separated tags used to filter virtual machines.''')
@click.option('--domain', '-D',
              default='cloudet.xyz',
              show_default=True,
              help='''Domain used to filter virtual machines.''')
@click.pass_context
def cli(ctx, tags, domain):
    ctx.obj['tags'] = tags.split(',')
    ctx.obj['domain'] = domain

@cli.command()
@click.pass_context
def list(ctx):
    '''List virtual machines.'''
    # List specific fields
    instances = _list_instances(
        tags=ctx.obj['tags'],
        domain=ctx.obj['domain'],
        mask='mask[id,hostname,fullyQualifiedDomainName,primaryIpAddress,status]'
    )
    # For checking if hosts have DNS entries
    dns_records = _get_dns_records(ctx.obj['domain'])
    dns_hosts = [x['host'] for x in dns_records]

    cols = ['ID', 'FQDN', 'PUBLIC_IP', 'STATUS', 'DNS']
    t = PrettyTable(cols, border=False)
    for instance in instances:
        t.add_row([
            instance['id'],
            instance['fullyQualifiedDomainName'],
            instance['primaryIpAddress'] if 'primaryIpAddress' in instance else '',
            instance['status']['name'],
            instance['hostname'] in dns_hosts
        ])
    click.echo(t)

@cli.command()
@click.pass_context
def nb_status(ctx):
    '''List status code of notebook servers.'''
    instances = _list_instances(
        tags=ctx.obj['tags'],
        domain=ctx.obj['domain'],
        mask='mask[id,hostname,fullyQualifiedDomainName,primaryIpAddress]'
    )

    cols = ['ID', 'FQDN', 'PUBLIC_IP', 'STATUS_CODE']
    t = PrettyTable(cols, border=False)
    for instance in instances:
        ip = instance['primaryIpAddress'] if 'primaryIpAddress' in instance else ''
        status_code = _check_nb_server_status(ip) if ip else ''
        t.add_row([
            instance['id'],
            instance['fullyQualifiedDomainName'],
            ip,
            status_code or ''
        ])
    click.echo(t)

@cli.command()
@click.option('--fqdn', 'host_field', flag_value='fullyQualifiedDomainName',
              default=True, show_default=True)
@click.option('--ip', 'host_field', flag_value='primaryIpAddress')
@click.pass_context
def ssh_cmd(ctx, host_field):
    '''Show ssh commands for virtual machines.'''
    instances = _list_instances(
        tags=ctx.obj['tags'],
        mask='mask[operatingSystem.passwords]'
    )
    for instance in instances:
        passwords = []
        try:
            passwords = instance['operatingSystem']['passwords']
        except KeyError:
            continue
        if not passwords:
            continue
        password = passwords[0]
        host = instance[host_field]
        click.echo('ssh {user}@{host} # {password}'.format(
            user=password['username'],
            host=host,
            password=password['password']
        ))

@cli.command()
@click.pass_context
@click.argument('hostname')
@click.option('-s', type=int, default=0, help='Starting number for hostname suffix')
@click.option('-n', type=int, default=1, help='Number of hosts to create')
def create(ctx, s, n, hostname):
    '''Create a virtual machine instance.'''
    for i in range(s, n+s):
        settings = VM_SETTINGS.copy()
        settings.update(dict(
            hostname='{}{}'.format(hostname, i if n > 1 else ''),
            domain=ctx.obj['domain'],
            tags=','.join(ctx.obj['tags'])
        ))
        settings['userdata'] = json.dumps(_create_user_metadata(settings))

        mgr = SoftLayer.VSManager(_client)
        # Verify virtual instance settings before pulling the trigger
        # (will raise exception if invalid)
        instance = mgr.verify_create_instance(**settings)
        click.echo('Creating host {}'.format(settings['hostname']))
        instance = mgr.create_instance(**settings)
        click.echo('Created instance {}'.format(instance['id']))

def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()

@cli.command()
@click.pass_context
@click.argument('hostname')
@click.option('-s', type=int, default=0, help='Starting number for hostname suffix')
@click.option('-n', type=int, default=1, help='Number of hosts to cancel')
@click.option('--yes', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt='Are you sure you want to delete this virtual machine?')
def cancel(ctx, s, n, hostname):
    '''Cancel virtual machine instance.'''
    for i in range(s, n+s):
        hostname_i = '{}{}'.format(hostname, i if n > 1 else '')
        # Remove DNS records
        zone_name = ctx.obj['domain']
        _delete_dns_records(zone_name, hostname_i)
        # Cancel instance
        instance = _get_instance(hostname_i)
        click.echo('Canceling {} ({})'.format(
            instance['fullyQualifiedDomainName'], instance['id']
        ))
        mgr = SoftLayer.VSManager(_client)
        mgr.cancel_instance(instance['id'])

@cli.command()
@click.pass_context
@click.option('-s', type=int, default=0, help='Starting number for hostname suffix')
@click.option('-n', type=int, default=1, help='Number of hosts to add DNS to')
@click.argument('hostname')
def add_dns(ctx, s, n, hostname):
    '''Add DNS record for hostname.'''
    for i in range(s, n+s):
        hostname_i = '{}{}'.format(hostname, i if n > 1 else '')
        zone_name = ctx.obj['domain']
        zone_id = _get_dns_zone_id(zone_name)
        instance = _get_instance(hostname_i)
        mgr = SoftLayer.DNSManager(_client)
        click.echo('Adding record {host} -> {data} in DNS zone {zone}'.format(
            host=hostname_i, data=instance['primaryIpAddress'], zone=zone_name,
        ))
        mgr.create_record(
            zone_id, hostname_i, 'a', instance['primaryIpAddress'], ttl=60*15
        )

@cli.command()
@click.pass_context
@click.option('-s', type=int, default=0, help='Starting number for hostname suffix')
@click.option('-n', type=int, default=1, help='Number of hosts to remove DNS from')
@click.argument('hostname')
def rm_dns(ctx, s, n, hostname):
    '''Remove DNS records for hostname.'''
    zone_name = ctx.obj['domain']
    for i in range(s, n+s):
        hostname_i = '{}{}'.format(hostname, i if n > 1 else '')
        _delete_dns_records(zone_name, hostname_i)

def _list_instances(**kwargs):
    mgr = SoftLayer.VSManager(_client)
    return mgr.list_instances(**kwargs)

def _get_instance(hostname, **kwargs):
    instances = _list_instances(hostname=hostname, **kwargs)
    return instances[0]

def _get_dns_records(zone_name):
    zone_id = _get_dns_zone_id(zone_name)
    mgr = SoftLayer.DNSManager(_client)
    return mgr.get_records(zone_id)

def _get_dns_zone_id(zone_name):
    mgr = SoftLayer.DNSManager(_client)
    zids = [zone['id'] for zone in mgr.list_zones()
            if zone.get('name') == zone_name]
    if not zids:
        raise ValueError('zone {} does not exist'.format(zone_name))
    if len(zids) > 1:
        raise ValueError('multiple zones defined with name {}'.format(zone_name))
    return zids[0]

def _delete_dns_records(zone_name, hostname):
    zone_id = _get_dns_zone_id(zone_name)
    dns_records = _get_dns_records(zone_name)
    instance = _get_instance(hostname)
    ip = instance['primaryIpAddress']
    # Look for A records matching ip
    records = [record for record in dns_records
               if record.get('type') == 'a' and record.get('data') == ip]
    mgr = SoftLayer.DNSManager(_client)
    for record in records:
        click.echo('Removing record {host} -> {data} in DNS zone {zone}'.format(
            zone=zone_name, **record
        ))
        mgr.delete_record(record['id'])

def _check_nb_server_status(host, port=8888):
    try:
        url = 'http://{}:{}'.format(host, port)
        return requests.get(url, timeout=0.5).status_code
    except (ConnectionError, Timeout) as e:
        pass
        
def _create_key(length):
    '''Creates a secure-enough-for-a-tutorial-session random string of numbers 
    and digits.
    '''
    chars = string.ascii_letters + string.digits
    rnd = random.SystemRandom()
    return ''.join(rnd.choice(chars) for i in range(length))

def _create_user_metadata(settings):
    '''Create user metadata in the format expected by setup-credentials.py'''
    return dict(
        nb_password=_create_key(10),
        db_username='pydata',
        db_password=_create_key(10),
        db_fqdn='{}.{}'.format(settings['hostname'], settings['domain']),
        api_token=_create_key(64)
    )

if __name__ == '__main__':
    cli(obj={})
