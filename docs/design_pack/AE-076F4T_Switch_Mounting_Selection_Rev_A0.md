# Project Shellac — AE-076F4T Switch Mounting Selection — Rev A0

**Date:** 15 October 2026
**Transaction type:** Selected-next mechanical mounting selection; native implementation and fabrication remain held.
**Release effect:** None. Not a drawing, drilling, PCB routing, BOM, PDR/CDR or manufacturing release.
**Baseline:** Git `develop` remote observed `450ed541d2ab58cd73671df245c8ff071116c236` (local HEAD/cleanliness NOT independently checked in this record). Original KiCad PCB SHA-256 `a5b519a21a2bbe2c9f3ad751134d43292a5b32184487100512ab045b6258861c`. Successful user-run AE-076F4R staging reports reviewed.

## 1. Selected switch mechanical concepts — CLOSED FOR ALTERNATIVE SELECTION

| Control(s) | Selected hardware | Mechanical retention and anti-rotation | Design-choice status |
|---|---|---|---|
| Bass L/R (2) | NKK `NR01105ANG13-2C`; standard **AT3009** knob | PCB mounting at fully seated bearing shoulders; shaft passes through Metcase cover without taking PCB structural load. No modified knobs. | Selected-next; alternative knob/standoff trades closed |
| Treble L/R (2) | NKK `NR01105ANG13-2A`; standard **AT3009** knob | Same as bass. Four original NKK bodies/knobs retained. | Selected-next; alternative trades closed |
| Rumble (1) | C&K `7201SYCBE` | Full PCB pin seating; keyed 1/4-40 threaded bushing in a **directly profiled cover opening with an inward anti-rotation tab**, adjusted **lower backing nut** and **upper external retaining nut**. No fabricated bracket/top-hat. | Selected-next; antirotation/retention *method* fixed |
| Mute (1) | C&K `7201SYCBE` | Same direct keyed cover-hole and two-nut mounting as Rumble. | Selected-next; antirotation/retention *method* fixed |
| Channel matrix (1) | TE/Alcoswitch `MRJE3404`, TE MPN `1825537-3` | **Restore the independent 1.5 mm aluminium three-arm plate on three independent pillars.** Secure TE threaded bushing against plate using TE-compatible retainer; D-flat may antirotate in the **bracket aperture** (not relied upon at cover). Switch shaft passes through Metcase upper cover; **no upper-cover nut or top-hat adaptor** for TE. | Selected-next; direct cover mounting and upright/recessed top-hat studies rejected for this configuration |

**Rejected/no longer selected:** TE direct two-nut cover mounting (insufficient nominal external bushing length above 2.0 mm lid); TE inverted top-hat bulkhead adaptor; extending TE bracket to capture C&K toggles; custom C&K top-hat fittings; modified NKK knobs; direct 18 mm NKK PCB support at the unmodified G1 datum. These may not be revisited without new contradictory physical evidence and an explicit design change.

## 2. Common selected-next geometry (not yet native implementation)

