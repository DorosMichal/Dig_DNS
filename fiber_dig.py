import argparse
import ipaddress
from config import TYPES, NS_IP, PROTOCOLS
from main import main

def ip_type(ip_str):
    try:
        ip = ipaddress.ip_address(ip_str)
        return str(ip)
    except ValueError:
        raise TypeError

parser = argparse.ArgumentParser()
parser.add_argument("domain", help="name of the domain to find", type=str)
parser.add_argument("-s", "--server", default=NS_IP, help="ip_v4 of the nameserver to ask", type=ip_type)
parser.add_argument("-t", "--type", default="A", choices= TYPES,
 help="indicates type of query eg. ANY, A, AAAA, MX, etc. A is a default value if type argument isn't provided")
parser.add_argument("-p", "--protocol", default="UDP", choices= PROTOCOLS,
 help="indicates protocol to send query. UDP is a default value if protocol argument isn't provided")
parser.add_argument("--trace", action="store_true")

args = parser.parse_args()

if __name__ == "__main__":
    main(args.domain, args.server, args.type, args.protocol, args.trace)