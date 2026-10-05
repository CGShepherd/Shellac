# AE-076B2C — MCAD Source Reconciliation Evidence — Rev A0

**Parent baseline:** `3183c07a61248aad648fdecc9cc883a5cfba14c6`
**Status:** SOURCE/GEOMETRY EVIDENCE PROMOTED — NATIVE PCB MODEL BINDING OPEN

## METCASE M5502119

Controlled drawing: 260.0 x 250.0 x 90.2 mm external body; inside width 256.0 mm; internal cover height 86.2 mm; PCB slot width 241.01 mm; inside face depth 229.0 mm; panel thickness 2.0 mm.

Authenticated STEP SHA-256 `9bf09314db1e8ffb596c27cceecb932141d3e43ba8d5ca4998fd4d16411b91fa`, measured external body approximately 260.004806 x 250.000000 x 90.204806 mm.

External body drawing-to-STEP reconciliation: **PASS**. Aggregate STEP extents from feet/lateral fasteners are not body-dimension failures. Assembly-level internal datums remain open.

## C30060 / C35060

Installed KiCad 9 contains exact `C_Rect_L7.2mm_W5.0mm_P5.00mm.wrl`. Temporary export proves the WRL correction removes both missing-model errors. Governed native binding remains open.

## H901

Exact Molex identity: `39-29-9063`, canonical `0039299063`, web number `39299063`, family `5566-06A2`. Earlier speculative `39-28-9068` is rejected/superseded.

Exact STEP ZIP SHA-256 `448ccc66ed709367f5016aebf1118f7ced04726d4d3b5b1bb076387f30647f5d`; exact KiCad ZIP SHA-256 `32470620fd16409a8906bf045b7482131064b3d90b002a9a62f016c17ec68cb4`.

Probe evidence verifies six electrical pads, two locator holes, successful model import and a temporary complete-board export with zero missing 3D models when combined with the capacitor correction. Governed project-local/native binding remains open.

## Release effect

No support/control migration, routing, layout freeze, BOM freeze or manufacturing release is authorised.
