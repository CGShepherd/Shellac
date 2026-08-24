# Project Shellac — Controlled Project Status

**Knowledge baseline:** SR-036 + Foundry FDR-001 candidate
**Engineering package:** G3-025 Foundry/RIAA/physical-control closure candidate
**Base commit:** `57716653d9b4c11d1c785863cb2c7ee03953d48a`

## Frozen / selected
- G3-024 external control hardware remains selected and unchanged.
- SW901/SW902: Grayhill 71BDF30-01-2-AJN, five stops.
- SW903: Grayhill 71BDF30-02-2-AJN, four stops.
- SW904/SW905: C&K 7201SYCBE common DPDT toggle.
- LED901/LED902: Vishay TLLG4401 in A104700BLACK black-brass bezels on the audio top-cover centre spine.
- External-switch bushings are secondary structural connections; PCB standoffs remain primary datum/support.
- Optional RIAA architecture: invariant 318/75 core plus dedicated stereo 3180 us section with internal ON/straight-through BYPASS.
- Foundry FDR-001 defines evidence/decision/release governance.

## Closed by G3-025
- The single-RC SCH103 branch cannot independently switch only the 3180 us term; this is proven and tested.
- The optional-pole requirement is factorised without altering the 318 us or 75 us terms.
- Selected external-control catalogue dimensions are captured as controlled mechanical evidence.
- Stale light-pipe/no-flying-indicator assumptions are superseded.

## Deliberately open
- Component-level implementation (RC/gain distribution) of the dedicated 3180 us section.
- Exact internal RIAA switch MPN after noise/gain/overload closure.
- Final verified custom footprints/3D models for all external controls.
- Upper-cover thickness/Z datum and complete washer/nut/knob stack.
- Final PCB/control coordinates, mounting holes and top-cover drilling release.

## Next package
**G3-026 — Optional-RIAA Circuit Realisation & Manufacturing-Control Geometry**

1. synthesise candidate 3180 us section implementations;
2. compare noise, gain, overload, loading and component practicality;
3. select exact internal switch hardware after topology is fixed;
4. verify/create custom external-control footprints;
5. close upper-cover Z stack;
6. only then synthesise/review datum-based machining coordinates.

## Manufacturing limitation
No PCB fabrication or top-cover machining is authorised by G3-025.
