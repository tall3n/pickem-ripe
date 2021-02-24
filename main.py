# Takes an IP address as a command line argument
# Gets json data from the RIPE network coordination center link here
# Use the ['data']['resources']['ipv4'] block in the json above to determine whether the IP provided on the CLI is in any of the CIDRs
# Output a Pass/Fail result based on the presence of the IP address in the CIDR ranges

import requests
import logging
import argparse
import sys
import re



def validate_input(ip_address :str) -> bool:
  ipaddress_regex =  r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
  logging.info("Validating input")
  regex_match = re.match(ipaddress_regex, ip_address) 
  if regex_match != None:
    # logging.info(f"Validation successful user input: {ip_address}")
    return False
  # logging.info(f"Validation failed for user input: {ip_address}")
  return True

def parse_args() -> str:
  parser = argparse.ArgumentParser()
  parser.add_argument("--ipaddress", required=True, help="IPV4 address to search")
  args = parser.parse_args()
  ip_address = args.ipaddress
  if validate_input(ip_address):
    logging.error(f"Please provide a proper IPV4 address, provided IPAddress: {ip_address}")
    return ""
  return args.ipaddress

# add retry decorator here
def get_ip_list() -> dict:
  ripe_network_list = "https://stat.ripe.net/data/country-resource-list/data.json?resource=US&v4_format=prefix"
  ip_list = requests.get(ripe_network_list).json()
  print(ip_list)


# functional tests
# get_ip_list retries
# validate_input proper validates
ip_address = parse_args()
if ip_address == "":
  sys.exit(2)

get_ip_list()