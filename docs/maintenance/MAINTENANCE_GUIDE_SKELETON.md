# Project Shellac — Maintenance Guide Skeleton

**Status:** ACTIVE STRUCTURE — populate progressively from implemented and verified baselines.

## Identification
Product/revision, PCB revision, release tag, toolchain baseline, build record.

## Safety
External PSU isolation, stored energy, chassis/0VA rules, ESD and safe probing.

## Functional overview
Cartridge input -> SCH101 -> SCH103 -> SCH107 -> SCH104 -> SCH105 -> SCH108 -> XLR.

## Configuration
DR-038 uses one removable four-gang gold service shunt for LOW/DEFAULT/HIGH programming.
DEFAULT is normal and electrically complete with no LOW/HIGH branch bridged; park the shunt
on the inert DEFAULT/PARK header. Do not substitute an ordinary DIP contact into the precision
feedback path. A separate two-gang shunt selects BASE/+47/+100 pF cartridge loading.

## DC checks
AE-074 DR-039 blocks SCH101/SCH103 static DC only in the SCH107 DIRECT/BYPASS branch; the FILTER branch is intrinsically DC-blocked by the SCH107 high-pass capacitors.

## Signal-level checks
Reference cartridge-equivalent input and expected PRE_EQ, RECOVERY_OUT, POST_EQ and output levels.

## Equalisation verification
Historical curves and complete RIAA verification.

## Rumble / channel / mute
Verify FILTER/BYPASS, Stereo/Dual/Mono and mute operation.

## Noise and CMRR
AE-023 defines analytical targets. Final measured production limits remain to be frozen.

## Power-up / power-down
Engage MUTE during power transitions. Allow at least 2 s after power-up before release,
pending prototype transient verification.

## Fault isolation / parts / return to service
Populate from prototype and production evidence.
