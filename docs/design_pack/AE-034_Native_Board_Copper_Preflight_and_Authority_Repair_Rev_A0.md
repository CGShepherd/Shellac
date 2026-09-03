# AE-034 — Native Board Copper Preflight and Authority Repair

**Revision:** A0  
**Status:** COPPER IMPLEMENTATION PRE-FLIGHT

AE-034 prevents blind editing of the native KiCad S-expression. Before creating the In1 0VA zone or In2 rail geometry, the actual board must disclose the exact net table, exact 0VA net number/name, actual four-layer state, current segment/via/zone counts and board-edge evidence.

KiCad zones bind to both textual net identity and numeric net identifiers. Guessing the numeric ID risks creating an incorrect or unconnected plane, so Foundry evidence rules require discovery from the authoritative native board before mutation.

AE-034 also repairs SR-043's direct-script import convention and records that its older `kicad_native_pipeline.py` manufacturing-hole statement is superseded by SR-040/SR-043.

Once the generated preflight proves a unique 0VA net and expected unrouted/four-layer state, the next patch may safely create the In1 0VA zone, In2 rail spine and first SCH101 critical routes. Rotary-dependent regions remain held.
