# Shellac MCAD workspace

AE-076B2 controls this workspace.

METCASE M5502119:
- public official PDF drawing is hash-controlled;
- exact STEP requires METCASE authentication and is ingested/hash-controlled by AE-076B2B;
- drawing-to-STEP dimensional reconciliation remains open.

Neutrik panel STEP models and the governed KiCad PCB STEP live only in ignored
local evidence caches.

Reproduce public/local inputs with:

    .venv\Scripts\python.exe tools\prepare_ae076b2b_mcad_inputs.py

After manually downloading M5502119.stp while logged in to METCASE:

    .venv\Scripts\python.exe tools\prepare_ae076b2b_mcad_inputs.py --verify-only --ingest-metcase-step "C:\path\M5502119.stp"
