#!/usr/bin/env python3
"""Self-check for the partition-map walk.  python tools/test_hfsls.py

No disc image needed: a Mac CD's layout up to the HFS volume is a driver
descriptor and a map of fixed-size entries, which is cheap to build by hand.
"""
import io
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hfsls import hfs_partition

SECTOR = 512


def cd_image(start_blk=30, blocks=8, n_parts=2, hfs_at=-1):
    """'ER' descriptor + a partition map; Apple_HFS is the entry at hfs_at."""
    if hfs_at < 0:
        hfs_at = n_parts - 1
    img = bytearray(b"ER" + bytes(SECTOR - 2))
    for i in range(n_parts):
        e = bytearray(SECTOR)
        e[0:2] = b"PM"
        e[4:8] = struct.pack(">I", n_parts)
        if i == hfs_at:
            e[8:16] = struct.pack(">II", start_blk, blocks)
            name = b"Apple_HFS"
        else:
            e[8:16] = struct.pack(">II", 1, 1)
            name = b"Apple_Driver"
        e[48:48 + len(name)] = name
        img += e
    img += bytes(max(0, (start_blk + blocks) * SECTOR - len(img)))
    return bytes(img)


def test_finds_the_hfs_partition():
    off, size = hfs_partition(io.BytesIO(cd_image()))
    assert (off, size) == (30 * SECTOR, 8 * SECTOR), (off, size)


def test_hfs_entry_need_not_be_last():
    # A map lists the driver partitions too, in whatever order the disc was
    # mastered; taking the first 'PM' entry would read the wrong partition.
    off, size = hfs_partition(io.BytesIO(cd_image(n_parts=4, hfs_at=2)))
    assert (off, size) == (30 * SECTOR, 8 * SECTOR), (off, size)


def test_bare_volume_has_no_map():
    # A floppy image is the HFS volume itself: no 'ER', so read from 0.
    off, size = hfs_partition(io.BytesIO(bytes(2048)))
    assert (off, size) == (0, None), (off, size)


if __name__ == "__main__":
    test_finds_the_hfs_partition()
    test_hfs_entry_need_not_be_last()
    test_bare_volume_has_no_map()
    print("hfsls self-check OK")
