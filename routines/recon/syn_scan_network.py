import itertools

from utils import validation
from utils import pretty_print as print

from core import multi_thread as multithread

from tasks.recon import syn_scan

def run(target_network_ip: str, target_network_mask: int | None = None, target_ports: list | int | str | None = None, max_threads: int = 100, timeout: int = 1) -> list[str]:
    host_ips, target_network_ip, target_network_mask = validation.validate_ip_network(target_network_ip, target_network_mask)

    print.info(f'[!] Performing SYN scan on network {target_network_ip}/{target_network_mask} ({len(host_ips)} addresses)')

    ports = validation.validate_ports(ports=target_ports)

    cases = [
        {'target_ip': ip, 'target_port': port}
        for ip, port in itertools.product(host_ips, ports)
    ]

    results = multithread.dipatch_cases(syn_scan.run, cases=cases, max_threads=max_threads, timeout=timeout)


