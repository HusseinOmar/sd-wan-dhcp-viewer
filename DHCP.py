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
import ipaddress

session = vapi()

# Support Functions
def printDHCP(i):
    for item in i:
        print('=================================================================================')
        print(f'=> Template Name:   {item["templateName"]}')
        print(f'=> Template ID:     {item["templateId"]}')
        print('Options Configured: ')
        definition = json.loads(item['templateDefinition'])
        for code in definition["options"]['option-code']['vipValue']:
            print(
                f' - DHCP Code = {code["code"]["vipValue"]}     ==>     Value = {code["ip"]["vipValue"]}')
    print('=================================================================================')

# Core Functions
def dhcpTemplates():
    '''
    Generate List of feature templates types
    '''

    data = session.getDataResponse('/dataservice/template/feature')
    cisco_dhcp_templates = []
    for item in data:
        if item['templateType'] == 'cisco_dhcp_server':
            cisco_dhcp_templates.append(item)
    return cisco_dhcp_templates

def matchByValue(value):
    matched = []
    for item in dhcpTemplates():
        for i in json.loads(item['templateDefinition'])["options"]['option-code']['vipValue']:
            for ip in i["ip"]["vipValue"]:
                if str(ip) == str(value):
                    matched.append(item)
    return matched    
# Task functions

def task1():
    printDHCP(dhcpTemplates())

def task2():
    '''
    Get list of templates that match specific value
    '''
    value = None
    while not value:
        value_typed = input("Please enter the ip address you want to match: ")
        try:
            value = ipaddress.ip_address(value_typed)
        except Exception:
            print(f'ERROR: ***{value_typed}*** is not a correct IPv4 or IPv6 address')
        
    printDHCP(matchByValue(value))

# Program execution
def banner():
    print('''
    Choose on the following options:
    01 - View => [Template Name] => DHCP Codes
    02 - View => Template name that match specific DHCP code value (IP address)
    xx - Exit ( ~ type xx or exit)
    ''')

def runner(select):
    switch = {
        1: task1,
        2: task2
    }
    return switch.get(select)()

def selector():
    while True:
        banner()
        print('')
        select = input('   - Please select one of the above options: ')
        try:
            if select.lower() == 'exit':
                break
            elif select.lower() == 'xx':
                break
            select = int(select)
            if select > 0 and select <= 8:
                pass
            else:
                print('')
                print('  %% Please enter a correct value')
                continue
        except:
            print('')
            print('  %% Wrong selection, please enter a number')
            continue
        runner(select)

selector()
