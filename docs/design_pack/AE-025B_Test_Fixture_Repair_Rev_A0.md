# AE-025B — Test Fixture Repair

**Revision:** A0  
**Status:** TEST-ONLY REPAIR

AE-025A corrected the production decision-status configuration and AE-024 audit
semantics. One AE-025 regression fixture still constructed
`authoritative_current_status` using YAML block-list syntax, which is outside the
deliberately narrow standard-library parser contract adopted by AE-024A/AE-025A.

AE-025B changes only that test fixture to use the supported inline-list syntax.

No production source, configuration, circuit, CAD, BOM, assurance model,
decision record or current documentation is changed.

Expected result:

- AE-024 audit: 0 vocabulary findings;
- AE-024 audit: 0 current-authority contradictions;
- full pytest suite: green.
