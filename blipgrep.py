#!/usr/bin/env python3

import re
import sys
import json
import argparse
from typing import List, TextIO, Optional, Generator

import ipcalc

ip_rxp = re.compile(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})")

OCTET_SIZE = 256

IpAddress = tuple[int, int, int, int]


class Matrix:
    def __init__(self, _arr: Optional[List[Optional[bool]]] = None):
        self._arr = [False] * (OCTET_SIZE * 4) if _arr is None else _arr

    def add(self, a: int, b: int, c: int, d: int) -> None:
        self._arr[a] = True
        self._arr[b + OCTET_SIZE] = True
        self._arr[c + OCTET_SIZE * 2] = True
        self._arr[d + OCTET_SIZE * 3] = True

    def test(self, a: int, b: int, c: int, d: int) -> bool:
        if self._arr[a]:
            if self._arr[b + OCTET_SIZE]:
                if self._arr[c + OCTET_SIZE * 2]:
                    if self._arr[d + OCTET_SIZE * 3]:
                        return True
        return False

    def __contains__(self, item: IpAddress) -> bool:
        return self.test(*item)


def get_ipv4_seq(ipv4_range: str) -> Generator[IpAddress, None, None]:
    """Get a sequence of IPv4 addresses"""
    for ipv4_address in ipcalc.Network(ipv4_range):
        matched = ip_rxp.search(str(ipv4_address))
        yield tuple(int(num) for num in matched.groups())


def generate_matrix(fd: TextIO):
    matrix = Matrix()
    for line in fd:
        if not line.startswith("#"):
            for ipv4_address in get_ipv4_seq(line.strip()):
                matrix.add(*ipv4_address)
    return matrix


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-b",
        "--blacklist",
        dest="blacklist",
        type=str,
        default="",
        required=False
    )
    args = parser.parse_args()
    try:
        with open(".cached.json") as fd:
            matrix = Matrix(_arr=json.load(fd))
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        blacklist = args.blacklist
        if blacklist:
            with open(blacklist) as fd:
                matrix = generate_matrix(fd)
                with open(".cached.json", "w") as fd2:
                    json.dump(matrix._arr, fd2)
        else:
            matrix = Matrix()

    for line in sys.stdin.readlines():
        match = ip_rxp.search(line)
        if (match):
            nums = match.groups()
            octet = (int(nums[0]), int(nums[1]), int(nums[2]), int(nums[3]))
            if octet not in matrix:
                print(line, end="")


if __name__ == '__main__':
    main()
