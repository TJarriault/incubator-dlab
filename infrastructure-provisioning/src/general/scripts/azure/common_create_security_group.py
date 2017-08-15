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

import json
import argparse
from dlab.actions_lib import *
from dlab.meta_lib import *
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--resource_group_name', type=str, default='')
parser.add_argument('--security_group_name', type=str, default='')
parser.add_argument('--region', type=str, default='')
parser.add_argument('--list_rules', default='[]')
args = parser.parse_args()


if __name__ == "__main__":
    try:
        list_rules = json.loads(args.list_rules)
        if AzureMeta().get_security_group(args.resource_group_name, args.security_group_name):
            print "REQUESTED SECURITY GROUP {} ALREADY EXISTS".format(args.security_group_name)
        else:
            print "Creating security group {}.".format(args.security_group_name)
            security_group = AzureActions().create_security_group(args.resource_group_name, args.security_group_name,
                                                                    args.region, list_rules)
            while AzureMeta().get_security_group(args.resource_group_name,
                                                 args.security_group_name).provisioning_state != "Succeeded":
                time.sleep(5)
            print "SECURITY GROUP {} has been created".format(args.security_group_name)
    except:
        sys.exit(1)

