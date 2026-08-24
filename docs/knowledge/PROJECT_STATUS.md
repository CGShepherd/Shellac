# Project Shellac — Controlled Project Status

**Knowledge baseline:** SR-036 + Foundry FDR-001
**Engineering package:** G3-026 optional-RIAA circuit/geometry closure candidate
**Base commit:** `89dfc9f8493ba6327d5ce175ccaaa75bb410dda4`

## Frozen / selected
- G3-024 external control hardware remains selected.
- G3-025 Foundry and factorised optional-RIAA architecture remain authoritative.
- Optional 3180 us realisation: RC-before-gain, non-inverting stereo OPA1656 implementation.
- Timing per channel: 31.5 kΩ with 68 nF + 33 nF C0G/NP0, giving 3181.5 us nominal.
- Optional-stage gain: 1 + 5.08 kΩ / 267 Ω = 20.0262; approximately unity at 1 kHz after the 3180 us pole.
- Internal ON/BYPASS switch: Nidec ASE2D-2M-10-Z, DPDT through-hole, gold, BBM.
- Bypass selects straight-through RIAA core output; ON selects optional-section output.
- Audio upper cover: 2.0 mm nominal manufacturer-drawing basis for stack analysis.
- GitHub Actions regression workflow is part of the G3-026 candidate.

## Closed by G3-026
- Component-level 3180 us section topology and nominal values.
- Exact internal RIAA switch MPN.
- Polarity continuity between ON and BYPASS.
- Basic bushing-through-cover reach concern for Grayhill and C&K controls.
- Automated pushed-branch pytest/compile regression infrastructure.

## Deliberately open
- Final SCH103/KiCad incorporation and native ERC review of the optional section.
- SPICE/bench confirmation of integrated noise, transient behaviour and overload margin.
- Final custom footprints/3D models for external controls.
- Upper-cover sheet-thickness tolerance and complete washer/nut/anti-rotation/knob stack.
- Final PCB/control coordinates, mounting holes and top-cover drilling release.

## Next package
**G3-027 — SCH103 Integration, Footprint Verification and Machining Datum Closure**

1. integrate the frozen optional-RIAA realisation into SCH103;
2. preserve/retune the invariant 318/75 core as required by the factorised architecture;
3. run electrical curve/headroom/noise regression on the integrated stage;
4. create/verify exact external-control footprints against manufacturer terminal drawings;
5. close the hardware stack and Z datum;
6. synthesise datum-based drilling coordinates only if all manufacturing gates pass.

## Manufacturing limitation
G3-026 is an electrical/component freeze and nominal stack closure. It does not
authorise PCB fabrication or top-cover machining.
