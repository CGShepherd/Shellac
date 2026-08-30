from pathlib import Path
changes = {
 "tests/test_detailed_placement_readiness.py": [("assert model.proposal_count == 243", "assert model.proposal_count == 249")],
 "tests/test_kicad_native_pipeline.py": [("assert baseline.footprint_count == 243", "assert baseline.footprint_count == 249")],
 "tests/test_preliminary_placement.py": [("assert len(placement.proposals) == len(contract.board_population_refs) == 243", "assert len(placement.proposals) == len(contract.board_population_refs) == 249")],
 "tests/test_real_footprint_audit.py": [("assert audit.accepted_identity_count == 243", "assert audit.accepted_identity_count == 249")],
}
for fn,repls in changes.items():
 p=Path(fn); t=p.read_text(encoding="utf-8")
 for old,new in repls:
  if new in t: continue
  if old not in t: raise SystemExit(f"Expected stale population assertion not found: {fn}: {old}")
  t=t.replace(old,new,1)
 p.write_text(t,encoding="utf-8"); print("migrated",fn)
print("AE-021C complete: all known 243->249 DR-039 population expectations migrated")
