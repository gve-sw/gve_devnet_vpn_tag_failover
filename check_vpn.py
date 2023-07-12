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
import meraki_api
from dotenv import load_dotenv
import os
# from pytz import timezone
# from datetime import datetime
import time

# load environmental variables from .env
load_dotenv()

# environmental variables
ORG_NAME = os.environ["ORG_NAME"]
MARKED_NETWORKS = {} # this dictionary will keep track of unreachable VPNs and how long they have been unreachable


def main():
    # get organization id associated with the organization given in .env
    org_id = meraki_api.get_organization_id(ORG_NAME)

    if org_id is None:
        print("There was an issue finding an organization id for the org with the name " + ORG_NAME)

        return

    # make API calls to get VPN statuses, networks, and devices
    vpn_statuses = meraki_api.get_vpn_statuses(org_id)
    networks = meraki_api.get_networks(org_id)
    devices = meraki_api.get_devices(org_id)

    # loop through VPN statuses
    for status in vpn_statuses:
        net_id = status["networkId"]
        # only perform the following steps on devices that are not offline
        if status["deviceStatus"] != "offline":
            # vpn_timezone = None
            device_name = None

            # get the timezone of the VPN
            # for network in networks:
                # if network["id"] == net_id:
                    # vpn_timezone = network["timeZone"]

            # if timezone is None:
                # print("There was an issue finding the timezone of the network")

                # return
            
            # get the device name of the device associated with the VPN
            for device in devices:
                if device["serial"] == status["deviceSerial"]:
                    device_name = device["name"]

            if device_name is None:
                print("There was an issue finding the device name.")

                return

            vpn_count = len(status["thirdPartyVpnPeers"])

            # if there are no third party VPN peers, then we do not need to change the networks tags
            if vpn_count == 0:
                print("Missing 3rd party VPNs")

                return

            # there should only be one third party VPN peer to change the network tags of
            if vpn_count == 1:
                if status["thirdPartyVpnPeers"]["reachability"] == "reachable":
                    if "-Pri" in status["thirdPartyVpnPeers"]["name"]:
                        # if the VPN status is reachable and the primary tunnel, then we just need to remove it from the tracked networks
                        if net_id in MARKED_NETWORKS.keys():
                            del MARKED_NETWORKS[net_id]
                    elif "-Sec" in status["thirdPartyVpnPeers"]["name"]:
                        # if the VPN status is reachable and the secondary tunnel, then we should try to switch the VPN to the primary tunnel and remove it from the tracked networks
                        # computer_timezone = timezone(os.environ["TIMEZONE"])
                        # now = datetime.now()
                        # now = computer_timezone.localize(now)

                        # network_timezone = timezone(vpn_timezone)
                        # network_time = now.astimezone(network_timezone)

                        # if network_time.hour == 3 and network_time.minute <= 30:
                            # tags = ["-Pri(Active)", "-Sec(Standby)"]
                            # meraki_api.switch_vpn_tags(net_id, tags)
                            # if net_id in MARKED_NETWORKS.keys():
                                # del MARKED_NETWORKS[net_id]
                        # else:
                            # if net_id in MARKED_NETWORKS.keys():
                                # del MARKED_NETWORKS[net_id]
                        tags = ["-Pri(Active)", "-Sec(Standby)"]
                        meraki_api.switch_vpn_tags(net_id, tags)
                        if net_id in MARKED_NETWORKS.keys():
                            del MARKED_NETWORKS[net_id]
                elif status["thirdPartyVpnPeers"]["reachability"] == "unreachable":
                    if "-Pri" in status["thirdPartyVpnPeers"]["name"]:
                        # if the VPN is unreachable and the primary tunnel, check if it has been unreachable for three iterations previously
                        if net_id in MARKED_NETWORKS.keys():
                            # the network has been unreachable previously
                            if MARKED_NETWORKS[net_id] != 3:
                                # the network has not been unreachable for at least three iterations previously, so add 1 to the count of iterations
                                MARKED_NETWORKS[net_id] += 1
                            else:
                                # the network has been unreachable for at least three iterations previously, so it needs to be switched to the secondary tunnel
                                tags = ["-Pri(Standby)", "-Sec(Active)"]
                                # replace the current VPN tags with the tags in the line above
                                meraki_api.switch_vpn_tags(net_id, tags)
                        else:
                            # the network has not been unreachable previously, so we need to add it to the tracked networks
                            MARKED_NETWORKS[net_id] = 1

                    elif "-Sec" in status["thirdPartyVpnPeers"]["name"]:
                        # if the VPN is unreachable and the secondary tunnel, check if it has been unreachable for three iterations previously
                        if net_id in MARKED_NETWORKS.keys():
                            # the network has been unreachable previously
                            if MARKED_NETWORKS[net_id] != 3:
                                # the network has not been unreachable for at least three iterations previously, so add 1 to the count of iterations
                                MARKED_NETWORKS[net_id] += 1
                            else:
                                # the network has been unreachable for at least three iterations previously, so it needs to be switched to the primary tunnel
                                tags = ["-Pri(Active)", "-Sec(Standby)"]
                                # replace the current VPN tags with the tags in the line above
                                meraki_api.switch_vpn_tags(net_id, tags)
                        else:
                            # the network has not been unreachable previously, so we need to add it to the tracked networks
                            MARKED_NETWORKS[net_id] = 1

                else:
                    # the reachability status is neither reachable or unreachable
                    print("There is an issue finding the reachability status. It is listed as " + status["thirdPartyVpnPeers"]["reachability"])



if __name__ == "__main__":
    while True:
        # call the function main function, wait 60 seconds, repeat indefinitely
        main()
        time.sleep(60)