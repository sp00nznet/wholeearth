# Roadmap

## Where this goes next

**Nowhere, and that is the finding.** The disc is a
[macrecomp](https://github.com/sp00nznet/macrecomp) input, not a project, and it
is now wired up as one: macrecomp reads this image directly, and its conformance
corpus names the fixture and baselines it. Work continues there.

The open blocker in macrecomp is no longer the one this repo's README used to
point at. Entry-point dispatch has landed — a computed jump into the middle of a
lifted function now resolves — so the next measurement there is a run of
HyperCard past that point, with `FSDispatch` and SANE still stubbed.

## Done

- **P0 — reconnaissance.** Identify the container, mount the volume, list it,
  and establish what kind of project this is. Answer: not a recompilation one.
- **P1 — identify the executable.** Extract the single `APPL/WILD` and version
  it: HyperCard 1.2.2 (Apple, 1987-88). Confirm against macrecomp's existing
  measurements that it is the same binary, not a second fixture.

## Out of scope

- **A `STAK` parser.** A recompiled HyperCard reads its own stacks with its own
  interpreter; that is the reason to recompile it rather than reimplement it.
  Revisit only if HyperCard never gets far enough to open a stack.
- **A HyperTalk interpreter.** Same argument, and macrecomp scopes a second one
  out on the same grounds.
- **Extraction and lifting.** Both live in macrecomp, which reads this image
  directly since the Apple partition-map path landed in its `load_hfs`. Adding
  a second extractor here would be a copy that drifts.
- **Redistributing any of it.** The catalog and HyperCard are both in copyright.
  Bring your own disc.

## Conformance harness

House rules ask for one where there is an external spec or observable ground
truth to compare against. There is — HFS is a documented on-disk format — but
the harness that matters for this disc is **macrecomp's**, which measures the
HyperCard extracted from it and fails on a regression. Duplicating it here would
track the same number twice.

What this repo keeps instead is proportionate to what it contains:
`tools/test_hfsls.py` covers the partition-map walk and the bare-volume
fallback, and runs in CI on every push.

## Deferred

- The BIN/CUE → ISO conversion is still done by hand with an external tool. It
  is a one-time step per disc and the README says what it has to do; a script
  for it would be a third way to do something two existing tools already do.
