# SR-021C — KiCad Session Guard and Build Provenance

**Status:** process and generator-foundation correction  
**Electrical changes:** none

## Trigger

The submitted archive contained a live KiCad lock file. Its native ERC report
described root-sheet wire endpoints even though the included root schematic
contained no wires. A clean rebuild from the same source produced different
file hashes only because KiCad had rewritten line endings; semantically, the
source and generated files were identical.

The contradiction is consistent with ERC running against a stale in-memory
hierarchy while the generator updated the files on disk.

## Controls introduced

- hard failure if any generated KiCad lock file is present;
- SHA-256 hash inventory of every generated CAD file;
- deterministic Build ID;
- generated-project verification command;
- regression tests for open-session rejection and file-tamper detection.

These controls make native ERC evidence attributable to one known generated
build.
