# AE-033 — Native Four-Layer Configuration

**Revision:** A0  
**Status:** NATIVE PCB PRE-ROUTING IMPLEMENTATION

AE-033 changes the native KiCad PCB to the controlled four-layer architecture without routing traces or freezing rotary-dependent geometry.

## Topology
- F.Cu — components/local signals
- In1.Cu — substantially continuous 0VA reference plane
- In2.Cu — power distribution / rail spine
- B.Cu — secondary signal routing

Fabrication remains manufacturer-neutral: use a standard four-layer stack wherever practical. Initial basis is 1.6 mm FR-4, 1 oz outer copper and lead-free HASL; ENIG requires a documented assembly/reliability benefit. Exact dielectric thicknesses follow the selected fabricator's standard stack.

KiCad layer type `power` is metadata only; actual zones belong to the routing phase. The board must remain unrouted after AE-033.
