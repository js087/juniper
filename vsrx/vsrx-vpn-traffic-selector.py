#build traffic-selectors from juniper srx to a palo alto firewall via existing ipsec vpn
#modules
import datetime

#traffic-selector counting
ts_counter = 0
srx_vpn = '<srx_vpn_name>'

#traffic-selector ip subnets to be built
firewall_routes_srx = [
'10.0.1.0/24',
'10.0.2.0/24',
'10.0.3.0/24',
'10.0.4.0/24',
'10.0.5.0/24',
'10.0.6.0/24'
]

firewall_routes_pa = [
'10.2.1.0/24',
'10.2.2.0/24',
'10.2.3.0/24',
'10.2.4.0/24',
'10.2.5.0/24',
'10.2.6.0/24'
]

for route_srx in firewall_routes_srx:
    for route_pa in firewall_routes_pa:
        config_output = f"""set security ipsec vpn {srx_vpn} traffic-selector ts{ts_counter:03} local-ip {route_srx} remote-ip {route_pa}"""
        print(config_output)
        ts_counter += 1

#timestamping
print(f"***** Generated: {datetime.datetime.now()} ***** ")
