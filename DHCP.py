#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2023 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""
from vAPI import main as vapi
from pprint import pprint
import json

session = vapi()

# Support Functions
def printDHCP(item):
    print('===========================================')
    print(f'Template Name: {item["templateName"]}')
    print(f'Template ID: {item["templateId"]}')
    print('Options Configured: ')
    definition = json.loads(item['templateDefinition'])
    for code in definition["options"]['option-code']['vipValue']:
        print(
            f'DHCP Code = {code["code"]["vipValue"]} ==> Value = {code["ip"]["vipValue"]}')

# Core Functions
def task1():
    '''
    Generate List of feature templates types
    '''

    data = session.getDataResponse('/dataservice/template/feature')
    cisco_dhcp_templates = []
    for item in data:
        if item['templateType'] == 'cisco_dhcp_server':
            printDHCP(item)


# Program execution
task1()
