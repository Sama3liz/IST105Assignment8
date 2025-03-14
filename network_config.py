import json
import re
import sys
import random
from ipaddress import IPv4Network, IPv6Network

# Predefined subnets
IPV4_SUBNET = IPv4Network("192.168.1.0/24")
IPV6_SUBNET = IPv6Network("2001:db8::/64")
LEASE_TIME = 3600  # 1 hour lease

# Lease database (temporary storage)
leases = {}

def validateMAC(mac):
    """Validate MAC address format."""
    return re.match(r"^[0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5}$", mac) is not None

def ipv4():
    """Generate a unique IPv4 address from the subnet."""
    used_ips = {lease['ip'] for lease in leases.values() if lease['version'] == 'DHCPv4'}
    for ip in IPV4_SUBNET.hosts():
        if str(ip) not in used_ips:
            return str(ip)
    return None  # No available IP

def ipv6(mac):
    """Generate an IPv6 address using EUI-64 format."""
    mac_parts = mac.split(":")
    mac_parts[0] = format(int(mac_parts[0], 16) ^ 2, '02x')
    eui64 = f"{mac_parts[0]}{mac_parts[1]}:{mac_parts[2]}ff:fe{mac_parts[3]}:{mac_parts[4]}{mac_parts[5]}"
    return str(IPV6_SUBNET.network_address) + eui64

def assign_ip(mac, version):
    """Assign an IP address based on DHCP version."""
    if mac in leases:
        return leases[mac]  # Return existing lease
    
    if version == "DHCPv4":
        ip = ipv4()
    elif version == "DHCPv6":
        ip = ipv6(mac)
    else:
        return {"error": "Invalid DHCP version"}
    
    if not ip:
        return {"error": "No available IP addresses"}
    
    leases[mac] = {
        "mac_address": mac,
        "ip": ip,
        "version": version,
        "lease_time": LEASE_TIME,
        "subnet": str(IPV4_SUBNET if version == "DHCPv4" else IPV6_SUBNET)
    }
    return leases[mac]

# Main execution
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(json.dumps({"error": "Usage: python network_config.py <MAC> <DHCPv4|DHCPv6>"}))
        sys.exit(1)
    
    mac, dhcp_version = sys.argv[1], sys.argv[2]
    
    if not validateMAC(mac):
        print(json.dumps({"error": "Invalid MAC address format"}))
        sys.exit(1)
    
    result = assign_ip(mac, dhcp_version)
    print(json.dumps(result))