- Independent G1-supported reinforced aluminium carrier and **six 17.0 mm M3 PCB supports**, not the older six-to-top-cover mechanical authority. Actual carrier positive vertical/longitudinal capture is **OPEN**.
- Proposed PCB **220 × 148 × 1.60 mm**, native KiCad X=20..240, Y=20..168. Existing four holes (25,28), (235,28), (235,152), (25,152). Additional support candidate (110,90), (110,157). F4R checked nominal geometry only; neither holes nor outline have been edited.
- Candidate switch centres in native PCB coordinates: Bass L (76,53), Bass R (184,53); Treble L (76,86), Treble R (184,86); Rumble (130,86); Matrix (125,118); Mute (126,153). External-panel handedness remains **OPEN**.
- TE plate pillar candidates (106,118), (142,92), (142,144) in native PCB XY. Plate underside/TE housing-front datum +27.0 mm above G1 carrier bearing; plate thickness 1.5 mm, nominal top +28.5 mm; cover underside +31.852512 mm. Pillar lengths/washer bearings require hardware design rather than assuming nominal +27.0 mm is an available standoff.
- Four NKK AT3009 flange-to-cover nominal clearance +0.952512 mm on 17 mm spacers; strictly positive **worst-case** clearance remains mandatory under controlled AE-076F4B.
- Fully seated C&K nominal housing-to-cover underside gap 4.362512 mm; available threaded projection above nominal 2.0 mm cover +2.527488 mm. Illustrative 1.57 mm thin outer nut with 0.46 mm lockwasher leaves nominal 0.497488 mm exposed thread; **not a tolerance/lock-up release**. Lower backing nut must be set without lifting toggle or preloading solder joints. C&K terminal length gives nominal 0.82 mm protrusion past 1.60 mm PCB if fully seated.
- C&K keyway is a groove in the threaded bushing; the panel feature must be an **inward tab**, not merely an outward notch. The alternative manufacturer locking-ring auxiliary-hole method is technical evidence only, not a concurrent selection. Confirm keyed panel tab dimensions from authenticated manufacturer drawing before machining.
- TE supplied CAD hardware is fused into a single STEP solid; F4L demonstrated modelled 96.476565 mm³ bracket overlap **as supplied**, which does not prove the bare TE switch/real adjustable retainer collides. Do not declare TE plate fastener or hole dimensions approved until bearing/washer/nut, plate bore and genuine switch seating are checked.

## 3. Closed design choice versus mandatory acceptance

The mounting **concepts** are closed by user selection. Fabrication release remains blocked on:

1. TE actual housing-front bearing/plate-hole/retaining nut assembly, 3-pillar fastening and antirotation; exact switch terminal positions and numbered, B.Cu-correct KiCad footprint.
2. C&K 7201SYCBE manufacturer-profiled keying, through-cover upper/lower nut fit, thread engagement under worst-case stack, installed pin seating/no solder-joint load, physical lever motion and genuine electrical orientation.
3. Four NKK actual knob/panel holes and **strictly positive tolerance-inclusive** AT3009 flange clearance; secured carrier datum without G1 slot vertical play.
4. All seven true shaft-to-panel registration and viewed-from-outside handedness, panel installation/removal and knobs; cover XLR/GX16/end panel and mated H801/H802/H901 harness/tool access.
5. Actual windowed carrier, positive G1 capture/end stops and isolated hardware against **sole R909 0VA–CHASSIS bond**; all six PCB support holes and TE pillar passages, all four layers DRC and fabricator DFM.

**Routing, layout freeze, BOM freeze, PDR/CDR, panel drilling and manufacturing remain HELD.** The legacy governed six-PCB-to-top-cover-support authority remains CURRENT until deliberately superseded after these integration gates. The matrix MPN selection under AE-076F4C remains unchanged. No TE top-hat adaptor or direct TE nut mounting is authorised.

## 4. Evidence

- AE-076F4I — 17 mm supports / AT3009 / dedicated TE plate nominal stack.
- AE-076F4L, F4M — genuine TE model, fused hardware and bracket-seating caveat.
- AE-076F4P — C&K manufacturer six-hole orientation evidence.
- **AE-076F4R** staged user-run PASS; genuine Metcase/populated PCB native collision screens, 256 footprints / 598 pad objects / 584 copper pads; exact report `Shellac_Engineering_Staging/reports/SHELLAC_AE076F4R_INTEGRATED_MECHANICAL_READONLY.md/.json`. This report remains a candidate mechanical qualification, not installed hardware.
- AE-076F4B — governed positive NKK flange/cover clearance requirement.

**Configuration-control note:** This record governs the selected-next *mounting methods* only when committed to `develop`. It does not supersede the governed six-PCB-to-cover support architecture, modify native design artefacts or clear any physical acceptance or release gate.
