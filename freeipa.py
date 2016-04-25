#!/usr/bin/env python

import argparse
from ipalib import api
import json

def initialize():
    '''
    This function initializes the FreeIPA/IPA API. This function requires
    no arguments. A kerberos key must be present in the users keyring in 
    order for this to work.
    '''

    api.bootstrap(context='cli')
    api.finalize()
    api.Backend.rpcclient.connect()
    
    return api

def list_hosts(api):
    '''
    This function returns a list of all host groups. This function requires
    one argument, the FreeIPA/IPA API object.
    '''

    inventory = {}
    hostvars={}
    meta={}
    args = []

    options = dict(raw=True, sizelimit=10000) # By default FreeIPA return only first 100 entries, so you need to specify manually how many entries do you want to get

    result = api.Command.host_find(*args, **options)['result']

    inventory['all'] = { 'hosts': [result[host]['fqdn'][0] for host in  xrange(len(result))]}
    for host in  xrange(len(result)):
        hostvars[result[host]['fqdn'][0]] = {}
    inventory['_meta'] = {'hostvars': hostvars}

    inv_string = json.dumps(inventory, indent=1, sort_keys=True)
    print inv_string
    
    return None

def parse_args():
    '''
    This function parses the arguments that were passed in via the command line.
    This function expects no arguments.
    '''

    parser = argparse.ArgumentParser(description='Ansible FreeIPA/IPA '
                                     'inventory module')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', action='store_true',
                       help='List active servers')
    group.add_argument('--host', help='List details about the specified host')

    return parser.parse_args()

def print_host(host):
    '''
    This function is really a stub, it could return variables to be used in 
    a playbook. However, at this point there are no variables stored in 
    FreeIPA/IPA.

    This function expects one string, this hostname to lookup variables for.
    '''

    print json.dumps({})

    return None

if __name__ == '__main__':
    args = parse_args()

    if args.host:
        print_host(args.host)
    elif args.list:
        api = initialize()
        list_hosts(api)
