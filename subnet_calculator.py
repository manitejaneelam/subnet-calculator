#!/usr/bin/env python3
"""
Subnet Calculator
-----------------
A simple CLI tool for IPv4 subnet math: network/broadcast addresses,
usable host range, subnet mask, and splitting a network into smaller subnets.
Standard library only — no dependencies.

Usage:
    python subnet_calculator.py 192.168.1.0/24
    python subnet_calculator.py 10.0.0.0/16 --split 24
"""

import argparse
import ipaddress
import sys


def ip_class(ip: ipaddress.IPv4Address) -> str:
    """Return the classful network class (A/B/C) of an IPv4 address."""
    first_octet = int(str(ip).split(".")[0])
    if first_octet < 128:
        return "A"
    if first_octet < 192:
        return "B"
    return "C"


def describe_network(cidr: str) -> None:
    """Print the key facts about a network in CIDR notation."""
    try:
        net = ipaddress.ip_network(cidr, strict=False)
    except ValueError as exc:
        print(f"Error: {exc}")
        sys.exit(1)

    print(f"Network:      {net.network_address}")
    print(f"Broadcast:    {net.broadcast_address}")
    print(f"Subnet mask:  {net.netmask} (/{net.prefixlen})")
    print(f"Wildcard:     {net.hostmask}")
    print(f"Total IPs:    {net.num_addresses:,}")

    hosts = list(net.hosts())
    if hosts:
        print(f"Usable hosts: {len(hosts):,}")
        print(f"First usable: {hosts[0]}")
        print(f"Last usable:  {hosts[-1]}")

    print(f"IP class:     {ip_class(net.network_address)}")
    print(f"Private:      {'Yes' if net.is_private else 'No'}")


def split_network(cidr: str, new_prefix: int) -> None:
    """Split a network into equal smaller subnets and list them."""
    try:
        net = ipaddress.ip_network(cidr, strict=False)
    except ValueError as exc:
        print(f"Error: {exc}")
        sys.exit(1)

    if not net.prefixlen < new_prefix <= 32:
        print(f"Error: new prefix must be between /{net.prefixlen + 1} and /32.")
        sys.exit(1)

    subnets = list(net.subnets(new_prefix=new_prefix))
    print(f"{cidr} split into /{new_prefix}: {len(subnets)} subnets\n")
    for i, sub in enumerate(subnets, 1):
        hosts = list(sub.hosts())
        first = hosts[0] if hosts else sub.network_address
        last = hosts[-1] if hosts else sub.broadcast_address
        print(f"{i:>3}. {sub}   usable: {first} - {last}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="IPv4 subnet calculator — network facts and subnet splitting."
    )
    parser.add_argument("cidr", help="Network in CIDR notation, e.g. 192.168.1.0/24")
    parser.add_argument(
        "--split",
        type=int,
        metavar="PREFIX",
        help="Split the network into subnets of this prefix length, e.g. --split 26",
    )
    args = parser.parse_args()

    if args.split:
        split_network(args.cidr, args.split)
    else:
        describe_network(args.cidr)


if __name__ == "__main__":
    main()
