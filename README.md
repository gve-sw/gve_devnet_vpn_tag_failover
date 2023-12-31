# GVE DevNet Meraki VPN Tag Failover
This repository contains the source code for a script that uses the Meraki APIs to automatically update the network tags of VPNs according to their reachability status. There is code written, though it is currently commented out, that will only update a reachable secondary network's keys at 3:30am in the timezone that the network is in. To utilize this code, be sure to uncomment the code on lines 21-22, 52, 56-63, and 92-106 and comment out the code on lines 107-110.

![IMAGES/workflow.png](IMAGES/workflow.png)

> For more information on Tag-Based IPsec VPN Failover with Meraki and an alternative script, read [this article](https://documentation.meraki.com/MX/Site-to-site_VPN/Tag-Based_IPsec_VPN_Failover).


## Contacts
* Danielle Stacy


## Solution Components
* Python 3.11
* Meraki SDK


## Prerequisites
#### Meraki API Keys
In order to use the Meraki API, you need to enable the API for your organization first. After enabling API access, you can generate an API key. Follow these instructions to enable API access and generate an API key:
1. Login to the Meraki dashboard
2. In the left-hand menu, navigate to `Organization > Settings > Dashboard API access`
3. Click on `Enable access to the Cisco Meraki Dashboard API`
4. Go to `My Profile > API access`
5. Under API access, click on `Generate API key`
6. Save the API key in a safe place. The API key will only be shown once for security purposes, so it is very important to take note of the key then. In case you lose the key, then you have to revoke the key and a generate a new key. Moreover, there is a limit of only two API keys per profile.

> For more information on how to generate an API key, please click [here](https://developer.cisco.com/meraki/api-v1/#!authorization/authorization). 

> Note: You can add your account as Full Organization Admin to your organizations by following the instructions [here](https://documentation.meraki.com/General_Administration/Managing_Dashboard_Access/Managing_Dashboard_Administrators_and_Permissions).


## Installation/Configuration
1. Clone this repository with `git clone [repository name]`
2. Add Meraki API key and organization name to environment variables in the .env file
```python
API_TOKEN = "API token goes here"
ORG_NAME = "name of organization goes here"
```
3. (Optional) If the user wishes to only update the network tags at specific times of day for the network, then a timezone needs to be provided in the .env file
```python
TIMEZONE = "if timezone is needed, provide a valid timezone from the tz database"
```
> Note: For a list of valid timezones, look through [this Wikipedia article](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
4. Set up a Python virtual environment. Make sure Python 3 is installed in your environment, and if not, you may download Python [here](https://www.python.org/downloads/). Once Python 3 is installed in your environment, you can activate the virtual environment with the instructions found [here](https://docs.python.org/3/tutorial/venv.html).
5. Install the requirements with `pip3 install -r requirements.txt`

## Usage
To run the program, use the command:
```
$ python3 check_vpn.py
```

# Screenshots

![/IMAGES/0image.png](/IMAGES/0image.png)

An example of network tags after the script runs
![/IMAGES/network_tags.png](/IMAGES/network_tags.png)

An example VPN topology from [this article](https://documentation.meraki.com/MX/Site-to-site_VPN/Tag-Based_IPsec_VPN_Failover)
![/IMAGES/topology.png](/IMAGES/topology.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.