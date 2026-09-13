# The Electronic Whole Earth Catalog — Static Recompilation

Static recompilation of **The Electronic Whole Earth Catalog** (Broderbund /
Point Foundation, 1988).

## Project Status: **P0 partial — and this one probably belongs to [macrecomp](https://github.com/sp00nznet/macrecomp), not here.**

---

## What P0 found

The disc is Mode1/2352 BIN/CUE. Converted with `tools/assets/bin2iso.js`, it is
**not ISO 9660**:

```
offset 0x0000   'ER'  Apple Driver Descriptor Record
offset 0x0200   'PM'  Apple Partition Map
offset 0x8001         no CD001 -- there is no ISO 9660 volume descriptor
```

This is a **Macintosh HFS disc**, and 7-Zip declines to mount the HFS volume
inside the partition map. So: a 1988 Broderbund title, 517 MB of it, for a
platform this repo does not target.

That makes it interesting rather than a mistake. It is the same shelf as
[shufflepuck](https://github.com/sp00nznet/shufflepuck) — Broderbund, 1988,
68k Macintosh — which is already a working static recomp living in this
directory, and the reason `macrecomp` (68k, A-trap dispatch, a QuickDraw/Toolbox
HAL) exists at all.

## What it probably is

The Electronic Whole Earth Catalog is one of the first commercial **HyperCard**
titles — Broderbund's CD-ROM edition of the Whole Earth Catalog, shipped when
HyperCard was a year old. If that holds when the volume is actually mounted,
then the "binary" is a stack, the "code" is HyperTalk, and there is no 68k
application to recompile at all beyond whatever XCMDs and XFCNs it ships.

That would make it a **format** project rather than a recompilation project:
read the HFS volume, read the stack, run the HyperTalk. Closer in shape to
Encarta 97 — which is in the collection precisely to prove the approach works
on applications and not only games — than to Shufflepuck Cafe.

It would also be the answer to a question nothing else here asks: an
interpreted title, where the interesting artifact is authored content rather
than compiled code.

## Where it goes next

1. **Mount the HFS volume.** 7-Zip will not; `hfsutils`, `libhfs` or a Linux
   `hfsplus`/`hfs` mount will. Nothing can be said with confidence until the
   file listing exists.
2. Look for `CREATOR`/`TYPE` codes. `WILD`/`STAK` means HyperCard and this
   project changes shape entirely. `APPL` means there is a 68k binary and it
   moves to `macrecomp`.
3. Decide which repo it lives in. This one is a holding pen.

Do not write any more of this README until step 1 is done. Everything above the
line is measured; everything below "What it probably is" is inference from the
title and the year, and it is flagged as such on purpose.

## Layout

```
wholeearth/
  original/   the .7z, the .bin/.cue, and wec.iso converted from it
  analysis/
  docs/
```

## Credits

The Electronic Whole Earth Catalog © 1988 Broderbund Software / Point
Foundation. This project neither contains nor distributes any part of it.
