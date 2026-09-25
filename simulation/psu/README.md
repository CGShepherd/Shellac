# Shellac PSU simulation

The PSU simulation namespace separates manufacturer-macromodel execution qualification
from physical PSU qualification.

- `config/p1v.yaml` is the current AIYIMA P1-V physically reconstructed authority,
  pending powered validation.
- `RUN00_QUALIFICATION.md` records the controlled model-execution qualification.
- RUN00 is PASS locally; AE-073 closes the long-settle discriminator and confirms
  that the exploratory 400 ms low-output condition was a startup-settling artefact,
  not a demonstrated DC adjustment ceiling. Powered hardware qualification remains open.
- Compact AE-073 evidence is retained under `evidence/ae073_long_settle/`.
- Vendor model payloads are local only and are not committed.
- The governing philosophy is retain the as-fitted PSU unless quantitative analysis
  or measurement identifies a material safety, reliability, stability, noise,
  regulation, thermal, protection or operating-margin deficiency.
