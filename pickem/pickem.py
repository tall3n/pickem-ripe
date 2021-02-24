# Takes an IP address as a command line argument
# Gets json data from the RIPE network coordination center link here
# Use the ['data']['resources']['ipv4'] block in the json above to determine whether the IP provided on the CLI is in any of the CIDRs
# Output a Pass/Fail result based on the presence of the IP address in the CIDR ranges

from typing import Tuple
import requests
import logging
import re
import ipaddress

class Pickem():
    def __init__(self, ip_address: str) -> None:
        self.ripe_api = "https://stat.ripe.net/data/country-resource-list/data.json?resource=US&v4_format=prefix"
        self.ip_cidr_list = []
        self.ip_address = ip_address
        self.headers = {}
    @property
    def ip_valid(self) -> bool:
        """Determines if the provided IP Address is Valid"""

        ipaddress_regex = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        try:
            regex_match = re.match(ipaddress_regex, self.ip_address)
            if regex_match is not None:
                return True
            return False
        except TypeError:
            return False

    # need to expand the cidr to get the start and ending IP range
    def expanded_cidr(self, cidr: str) -> list:
        """Expand a given cidr into a list of individual IP Addresses"""

        cidr_list = [str(ip) for ip in ipaddress.IPv4Network(cidr)]
        return cidr_list

    # would like to implement retry decorator here.
    def get_cidr_list(self):
        response = requests.get(self.ripe_api, )
        self.headers = response.headers
        return response

    @property
    def source_cidr_list(self) -> list:
        """Retrieves CIDR list from the RIPE Endpoint"""
        response = self.get_cidr_list()

        if response is None or response == requests.exceptions.Timeout:
            return [] 
        if response.status_code == 200:
            return response.json().get("data").get("resources").get("ipv4")
            logging.error(f"""Recieved non 200 status code from RIPE Endpoint,
                        status code: {response.status_code}""")
        return []

    @property
    def first_two_octets(self) -> str:
        """Grabs the first two octets for a given IP Address 
        to decrease the number of CIDR blocks expanded on interation
        """
        # split the ip address up to speed up the process
        two_octets = self.ip_address.split(".")[0:2]
        if len(two_octets) < 2:
            logging.error("Unable to split ip address into first two octets.")
            return ""
        first_two_octets = ".".join(two_octets)
        logging.info(f"Collected offsets {first_two_octets} for ip: {self.ip_address}")
        return first_two_octets

    def find_ip(self) -> Tuple[bool, str]:
        """Iterates through the available CIDRs returned from RIPE
           compares provided IP address and checks it against the expanded
           cidr
        """

        found = False
        found_cidr = ""
        if len(self.source_cidr_list) == 0:
            logging.error("Empty Source CIDR List exiting.")
        else:
            for cidr in self.source_cidr_list:
                if self.first_two_octets in cidr:
                    if self.ip_address in self.expanded_cidr(cidr):
                        found = True
                        found_cidr = cidr
        return found, found_cidr
