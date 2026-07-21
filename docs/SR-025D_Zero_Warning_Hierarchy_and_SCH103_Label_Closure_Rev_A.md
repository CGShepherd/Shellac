# SR-025D — Zero-Warning Hierarchy and SCH103 Label Closure

**Trigger:** SR-025C native ERC: 0 errors, 14 warnings  
**Scope:** root hierarchy naming and SCH103 label placement only

## Root hierarchy

SR-025C used engineering signal names for root global labels. Child sheets also use local labels with those names, causing KiCad's `same_local_global_label` warning.

SR-025D gives root-only global nets private names of the form `ROOT__<signal>`. The hierarchical sheet pins still carry the authoritative engineering signal names, so connectivity and interfaces are unchanged.

## SCH103

Six supply and ground labels were placed directly at conductor junctions, causing `label_multiple_wires` warnings. Each affected label now sits at the end of a dedicated second stub segment beyond the electrical node.

## Design impact

None. This is deterministic CAD presentation cleanup only.
