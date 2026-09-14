# AE-057 — Shellac LTspice Windows Compatibility Rev A1

**Project:** Shellac
**Status:** PRE-SPICE TOOLCHAIN COMPATIBILITY CORRECTION
**Date:** 2026-09-13

## Purpose

Correct the target-machine interoperability issue observed during AE-056 execution.

## Observed anomaly

LTspice executed the DR039 direct-RC correlation case, but Python reported the expected
`.meas` records as absent.

## Correction

The correlation runner now decodes:
- UTF-8;
- UTF-8 with BOM;
- UTF-16 with BOM;
- BOM-less UTF-16LE characteristic of Windows LTspice logs.

Automatic LTspice discovery now also includes:

`C:/Users/chris/AppData/Local/Programs/ADI/LTspice/LTspice.exe`

`LTSPICE_EXE` remains the highest-precedence override.

## Authority impact

No analogue architecture, DR-038, DR-039, BOM or manufacturing authority is changed.
This is toolchain compatibility only.
