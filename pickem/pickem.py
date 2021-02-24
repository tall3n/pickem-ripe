# Takes an IP address as a command line argument
# Gets json data from the RIPE network coordination center link here
# Use the ['data']['resources']['ipv4'] block in the json above to determine whether the IP provided on the CLI is in any of the CIDRs
# Output a Pass/Fail result based on the presence of the IP address in the CIDR ranges

from typing import Tuple
import requests
import sys
import logging
import argparse
import re
import ipaddress

class Pickem():
  def __init__(self, ip_address :str) -> None:
      self.ripe_api = "https://stat.ripe.net/data/country-resource-list/data.json?resource=US&v4_format=prefix"
      self.ip_cidr_list = []
      self.ip_address = ip_address
      
  @property
  def ip_valid(self) -> bool:
    ipaddress_regex =  r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    
    try:
      regex_match = re.match(ipaddress_regex, self.ip_address) 
      if regex_match != None:
        return True
      return False
    except TypeError:
      return False
  # need to expand the cidr to get the start and ending IP range
  def expanded_cidr(self, cidr :str) -> list:
    cidr_list = [str(ip) for ip in ipaddress.IPv4Network(cidr)]
    return cidr_list 

  @property
  def source_cidr_list(self) -> list:
    response = requests.get(self.ripe_api)
    if response.status_code == 200:
      return response.json().get("data").get("resources").get("ipv4")
    logging.error(f"Recieved non 200 status code from RIPE Endpoint, status code: {response.status_code}")
    return []

  @property
  def first_two_octets(self) -> str:
    # split the ip address up to speed up the process
    first_two_octets = self.ip_address.split(".")[0:2]
    if len(first_two_octets) < 2:
      logging.error("Unable to split ip address into first two octets.")
      return "" 
    first_two_octets = ".".join(first_two_octets)
    return first_two_octets

  def find_ip(self) -> Tuple[bool, str]:
    found = False
    found_cidr = ""
    if len(self.source_cidr_list) == 0:
      logging.error("Empty Source CIDR List exiting.")
    else:
      for cidr in self.source_cidr_list:
        if self.first_two_octets in cidr:
          if self.ip_address in p.expanded_cidr(cidr):
            found = True
            found_cidr = cidr
    return found, found_cidr

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("--ipaddress", required=True, help="IPV4 address to search")
  args = parser.parse_args()
  ip_address = args.ipaddress
  p = Pickem(ip_address)
  if not p.ip_valid:
    logging.error(f"Please provide a proper IPV4 address, provided IPAddress: {ip_address}")
    sys.exit(2)
  found, result_cidr = p.find_ip()
  if found:
    print(f"Found ip address: {ip_address} in CIDR: {result_cidr}")
  else:
    print(f"Did not find a CIDR for the given IP: {ip_address}")