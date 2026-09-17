# The Electronic Whole Earth Catalog — Static Recompilation

The Electronic Whole Earth Catalog (Broderbund / Point Foundation, 1988) on
CD-ROM: a Macintosh HyperCard title.

## Project Status: **P0 complete — and there is nothing here to recompile.**

The volume is mounted and listed. The conclusion P0 guessed at is now measured,
and it is stronger than the guess: **the only executable on the disc is
HyperCard itself.** Broderbund shipped Apple's runtime alongside the content and
wrote no application of their own.

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

Two real projects fall out of that, and neither one is this repo:

1. **Recompile HyperCard** — a 68k `APPL` with a Toolbox/QuickDraw surface,
   which is exactly what [macrecomp](https://github.com/sp00nznet/macrecomp)
   exists for. The payoff is not one catalog: it is every HyperCard stack ever
   authored. Shufflepuck Cafe (Broderbund, 1988, 68k) already proves the path.
2. **Read the STAK format and run HyperTalk** — a format-and-interpreter
   project, closer to Encarta 97 than to a game. Wanted either way, since a
   recompiled HyperCard still needs the stacks handed to it.

Both want the same first step: a `STAK` parser. Neither wants a repo named after
one 1988 CD-ROM.

## Is there a Windows version?

No. HyperCard never shipped on Windows in any form, and this title was Macintosh
only — the 1988 packaging lists Mac Plus/SE/II and an Apple CD SC drive. There
is no DOS or Windows edition on archive.org or anywhere else, because there was
never one to dump.

## Where it goes next

This repo is a holding pen and should probably close. The disc is a `macrecomp`
input, not a project.

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
