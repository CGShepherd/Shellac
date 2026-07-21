# G3-009 — Schematic-to-PCB Footprint Contract

The footprint contract separates approved PCB members, explicit panel/virtual
components and unresolved mechanical-interface components.  It exposes three
controlled ECO items: J101 and J201 input XLRs, and J901 five-pin regulated-DC
inlet.  These are electrically correct but mechanically inconsistent with the
agreed panel-mounted harness architecture.

The preliminary population export omits all three until a controlled schematic
mechanical-ownership ECO is approved.  The accepted electrical topology and
native ERC baseline remain unchanged.
