import setuptools
from setuptools import setup

setup_options = dict(
    name        = "pickem",
    description = "An application that allows you to verify if the provided IP address exists within the RIPE Coordination Center's IPV4 CIDR List",
    author      = "tall3n",
    author_email = "tallen2@outlook.com",
    url         = "https://github.com/tall3n/pickem-ripe.git",
    classifiers = [
      "Programming Language :: Python :: 3.6",
      "Programming Language :: Python :: 3.7",
      "Programming Language :: Python :: 3.8",
      "Programming Language :: Python :: 3.9",
    ]
)
setup_options["version"] = "1.0.2"
setup_options.update(dict(
  packages         = ['pickem'],
))

setup(**setup_options)