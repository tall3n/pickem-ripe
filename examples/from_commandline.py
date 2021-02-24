import argparse
from pickem import Pickem


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ipaddress",
                        required=True,
                        help="IPV4 address to search")
    args = parser.parse_args()
    return args


def start():
    args = parse_args()
    ip_address = args.ipaddress
    p = Pickem(ip_address)
    found, result_cidr = p.find_ip()
    if found:
        print(f"Found ip address: {ip_address} in CIDR: {result_cidr}")
    else:
        print(f"Did not find a CIDR for the given IP: {ip_address}")


start()
