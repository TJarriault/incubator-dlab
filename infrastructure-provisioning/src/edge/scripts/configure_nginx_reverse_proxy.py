#!/usr/bin/python

# *****************************************************************************
#
# Copyright (c) 2016, EPAM SYSTEMS INC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ******************************************************************************

import logging
import traceback
from fabric.api import *
import argparse
import json
import sys
import os
from dlab.edge_lib import install_nginx_ldap

parser = argparse.ArgumentParser()
parser.add_argument('--hostname', type=str, default='')
parser.add_argument('--keyfile', type=str, default='')
parser.add_argument('--user', type=str, default='')
args = parser.parse_args()

if __name__ == "__main__":
    local_log_filename = "{}_{}_{}.log".format(os.environ['conf_resource'],
                                               os.environ['edge_user_name'],
                                               os.environ['request_id'])
    local_log_filepath = "/logs/edge/" + local_log_filename
    logging.basicConfig(format='%(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.DEBUG,
                        filename=local_log_filepath)

    print("Configure connections")
    try:
        env['connection_attempts'] = 100
        env.key_filename = [args.keyfile]
        env.host_string = '{}@{}'.format(args.user, args.hostname)
    except Exception as err:
        print("Failed establish connection. Excpeption: " + str(err))
        sys.exit(1)

    try:
        edge_ip = args.hostname
        nginx_version = os.environ['reverse_proxy_nginx_version']
        ldap_ip = os.environ['reverse_proxy_ldap_host']
        ldap_dn = os.environ['reverse_proxy_ldap_dn']
        ldap_user_pass = os.environ['ldap_pass']
        ldap_user = os.environ['reverse_proxy_ldap_user']
        install_nginx_ldap(edge_ip ,nginx_version, ldap_ip, ldap_dn, ldap_user_pass, ldap_user)
    except Exception as err:
        print("Failed install nginx: " + str(err))
        sys.exit(1)

