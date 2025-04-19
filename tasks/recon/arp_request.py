import argparse

import scapy.all as scapy
import requests

from core.record import singleton as record
from utils import pretty_print as print
from utils import validation

input_types = {
    'target_ip': str, 
    'iface': [str, type(None)],
    'timeout': int,
}

@validation.input_types(input_types)
def run(target_ip: str, iface: str | None, timeout: int):
    arp_request = scapy.ARP(pdst=target_ip)
    layer2_broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    layer2_frame = layer2_broadcast / arp_request

    answered, _ = scapy.srp(layer2_frame, iface=iface, timeout=timeout, verbose=False)

    if not answered: 
        return False
    
    mac_address = answered[0][1].hwsrc

    url = f'https://www.macvendorlookup.com/api/v2/{mac_address}'

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            vendor =  data[0].get('company', 'unknown') if data else 'unknown'
    except Exception as e:
        vendor = 'error'

    record.add_host_spec(target_ip, 'mac_vendor', vendor)
    record.add_host_spec(target_ip, 'mac_address', mac_address)

    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get MAC address of host')
    parser.add_argument('target_ip', help='target IP address')
    parser.add_argument('-i', nargs='?', help='source network interface (e.g., eth0, wlo1)', type=str, metavar='interface', dest='iface')
    parser.add_argument('-w', nargs='?', default=1, help='seconds to wait for reply', type=int, metavar='wait', dest='timeout')
    args = parser.parse_args()

    result = run(
        target_ip=args.target_ip,
        timeout=args.timeout,
        iface=args.iface,
    )

    mac_address = record.get_host_spec(args.target_ip, 'mac_address')
    vendor = record.get_host_spec(args.target_ip, 'vendor')

    if result:
        print.success(f'Host {args.target_ip} is up: {mac_address} (vendor: {vendor})')
    else:
        print.warning(f'Host {args.target_ip} is unreachable')