import argparse

import itertools

from core import multi_thread as multithread

from tasks.recon import syn_scan

from utils import pretty_print as print
from utils import validation


def run(target_ips: str | list[str], target_ports: str | int | list[int], max_threads: int = 100, timeout: int = 2):
    target_ips_list = validation.validate_ip_addresses(target_ips)
    target_ports_list = validation.validate_ports(target_ports)

    if len(target_ips) == 1:
        print.info(f'[!] Performing SYN scan on {target_ports_list[0]}')
    else:
        print.info(f'[!] Performing SYN scan on {len(target_ports_list)} addresses')

    cases = [
        {'target_ip': ip, 'target_port': port}
        for ip, port in itertools.product(target_ips_list, target_ports_list)
    ]

    results = multithread.dipatch_cases(syn_scan.run, cases=cases, max_threads=max_threads, timeout=timeout)

    return results

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='syn scan one or many hosts')
    parser.add_argument('target_ips', help='list of target ips (e.g., 192.168.8.1,192.168.8.2,192.168.8.3')
    parser.add_argument('target_ports', help='list of target ports (e.g., 1,2,8-15,22)')
    parser.add_argument('-w', nargs='?', default=1, help='seconds to wait for reply', type=int, metavar='wait', dest='timeout')
    parser.add_argument('-t', nargs='?', default=100, help='number of threads to use', type=int, metavar='threads', dest='max_threads')
    args = parser.parse_args()

    results = run(
        target_ips=args.target_ips,
        timeout=args.timeout,
        max_threads=args.max_threads,
        target_ports=args.target_ports
    )

