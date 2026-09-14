# Project Shellac — AE-041 3P4T Matrix and Top-Cover Control Authority

**Revision:** A1
**Status:** ARCHITECTURE SELECTED — QUALIFICATION AND ABSOLUTE MECHANICAL COORDINATES OPEN
**Date:** 10 September 2026
**Scope:** Supersedes AE-041 A0 DP4 permanent-summing matrix authority while retaining its analysis as traceability evidence.

## 1. Decision
The channel matrix shall use a passive **3P4T, four-position, BBM/non-shorting** selector. Preferred production switch is **C&K A30403RNCB**; **TE/Alcoswitch MRJE3404** is the procurement fallback. The operator sequence remains **CCW -> CW: DUAL L, STEREO, L+R, DUAL R**.

Two 4.7 kOhm, 0.1% averaging resistors remain at the SCH104 OPA1656 outputs before the existing 100 Ohm isolation resistors. The left branch terminates permanently at `MONO_AVG`; the right branch terminates at `MONO_R_LEG`. SW903 Pole C connects `MONO_R_LEG` to `MONO_AVG` **only in L+R**.

Consequently there is **no intentional conductive L-R resistive path** in DUAL L, STEREO or DUAL R. One dormant 4.7 kOhm branch remains connected from L to the otherwise-unselected `MONO_AVG` node; this is accepted because the opposite leg is open and therefore it does not create inter-channel coupling.

## 2. Pole truth table
| Position | Pole A left output | Pole B right output | Pole C mono right leg |
|---|---|---|---|
| DUAL L | BUFFERED_L | BUFFERED_L | OPEN |
| STEREO | BUFFERED_L | BUFFERED_R | OPEN |
| L+R | MONO_AVG | MONO_AVG | CONNECT MONO_R_LEG -> MONO_AVG |
| DUAL R | BUFFERED_R | BUFFERED_R | OPEN |

The existing `ProjectShellac:Mode_Switch_Block` symbol may retain legacy `SUM_L/SUM_R` pins. `SUM_R` is repurposed to represent Pole C / `MONO_R_LEG`; `SUM_L` remains NC. A future symbol-library cleanup is cosmetic and does not block electrical authority.

## 3. Switch authority
Preferred: **C&K A30403RNCB** — 3P4T, four positions, 30-degree indexing, BBM/non-shorting, low-level gold-contact construction, PC terminals, 6.35 mm flatted shaft, approximately 9.53 mm shaft projection and approximately 14.48 mm behind-panel depth. This preserves compatibility with the selected TE/Alcoswitch KN900B1/4 knob concept.

Fallback: **TE/Alcoswitch MRJE3404** — 3P4T, four-position, BBM, low-level gold-finish contact system and PC termination. Its 3.17 mm shaft requires different knob treatment and therefore it is not the preferred mechanical option.

Preferred-part procurement remains PARTIAL because the C&K part has lead-time exposure. The stocked TE part demonstrates that the architecture itself is procurable in quantity one.

Final clockwise detent-to-terminal mapping shall be confirmed by continuity measurement on a production switch before PCB/panel manufacturing release. Published terminal grouping is sufficient for architecture but not used as sole authority for operator-side legend orientation.

## 4. Superseded alternatives
**AE-041 A0 DP4 permanent averaging:** electrically workable but superseded because its two permanent 4.7 kOhm legs form a 9.4 kOhm intentional L-R path in all modes. Analysis indicated that active OPA1656 outputs would probably make resulting crosstalk negligible, but 3P4T removes the concern directly for modest additional switching complexity.

**4P4T fully isolated averaging:** electrically cleanest because both averaging legs can be disconnected outside L+R. Rejected for the current design because conventional gold-contact 4P4T parts found were substantially worse in cost, size, termination and/or single-unit availability. The fourth pole would eliminate only an unloaded dormant 4.7 kOhm branch; it would not remove any remaining L-R path, because 3P4T already removes that path.

**Historical Lorlin/Grayhill 4P4 concepts:** remain rejected historical evidence unless future procurement circumstances materially change.

## 5. Switching and mute dependency
SW903 remains BBM/non-shorting. The 2.2 MOhm SCH105 input returns prevent materially floating buffer inputs during the break interval but do not prove click-free live switching. Operating architecture is therefore **MUTE -> change MATRIX -> RUN**. Exact matrix transient magnitude remains a SPICE/bench qualification item and is an explicit input to the unresolved output-mute design.

## 6. Retained control authority
Signal/top-cover sequence remains `FRONT -> Input -> Bass -> Treble -> Rumble -> Matrix -> Mute -> Output -> REAR` on the removable top cover. Bass/Treble remain four independent NKK NR01-family controls local to their channel circuitry. SW904 Rumble and SW905 Mute remain C&K 7201SYCBE with transverse LEFT/RIGHT convention: Rumble `BYPASS / IN`; Mute `RUN / MUTE`. REG-08 remains top-cover mechanical-registration authority, not a central control strip.

Relative ergonomic targets remain: Treble->Rumble >=25 mm, Rumble->Matrix >=32 mm, Matrix->Mute >=35 mm, matrix operator envelope approximately 40 mm. These are not drilling dimensions.

## 7. Open qualification / release boundary
Not released: final PCB/top-cover coordinates; final switch footprint orientation; matrix legend angles; production-switch detent/terminal continuity confirmation; switching-transient qualification; mono accuracy/tolerance/SPICE/bench confirmation; mute topology and mute-transient suppression; final procurement baseline.

## 8. Acceptance assertions
1. Matrix is 3P4T, four-position, BBM/non-shorting.
2. Preferred SW903 is C&K A30403RNCB; TE MRJE3404 is documented fallback.
3. Mode order remains DUAL L / STEREO / L+R / DUAL R, CCW->CW.
4. Two 4.7 kOhm 0.1% averaging resistors originate at SCH104 OPA1656 outputs before 100 Ohm isolation.
5. Left averaging leg reaches MONO_AVG permanently.
6. Right averaging leg reaches MONO_R_LEG and is connected to MONO_AVG only in L+R.
7. No intentional L-R resistive bridge exists in DUAL L, STEREO or DUAL R.
8. BBM live-switch transients are managed operationally by MUTE -> MATRIX -> RUN pending bench evidence.
9. Absolute mechanical coordinates and detent-to-terminal panel mapping remain unreleased.
10. AE-041 A0 DP4 permanent-summing authority is superseded but retained as design-history evidence.
