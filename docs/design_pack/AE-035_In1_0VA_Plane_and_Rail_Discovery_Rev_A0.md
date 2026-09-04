# AE-035 — In1 0VA Plane and Rail Discovery

**Revision:** A0  
**Status:** FIRST NATIVE COPPER IMPLEMENTATION

AE-035 adds a full-board 0VA reference zone on In1.Cu, inset 0.5 mm from the 220 × 140 mm board edge, using the actual native-board 0VA net discovered by AE-034. Initial clearance/minimum-thickness values are 0.25 mm with 0.30 mm thermal gap/bridge.

The apply tool is fail-safe: it requires `kicad-cli`, saves a pre-AE035 backup, writes the zone, asks KiCad to parse/export the modified board, and automatically restores the original if KiCad rejects it. No manual source editing is required.

AE-035 also discovers the exact +17 V and −17 V rail identities. It does not arbitrarily split In2.Cu; the next copper step uses those net IDs plus actual placement to implement the rail spine. Rotary-dependent regions remain held.
