# Project Shellac — Maintenance Guide Skeleton

**Status:** STRUCTURE ONLY — populate from implemented, verified baseline.

## Identification
Product/revision, PCB revision, firmware/generator baseline if applicable, serial/build record.

## Safety
External PSU isolation, stored energy, chassis/0VA rules, ESD and safe probing.

## Functional overview
Cartridge input → SCH101 → SCH103 → SCH107 → SCH104 → SCH105 → SCH108 → XLR.

## Configuration
Document only implemented controls and service links. Selected-but-pending DR-038 service links must not be described as fitted until migration closes.

## Test equipment
Audio generator/analyser, DMM, oscilloscope, suitable balanced interface/load.

## DC checks
Rail voltages, quiescent offsets, test-point limits, output DC acceptance.

## Signal-level checks
Reference cartridge-equivalent input, expected levels at PRE_EQ, POST_EQ and output for defined curves/gain settings.

## Equalisation verification
Historical bass/treble selections and complete RIAA verification with tolerances.

## Rumble filter
FILTER/BYPASS response and switching checks.

## Channel modes and mute
Stereo, Dual L, Dual R, mono average, mute operation.

## Noise and CMRR
Production/maintenance acceptance limits once DR-038 implementation is closed.

## Fault isolation
Symptoms → block/test point → likely causes → safe substitution/check.

## Parts and substitutions
Approved parts, precision/matching requirements, obsolete-part alternatives.

## Return to service
Full commissioning subset required after repair.
