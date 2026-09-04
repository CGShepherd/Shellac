# Project Shellac — Independent Review and Design Assurance Plan

**Revision:** A0
**Status:** CURRENT AUTHORITY
**Introduced after:** AE-040B / `dfc33c4`

## 1. Purpose

Project Shellac shall be subjected to multiple independent technical reviews before
manufacturing release. The review process is deliberately broader than a conventional
audio-product review because Shellac is intended to function both as high-quality audio
equipment and as characterised test/measurement equipment.

The objective is not to obtain reviewer consensus. It is to expose defects, weak evidence,
uncontrolled assumptions, marginal design regions, cross-discipline conflicts and unjustified
release claims before hardware manufacture.

## 2. Review principles

1. Reviewers examine the same frozen candidate unless a review stage explicitly states otherwise.
2. First-pass reviews are independent. A reviewer shall not see another reviewer's findings
   before freezing their own first-pass report.
3. Evidence, analysis, judgement and assumption shall be distinguished explicitly.
4. Severity and confidence are separate attributes.
5. Minority and dissenting opinions shall be retained rather than averaged away.
6. A finding is not closed merely because an implementation exists; closure requires defined
   evidence.
7. Final release includes a fresh review of the resulting candidate, not only confirmation that
   previous findings are marked closed.
8. Review checklists may evolve during development; the governing principles and reviewer roles
   in this document remain authoritative unless superseded by a controlled record.

## 3. Specialist independent reviewers

### 3.1 Principal Analogue Designer

Primary focus:
- signal-chain architecture;
- cartridge loading and source interaction;
- gain, headroom and overload behaviour;
- noise and distortion;
- replay-equalisation accuracy;
- impedance interactions;
- stability;
- component tolerance and sensitivity;
- grounding from an analogue-performance perspective.

Central question: **Does the circuit achieve the intended analogue performance over the full
operating envelope?**

### 3.2 Hostile Design Reviewer

Primary focus:
- search deliberately for ways the design can be wrong;
- challenge comfortable assumptions;
- inspect boundary conditions and pathological operating states;
- seek hidden coupling between apparently independent functions;
- identify design-invalidating single mistakes.

Central question: **If there is a serious design error, where is it most likely hiding?**

### 3.3 PCB / EMC Engineer

Primary focus:
- return-current paths;
- analogue partitioning;
- decoupling;
- parasitic coupling;
- RF susceptibility;
- crosstalk;
- chassis and signal-ground interfaces;
- layer-stack implications;
- routing constraints and sensitive-node protection.

Central question: **Will the schematic still behave as intended when implemented as a real PCB?**

### 3.4 Mechanical / Integration Engineer

Primary focus:
- enclosure interfaces;
- PCB-to-panel datum;
- switch, connector and indicator stack-up;
- tolerances and keep-outs;
- cable routing;
- structural load paths;
- thermal and service-access constraints.

### 3.5 Component and Procurement Engineer

Primary focus:
- lifecycle and availability;
- exact MPN authority;
- second-source exposure;
- counterfeit and obsolescence risk;
- tolerances;
- MOQ and lead time;
- cost/performance proportionality;
- custom or non-standard component gates.

### 3.6 Reliability / FMEA Engineer

Primary focus:
- component open/short failure;
- connector and wiring errors;
- power sequencing;
- switch transients;
- ESD and misuse;
- thermal stress;
- ageing;
- failure propagation and detectability.

### 3.7 Verification and Test Engineer

Primary focus:
- requirement-to-test traceability;
- measurable acceptance criteria;
- test repeatability;
- measurement uncertainty where material;
- equipment capability;
- calibration state;
- commissioning sequence;
- guard-banding where required by the acceptance decision.

### 3.8 Manufacturing / DFM Engineer

Primary focus:
- footprint suitability;
- assembly access;
- solderability;
- tolerance stack;
- manufacturability;
- inspection;
- test-point access;
- repeatable build documentation.

### 3.9 Service / Repair Engineer

Primary focus:
- diagnosis and fault isolation;
- access for measurement and replacement;
- component identification;
- expected voltages and signals;
- maintainability;
- availability of service evidence;
- avoiding destructive disassembly for ordinary faults.

Central question: **Could a competent engineer diagnose and repair this unit many years later?**

### 3.10 Configuration and Release Authority

Primary focus:
- single-source design authority;
- stale or contradictory records;
- schematic/BOM/PCB/mechanical consistency;
- revision control;
- manufacturing artefacts;
- release evidence;
- closure state of controlled findings.

## 4. Cross-cutting Technical Authorities

The following are institutional-style review personas. They represent distinct engineering
approaches and are not impersonations of particular real engineers.

### 4.1 QUAD-style Audio Technical Authority

Reviews Shellac as serious audio equipment.

Emphasis:
- circuit economy and elegance;
- measurable performance;
- low noise and distortion;
- overload and recovery behaviour;
- stability;
- sensible component engineering;
- avoidance of complexity without material benefit.

Central challenge: **Is every component and circuit function justified, and can the same
performance and robustness be achieved more simply?**

### 4.2 HP / Agilent / Keysight-style Instrument Technical Authority

Reviews Shellac as characterised test and measurement equipment.

Emphasis:
- defensible specifications;
- distinction between typical, calculated, simulated, measured and guaranteed performance;
- repeatability;
- calibration and traceability;
- measurement uncertainty;
- acceptance limits and guard-banding where appropriate;
- environmental and setup sensitivity;
- test configuration as part of the evidence;
- observability and diagnostic value.

Central challenge: **What performance can legitimately be stated on a datasheet and objectively
demonstrated?**

This authority may reject a verification method even when the circuit itself is likely compliant
if the proposed experiment cannot demonstrate compliance with adequate confidence.

### 4.3 Airbus Civil-style Technical Design Authority

Reviews Shellac using a controlled-system and design-assurance perspective.

Emphasis:
- requirement provenance;
- architecture and interface integrity;
- explicit assumptions;
- configuration control;
- failure consequences;
- verification independence;
- evidence sufficiency;
- traceable release rationale.

Central challenge: **Demonstrate that each material design decision follows from an understood
requirement and that the evidence is sufficient to release the design.**

## 5. Design Assurance Challenger

This role attacks the reasoning and evidence chain rather than specialising in one implementation
discipline.

It repeatedly asks:
- What do we know?
- How do we know it?
- What are we assuming?
- What evidence would prove us wrong?
- Is the requirement actually necessary?
- Has a provisional choice silently become authoritative?
- What alternative architecture was rejected, and was the rejection justified?
- Have boundary conditions been tested rather than only nominal conditions?

The Hostile Design Reviewer searches for faults in the product. The Design Assurance Challenger
searches for faults in the reasoning.

## 6. Independent Chief Engineer

The Independent Chief Engineer receives:
- the frozen design candidate;
