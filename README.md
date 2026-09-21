# The Electronic Whole Earth Catalog — Static Recompilation

The Electronic Whole Earth Catalog (Broderbund, 1988) is a Macintosh CD-ROM.
This repo works out what is actually on it, ships the classic-HFS lister that
reads it, and hands the result to
[macrecomp](https://github.com/sp00nznet/macrecomp).

The short answer: the disc holds no Broderbund executable. The catalog is
HyperCard stacks, and the only program on the volume is **HyperCard 1.2.2**
itself. So the thing worth recompiling was never this title — it was the
interpreter underneath it.

## The catalog

Worth knowing what this disc is, because it is not an ordinary piece of 1988
shovelware.

The **Whole Earth Catalog** was a paper book. Stewart Brand and the Portola
Institute put out the first one in Menlo Park in the autumn of 1968, an
oversized paperback with the whole earth on the cover and the words *Access to
Tools* under it. It reviewed things — looms, chainsaws, books, calculators,
geodesic domes — and told you where to send the cheque. In 1971 it won the
National Book Award, the only catalog ever to do so. Steve Jobs, giving the
Stanford commencement address in 2005, called it *"sort of like Google in
paperback form, thirty-five years before Google came along"*, and closed by
quoting the back cover of the final 1974 edition: *Stay hungry. Stay foolish.*

So: an index of everything, cross-referenced by hand, decades before anyone
could type a query into a box.

The **electronic** edition is the interesting part for this repo. Apple funded a
hypertext version built in HyperCard — Bill Atkinson's, bundled with every Mac
since 1987 — and Broderbund shipped it on CD-ROM in 1988, with Stewart Brand and
Kevin Kelly. Over 9,000 cards, linked to one another, browsable by clicking.

Tim Berners-Lee did not write his proposal for the World Wide Web until March
1989, and the first web page went up in 1991. This disc was doing hyperlinked
browsing a year before the Web was proposed, and doing it offline, off a disc
that shipped in a box. It is the web before the web, and the whole of it fits in
450 MB.

That is what is being recompiled here: not a game, but one of the first things
that ever worked the way the internet does.

![The catalog's HEALTH contents card, running under macrecomp's recompiled HyperCard 1.2.2](docs/catalog.png)

macrecomp's recompiled HyperCard 1.2.2 opening this disc's `HEALTH` stack at the
Macintosh's 512×342, reached by clicking from Home through the catalog's table
of contents. Cards navigate, scripts compile and run, and the card art decodes;
the bitmap expander still stops about two thirds of the way down a card, which
is the white band under the illustration.

This repo is finished — it is the reconnaissance and the lister, and it is not
growing. The recompilation continues in macrecomp.

## Getting started

Everything below runs from a clean machine and ends with HyperCard's 68k code
extracted and ready for the lifter. You do not need to rip anything: the disc is
on the Internet Archive as a plain HFS volume image.

**Prerequisites** — Python 3.9 or newer.

**1. Get the repo and the disc image** (450 MB; `original/` is gitignored):

```bash
git clone https://github.com/sp00nznet/wholeearth.git
cd wholeearth
mkdir -p original
curl -L -o original/EWEC.img \
  https://archive.org/download/the-electronic-whole-earth-catalog/EWEC.img
```

That file is a bare HFS volume — no partition map, no ISO 9660, no 2352-byte
sectors. Nothing needs converting.

**2. List it:**

```bash
pip install machfs
python tools/hfsls.py original/EWEC.img
```

One line per file: data fork, resource fork, TYPE/CREATOR, path.

```
original/EWEC.img  HFS at 0  volume 'Untitled'
   4153344      67974  STAK/WILD  /COMMUNICATIONS
   1622016      67532  STAK/WILD  /COMMUNITY
         0     400640  APPL/WILD  /HyperCard
```

**281 files.** 279 of them are the catalog; the other two sit in
`/TheVolumeSettingsFolder/` and are Mac OS desktop-database leftovers from
whenever the volume was last mounted read-write, not disc content.

**3. Hand it to macrecomp** — it reads this image directly:

```bash
pip install macresources
git clone https://github.com/sp00nznet/macrecomp ../macrecomp
python ../macrecomp/tools/extract_resources.py original/EWEC.img -o work/hypercard
```

```
volume 'Untitled'  app '/HyperCard'  type=b'APPL' creator=b'WILD' data=0 rsrc=400640
jump table: 1110 functions over 21 segments -> work/hypercard/jumptable.json

264 resources -> work/hypercard/  (by size:)
  CODE  x 22    326088 B
  ICON  x104     13312 B
  snd   x  3     13158 B
  WTLK  x  4     12248 B
```

`work/hypercard/code/CODE_*.bin` is what the lifter consumes. From here it is
macrecomp's README: lift the segments, build, run.

**If you have your own rip** instead, it is likely Mode1/2352 BIN/CUE. Strip the
16-byte sync/header and 288-byte ECC from each 2352-byte sector to get plain
sectors. A rip of the physical disc *does* carry an Apple partition map, so
`hfsls.py` reports `HFS at 15360` rather than `HFS at 0`. Both work. If you see
`no CD001` errors or a stack trace from `machfs`, the image is still raw
2352-byte sectors.

## What is on the disc

A rip of the physical disc, converted to plain sectors, is not ISO 9660:

```
offset 0x0000   'ER'  Apple Driver Descriptor Record
offset 0x0200   'PM'  Apple Partition Map -> Apple_HFS at block 30
offset 0x3C00   'BD'  classic HFS Master Directory Block
offset 0x8001         no CD001 -- there is no ISO 9660 volume descriptor
```

`drEmbedSigWord` is zero, so this is **classic HFS**, not an HFS+ volume inside
an HFS wrapper. That distinction decides the tooling: neither 7-Zip nor
[bulkhead](https://github.com/sp00nznet/bulkhead) will open it, because
bulkhead's HFS driver is HFS+/HFSX only and bails on the classic signature by
design (`src/hfs.rs`). `tools/hfsls.py` reads it with `machfs` instead.

### Volume contents

279 files, 450 MB, in six kinds:

| Count | TYPE/CREATOR | What it is |
|---|---|---|
| 19 | `STAK/WILD` | HyperCard stacks — the catalog itself |
| 97 | `STAK/SFX!` | `soundFiles/*.chunx`, sound resources, **344 MB** |
| 100 | `TEXT/????` | search index |
| 54 | `TEXT/MACA` | MacWrite text, source for the search index |
| 8 | `CTLZ/????` | search index |
| **1** | **`APPL/WILD`** | **HyperCard — 0-byte data fork, 400 KB of resources** |

The 19 stacks are the sections of the catalog (`COMMUNICATIONS`, `CRAFT`,
`HEALTH`, `MUSIC`, `WHOLE SYSTEMS`, …) plus `Home`, `INDEX` and `QUICK SEARCH`.
The disc is 76% audio by volume.

## Why there is nothing here to recompile

There is no Broderbund binary. The "code" is HyperTalk inside the stacks, run by
an interpreter Broderbund licensed and copied onto the disc. Statically
recompiling *this title* is not a thing that can be done, because this title is
data.

The recompile target is therefore HyperCard itself — a 68k `APPL` with a
Toolbox/QuickDraw surface, which is exactly what macrecomp exists for. The
payoff is not one catalog: it is every HyperCard stack ever authored.

Extracted and measured, the disc's copy is:

```
22 CODE segments, 326,088 bytes
1,110 jump-table functions over 21 segments
3,166 trap call sites, 418 distinct traps
vers 1 -> "1.2.2  Copyright Apple Computer, Inc. 1987-88"
```

Those are the figures already in macrecomp's coverage table, so the one new fact
was the version number: the "user-supplied CD / HyperCard 1.x" row in that
corpus is **this disc**, and it is HyperCard 1.2.2 — the 1988 build, the oldest
and simplest. It is now the first row of macrecomp's conformance corpus at
2642/3166 covered call sites (83%).

Finding that needed one fix, and it went upstream where it belongs. macrecomp's
`extract_resources.py` read DiskCopy 4.2 and raw HFS only, so it parsed a CD-ROM
from offset 0 and got garbage. A Mac CD starts with an `ER` driver descriptor
and an Apple partition map, with the HFS volume at whatever block the
`Apple_HFS` entry names — the same map `tools/hfsls.py` here already walked. That
logic now lives in macrecomp's `load_hfs`, so **every** CD-sourced classic-Mac
title is reachable, not just this one.

## Usage

List any classic-HFS Mac disc image, not just this one:

```bash
python tools/hfsls.py <image>
```

It walks an Apple partition map if one is present, so Mac CD-ROMs work as well
as bare floppy volumes.

Self-check (no disc needed):

```bash
python tools/test_hfsls.py
```

There is nothing to build here: two Python files, one dependency, no compiled
artifacts.

## Scope

No `STAK` parser, and no HyperTalk interpreter behind it. A recompiled HyperCard
reads its own stacks with its own interpreter — that is the entire point of
recompiling it rather than reimplementing it, and macrecomp puts a second
interpreter out of scope on the same grounds. The stacks on this disc are input
to a working HyperCard, not a format project, and that bet has settled: it got
far enough to open them.

See [ROADMAP.md](ROADMAP.md) for the rest of what is out of scope and why.

## Layout

```
wholeearth/
  original/   EWEC.img and anything else you bring (gitignored)
  tools/      hfsls.py -- list a classic-HFS Mac disc image
              test_hfsls.py -- its self-check
  docs/       catalog.png -- the screenshot above
```

## Credits

The Electronic Whole Earth Catalog © 1988 Broderbund Software; the Whole Earth
Catalog and its contents © Point Foundation and the respective authors.
HyperCard © Apple Computer. This project contains no code or data from any of
them, and distributes none; the screenshot above is a single frame of the
running program, included to show what the reconnaissance was for.

- **[machfs](https://github.com/tashtego/machfs)** by Elliot Nunn — pure-Python
  HFS parsing. `hfsls.py` stands on it.
- **[The Internet Archive](https://archive.org/details/the-electronic-whole-earth-catalog)**
  for preserving the disc.

## License

MIT — see [LICENSE](LICENSE).
