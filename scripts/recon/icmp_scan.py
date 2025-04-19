import subprocess
import argparse

from core.record import singleton as record
from utils import pretty_print as print
from utils import validation

input_types = {
    'target_ip': str,
    'timeout': int,
    'count': int, 
}

@validation.input_types(input_types)
def run(target_ip: str, timeout: int = 1, count: int = 1) -> bool:
    command = ['ping', '-c', str(count), '-W', str(timeout), target_ip]
    result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    
    for line in result.stdout:
        if 'ttl=' in line.lower():
            ttl = int(line.split('ttl=')[1].split()[0])
            record.add_host_spec(target_ip, 'ttl', ttl)
            return True

    return False   

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ping single host')
    parser.add_argument('target_ip', help='target IP address')
    parser.add_argument('-w', nargs='?', default=1, help='seconds to wait for reply', type=int, metavar='wait', dest='timeout')
    parser.add_argument('-c', nargs='?', default=5, help='amount of pings to send.', type=int, metavar='count', dest='count')
    args = parser.parse_args()

    result = run(
        target_ip=args.target_ip,
        timeout=args.timeout,
        count=args.count,
    )

    if result:
        print.success(f'Host {args.target_ip} is reachable (TTL = {record.get_host_spec(args.target_ip, 'ttl')})')
    else:
        print.warning(f'Host {args.target_ip} is unreachable.')

