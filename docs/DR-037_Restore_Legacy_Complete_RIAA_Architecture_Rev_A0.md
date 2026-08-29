# Project Shellac — DR-037 Restore Legacy Complete-RIAA Architecture

**Revision:** A0  
**Status:** SELECTED  
**Date:** 28 August 2026  
**Base commit:** `4581c49fb16584a6c5c1410eafaa0d8052232f5f`

## 1. Decision

Restore the previously validated complete-RIAA implementation as the active Project Shellac architecture.

The authoritative RIAA replay configuration is:

- SCH103 bass selector: `TRUE RIAA 3180/318 us`;
- SCH103 treble selector: `2121 Hz RIAA` (75 us);
- no independent downstream 3180 us stage;
- no independent 3180 us ON/BYPASS switch.

## 2. Rationale

The legacy SCH103 implementation already realises the complete canonical RIAA replay response:

- approximately 3180 us / 50.05 Hz pole;
- approximately 318 us / 500.5 Hz zero;
- approximately 75 us / 2121 Hz pole.

The later G3-025/G3-026 architecture added an independent 3180 us stage. G3-027 correctly identified that this duplicates the 3180 us term when combined with the existing TRUE-RIAA bass branch.

The additional stage does not provide a required Shellac operating capability. Removing it reduces component count, signal-path complexity, switching complexity, PCB area and risk while returning to a previously validated complete-RIAA implementation.

## 3. Supersession

This decision supersedes the **active architectural effect** of:

- G3-025 optional-3180 architecture;
- G3-026 optional-3180 circuit/manufacturing geometry;
- G3-027 requirement to resynthesise the TRUE-RIAA branch for compatibility with the independent 3180 us stage.

Those records shall remain in Git unchanged as historical design evidence. They are not to be deleted or rewritten.

The G3-027 finding remains valid evidence explaining why the optional architecture was rejected.

## 4. Required active-design changes

Remove from the active generated design:

1. independent 3180 us signal-processing stage;
2. its stereo ON/BYPASS switch;
3. stage-specific passives and active device(s);
4. stage-specific interconnects, test points and labels;
5. stage-specific PCB placement/reservation;
6. stage-specific BOM and procurement entries;
7. stage-specific commissioning tests.

Retain:

1. existing SCH103 TRUE-RIAA bass branch;
2. existing 2121 Hz RIAA treble position;
3. existing RIAA curve-analysis target;
4. legacy full-RIAA acceptance tests;
5. G3-025/G3-026/G3-027 historical documents.

## 5. Acceptance criteria

The rollback is closed when:

- generated signal path contains no independent 3180 us stage;
- no operator/service switch exists solely for the 3180 us function;
- `TRUE RIAA 3180/318 us + 2121 Hz RIAA` remains selectable;
- current RIAA transfer-function tests pass;
- end-to-end 1 kHz nominal output remains approximately 0.64 V RMS differential for a 5 mV RMS cartridge input at default SCH101 gain;
- no active BOM entries remain solely for the removed optional stage;
- no physical-layout reservation remains solely for the removed optional stage;
- repository history still preserves G3-025/G3-026/G3-027.

## 6. Release disposition

**Selected for implementation.**

This is a controlled rollback to an earlier validated architecture, not a new RIAA design.
