# The Electronic Whole Earth Catalog — Static Recompilation

The Electronic Whole Earth Catalog (Broderbund / Point Foundation, 1988) is a
Macintosh CD-ROM. This repo works out what is actually on it, and ships the
classic-HFS lister that reads it.

The short answer: the disc holds no Broderbund executable. The catalog is
HyperCard stacks, and the only program on the volume is **HyperCard 1.2.2**
itself. So the thing worth recompiling was never this title — it was the
interpreter underneath it, which is now a named fixture in
[macrecomp](https://github.com/sp00nznet/macrecomp).

![The catalog's HEALTH section, running under macrecomp's recompiled
HyperCard 1.2.2](docs/catalog.png)

macrecomp's recompiled HyperCard 1.2.2 opening this disc's `HEALTH` stack at the
Macintosh's 512×342, reached by clicking from Home through the catalog's table of
contents. Navigation between cards works; cards deeper in still hit a HyperTalk
error.

This repo is finished — it is the reconnaissance and the lister, and it is not
growing. The recompilation continues in macrecomp.

## What is on the disc

It is a Mode1/2352 BIN/CUE rip. Converted to plain sectors as `wec.iso`, it is
not ISO 9660 at all:

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

## Getting started

**Prerequisites**

- Python 3.9 or newer
- `pip install machfs` (pure Python; nothing to compile)
- Your own copy of the disc. It is in copyright and is not distributed here.

**Steps**

1. Clone this repo and enter it:
   ```bash
   git clone https://github.com/sp00nznet/wholeearth.git
   cd wholeearth
   ```
2. Install the one dependency:
   ```bash
   pip install machfs
   ```
3. Put your own disc image in `original/` (gitignored). If you have a BIN/CUE
   rip, convert the Mode1/2352 track to plain sectors first — any tool that
   strips the 16-byte sync/header and 288-byte ECC per 2352-byte sector will do:
   ```
   original/wec.iso
   ```
4. Confirm it works:
   ```bash
   python tools/hfsls.py original/wec.iso
   ```

**Expected output** — one line per file (data fork, resource fork,
TYPE/CREATOR, path), 279 of them, beginning:

```
original/wec.iso  HFS at 15360  volume 'Untitled'
   4153344      67974  STAK/WILD  /COMMUNICATIONS
   1622016      67532  STAK/WILD  /COMMUNITY
         0     400640  APPL/WILD  /HyperCard
```

If you see `no CD001` errors or a stack trace from `machfs`, the image is
probably still raw 2352-byte sectors — go back to step 3.

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

To go further than listing — extract an application's resources and measure it —
use macrecomp, which reads this image directly:

```bash
python macrecomp/tools/extract_resources.py original/wec.iso -o work/hypercard
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
  original/   the .7z, the .bin/.cue, and wec.iso converted from it (gitignored)
  tools/      hfsls.py -- list a classic-HFS Mac disc image
              test_hfsls.py -- its self-check
  docs/       catalog.png -- the screenshot above
```

## Credits

The Electronic Whole Earth Catalog © 1988 Broderbund Software / Point
Foundation. HyperCard © Apple Computer. This project contains no code or data
from either, and distributes neither; the screenshot above is a single frame of
the running program, included to show what the reconnaissance was for.

- **[machfs](https://github.com/tashtego/machfs)** by Elliot Nunn — pure-Python
  HFS parsing. `hfsls.py` stands on it.

## License

MIT — see [LICENSE](LICENSE).
