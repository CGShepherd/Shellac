# AE-040B — Control Authority Reconciliation

**Revision:** A0  
**Status:** CONTROL AUTHORITY RECONCILED — ROTARY PROCUREMENT GATE REMAINS OPEN  
**Base:** `606476544fc185dd68eefcf20ef5c1068c03d58b`

## Objective

Close AE036-F04 without inventing production hardware. The repository contains a real authority conflict:

- G3-024 and the older controls/BOM models still describe Grayhill Series 71 as selected hardware;
- AE-026 explicitly rejects the Grayhill 71BDF30 geometry because it is right-angle;
- AE-026 selects Lorlin PT as the preferred common rotary platform;
- AE-027 deliberately leaves the exact gold-contact Lorlin production order codes open pending manufacturer confirmation and dimensional/sample gates.

AE-040B reconciles those statements into one live authority.

## Reconciled authority

### SW901 / SW902 — Bass and Treble

Electrical requirement remains linked-stereo 2P5, BBM/non-shorting.

Current physical-platform authority is **Lorlin PT**, vertical PCB mounting, metric 6 mm shaft / M10 x 0.75 bush, with gold-plated contacts preferred. The exact production MPN remains **OPEN** under AE-027.

### SW903 — Channel Mode

Electrical requirement remains 4P4, BBM/non-shorting.

Current physical-platform authority is **Lorlin PT**, realised as two synchronised 2-pole wafers stopped at four positions and sharing the same front-panel datum as SW901/SW902. The exact production MPN remains **OPEN** under AE-027.

### SW904 / SW905 and indicators

No authority change. C&K `7201SYCBE` remains selected for Rumble and Mute. Vishay `TLLG4401` and Arcolectric/Bulgin `A104700BLACK` remain selected for the two rail indicators.

## Grayhill disposition

Grayhill `71BDF30-01-2-AJN` and `71BDF30-02-2-AJN` are retained only as historical mechanical evidence. They are **REJECTED / NOT FOR PROCUREMENT** and do not constitute current control authority.

The controlled partial BOM retains the old Grayhill lines for traceability until the AE-027 exact-MPN gate is closed; those lines must be explicitly non-procurable. No guessed Lorlin MPN is added.

## Manufacturing boundary

AE-040B does **not** release:

- production Lorlin order codes;
- rotary footprints;
- PCB placement coordinates;
- panel drilling;
- shaft length;
- Channel rear-depth keep-out;
- knob/nut/washer stack.

Those remain gated by AE-027 and the open AE036-F05 controls-PCB finding.

## Disposition

AE036-F04 is **CLOSED**.

AE036-F05 through F13 remain open. The next control-specific increment is F05: instantiate the PCB-mounted controls as verified physical PCB objects only after the AE-027 procurement/mechanical evidence is sufficient to support exact footprints and geometry.
