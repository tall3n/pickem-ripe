# pickem_ripe

## Introduction
Checks to see if an IP address exists in the ripe network coordination center cidr list.

Enter a valid IP address an IP CIDR list will be retrieved from the RIPE network coordination center. It will expand the returned cidrs and will check the provided IP address against each expanded cidr and return the result

## How to Install

### From Source

```
python setup.py install
```
## Examples

### From Command Line

```
python examples/from_commandline.py --ipaddress 199.127.92.1
```

### From a function

```
python examples/from_function.py
```


