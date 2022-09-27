#!/usr/bin/env python3

import re
import sys
import json
import argparse
from pathlib import Path
from typing import List, Optional, Generator, TextIO

import ipcalc  # type: ignore

IpAddress = tuple[int, int, int, int]
FlatMatrix = List[bool]

ip_rxp = re.compile(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})")

OCTET_2_OFFSET = OCTET_SIZE = 256
OCTET_3_OFFSET = OCTET_SIZE * 2
OCTET_4_OFFSET = OCTET_SIZE * 3
FLAT_MATRIX_LENGTH = OCTET_SIZE * 4


class BaseBlipGrepException(Exception):
    """The base exception for Blipgrep"""


class InvalidMatrixException(BaseBlipGrepException):
    """Not a conformant flattened matrix"""


class Matrix:
    """An object that search rapidly inside its list of IP addresses"""

    def __init__(self, _arr: Optional[FlatMatrix] = None):
        if _arr is None:
            self._arr = [False] * FLAT_MATRIX_LENGTH
        else:
            self.check_arr(_arr)
            self._arr = _arr

    def add(self, a: int, b: int, c: int, d: int) -> None:
        """Add an IPv4 address using the given octets"""
        arr = self._arr
        arr[a] = True
        arr[b + OCTET_2_OFFSET] = True
        arr[c + OCTET_3_OFFSET] = True
        arr[d + OCTET_4_OFFSET] = True

    def contains(self, a: int, b: int, c: int, d: int) -> bool:
        """Check an IPv4 address using the given octets"""
        arr = self._arr
        if arr[a]:
            if arr[b + OCTET_2_OFFSET]:
                if arr[c + OCTET_3_OFFSET]:
                    if arr[d + OCTET_4_OFFSET]:
                        return True
        return False

    def __contains__(self, item: IpAddress) -> bool:
        return self.contains(*item)

    def serialize(self) -> list[bool]:
        """Serialize this matrix as a list"""
        return list(self._arr)

    @property
    def is_empty(self) -> bool:
        """Is the Matrix devoid of any ip?"""
        return not any(self._arr)

    def populate_from(self, fd: TextIO) -> None:
        """Populate this matrix from a blacklist file"""
        for line in (line_.strip() for line_ in fd):
            if not line.startswith("#"):
                for ipv4_address in get_ipv4_seq(line):
                    self.add(*ipv4_address)

    @staticmethod
    def check_arr(arr: FlatMatrix) -> None:
        """Check if the given flattened matrix is conformant"""
        length = len(arr)
        if length != FLAT_MATRIX_LENGTH:
            raise AssertionError(
                f"Invalid matrix of length {length}. "
                f"Was expecting '{FLAT_MATRIX_LENGTH}': "
                f"{arr}"
            )


def get_ipv4_seq(ipv4_range: str) -> Generator[IpAddress, None, None]:
    """Get a sequence of IPv4 addresses"""
    for ipv4_address in ipcalc.Network(ipv4_range):
        matched = ip_rxp.search(str(ipv4_address))
        if matched:
            a, b, c, d = matched.groups()
            yield (int(a), int(b), int(c), int(d))


def grep(fd: TextIO, matrix: Matrix) -> Generator[str, None, None]:
    """Grep an access log file using the given matrix"""
    for line in fd.readlines():
        match = ip_rxp.search(line)
        if match:
            a, b, c, d = match.groups()
            octet = (int(a), int(b), int(c), int(d))
            # if octet in matrix:
            if matrix.contains(*octet):
                yield line


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        dest="file",
        type=str,
        default="",
        required=False,
        help=(
            "the file to contains the list of ips and ranges "
            "to use as a blacklist."
        )
    )
    parser.add_argument(
        "-c",
        "--cache",
        dest="cache",
        type=str,
        default="",
        required=False,
        help=(
            "use the given JSON cache file; "
            "it will be created if it doesn't exist"
        )
    )
    args = parser.parse_args()
    cache_exists = Path(args.cache).is_file()

    matrix = Matrix()

    if cache_exists:
        with open(args.cache) as fd:
            arr = json.load(fd)
            matrix = Matrix(_arr=arr)
    elif args.file:
        with open(args.file) as fd:
            matrix.populate_from(fd)
        with open(args.cache, "w") as fd:
            json.dump(matrix.serialize(), fd)

    for line in grep(sys.stdin, matrix):
        print(line, end="")


if __name__ == '__main__':
    main()
