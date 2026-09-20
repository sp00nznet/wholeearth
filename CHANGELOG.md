# Changelog

All notable changes to this project are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); this project uses
[SemVer](https://semver.org/).

Nothing is tagged yet, so everything below is unreleased. The repo reached its
conclusion before it reached a version, which is the honest ordering for a
reconnaissance project that found there was nothing to build.

## [Unreleased]

### Added

- **A section on what the catalog actually was.** The Whole Earth Catalog was a
  paper book, Stewart Brand and the Portola Institute, Menlo Park, autumn 1968,
  "Access to Tools" under a photograph of the earth. It won the National Book
  Award in 1971, the only catalog ever to. Steve Jobs called it "Google in
  paperback form, thirty-five years before Google came along". The 1988 CD-ROM
  in this repo is the hypertext edition Apple funded and Broderbund shipped:
  over 9,000 cards linked to one another, browsable by clicking, a year before
  Tim Berners-Lee wrote the proposal for the Web and three before the first web
  page. That is the reason this disc is worth the trouble, and the README never
  said so.

- **An end-to-end path from nothing to lifter input.** The disc is on the
  Internet Archive as `EWEC.img`, a bare HFS volume: no partition map, no ISO
  9660, no 2352-byte sectors, nothing to convert. The README now gives the
  `curl`, the listing, and the `extract_resources.py` handoff that leaves 22
  `CODE` segments in `work/hypercard/code/`. Every command was run verbatim
  against that download.

### Changed

- The README told you to bring your own rip and convert Mode1/2352 BIN/CUE by
  hand, with no command to do it and a code block containing nothing but the
  filename `original/wec.iso`. The Archive image needs none of that; the rip
  path is kept as a footnote for anyone holding a physical disc, including the
  detail that a real rip reports `HFS at 15360` where the Archive image reports
  `HFS at 0`.
- The Archive image lists **281** files, not 279. The two extra are Mac OS
  desktop-database leftovers in `/TheVolumeSettingsFolder/` from a read-write
  mount, not disc content. Said so rather than letting the count look wrong.
- Credits split the copyright properly: the electronic edition is Broderbund's,
  the catalog and its contents are Point Foundation's and its authors'.


### Added

- **A screenshot of the catalog actually running** (`docs/catalog.png`), and the
  README brought up to date around it. The reconnaissance here pointed at
  [macrecomp](https://github.com/sp00nznet/macrecomp), and macrecomp's
  recompiled HyperCard 1.2.2 now opens this disc's stacks, draws their cards,
  and follows a click from one to the next. The `HEALTH` section is the frame
  shown. It is a single frame of the running program; no code or data from the
  disc is in this repo, and the Credits note says so explicitly.

### Changed

- The corpus baseline cited in the README was stale: macrecomp has HyperCard
  1.2.2 at **2642/3166** covered call sites (83%), not 2452/3166 (77%).
- "If HyperCard never gets far enough to open a stack, *then* the format is
  worth reading directly" -- that bet has settled, and the README says which way.
- Dropped the "Is there a Windows version?" section. The answer is still no, but
  a README is not the place to litigate a question nobody reading it asked.
- Layout no longer lists an empty `analysis/`.
- **The README is documentation now, not a work log.** It was written while the
  work was happening and read that way: a `Status: Closed` header, phase labels
  (`What P0 found`), and a narrative in the tense of a project still deciding
  what it was. All of it had been overtaken. It now opens with what the disc is
  and what was found, and the one line a visitor needs about this repo being
  finished sits in the intro instead of a section of its own.
- The roadmap said the next step in macrecomp was "a run of HyperCard past that
  point, with `FSDispatch` and SANE still stubbed". `FSDispatch` landed;
  HyperCard now opens this disc's stacks and navigates between cards, and the
  blocker is a HyperTalk compile error further in. SANE is still a stub, and the
  roadmap now says what kind: its packages pop their selectors so the stack
  stays balanced, but none of the arithmetic is emulated.
- `P0`/`P1` phase labels replaced with what they actually were.


### Added

- **The disc's HyperCard identified as 1.2.2** (Apple, 1987-88), from its `vers`
  resource. Extracted and measured: 22 `CODE` segments, 326,088 bytes, 1,110
  jump-table functions over 21 segments, 3,166 trap call sites across 418
  distinct traps. Those are the figures already in
  [macrecomp](https://github.com/sp00nznet/macrecomp)'s coverage table, so the
  "user-supplied CD / HyperCard 1.x" row in its corpus is **not a second
  fixture** — it is this disc, supplying the binary macrecomp is working on. It
  is now the first row of macrecomp's conformance corpus, baselined at 2452/3166
  covered call sites.
- **P0 reconnaissance.** The disc is Mode1/2352 BIN/CUE wrapping a classic HFS
  volume inside an Apple partition map — no ISO 9660 descriptor, and
  `drEmbedSigWord` zero, so classic HFS rather than HFS+ in a wrapper. Neither
  7-Zip nor [bulkhead](https://github.com/sp00nznet/bulkhead) reads it;
  bulkhead's driver is HFS+/HFSX only and refuses the classic signature by
  design.
- `tools/hfsls.py` — list a classic-HFS Mac disc image (data fork, resource
  fork, TYPE/CREATOR, path), walking an Apple partition map when present.
- The finding that drove everything after it: **the only executable on the disc
  is HyperCard.** 279 files, 450 MB, 76% of it audio; the catalog itself is 19
  `STAK/WILD` HyperCard stacks. Broderbund shipped Apple's runtime alongside the
  content and wrote no application of their own, so there is no Broderbund
  binary to statically recompile.
- `tools/test_hfsls.py` — self-check for the partition-map walk, including an
  `Apple_HFS` entry that is not the first in the map, and the bare-volume
  fallback. No disc image needed.
- `ROADMAP.md` and this file, per house rules.
- CI on every push and PR: lint, byte-compile, and the self-check.
- README restructured to the house section order, with a Getting Started that
  works from a clean machine and states the expected output.

### Changed

- **Status is now closed, not "should probably close".** The open question was
  which HyperCard the disc carried; it has an answer, so the repo has an end
  rather than an intention.
- Written down as deliberate, rather than left as an implied next step: **no
  `STAK` parser and no HyperTalk interpreter**. A recompiled HyperCard brings
  its own interpreter, which is the reason to recompile rather than reimplement.

### Fixed

- The partition-map handling that `tools/hfsls.py` had all along now also lives
  in macrecomp's `extract_resources.py`, which previously read DiskCopy 4.2 and
  raw HFS only and so parsed any Mac CD-ROM from offset 0 as garbage. Fixed
  upstream in the container layer, where it covers every CD-sourced classic-Mac
  title rather than only this disc.

[Unreleased]: https://github.com/sp00nznet/wholeearth/commits/main/
