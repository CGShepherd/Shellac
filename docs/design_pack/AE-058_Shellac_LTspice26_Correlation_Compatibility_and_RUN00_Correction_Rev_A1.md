# AE-058 — LTspice 26 Correlation Compatibility and RUN00 Correction — Rev A1

## Status
Pre-SPICE design-assurance evidence. This record does not constitute manufacturing baseline authority.

## Revision A1
Target-machine LTspice 26.0.2 evidence showed that crossing measurements are logged as `name: expression ... AT value` without the literal word `WHEN`, and AC amplitude measurements can be rendered as `(dB, phase) at frequency`, including when the measured expression is `mag(V(...))`.

The correlation harness therefore uses measurement-specific extraction modes controlled by YAML:
- `when_at`: take the trailing `AT` value only for an explicitly configured crossing metric;
- `complex_db`: take the first dB component of LTspice's AC `(dB, phase)` result;
- `scalar`: accept only an unambiguous scalar result.

A root `pytest.ini` constrains authoritative regression discovery to `tests/` and excludes extracted payloads, caches, environments and generated simulation state. This prevents historical transport payloads from being collected as duplicate test modules while repository cleanup is handled separately under configuration control.

AE-048/AE-049/AE-050 retain qualification, numerical acceptance and execution authority. AE-053 remains toolchain architecture authority. AE-055 remains independent analytical evidence. AE-056 remains the initial LTspice correlation implementation. AE-058 documents compatibility corrections only.
