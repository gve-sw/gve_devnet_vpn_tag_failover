#!/usr/bin/env python3
"""
Copyright (c) 2022 Cisco and/or its affiliates.

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
import meraki
import os
from dotenv import load_dotenv

# load all environment variables
load_dotenv()

BASE_URL = "https://api.meraki.com/api/v1"

# connect to the Meraki dashboard with the API key in the environmental variables
DASHBOARD = meraki.DashboardAPI(
            api_key=os.environ['API_TOKEN'],
            base_url=BASE_URL,
            print_console=False,
            suppress_logging=True)

#API calls
#Organizations
def get_organizations():
    response = DASHBOARD.organizations.getOrganizations()

    return response


#Get specific organization ID
def get_organization_id(org_name):
    organizations = get_organizations()
    for org in organizations:
        if org["name"] == org_name:
            return org["id"]

    return None

#Networks
def get_networks(org_id):
    try:
        response = DASHBOARD.organizations.getOrganizationNetworks(org_id, total_pages='all')

        return response
    except Exception as e:
        print("There was an error getting the networks of the organization with org id " + org_id)
        print(e)

        return None

#Devices
def get_devices(org_id):
    try:
        response = DASHBOARD.organizations.getOrganizationDevices(org_id, total_pages='all')

        return response
    except Exception as e:
        print("There was an error getting the devices of the organization with org id " + org_id)
        print(e)

        return None

#VPN Statuses
def get_vpn_statuses(org_id):
    try:
        response = DASHBOARD.appliance.getOrganizationApplianceVpnStatuses(org_id, total_pages='all')

        return response
    except Exception as e:
        print("There was an error getting the VPN statuses of the organization with org id " + org_id)
        print(e)

        return None

#Switch VPN tags
def switch_vpn_tags(net_id, tags):
    try:
        response = DASHBOARD.networks.updateNetwork(net_id, tags=tags)
        print(response)
    except Exception as e:
        print("There was an error changing the tags of the network with network id " + net_id)
        print(e)