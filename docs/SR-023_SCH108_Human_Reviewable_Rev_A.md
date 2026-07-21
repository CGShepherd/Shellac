# Project Shellac — SR-023 SCH108 Human-Reviewable Conversion

**Revision:** A  
**Status:** candidate pending native KiCad ERC  
**Parent:** accepted SR-022 baseline

## Scope

SCH108 is rearranged into a conventional left-to-right review drawing. No
component value, gain, protection device, mute truth table or connector
assignment changes.

## Presentation changes

- MODE_L and MODE_R are the only external signal labels at the sheet input.
- Both input test points sit directly in the visible conductors.
- Mute contacts route visibly to each THAT1646 input.
- OUT+/SNS+ and OUT-/SNS- capacitor loops are explicit.
- Each output leg is continuous through its ferrite bead to XLR pin 2 or 3.
- RFI and surge-protection branches meet at explicit split nodes.
- Positive and negative output protection branches point away from each other.
- Output test points sit on the connector-side conductors.
- Local decoupling is grouped below each driver.
- XLR pin 1 remains directly connected to CHASSIS.

## Acceptance

Local acceptance requires:

- full Python regression suite;
- engineering-model validation;
- model-driven build;
- immutable-project provenance verification;
- internal electrical-integrity audit;
- byte-identical clean rebuilds;
- native hierarchical KiCad ERC on the user's Windows installation.
