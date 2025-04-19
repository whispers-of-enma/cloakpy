import argparse

import scapy.all as scapy
import socket
import random

from core.record import singleton as record
from core.structures import port_status
from utils import pretty_print as print
from utils import validation

input_types = {
    'target_ip': str,
    'timeout': int,
    'port': int, 
}

@validation.input_types(input_types)
def run(target_ip: str, port: int, timeout: int = 1):
    print.info(f'\ntarget_ip: {target_ip}, port: {port}, timeout: {timeout}')
    return True
    header4 = scapy.TCP(dport=port, flags='S', sport=random.randint(1024, 65535))
    header3 = scapy.IP(dst=target_ip)
    pdu = header3 / header4

    response = scapy.sr1(pdu, timeout=timeout, verbose=False)

    if not response:
        return False
    
    if response.haslayer(scapy.TCP):
        if response[scapy.TCP].flags == 0x12:
            record.add_port(target_ip, port, 'tcp', port_status.OPEN)
            header4.flags = 'R'
            pdu = header3 / header4
            scapy.send(pdu, verbose=False)
        elif response[scapy.TCP] == 0x14:
            record.add_port(target_ip, port, 'tcp', port_status.CLOSED)
        else:
            record.add_port(target_ip, port, 'tcp', port_status.UNREACH)
        
        return True
    
    return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ping single host')
    parser.add_argument('target_ip', help='target IP address')
    parser.add_argument('port', help='target port', type=int, metavar='port')
    parser.add_argument('-w', nargs='?', default=1, help='seconds to wait for reply', type=int, metavar='wait', dest='timeout')
    args = parser.parse_args()
    
    result = run(
        target_ip=args.target_ip,
        port=args.port,
        timeout=args.timeout,
    )

    status = record.get_port_status(args.target_ip, port=args.port, protocol='tcp',)

    if result:
        print.success(f'Host {args.target_ip} is up: port {args.port} is {status.upper()}')
    else:
        print.warning(f'Host {args.target_ip} is unreachable or traffic was filtered.')