#modules
import datetime

#firewall zones
zone_src = ['trust']
zone_dst = ['untrust']

#hosts in question
ip_src = ['10.0.0.1']
ip_dst = ['10.1.0.1']

#network protocol ports
port_protocol = 'tcp' #udp
port_src = 1 #almost always source from port 1, rarely do you filter on source ports
port_dst = [514, 22, 23] #integers, e.g. 22, 25, 80, 443

#for src to dst, original requests
for zone_s in zone_src:
    for zone_d in zone_dst:
        for ip_s in ip_src:
            for ip_d in ip_dst:
                for port_d in port_dst:
                    print(f"show security match-policies global from-zone {zone_s} to-zone {zone_d} source-ip {ip_s} destination-ip {ip_d} source-port {port_src} destination-port {port_d} protocol {port_protocol} | match action-type")
                    #for dst to src, inversion of original requests
                    print(f"show security match-policies global from-zone {zone_d} to-zone {zone_s} source-ip {ip_d} destination-ip {ip_s} source-port {port_src} destination-port {port_d} protocol {port_protocol} | match action-type")
                    print() #empty return

#timestamping
print(f"***** Generated: {datetime.datetime.now()} ***** ")
