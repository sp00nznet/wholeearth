# The Electronic Whole Earth Catalog — Static Recompilation

The Electronic Whole Earth Catalog (Broderbund / Point Foundation, 1988) on
CD-ROM: a Macintosh HyperCard title.

## Project Status: **closed — the disc is a macrecomp fixture, and now a named one.**

The volume is mounted and listed. The conclusion P0 guessed at is now measured,
and it is stronger than the guess: **the only executable on the disc is
HyperCard itself.** Broderbund shipped Apple's runtime alongside the content and
wrote no application of their own.

That executable has now been extracted and identified — it is **HyperCard
1.2.2**, and it is the binary [macrecomp](https://github.com/sp00nznet/macrecomp)
is already lifting. Nothing further happens in this repo; work continues there.

---

## What P0 found

The disc is Mode1/2352 BIN/CUE. Converted to `wec.iso`, it is not ISO 9660:

```
offset 0x0000   'ER'  Apple Driver Descriptor Record
offset 0x0200   'PM'  Apple Partition Map -> Apple_HFS at block 30
offset 0x3C00   'BD'  classic HFS Master Directory Block
offset 0x8001         no CD001 -- there is no ISO 9660 volume descriptor
```

`drEmbedSigWord` is zero, so this is **classic HFS**, not an HFS+ volume in an
HFS wrapper. That matters for tooling: neither 7-Zip nor
[bulkhead](https://github.com/sp00nznet/bulkhead) reads it. bulkhead's HFS
driver is HFS+/HFSX only and bails on the classic signature by design
(`src/hfs.rs`). `tools/hfsls.py` reads it with `machfs` instead.

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

## What that means

There is no Broderbund binary. The "code" is HyperTalk inside the stacks, run by
an interpreter that Broderbund licensed and copied onto the disc. Statically
recompiling *this title* is not a thing that can be done, because this title is
data.

The recompile target is therefore HyperCard itself — a 68k `APPL` with a
Toolbox/QuickDraw surface, which is exactly what
[macrecomp](https://github.com/sp00nznet/macrecomp) exists for. The payoff is
not one catalog: it is every HyperCard stack ever authored. Shufflepuck Cafe
(Broderbund, 1988, 68k) already proves the path.

## What the disc turned out to be good for

macrecomp's corpus listed a "user-supplied CD" carrying "HyperCard 1.x" as
though it were a second fixture waiting to be brought in. It is not a second
anything — **it is this disc, and it is the binary macrecomp is already
working on.** Extracted and measured:

```
22 CODE segments, 326,088 bytes
1,110 jump-table functions over 21 segments
3,166 trap call sites, 418 distinct traps
vers 1 -> "1.2.2  Copyright Apple Computer, Inc. 1987-88"
```

Those are the exact figures in macrecomp's coverage table, so the only new fact
is the version number: the 1.x in the roadmap is **HyperCard 1.2.2**, the 1988
build, the oldest and simplest one. Coverage against the current HAL re-measured
at 77% of call sites and 47% of distinct traps.

Getting there needed one fix, and it went upstream where it belongs: macrecomp's
`extract_resources.py` read DiskCopy 4.2 and raw HFS only, so it parsed a
CD-ROM from offset 0 and got garbage. A Mac CD starts with an `ER` driver
descriptor and an Apple partition map, with the HFS volume at whatever block the
`Apple_HFS` entry names — the same map `tools/hfsls.py` here already walked.
That logic now lives in `load_hfs`, so **every** CD-sourced classic-Mac title is
reachable, not just this one.

```
python tools/extract_resources.py /path/to/wec.iso -o work/hypercard
```

## What is deliberately not being built

A `STAK` parser, and a HyperTalk interpreter behind it. A recompiled HyperCard
reads its own stacks with its own interpreter — that is the entire point of
recompiling it rather than reimplementing it, and macrecomp puts a second
interpreter out of scope for the same reason. The stacks on this disc are input
to a working HyperCard, not a format project. If HyperCard never gets far
enough to open a stack, *then* the format is worth reading directly.

## Is there a Windows version?

No. HyperCard never shipped on Windows in any form, and this title was Macintosh
only — the 1988 packaging lists Mac Plus/SE/II and an Apple CD SC drive. There
is no DOS or Windows edition on archive.org or anywhere else, because there was
never one to dump.

## Where it goes next

Nowhere, and that is the right outcome. The disc is a `macrecomp` input, not a
project, and it is now wired up as one: macrecomp reads this image directly and
its roadmap names the fixture. Follow the work at
[macrecomp](https://github.com/sp00nznet/macrecomp) — the open blocker there is
entry-point dispatch in the lifter, not anything on this CD.

## Layout

```
wholeearth/
  original/   the .7z, the .bin/.cue, and wec.iso converted from it (gitignored)
  tools/      hfsls.py -- list a classic-HFS Mac disc image
  analysis/
  docs/
```

## Usage

```
pip install machfs
python tools/hfsls.py original/wec.iso
```

Prints one line per file: data fork size, resource fork size, TYPE/CREATOR, path.

## Credits

The Electronic Whole Earth Catalog © 1988 Broderbund Software / Point
Foundation. HyperCard © Apple Computer. This project neither contains nor
distributes any part of either.
