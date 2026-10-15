# Subnet Calculator

A simple command-line tool for IPv4 subnet math — network/broadcast addresses, usable host ranges, subnet masks, and splitting networks into smaller subnets. Built with Python's standard library only (no dependencies).

## Usage

```bash
# Describe a network
python subnet_calculator.py 192.168.1.0/24

# Split a /16 into /24 subnets
python subnet_calculator.py 10.0.0.0/16 --split 24
```

## Example output

```
Network:      192.168.1.0
Broadcast:    192.168.1.255
Subnet mask:  255.255.255.0 (/24)
Wildcard:     0.0.0.255
Total IPs:    256
Usable hosts: 254
First usable: 192.168.1.1
Last usable:  192.168.1.254
IP class:     C
Private:      Yes
```

## Features

- Network, broadcast, mask, wildcard, and usable-range calculation
- Subnet splitting (`--split`) with per-subnet usable ranges
- IP class detection and private-address identification
- Input validation with clear error messages

## Tech

Python 3 · `ipaddress` (stdlib) · `argparse`
