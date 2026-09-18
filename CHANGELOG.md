# Changelog

All notable changes to this project are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); this project uses
[SemVer](https://semver.org/).

Nothing is tagged yet, so everything below is unreleased. The repo reached its
conclusion before it reached a version, which is the honest ordering for a
reconnaissance project that found there was nothing to build.

## [Unreleased]

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
