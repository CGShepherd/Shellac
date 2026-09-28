# Project Shellac — Signal-Chain Commissioning and Maintenance Baseline

**Status:** PRE-PRODUCTION MAINTENANCE BASELINE  
**Evidence:** DR-037, DR-038, DR-039, AE-012 through AE-023, AE-066, AE-067, AE-074, AE-075A, AE-075B

## Normal configuration

- SCH101 gain: DEFAULT / approximately 18 dB.
- HIGH gain is reserved for lower-output cartridges and has reduced low-frequency headroom.
- Rumble filter may be FILTER or BYPASS; AE-074 DR-039 provides branch-local DC isolation in BYPASS, while SCH107's high-pass capacitors provide intrinsic DC isolation in FILTER.
- Full RIAA replay uses TRUE RIAA 3180/318 us bass plus 2121 Hz treble.

## Power sequencing

The DR-039 DIRECT/BYPASS 1 µF / 330 kΩ network has a time constant of approximately 0.33 s.

For commissioning and conservative operation:

1. engage MUTE before applying or removing power;
2. apply power;
3. allow at least 2 s before releasing MUTE;
4. before power-down, engage MUTE first.

Two seconds corresponds to more than six DR-039 DIRECT/BYPASS time constants
and leaves less than 0.3% of an initial direct-branch DC-block charging
transient. FILTER has its own SCH107 high-pass dynamics; RUN12 and prototype
evidence retain authority for final switching/transient acceptance.

This is an operating/commissioning recommendation, not an automatic timing
function; Shellac retains its mechanical mute philosophy.

## Expected nominal level

At DEFAULT gain with a 5 mV RMS cartridge reference and complete RIAA, the
balanced XLR output around 1 kHz is approximately 0.65 V RMS differential.

## Headroom

The conservative Shellac design ceiling remains 10 V RMS differential.

- DEFAULT retains useful wanted-band headroom at the 5 mV reference.
- HIGH is valid but is a lower-output-cartridge sensitivity setting and should
  not be used merely to obtain a louder output.

## CMRR commissioning targets

With a symmetrical low-impedance test source:

- >=70 dB, 20 Hz to 1 kHz, at LOW/DEFAULT/HIGH;
- >=60 dB at 20 kHz.

AE-066 RUN02 establishes the nominal gain/CMRR evidence. AE-075B selects
LT5400BIMS8E-7#PBF and bonds EP9 to quiet 0VA; RUN10 still owns complete-stage
tolerance/mismatch qualification for RF-series, service-gain, LT5400 ratio
errors and 20 kHz parasitic behaviour. The historical AE-023 A-grade tolerance
model is not current production acceptance authority.

## DC offset

With AE-074 fitted, upstream SCH101/SCH103 static offset is blocked by DR-039
in the DIRECT/BYPASS branch and by the intrinsic SCH107 high-pass capacitors in
the FILTER branch.

A conservative analytical downstream differential DC limit is approximately
20 mV. A tighter measured production acceptance value should be frozen after
prototype data exists.

## Electronics noise

The current first-order complete-RIAA electronics model predicts an output
noise of order 0.1 mV RMS and electronics SNR in the mid-70 dB range against
the nominal output. 78-rpm record/surface noise will normally dominate.

## Service caution

Do not substitute an ordinary DIP switch into the SCH101 precision feedback
path. One four-gang removable gold shunt configures all gain legs together:
LOW bridges the 332 ohm RF-parallel branches, HIGH bridges the 866 ohm
RG-parallel branches, and DEFAULT leaves both active branches open with the
shunt parked. AE-075B selects Samtec TSW-104-07-G-D/MNT-104-BK-G for gain and
TSW-102-07-G-D/MNT-102-BK-G for loading. Verify production shunt
pairing/orientation before relying on silkscreen position and retain the
short/symmetric routing-parasitic check. A separate two-gang shunt selects
BASE/+47/+100 pF cartridge loading.
