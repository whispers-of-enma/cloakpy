import argparse

import itertools

from utils import validation
from utils import pretty_print as print

from core import multi_thread as multithread

from tasks.recon import syn_scan

def run(target_network_ip: str, target_network_mask: int | None = None, target_ports: list | int | str | None = None, max_threads: int = 100, timeout: int = 1) -> list[str]:
    target_ips_list, target_network_ip, target_network_mask = validation.validate_ip_network(target_network_ip, target_network_mask)

    print.info(f'[!] Performing SYN scan on network {target_network_ip}/{target_network_mask} ({len(target_ips_list)} addresses)')

    target_ports_list = validation.validate_ports(ports=target_ports)

    cases = [
        {'target_ip': ip, 'target_port': port}
        for ip, port in itertools.product(target_ips_list, target_ports_list)
    ]

    results = multithread.dipatch_cases(syn_scan.run, cases=cases, max_threads=max_threads, timeout=timeout)

    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='syn scan one or many hosts')
    parser.add_argument('target_network_ip', help='ip address of targetted network')
    parser.add_argument('target_ports', help='list of target ports (e.g., 1,2,8-15,22)')
    parser.add_argument('-m', nargs='?', help='maks of targetted network', type=int, metavar='mask', dest='target_network_mask')
    parser.add_argument('-w', nargs='?', default=1, help='seconds to wait for reply', type=int, metavar='wait', dest='timeout')
    parser.add_argument('-t', nargs='?', default=100, help='number of threads to use', type=int, metavar='threads', dest='max_threads')
    args = parser.parse_args()

    results = run(
        target_network_ip=args.target_network_ip,
        timeout=args.timeout,
        max_threads=args.max_threads,
        target_ports=args.target_ports,
        target_network_mask=args.target_network_mask
    )

