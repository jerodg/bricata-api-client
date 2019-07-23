```
 ___     _         _            _   ___ ___    ___ _ _         _   
| _ )_ _(_)__ __ _| |_ __ _    /_\ | _ \_ _|  / __| (_)___ _ _| |_ 
| _ \ '_| / _/ _` |  _/ _` |  / _ \|  _/| |  | (__| | / -_) ' \  _|
|___/_| |_\__\__,_|\__\__,_| /_/ \_\_| |___|  \___|_|_\___|_||_\__|
```
![platform](https://img.shields.io/badge/Platform-Linux/Unix/Windows-blue.svg)
![python](https://img.shields.io/badge/Python-3.6/7/8%2B-blue.svg)
![bricata](https://img.shields.io/badge/Bricata-4.4.1+-blue.svg)
<a href="https://www.mongodb.com/licensing/server-side-public-license"><img src="https://img.shields.io/badge/License-SSPL-green.svg"></a>
![0%](https://img.shields.io/badge/Coverage-0%25-red.svg)
<a href="https://saythanks.io/to/jerodg"><img src="https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg"></a>


Bricata API Client

## Installation
```bash
pip install bricata-api-client
```

## Basic Usage
Works with Bricata API v4.1.1

*See examples folder for more*

### Class Inheritence
```python
from bricata_api_client import BricataApiClient

class MyClass(BricataApiClient):
    def __init__(self):
        BricataApiClient.__init__(self, cfg='/path/to/config.toml')
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        BricataApiClient.__aexit__(self, exc_type, exc_val, exc_tb)
```

### Context Manager
```python
from bricata_api_client import BricataApiClient

async with BricataApiClient(cfg='/path/to/config.toml') as bac:
    alerts = bac.get_alerts()
```

## Documentation
[GitHub Pages](https://jerodg.github.io/bricata-api-client/)
- Work in Process

## API Implementation
- [ ] suricata_rules : policy
    - [ ] post /rules/file/suricata/-import/ Import from URL
    - [ ] post /rules/file/suricata/-upload/ Import suricata rules
    - [ ] get /rules/file/suricata/url-file/ List Suricata sync URL(s)
    - [ ] post /rules/file/suricata/url-file/ Import from file
    - [ ] get /rules/gc/ Preview Garbage Collection
    - [ ] delete /rules/gc/ Run Garbage Collection
    - [ ] get /rules/gc/count/ Fast preview Garbage Collection
    - [ ] delete /rules/group/suricata/{name}/ Delete group
    - [ ] get /rules/group/suricata/{name}/policies/ Get policies with group enabled
    - [ ] put /rules/policy/refresh/ Refresh policy cache
    - [ ] get /rules/policy/suricata/summary/ List policy stats
    - [ ] put /rules/policy/suricata/{policy}/{type} Update policy
    - [ ] get /rules/policy/suricata/{policy}/{type}/btinfo/ Get policy backtesting
    - [ ] get /rules/policy/suricata/{policy}/{type}/group/ List policy groups
    - [ ] get /rules/policy/suricata/{policy}/{type}/rule/ List policy rules
    - [ ] get /rules/policy/suricata/{policy}/{type}/rule/{id}/ Get policy rule
    - [ ] post /rules/rule/suricata/ Create custom rule
    - [ ] get /rules/rule/suricata/{id}/ Get Rule Details
    - [ ] put /rules/rule/suricata/{id}/ Update custom rule
    - [ ] delete /rules/rule/suricata/{id}/ Delete Rule
    - [ ] get /rules/rule/suricata/{id}/history/ Get rule version history
    - [ ] get /rules/rule/suricata/{id}/policies/ Get policies with rule changes
    - [ ] get /rules/rule/suricata/{id}/rules/ Get rule from all policies
- [ ] bro_scripts : policy
    - [ ] delete /rules/file/bro/imports/ Clear imports directory
    - [ ] get /rules/file/bro/url-conf/ Get scripts URL
    - [ ] post /rules/file/bro/url-conf/ Update scripts URL
    - [ ] get /rules/policy/bro/btinfo/{group}/{type} Get Backtesting
    - [ ] post /rules/policy/bro/btinfo/{group}/{type} Update backtesting
    - [ ] get /rules/policy/bro/conf/{group}/{type} Get policy configuration
    - [ ] put /rules/policy/bro/conf/{group}/{type} Update policy configuration
    - [ ] get /rules/policy/bro/lib/{name}/{type} Download Bro scripts library
    - [ ] get /rules/policy/bro/list/{group}/{type} Get scripts list
    - [ ] put /rules/policy/bro/list/{group}/{type} Update scripts list
    - [ ] get /rules/policy/bro/script/{type}/{folder}/{name} Get script
    - [ ] put /rules/policy/bro/script/{type}/{folder}/{name} Update script
    - [ ] delete /rules/policy/bro/script/{type}/{folder}/{name} Delete script
    - [ ] post /rules/policy/bro/script/{type}/{name} Create script
    - [ ] post /rules/policy/bro/upload/{type} Upload Bro scripts file
- [ ] alerts
    - [x] get /alert/{uuid} Get Alert
    - [ ] put /alert/{uuid}/_savenote Label Alert
    - [x] get /alerts/ List alerts
    - [ ] get /alerts/geo/history/ Alerts geomap history
    - [ ] get /alerts/geo/stream/ Geo Stream
    - [ ] post /alerts/malware Download Maleware file
    - [ ] get /alerts/meta/{uuid}/{timestamp} Get Alert Metadata
    - [ ] put /alerts/tags/{tag}/ Tag Alerts
    - [ ] delete /alerts/tags/{tag}/ Untag Alerts
    - [ ] get /alerts/timeline/ Alerts timeline
    - [x] put /alerts/{uuid}/tag/{tag}/ Tag Alert
    - [x] delete /alerts/{uuid}/tag/{tag}/ Untag Alert
- [ ] audit
    - [ ] get /audittrails/ Get audit records
- [ ] datanodes
    - [ ] post /datanodes/ Add node
    - [ ] get /datanodes/_cmc_data Get enabled
    - [ ] put /datanodes/_cmc_data Enable
    - [ ] delete /datanodes/{host} Delete node
- [ ] metadata
    - [ ] get /es/all-fields/ Add fields
    - [ ] put /es/delete-index/{name} Delete index
    - [ ] get /es/indexed-fields/ Get indexed fields
    - [ ] post /metadata/_uuids/{uuids}/{tag}/ Tag Metadata records
    - [ ] delete /metadata/_uuids/{uuids}/{tag}/ Untag metadata records
    - [ ] get /metadata/activity/ List activity
    - [ ] get /metadata/agents/ Get user-agent counts
    - [ ] get /metadata/alerts/ Lookup alerts
    - [ ] post /metadata/connections/{tag}/ Tag by filter
    - [ ] delete /metadata/connections/{tag}/ Untag by filter
    - [ ] get /metadata/connections/{uid}/ Get Metadata details
    - [ ] get /metadata/group-timeline/ Group aggregation timeline
    - [ ] get /metadata/groups/ Group aggregation
    - [ ] get /metadata/sources/ List data sources
    - [ ] get /metadata/start/ Get earliest Metadata date
    - [ ] get /metadata/timeline/ Activity timeline
    - [ ] post /metadata/{index}/{doc}/{tag}/ Tag Metadata
    - [ ] delete /metadata/{index}/{doc}/{tag}/ Untag metadata
- [ ] auth
    - [x] post /login/ Login
    - [x] post /logout/ Logout
    - [ ] put /users/{username}/password-token Create password reset token
    - [ ] put /users/{username}/reset-password Start password reset
    - [ ] put /users/{username}/set-password Finish password reset
- [ ] named_storage
    - [ ] get /named_storage/{type}/ List named storage
    - [ ] put /named_storage/{type}/ Upsert named storage
    - [ ] delete /named_storage/{type}/{uuid}/ Delete named storage
- [ ] roles
    - [ ] get /roles/ List roles
    - [ ] post /roles/ Create a role
    - [ ] get /roles/{rolename} Read a role
    - [ ] put /roles/{rolename} Update a role
    - [ ] delete /roles/{rolename} Delete a role
- [ ] sensors
    - [ ] get /sensornames/ Lightweight Sensors list
    - [ ] get /sensors/ Sensors list with health and delivery stats
    - [ ] post /sensors/ Register a new Sensor
    - [ ] get /sensors/apps/{uuid} Get Sensor running apps
    - [ ] post /sensors/gators/togator Get GATOR from JSON
    - [ ] get /sensors/health/count Get critical Sensors count
    - [ ] get /sensors/{host}/capture/ Get packet capture
    - [ ] get /sensors/{host}/logdump/ Get Sensor logs
    - [ ] put /sensors/{uuid} Update a Sensor
    - [ ] delete /sensors/{uuid} Delete a Sensor
    - [ ] get /sensors/{uuid}/ Get a Sensor
    - [ ] get /sensors/{uuid}/feature/{name} Get Sensor Feature status
    - [ ] put /sensors/{uuid}/feature/{name} Enable/Disable Sensor Feature
    - [ ] delete /sensors/{uuid}/health/ Clear Sensor health issue
    - [ ] get /sensors/{uuid}/health/btstatus Get backtesting status
    - [ ] get /sensors/{uuid}/health/history Get Sensor health history
    - [ ] get /sensors/{uuid}/pcap_stats Get Sensor PCAP availability
- [ ] policy
    - [ ] put /sensors/groups/assign/{type}/{name}/ Assign policy
    - [ ] put /sensors/groups/assignall/{type}/{name} Assign policy to all
    - [ ] get /sensors/groups/sensor/{type}/{host} Get Sensor policy
    - [ ] get /sensors/groups/types List policy types
    - [ ] get /sensors/groups/{type} List policies
    - [ ] get /sensors/groups/{type}/{name} Get policy
    - [ ] put /sensors/groups/{type}/{name} Update policy
    - [ ] delete /sensors/groups/{type}/{name} Delete policy
    - [ ] post /sensors/groups/{type}/{name}/ Create policy
- [ ] shoeboxes
    - [ ] get /shoeboxes/ Get shoebox
    - [ ] put /shoeboxes/{name}/ Upsert shoebox
    - [ ] post /shoeboxes/{name}/-add/ Add to shoebox
- [ ] system
    - [ ] get /system/ Get system settings
    - [ ] put /system/ Update system settings
    - [ ] post /system/-check-ldap-conn Check LDAP connection
    - [ ] post /system/-check-mail-host Check email host connection
    - [ ] post /system/-check-proxy-url Check proxy URL
    - [ ] get /system/-constants Read system constants
    - [ ] get /system/-ldap-logs Read ldap logs
    - [ ] get /system/-ui Read system UI settings
    - [ ] get /system/awsconfigstatus Get AWS enabled status
    - [ ] put /system/awsconfigverify Check AWS credentials
    - [ ] put /system/cert/attribs Parse pem certificate
    - [ ] get /system/health Get CMC system health
    - [ ] get /system/logdump Get CMC logs
    - [ ] get /system/mail-logs Read email logs
- [ ] reports
    - [ ] post /system/-export Download report
    - [ ] get /system/reports List user reoprts
    - [ ] post /system/reports Create report template
    - [ ] get /system/reports/-constants Get reort constants
    - [ ] get /system/reports/alerts/ Download report from Alerts page
    - [ ] delete /system/reports/history/-all Delete all report history
    - [ ] get /system/reports/settings/ Get report max rows
    - [ ] put /system/reports/{uuid} Update report template
    - [ ] delete /system/reports/{uuid} Delete report template
    - [ ] delete /system/reports/{uuid}/history/{seq} Delete report history
    - [ ] post /system/reports/{uuid}/history/{seq}/{key}/-download Download report from history
- [ ] assets
    - [ ] get /system/assets List Assets
    - [ ] post /system/assets Create Asset
    - [ ] get /system/assets/{ip} Get Asset
    - [ ] put /system/assets/{ip} Update Asset
    - [ ] delete /system/assets/{ip} Delete Asset
    - [ ] get /system/dns/{ip}/_lookup_addr Lookup address
    - [ ] get /system/dns/{uuid}/{ip}/_lookup_addr Lookup address from sensor
    - [ ] get /system/passive_dns/{ip}/_lookup_addr Passive lookup
- [ ] upgrade
    - [ ] get /system/upgrades/files/{app} List upgrade files
    - [ ] post /system/upgrades/files/{app} Upload upgrade file
    - [ ] get /system/upgrades/files/{app}/{name} Validate upgrade file
    - [ ] put /system/upgrades/files/{app}/{name} Deploy upgrade file
    - [ ] delete /system/upgrades/files/{app}/{type}/{name} Delete upgrade file
    - [ ] get /system/upgrades/status Get upgrade status
- [ ] tags
    - [x] get /tags/ List tags
    - [x] put /tags/{tag}/ Upsert tag
    - [x] delete /tags/{tag}/ Delete a tag
- [ ] users
    - [ ] get /users/ List users
    - [ ] post /users/ Create a user
    - [ ] post /users/email-req Email Support
    - [ ] put /users/profile/{component}/ Update user GUI state
    - [ ] get /users/{username} Read a user
    - [ ] put /users/{username} Update user
    - [ ] delete /users/{username} Delete a user
    - [ ] get /users/{username}/-self Read own profile
    - [ ] put /users/{username}/grace/ Temporarily enable a user
    - [ ] delete /users/{username}/grace/ Delete a temporary user activation
- [ ] validators
    - [ ] get /validatorz/custom_geoip_expr/{val} Validate IP expression
    - [ ] post /validatorz/gator_expr/ Validate GATOR

## License
Copyright © 2019 Jerod Gawne <https://github.com/jerodg/>

This program is free software: you can redistribute it and/or modify
it under the terms of the Server Side Public License (SSPL) as
published by MongoDB, Inc., either version 1 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
SSPL for more details.

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

You should have received a copy of the SSPL along with this program.
If not, see <https://www.mongodb.com/licensing/server-side-public-license>.
