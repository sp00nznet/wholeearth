#!/usr/bin/env python3
"""List a classic-HFS Mac disc image: path, forks, TYPE/CREATOR.

bulkhead reads HFS+ only and refuses classic HFS, and 7-Zip will not mount the
volume inside an Apple partition map. `pip install machfs` and use this instead.

    python tools/hfsls.py original/wec.iso
"""
import struct
import sys

import machfs


def hfs_partition(f):
    """Byte offset and length of the first Apple_HFS partition, or (0, None)."""
    f.seek(0)
    if f.read(2) != b"ER":  # no driver descriptor -> assume a bare volume
        return 0, None
    f.seek(0x200)
    n = 1
    i = 0
    while i < n:
        b = f.read(512)
        if b[:2] != b"PM":
            break
        n = struct.unpack(">I", b[4:8])[0]
        start, blocks = struct.unpack(">II", b[8:16])
        if b[48:80].split(b"\0")[0] == b"Apple_HFS":
            return start * 512, blocks * 512
        i += 1
    return 0, None


def walk(d, path=""):
    for name, obj in d.items():
        p = f"{path}/{name}"
        if isinstance(obj, machfs.Folder):
            yield from walk(obj, p)
        else:
            yield p, obj


def main(path):
    with open(path, "rb") as f:
        off, size = hfs_partition(f)
        f.seek(off)
        v = machfs.Volume()
        v.read(f.read(size) if size else f.read())
    print(f"{path}  HFS at {off}  volume {v.name!r}")
    for p, o in sorted(walk(v)):
        t = o.type.decode("mac-roman")
        c = o.creator.decode("mac-roman")
        print(f"{len(o.data):>10} {len(o.rsrc):>10}  {t}/{c}  {p}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "original/wec.iso")
