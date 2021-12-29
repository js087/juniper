#modules
import datetime

#peering information
ipsec_psk = '<change_me>'
ipsec_peer_ip = '<peer_ip_add>'
ipsec_peer_name = '<peer_name_desc>'

#ike naming
ike_vpn_profile = 'company-vpn-ike-001' #company-vpn-ike-001
ike_vpn_gateway = 'company-vpn-ike-001-gw' #company-vpn-ike-001-gw

#ipsec naming
ipsec_vpn_profile = 'company-vpn-ipsec-001'
#binding tunnel interface
ipsec_bind_int = 'st0.<tunnel_num>' #this will change per tunnel, e.g. st0.500

#static routes to build via new tunnel
ipsec_vpn_routes = ['10.0.0.0/24', '10.0.1.0/24']

#security zones
zone_src = 'company-trust'
zone_dst = 'company-untrust' #possible to write this as a list or dictionary
#zone-dst = ['company-untrust', 'company-untrust2']

#phase 1 parameters
ike_vpn_dh = 'group14' #group5
ike_vpn_authalg = 'sha-256'
ike_vpn_encryptalg = 'aes-256-cbc'
ike_vpn_lifetime = '28800'
ike_vpn_mode = 'main'
ike_vpn_version = 'v2-only' #v1-only

#phase 2 parameters
ipsec_vpn_protocol = 'esp'
ipsec_vpn_authalg = 'hmac-sha-256-128' #not required if using 'aes-256-gcm' on 'ipsec_vpn_encryptalg' encryption algorithm
ipsec_vpn_encryptalg = 'aes-256-gcm'
ipsec_vpn_lifetime = '28800'

#sourcing ipsec connections publicly
ipsec_src_int = '<source_interface>' #e.g. lo0.1000

#begin config template to populate and dump
config_output = f"""
set security ike proposal {ike_vpn_profile} authentication-method pre-shared-keys
set security ike proposal {ike_vpn_profile} dh-group {ike_vpn_dh}
set security ike proposal {ike_vpn_profile} authentication-algorithm {ike_vpn_authalg}
set security ike proposal {ike_vpn_profile} encryption-algorithm {ike_vpn_encryptalg}
set security ike proposal {ike_vpn_profile} lifetime-seconds {ike_vpn_lifetime}

set security ike policy {ike_vpn_gateway} mode {ike_vpn_mode}
set security ike policy {ike_vpn_gateway} proposals {ike_vpn_profile}
set security ike policy {ike_vpn_gateway} pre-shared-key ascii-text {ipsec_psk}

set security ike gateway {ike_vpn_gateway} ike-policy {ike_vpn_gateway}
set security ike gateway {ike_vpn_gateway} address {ipsec_peer_ip}
set security ike gateway {ike_vpn_gateway} no-nat-traversal
set security ike gateway {ike_vpn_gateway} external-interface {ipsec_src_int}
set security ike gateway {ike_vpn_gateway} version {ike_vpn_version}

set security ipsec proposal {ike_vpn_profile} protocol {ipsec_vpn_protocol}
#!set security ipsec proposal {ike_vpn_profile} authentication-algorithm {ipsec_vpn_authalg}
set security ipsec proposal {ike_vpn_profile} encryption-algorithm {ipsec_vpn_encryptalg}
set security ipsec proposal {ike_vpn_profile} lifetime-seconds {ipsec_vpn_lifetime}

set security ipsec policy {ipsec_vpn_profile} proposals {ike_vpn_profile}

set security ipsec vpn {ipsec_vpn_profile} bind-interface {ipsec_bind_int}
set security ipsec vpn {ipsec_vpn_profile} ike gateway {ike_vpn_gateway}
set security ipsec vpn {ipsec_vpn_profile} ike ipsec-policy {ipsec_vpn_profile}
set security ipsec vpn {ipsec_vpn_profile} establish-tunnels immediately

set interfaces {ipsec_bind_int} family inet 
set interfaces {ipsec_bind_int} description "{ipsec_peer_name}|{ipsec_peer_ip}"
set security zones security-zone {zone_src} interfaces {ipsec_bind_int}
"""
#print meat and potatoes of config
print(config_output)

#looping through static routes
for static in ipsec_vpn_routes:
    print(f"set routing-options static route {static} next-hop {ipsec_bind_int}")

print() #empty line
print(f"***** Generated: {datetime.datetime.now()} ***** ")
