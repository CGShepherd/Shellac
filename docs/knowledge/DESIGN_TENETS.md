# Project Shellac — Design Tenets

**Status:** CONTROLLED BASELINE  
**Introduced:** SR-035

1. **Affordable performance.** Spend where measurable engineering benefit justifies it; premium parts are not preferred merely because they are premium.
2. **Optimise the whole BOM.** Consider commonality, quantity breaks, useful spares, supplier consolidation, assembly effort, lifecycle risk and second-source practicality—not isolated line-item price.
3. **Prefer commonality.** Minimise unnecessary manufacturers, families, packages and values where all hard requirements remain satisfied. Never force commonality through an electrical, safety, reliability or mechanical constraint.
4. **Simple, proven architecture.** Prefer the least complex solution that satisfies the requirement; added complexity needs a material benefit.
5. **Design for construction and service.** Support staged commissioning, diagnosis, repair, replacement and practical adjustment.
6. **Evidence before freeze.** Missing evidence is surfaced, not replaced by invented dimensions, temperatures, availability or performance.
7. **Preserve signal integrity.** Keep sensitive paths short, control return currents, preserve channel symmetry, segregate mains/noisy/low-level analogue functions and use appropriate local decoupling.
8. **Incremental convergence.** Each package has one primary objective. Required changes belong in it; unrelated ideas are deferred. Prefer evolution over redesign.
9. **Freeze means freeze.** Reopen a frozen decision only with documented reason, evidence, impact and a superseding decision.
10. **Git is authoritative project memory.** Design rules, rationale, BOM intent, risks, release gates and evidence belong under configuration control; conversation history is not an authoritative substitute.
