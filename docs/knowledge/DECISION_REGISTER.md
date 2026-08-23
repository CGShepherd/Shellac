# Project Shellac — Decision Register

**Baseline:** SR-035  
**Engineering base:** `97d333cb66cff90b5685dc6e0a73d3b28d3cf601`

| ID | Decision | Status | Provenance | Evidence / note |
|---|---|---|---|---|
| DEC-001 | Affordable-performance / whole-BOM optimisation governs component selection | SELECTED | RECONSTRUCTED_PRIOR_INTENT | Formalised SR-035 |
| DEC-002 | Prefer component-family commonality and quantity-break economies where hard requirements remain satisfied | SELECTED | RECONSTRUCTED_PRIOR_INTENT | Formalised SR-035 |
| DEC-003 | Replay timing capacitors: C0G/NP0, 1%, >=50 V; <27 nF 0805, >=27 nF 1206 | FROZEN | REPOSITORY_EVIDENCE | `generator/component_selection.py` |
| DEC-004 | SCH101 internal gain selector uses an eight-way DIP bank | FROZEN | REPOSITORY_EVIDENCE | AE-010 |
| DEC-005 | Audio enclosure: black METCASE UNICASE 2 M5502119 | FROZEN | REPOSITORY_EVIDENCE | G3-020/G3-023 |
| DEC-006 | PSU enclosure: black METCASE UNICASE 2 M5502119 | FROZEN | REPOSITORY_EVIDENCE | G3-023 |
| DEC-007 | PSU mains-entry architecture uses SCHURTER KMF1.1121.11 | FROZEN | REPOSITORY_EVIDENCE | G3-022/G3-023 |
| DEC-008 | PCB/standoffs establish position; control nuts must not force alignment | FROZEN | REPOSITORY_EVIDENCE | G3-019/G3-020 |
| DEC-009 | Bass/Treble require linked-stereo 2P5 functions; analogue switches BBM/non-shorting | FROZEN | REPOSITORY_EVIDENCE | AE-009 |
| DEC-010 | Channel Mode requires 4P4T: Stereo/Dual Left/Dual Right/L+R Mono | FROZEN | REPOSITORY_EVIDENCE | AE-007/AE-009 |
| DEC-011 | Prior BOM work favoured affordable Lorlin adjustable-stop rotary commonality and quantity-break value | SELECTED | RECONSTRUCTED_PRIOR_INTENT | Exact MPN/physical suitability to verify in G3-024 |
| DEC-012 | Grayhill/C&K/other premium rotaries are alternatives/benchmarks, not defaults without material benefit | SELECTED | RECONSTRUCTED_PRIOR_INTENT | Formalised SR-035 |
| DEC-013 | Exact external-control MPNs, footprints and drilling coordinates remain unresolved | DEFERRED | REPOSITORY_EVIDENCE | G3-020/G3-023; target G3-024 |
| DEC-014 | Release drilling templates only after exact hardware and PCB/control coordinates are frozen | FROZEN | REPOSITORY_EVIDENCE | G3-019/G3-020 |
| DEC-015 | First powered PSU prototype requires closed-box thermal verification | FROZEN | REPOSITORY_EVIDENCE | G3-023 |

DEC-011 records prior direction without inventing an exact historical part freeze. G3-024 starts from this commonality strategy and deviates only where a hard requirement proves the common family unsuitable.

The SCH101 gain selector is **not** part of rotary commonality: AE-010 freezes an internal eight-way DIP bank.
